"""The census: every collection row placed in exactly one named category.

WHAT THIS MODULE REFUSES TO DO. The obvious shape for a scan is "walk the
library, keep what you can read, and plan for those". AE12 exists because that
shape was shipped: a library holding cloud-backed or online-only files produced
a plan that quietly covered fewer tracks than the library has, and nothing in
the output said so. A track that is not in the plan and not in a named category
is a track nobody decided about, and the person who ran the scan cannot tell it
apart from a track the plan simply had nothing to say about.

So this module is TOTAL. Every row it is handed comes back as a
:class:`ScannedTrack`, carrying a :class:`Readability` that says what the file
is and a :class:`Disposition` that says what adoption means to do about it. The
plan layer above then holds every one of them, and the arithmetic that proves
nothing was dropped is a set comparison rather than a count.

THE THIRD POPULATION, AND WHY IT IS NOT A ROUTING PROBLEM.
:func:`cratekit.core.routing.resolve_bucket` is total by design: it never
returns None and never raises, because a router that can fail has to be wrapped
at every call site. Its last tier is the declared fallback bucket, and it says
so through ``Resolution.match``. Adoption is the one caller for which that last
tier is NOT an answer. A track whose genre is blank, or is one of the strings
the taxonomy declares too coarse to be a source, cannot be split by tag at all;
accepting the fallback would file thousands of tracks into one folder and report
a complete adoption. Those tracks get :attr:`Disposition.NEEDS_GENRE`, which is
a declared disposition rather than a silent omission, and the plan carries them
as review items. This is read OFF the router's own report rather than by asking
the genre a second question, so there is no second opinion to drift.

WHY THE PROBE IS INJECTED. Deciding whether a file is readable, missing, or a
cloud placeholder is the one thing here that touches the disk, and the shapes it
has to recognise (a dataless file the operating system will fetch on open, a
provider stub sitting beside the name the library records) cannot be created
inside a test on demand. So the probe is a parameter with a real default, the
default is small enough to read, and every category it can return is exercised
against a temporary directory.

Layer: modules. It reads configuration and the disk and names no verb.
"""

from __future__ import annotations

import os
import stat as stat_module
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Callable, Iterable, Iterator, Sequence

from cratekit.core import locations, routing, tags, taxonomy

#: The suffix a well-known consumer file synchroniser leaves beside a name whose
#: bytes it has evicted. Recognised because the library's recorded location
#: names the ORIGINAL, so a probe that only asked about the recorded path would
#: report the track missing and adoption would propose nothing for a file the
#: user still has.
PLACEHOLDER_SUFFIX = ".icloud"

#: The prefix that same synchroniser puts on the placeholder's own name.
PLACEHOLDER_PREFIX = "."

#: ``SF_DATALESS``. macOS sets this in ``st_flags`` on a file whose bytes a file
#: provider has evicted, which is the ONE authoritative answer to "are the bytes
#: here" that costs nothing and downloads nothing. Spelled as a literal because
#: Python's :mod:`stat` module does not export it; the value is copied from
#: ``sys/stat.h``, where the line reads
#: ``#define SF_DATALESS 0x40000000 /* file is dataless object */``, and is inert
#: on every platform that has no ``st_flags`` at all. The comment said
#: ``UF_DATALESS`` at first, which is a constant that does not exist: the value
#: was right and the name was invented, and a name nobody can grep for in the
#: header is a name the next reader cannot check.
DATALESS_FLAG = 0x40000000


class Readability(StrEnum):
    """What the scan found where the library says a track's file is.

    A CLOSED SET OF NAMES, and the naming is the requirement rather than a
    convenience. AE12 says an unreadable file is REPORTED as a named category,
    so a category that collapsed two different facts would satisfy the letter and
    lose the thing a person needs: "the file is gone" and "the file is in the
    cloud" have different answers, and only one of them is fixed by plugging in
    a drive.
    """

    #: The file is present and its bytes can be read on this machine.
    READABLE = "readable"

    #: The recorded location resolves to a path on this machine and nothing is
    #: there. The row is real; the file is not.
    MISSING = "missing"

    #: Something is there and this account cannot read it: a permission, an
    #: input-output error, a filesystem that answered and refused.
    UNREADABLE = "unreadable"

    #: Cloud-backed or online-only. The name exists and the bytes do not, so any
    #: read is a download that may take minutes or fail. AE12 names this case.
    ONLINE_ONLY = "online-only"

    #: The recorded location is an absolute path this installation maps no prefix
    #: for. Distinct from MISSING on purpose: the remedy is configuration, not a
    #: drive, and reporting a configuration gap as a missing file is exactly the
    #: fusion :func:`cratekit.core.locations.resolve_recorded_path` refuses.
    UNMAPPED = "unmapped"

    #: The recorded location is not a path on this machine at all: a streaming
    #: pseudo-location, something device-relative, a location naming ANOTHER HOST
    #: (which has no local path and must not be guessed into one), or a string
    #: the operating system cannot name a file with. Not a failure, and not a
    #: file either. These are folded together on purpose and the fusion is the
    #: one in this enumeration: every one of them is a row whose location this
    #: installation can do nothing local about, so they share a remedy where the
    #: other five do not.
    NOT_A_PATH = "not-a-path"


#: The categories a track can be adopted FROM. Everything else is excluded, and
#: the exclusion is named. Derived as a set here rather than spelled at each
#: call site, so a seventh category cannot arrive and be silently adoptable.
ADOPTABLE: frozenset[Readability] = frozenset({Readability.READABLE})


class Disposition(StrEnum):
    """What adoption means to do about one track. Every track has exactly one.

    There is no member meaning "nothing", and that absence is the design. The
    defect this replaces was a plan that simply did not mention a track, which
    reads identically to a plan that has not been built yet.
    """

    #: A bucket resolved from the track's own genre, so the plan can place it.
    ROUTE = "route"

    #: The genre is blank, or is declared too coarse to be a source, or resolved
    #: only through the fallback tier. The track cannot be split by tag and goes
    #: to a person as a review item rather than into the fallback folder.
    NEEDS_GENRE = "needs-genre"

    #: The file is not in an adoptable category. The plan carries the track with
    #: the category that says why, so it is reported rather than omitted.
    EXCLUDED = "excluded"

    #: The destination folder already exists holding tracks this plan does not
    #: name, and a person answered "leave that folder alone". Its own member
    #: rather than a silent removal from the applicable set: the track was
    #: routable, the genre was right, and the reason it is not being placed is a
    #: decision somebody made rather than anything about the track. Set by the
    #: plan layer, which is where collisions and their verdicts live.
    WITHHELD = "withheld"

    #: The genre resolved to a bucket and the taxonomy declares no sub-playlist
    #: under it for this track's energy reading. Set by the plan layer rather
    #: than here, because it is the sub resolution that discovers it. Its own
    #: member rather than NEEDS_GENRE: the genre answered perfectly, and telling
    #: a person to fix a genre that is already right is the shape of advice
    #: people learn to ignore.
    UNDECLARED = "undeclared"


@dataclass(frozen=True, slots=True)
class CollectionRow:
    """The three things the census needs from one row of the user's collection.

    A narrow record rather than the binding's own object, for the reason
    :class:`cratekit.write.trees.ContentRow` is one: the producer that reads a
    real database and the tests that do not then agree on one shape, and nothing
    here depends on a binding attribute name.

    ``content_id`` IS THE IDENTITY, and it is the row identifier rekordbox
    allocated rather than anything derived. A display name, a filename, or a
    title would all be re-derived on the next scan and would move under a rename,
    which is how a second adoption of one track happens.

    ``deleted`` has NO DEFAULT. False means active, which is the permissive
    answer for a soft-delete marker, and a producer that supplies it hands every
    tombstone to the census as a live row. U18 made this call for the tree
    writer's row record and U19 undid it through a defaulting accessor; the
    lesson generalizes to every producer of library rows, so it is made the same
    way here.
    """

    content_id: str
    recorded: str
    genre: str
    deleted: bool


@dataclass(frozen=True, slots=True)
class ScannedTrack:
    """One row, where its file is, and what adoption proposes about it.

    ``bucket`` is a stable taxonomy identifier and is empty for anything that is
    not routing. It is never a display name (R19, D5): the folder a bucket shows
    in rekordbox is resolved from the active taxonomy at write time, so renaming
    it between the scan and the apply changes nothing about the record.
    """

    content_id: str
    recorded: str
    path: str | None
    readability: Readability
    disposition: Disposition
    genre: str
    bucket: str = ""
    #: How the router reached the bucket, kept so a report can show the share of
    #: tracks that resolved only fuzzily rather than presenting them as exact.
    match: str = ""
    #: The energy level the file's own tag holds, or None when it holds none or
    #: could not be read. Read here rather than in the plan because the plan
    #: layer takes no library input, and read only for an adoptable file,
    #: because opening an online only one is what fetches it.
    energy: int | None = None
    #: True when the file's tags could not be read, which is not the same fact
    #: as a file holding no energy tag. Both land in the no reading sub, and
    #: this is what keeps the first from landing there silently.
    energy_unreadable: bool = False


def probe_readability(path: Path) -> Readability:
    """Classify one resolved path on this machine. The default probe.

    TOTAL BY CONSTRUCTION, and that is a property of THIS function rather than
    of the inputs it happens to be given. The census is a generator, so anything
    raising out of a probe does not fail one row, it kills the walk and takes
    every row after it with no output and no count. Two ordinary library shapes
    do exactly that to the obvious implementation: a directory with no execute
    bit anywhere under the library makes every probe under it raise
    ``PermissionError``, and a recorded location carrying a null byte makes
    ``stat`` raise ``ValueError``, which is not an ``OSError`` and is not caught
    by anything that only expects one. So every answer is a named category and
    the two outer handlers are the reason the walk cannot end early.

    THE ORDER, AND WHY THE RECORDED NAME IS ASKED ABOUT FIRST. The file itself
    decides. A synchroniser that evicts a file's bytes leaves a stub whose name
    is the original with a dot in front and a suffix on the end, and the library
    still records the ORIGINAL, so the stub is what distinguishes "the bytes are
    in the cloud" from "the file is gone". But a stub is DEBRIS as often as it is
    evidence: it outlives the file coming back, and a probe that asked about it
    first reported a file it could have read in full as online-only, refusing to
    adopt a track that was sitting right there. So the stub is consulted only
    where the recorded name is absent, which is the only case it can settle.

    WHETHER THE BYTES ARE HERE IS ASKED WITHOUT READING THEM. Opening a dataless
    file triggers a download, and doing that per file across a library is the
    opposite of a scan. The platform answers it exactly, in ``st_flags``, and
    :func:`_is_dataless` says why that replaced the block count it used to ask.
    """
    try:
        return _probe(path)
    except ValueError:
        # A string the operating system cannot name a file with at all, an
        # embedded null byte being the one that reaches here from a real library.
        # It is not a path, which is a fact about the row rather than the disk.
        return Readability.NOT_A_PATH
    except OSError:
        # A permission, an input-output error, a filesystem that answered and
        # refused. Something is there and this account cannot read it.
        return Readability.UNREADABLE


def _placeholder_beside(path: Path) -> bool:
    """Whether a synchroniser's stub sits beside the recorded name."""
    placeholder = path.with_name(f"{PLACEHOLDER_PREFIX}{path.name}{PLACEHOLDER_SUFFIX}")
    try:
        return placeholder.exists()
    except OSError:
        # The directory refused the question. That is not evidence of a stub,
        # and the recorded name has already answered what it could.
        return False


def _is_dataless(info) -> bool:
    """Whether the name is here and the bytes are not, asked without a read.

    THE BLOCK COUNT IS NOT THE QUESTION, and it used to be. "This file reports a
    size and occupies no blocks" describes a dataless file and it also describes
    a SPARSE file, and on a filesystem that does not populate the count at all it
    describes every file there is. Some network and FUSE mounts do exactly that,
    so the block count would exclude a whole library and report it as cloud
    backed, which is a worse failure than the one it was guarding: an excluded
    track is one nobody decided about, and there would be no readable file
    anywhere in the census to make it look wrong.

    The flag is the platform's own answer to the actual question, it costs
    nothing, and it has no second meaning. A platform that does not expose it has
    no file provider doing this either, and falls through to the read, which is
    the honest answer where the cheap question cannot be asked.
    """
    return bool(getattr(info, "st_flags", 0) & DATALESS_FLAG)


def _probe(path: Path) -> Readability:
    """The probe's actual questions. Raises; :func:`probe_readability` does not."""
    try:
        info = path.stat()
    except FileNotFoundError:
        return (
            Readability.ONLINE_ONLY if _placeholder_beside(path) else Readability.MISSING
        )
    if not stat_module.S_ISREG(info.st_mode):
        return Readability.MISSING
    if _is_dataless(info):
        return Readability.ONLINE_ONLY
    with path.open("rb") as handle:
        handle.read(1)
    return Readability.READABLE


def _as_recorded_text(recorded: object) -> str | None:
    """One recorded location as text, or None when it is not a location at all.

    THE ANNOTATION SAYS ``str`` AND A DATABASE DOES NOT HAVE TO AGREE, so this
    coerces what can be coerced and refuses the rest, both without raising. Two
    shapes have already cost a whole census between them:

    * ``None``, an ordinary null ``FolderPath``. The decoder asks a string method
      of whatever it is handed, so a null raised ``AttributeError`` out of the
      census generator and took every later row with it.
    * a :class:`~pathlib.Path`, which is what a caller building rows from disk
      naturally holds. Refusing it as "not a string" excluded EVERY row in such a
      library and named the category ``not-a-path``, which is the whole-library
      misclassification this module exists to prevent, arriving through the fix
      for it. ``os.fspath`` is what turns it back into the location it always was.

    Anything else is refused rather than passed through ``str()``. The resolver
    this replaced coerced unconditionally, which turns an integer into ``"5"`` and
    an arbitrary object into its repr; both then classify as ``not-a-path``
    anyway, so refusing here reaches the same answer without inventing a location.
    """
    if isinstance(recorded, str):
        return recorded
    if isinstance(recorded, os.PathLike):
        coerced = os.fspath(recorded)
        return coerced if isinstance(coerced, str) else None
    return None


def _resolved_path(
    recorded: str,
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule],
) -> tuple[str | None, Readability | None]:
    """Where a recorded location lives here, or the category that says why not.

    IT IS DECODED FIRST, AND THAT IS NOT A DETAIL. rekordbox's ``Location``
    column is a percent-encoded file URL. It opens ``file://localhost`` or
    ``file://`` and the mount point follows, so it is a URL and not a path.
    :func:`locations.resolve_recorded_path` refuses anything that does not
    open with a slash, correctly, because a value that is not a path must not be
    guessed into one. Hand it the raw column and EVERY row in a real library
    comes back ``NOT_A_PATH``, every one of them is excluded, and the plan then
    carries the whole library in a category none of it belongs to.

    That failure is invisible to the arithmetic that is supposed to catch it:
    :func:`cratekit.adopt.plan.covers` compares content identifiers, so a plan
    holding every row under the wrong category satisfies "nothing fell out"
    exactly as well as a correct one does. The proof is about presence, not about
    correctness, and only a test using the shape rekordbox actually writes can
    see the difference.

    So both consumers of a recorded location decode before they resolve. The
    sibling is :func:`cratekit.write.trees._comparable`, whose docstring already
    said both sides must; this is the side that was not.

    The unresolved answers are kept apart because their remedies are, which is
    the whole argument :func:`locations.resolve_recorded_path` already makes one
    layer down. This function adds nothing to that decision; it translates it
    into this module's vocabulary once, so no caller re-interprets it.
    """
    text = _as_recorded_text(recorded)
    if text is None:
        return None, Readability.NOT_A_PATH
    try:
        decoded = locations.location_to_path(text)
    except locations.LocationDecodeError:
        # A location naming another host. There is no local path behind it and
        # inventing one is what the decoder refuses to do, so the row is reported
        # rather than resolved.
        return None, Readability.NOT_A_PATH
    resolution = locations.resolve_recorded_path(
        decoded, root=root, prefix_map=prefix_map
    )
    if resolution.resolution is locations.Resolution.NOT_A_PATH:
        return None, Readability.NOT_A_PATH
    if resolution.resolution is locations.Resolution.UNMAPPED:
        return None, Readability.UNMAPPED
    return resolution.path, None


def classify_genre(
    declared: taxonomy.Taxonomy, genre: str
) -> tuple[Disposition, str, str]:
    """Decide what a track's own genre entitles adoption to do with it.

    Returns the disposition, the bucket identifier when there is one, and how the
    router reached it.

    THE FALLBACK TIER IS NOT AN ANSWER HERE, and this is the whole of approach
    point 2. The router's fourth tier exists so that routing a single track never
    crashes, and it reports itself as a fallback so a caller can see it happened.
    An adoption pass that accepted it would file every unrecognised genre in one
    library into a single folder, in bulk, on approval given for a plan that
    looked complete. A person can answer the genre question per track; nobody can
    un-answer it for four thousand tracks afterwards.

    THE TOO-COARSE TEST IS THE TAXONOMY'S OWN. ``is_too_coarse_as_source``
    replaced two constants in the source system that always meant one thing and
    were never the same string. Asking it here rather than keeping a list is what
    makes a user's own template able to say what is too coarse for THEIR library.
    """
    value = (genre or "").strip()
    if not value or declared.is_too_coarse_as_source(value):
        return Disposition.NEEDS_GENRE, "", ""
    resolution = routing.resolve_bucket(declared, value)
    if resolution.match is routing.Match.FALLBACK:
        return Disposition.NEEDS_GENRE, "", str(resolution.match)
    return Disposition.ROUTE, resolution.bucket_id, str(resolution.match)


def scan_rows(
    rows: Iterable[CollectionRow],
    declared: taxonomy.Taxonomy,
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
    probe: Callable[[Path], Readability] = probe_readability,
    energy_reader: Callable[[Path], int | None] = tags.read_energy_checked,
) -> Iterator[ScannedTrack]:
    """Classify every row, once, in one walk.

    A GENERATOR OVER THE CALLER'S ROWS, consumed exactly once. That is the shape
    a whole-library read arrives in, and it is the shape that punishes a consumer
    who walks it twice: U18's row index was rebuilt per plan entry, which was
    merely quadratic against a list and reported an empty library against a
    database cursor. The plan layer materializes this once and never re-walks it.

    A TOMBSTONE IS SKIPPED, and skipping is correct here rather than a silent
    omission. A soft-deleted row is a track the user removed from their library
    on purpose; proposing to adopt it would put it back. The census is total over
    the LIVE collection, which is what the row's own marker defines.

    THE INJECTED PROBE IS NOT TRUSTED TO BE TOTAL, even though the default one
    is. A probe is a parameter, so its totality is somebody else's property, and
    the cost of being wrong about it is not one misclassified row: this is a
    generator, so an exception ends the walk and every row after it is never
    produced, never counted, and never reported missing by anything. The two
    shapes a filesystem raises are caught and named here for that reason. A
    programming error in a caller's probe still surfaces, because nothing wider
    is caught.

    THE ENERGY READING COMES OFF THE FILE, through the reader the routing pass
    uses, so adoption files a track where routing would. Adoption once passed no
    reading at all and filed 7,401 of 7,773 tracks as unsorted over a library
    where 7,726 carried one. A reader failure is caught for the same reason a
    probe failure is, and recorded on the track rather than read as absence.
    """
    for row in rows:
        if row.deleted:
            continue
        path, refusal = _resolved_path(row.recorded, root=root, prefix_map=prefix_map)
        if refusal is not None:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=None,
                readability=refusal,
                disposition=Disposition.EXCLUDED,
                genre=row.genre,
            )
            continue
        try:
            readability = probe(Path(path or ""))
        except ValueError:
            readability = Readability.NOT_A_PATH
        except OSError:
            readability = Readability.UNREADABLE
        if readability not in ADOPTABLE:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=path,
                readability=readability,
                disposition=Disposition.EXCLUDED,
                genre=row.genre,
            )
            continue
        disposition, bucket, match = classify_genre(declared, row.genre)
        energy, unreadable = _energy_of(Path(path or ""), energy_reader)
        yield ScannedTrack(
            content_id=row.content_id,
            recorded=row.recorded,
            path=path,
            readability=readability,
            disposition=disposition,
            genre=row.genre,
            bucket=bucket,
            match=match,
            energy=energy,
            energy_unreadable=unreadable,
        )


def _energy_of(
    path: Path, reader: Callable[[Path], int | None]
) -> tuple[int | None, bool]:
    """The file's energy level and whether reading it failed."""
    try:
        return reader(path), False
    except (tags.TagReadFailed, OSError):
        return None, True


def categories(scanned: Iterable[ScannedTrack]) -> dict[str, int]:
    """How many tracks landed in each named category, DERIVED from the members.

    Every member of :class:`Readability` is present with a count, including the
    zeroes. A summary that listed only the categories it happened to see would
    make "no online-only files in this library" and "this build does not look for
    online-only files" the same output, and AE12 is precisely about being able to
    tell those apart.
    """
    counts = {str(member): 0 for member in Readability}
    for track in scanned:
        counts[str(track.readability)] += 1
    return counts


def dispositions(scanned: Iterable[ScannedTrack]) -> dict[str, int]:
    """How many tracks carry each disposition. Derived, zeroes included."""
    counts = {str(member): 0 for member in Disposition}
    for track in scanned:
        counts[str(track.disposition)] += 1
    return counts


__all__ = [
    "ADOPTABLE",
    "PLACEHOLDER_PREFIX",
    "PLACEHOLDER_SUFFIX",
    "CollectionRow",
    "Disposition",
    "Readability",
    "ScannedTrack",
    "categories",
    "classify_genre",
    "dispositions",
    "probe_readability",
    "scan_rows",
]
