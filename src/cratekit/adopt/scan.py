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

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Callable, Iterable, Iterator, Sequence

from cratekit.core import locations, routing, taxonomy

#: The suffix a well-known consumer file synchroniser leaves beside a name whose
#: bytes it has evicted. Recognised because the library's recorded location
#: names the ORIGINAL, so a probe that only asked about the recorded path would
#: report the track missing and adoption would propose nothing for a file the
#: user still has.
PLACEHOLDER_SUFFIX = ".icloud"

#: The prefix that same synchroniser puts on the placeholder's own name.
PLACEHOLDER_PREFIX = "."


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

    #: The recorded location is not a path at all: a streaming pseudo-location or
    #: something device-relative. Not a failure, and not a file either.
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

    #: The genre resolved to a bucket and the taxonomy declares no sub-playlist
    #: under it for a track with no energy reading. Set by the plan layer rather
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


def probe_readability(path: Path) -> Readability:
    """Classify one resolved path on this machine. The default probe.

    THREE QUESTIONS IN ONE ORDER, and the order is what keeps the categories
    apart.

    First, a placeholder beside the name. A file evicted to the cloud is
    replaced by a stub whose name is the original with a dot in front and a
    suffix on the end, and the library still records the ORIGINAL. Asking about
    the recorded name alone reports the track missing, which sends the person
    looking for a drive that is already attached.

    Second, presence. Nothing there is MISSING, and it is asked before the read
    so that a missing file is never reported as an unreadable one.

    Third, whether the bytes are actually here. A dataless file reports a size
    and occupies no blocks, because the size is metadata the synchroniser kept
    and the contents are not on this disk. Opening it triggers a download, which
    is precisely what a scan over a whole library must not do, so the block count
    is asked instead of the file being read. A platform whose stat has no block
    count falls through to the read, which is the honest answer where the cheap
    question cannot be asked.
    """
    placeholder = path.with_name(f"{PLACEHOLDER_PREFIX}{path.name}{PLACEHOLDER_SUFFIX}")
    if placeholder.exists():
        return Readability.ONLINE_ONLY
    try:
        stat = path.stat()
    except FileNotFoundError:
        return Readability.MISSING
    except OSError:
        return Readability.UNREADABLE
    if not path.is_file():
        return Readability.MISSING
    blocks = getattr(stat, "st_blocks", None)
    if blocks == 0 and stat.st_size > 0:
        return Readability.ONLINE_ONLY
    try:
        with path.open("rb") as handle:
            handle.read(1)
    except OSError:
        return Readability.UNREADABLE
    return Readability.READABLE


def _resolved_path(
    recorded: str,
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule],
) -> tuple[str | None, Readability | None]:
    """Where a recorded location lives here, or the category that says why not.

    The two unresolved answers are kept apart because their remedies are, which
    is the whole argument :func:`locations.resolve_recorded_path` already makes
    one layer down. This function adds nothing to that decision; it translates it
    into this module's vocabulary once, so no caller re-interprets it.
    """
    resolution = locations.resolve_recorded_path(
        recorded, root=root, prefix_map=prefix_map
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
        readability = probe(Path(path or ""))
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
        yield ScannedTrack(
            content_id=row.content_id,
            recorded=row.recorded,
            path=path,
            readability=readability,
            disposition=disposition,
            genre=row.genre,
            bucket=bucket,
            match=match,
        )


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
