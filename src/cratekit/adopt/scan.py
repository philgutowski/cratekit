"""The census: every collection row placed in exactly one named category.

THIS MODULE IS TOTAL (AE12). "Keep what you can read and plan for those" was
shipped once, and a library holding online-only files produced a plan quietly
covering fewer tracks than it had. So every row comes back as a
:class:`ScannedTrack` with a :class:`Readability` saying what the file is and a
:class:`Disposition` saying what adoption means to do, and the plan above proves
nothing was dropped by a set comparison.

THE ROUTER'S FALLBACK TIER IS NOT AN ANSWER HERE. A track whose genre is blank or
declared too coarse cannot be split by tag, and accepting the fallback would file
thousands of tracks into one folder on an approval that looked complete. Those
get :attr:`Disposition.NEEDS_GENRE`, read off the router's own report so there is
no second opinion to drift.

THE PROBE IS INJECTED, because the shapes it recognises (a dataless file, a
provider stub beside the recorded name) cannot be made in a test on demand. The
default is small, and every category it returns is exercised against a
temporary directory.

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

#: The suffix and prefix a consumer file synchroniser gives the stub it leaves
#: beside a name whose bytes it evicted. The library records the ORIGINAL name,
#: so asking only about it would report a file the user still has as missing.
PLACEHOLDER_SUFFIX = ".icloud"
PLACEHOLDER_PREFIX = "."

#: ``SF_DATALESS`` from macOS ``sys/stat.h``: set in ``st_flags`` on a file whose
#: bytes a file provider has evicted, the one answer to "are the bytes here" that
#: downloads nothing. A literal because :mod:`stat` does not export it; inert
#: where there is no ``st_flags``.
DATALESS_FLAG = 0x40000000


class Readability(StrEnum):
    """What the scan found where the library says a track's file is.

    A CLOSED SET OF NAMES, because each has its own remedy: "the file is gone" and
    "the file is in the cloud" are not fixed the same way (AE12).
    """

    #: The file is present and its bytes can be read on this machine.
    READABLE = "readable"

    #: The location resolves to a path here and nothing is there.
    MISSING = "missing"

    #: Something is there and this account cannot read it.
    UNREADABLE = "unreadable"

    #: Cloud-backed or online-only: the name exists and the bytes do not.
    ONLINE_ONLY = "online-only"

    #: An absolute path this installation maps no prefix for. The remedy is
    #: configuration, not a drive, so it is not MISSING.
    UNMAPPED = "unmapped"

    #: Not a path on this machine at all: a streaming pseudo-location, a
    #: device-relative one, one naming another host, or a string no file can have.
    #: Folded together because they share a remedy: nothing local can be done.
    NOT_A_PATH = "not-a-path"


#: The categories a track can be adopted FROM, as a set, so a new category is
#: never silently adoptable.
ADOPTABLE: frozenset[Readability] = frozenset({Readability.READABLE})


class Disposition(StrEnum):
    """What adoption means to do about one track. Every track has exactly one.

    There is no member meaning "nothing": a plan that does not mention a track
    reads like a plan not yet built.
    """

    #: A bucket resolved from the track's own genre, so the plan can place it.
    ROUTE = "route"

    #: The genre is blank, declared too coarse, or resolved only through the
    #: fallback tier. It goes to a person as a review item.
    NEEDS_GENRE = "needs-genre"

    #: The file is not in an adoptable category. The plan carries it with the
    #: category that says why.
    EXCLUDED = "excluded"

    #: Routable, and the plan will not place it: a person answered "leave that
    #: folder alone", or the track already holds a different competing sub in the
    #: same bucket and the writer only adds (R-731). One member with a reason,
    #: because both answers are "nothing". Set by the plan layer.
    WITHHELD = "withheld"

    #: The genre resolved to a bucket that declares no sub for this track's energy
    #: reading. Set by the plan layer; not NEEDS_GENRE, since the genre is right.
    UNDECLARED = "undeclared"


@dataclass(frozen=True, slots=True)
class CollectionRow:
    """The four things the census needs from one row of the user's collection.

    A narrow record, so the database producer and the tests agree on one shape.
    ``content_id`` is the row identifier rekordbox allocated, which a rename
    cannot move. ``deleted`` has NO DEFAULT: False would hand every tombstone to
    the census as a live row (U19).
    """

    content_id: str
    recorded: str
    genre: str
    deleted: bool


@dataclass(frozen=True, slots=True)
class ScannedTrack:
    """One row, where its file is, and what adoption proposes about it.

    ``bucket`` is a stable taxonomy identifier, empty unless routing, never a
    display name (R19, D5).
    """

    content_id: str
    recorded: str
    path: str | None
    readability: Readability
    disposition: Disposition
    genre: str
    bucket: str = ""
    #: How the router reached the bucket, so a report can show the fuzzy share.
    match: str = ""
    #: The energy level the file's own tag holds, or None. Read only for an
    #: adoptable file, because opening an online only one fetches it.
    energy: int | None = None
    #: True when the tags could not be read, which is not holding no energy tag.
    energy_unreadable: bool = False
    #: The file's second genre (U340), and the bucket it files the track into
    #: beside ``bucket``, both empty when it names none or was not read.
    second_genre: str = ""
    second_bucket: str = ""


def probe_readability(path: Path) -> Readability:
    """Classify one resolved path on this machine. The default probe.

    TOTAL: the census is a generator, so a raise kills the walk and every row
    after it. A directory with no execute bit raises ``PermissionError`` and a
    null byte raises ``ValueError``, so both outer handlers name a category.

    THE RECORDED NAME IS ASKED FIRST. A synchroniser's stub outlives the file
    coming back, so it is consulted only where the recorded name is absent.
    Whether the bytes are here is asked of ``st_flags`` without reading them,
    since opening a dataless file downloads it.
    """
    try:
        return _probe(path)
    except ValueError:
        # A string no file can be named by, an embedded null byte in practice.
        return Readability.NOT_A_PATH
    except OSError:
        # Something is there and this account cannot read it.
        return Readability.UNREADABLE


def _placeholder_beside(path: Path) -> bool:
    """Whether a synchroniser's stub sits beside the recorded name."""
    placeholder = path.with_name(f"{PLACEHOLDER_PREFIX}{path.name}{PLACEHOLDER_SUFFIX}")
    try:
        return placeholder.exists()
    except OSError:
        # A directory that refused the question is no evidence of a stub.
        return False


def _is_dataless(info) -> bool:
    """Whether the name is here and the bytes are not, asked without a read.

    The flag, not the block count: a sparse file and every file on a mount that
    does not populate the count also report no blocks, and would exclude a whole
    library as cloud backed. A platform without the flag falls through to a read.
    """
    return bool(getattr(info, "st_flags", 0) & DATALESS_FLAG)


def _probe(path: Path) -> Readability:
    """The probe's actual questions. Raises; :func:`probe_readability` does not."""
    try:
        info = path.stat()
    except FileNotFoundError:
        return Readability.ONLINE_ONLY if _placeholder_beside(path) else Readability.MISSING
    if not stat_module.S_ISREG(info.st_mode):
        return Readability.MISSING
    if _is_dataless(info):
        return Readability.ONLINE_ONLY
    with path.open("rb") as handle:
        handle.read(1)
    return Readability.READABLE


def _as_recorded_text(recorded: object) -> str | None:
    """One recorded location as text, or None when it is not a location at all.

    A database need not agree with the annotation. A null ``FolderPath`` once
    raised out of the census, and a :class:`~pathlib.Path` refused as "not a
    string" excluded a whole library; ``os.fspath`` turns it back. Anything else
    is refused rather than passed through ``str()``.
    """
    if isinstance(recorded, str):
        return recorded
    if isinstance(recorded, os.PathLike):
        coerced = os.fspath(recorded)
        return coerced if isinstance(coerced, str) else None
    return None


#: The resolver's two refusals, in this module's vocabulary.
_REFUSED = {
    locations.Resolution.NOT_A_PATH: Readability.NOT_A_PATH,
    locations.Resolution.UNMAPPED: Readability.UNMAPPED,
}


def _resolved_path(
    recorded: str, *, root: Path | str, prefix_map: Sequence[locations.PrefixRule]
) -> tuple[str | None, Readability | None]:
    """Where a recorded location lives here, or the category that says why not.

    DECODED FIRST: rekordbox records a percent-encoded file URL, and
    :func:`locations.resolve_recorded_path` rightly refuses anything not opening
    with a slash, so the raw column would make every row ``not-a-path``. The
    presence proof cannot see that, since :func:`cratekit.adopt.plan.covers`
    compares identifiers, so only a test of the real shape can. The decision is
    the resolver's, translated here once.
    """
    text = _as_recorded_text(recorded)
    if text is None:
        return None, Readability.NOT_A_PATH
    try:
        decoded = locations.location_to_path(text)
    except locations.LocationDecodeError:
        # A location naming another host has no local path to invent.
        return None, Readability.NOT_A_PATH
    resolution = locations.resolve_recorded_path(decoded, root=root, prefix_map=prefix_map)
    refused = _REFUSED.get(resolution.resolution)
    return (None, refused) if refused is not None else (resolution.path, None)


def classify_genre(declared: taxonomy.Taxonomy, genre: str) -> tuple[Disposition, str, str]:
    """Decide what a track's own genre entitles adoption to do with it.

    The disposition, the bucket identifier when there is one, and how the router
    reached it. The fallback tier is not an answer here, and the too-coarse test
    is the taxonomy's own, so a user's template says what is too coarse.
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
    second_reader: Callable[[Path], str | None] | None = tags.read_second_genre_checked,
) -> Iterator[ScannedTrack]:
    """Classify every row, once, in one walk.

    A GENERATOR consumed once (U18). A tombstone is skipped: the census is total
    over the LIVE collection, and adopting a removed track would put it back. The
    injected probe is not trusted to be total, so the two shapes a filesystem
    raises are named here. The energy reading comes off the file through the
    reader the routing pass uses, and a reader failure is recorded on the track
    rather than read as absence. The second genre (U340) is read the same way
    for a routed track, and ``second_reader`` None reads none, for a walk that
    files nothing.
    """
    for row in rows:
        if row.deleted:
            continue
        path, readability = _resolved_path(row.recorded, root=root, prefix_map=prefix_map)
        if readability is None:
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
        second = (
            _second_of(Path(path or ""), second_reader)
            if disposition is Disposition.ROUTE and second_reader is not None
            else ""
        )
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
            second_genre=second,
            second_bucket=routing.second_bucket(declared, row.genre, second) or "",
        )


def _second_of(path: Path, reader: Callable[[Path], str | None]) -> str:
    """The file's second genre, empty when it holds none or could not be read.

    AN UNREAD SECOND GENRE PLANS NO SECOND ENTRY: the track's first genre
    entry is the census's whole answer, as it was before U340.
    """
    try:
        return (reader(path) or "").strip()
    except (tags.TagReadFailed, OSError):
        return ""


def _energy_of(path: Path, reader: Callable[[Path], int | None]) -> tuple[int | None, bool]:
    """The file's energy level and whether reading it failed."""
    try:
        return reader(path), False
    except (tags.TagReadFailed, OSError):
        return None, True


def _tally(members: Iterable[StrEnum], found: Iterable[StrEnum]) -> dict[str, int]:
    """One count per member, derived from the members so zeroes are present (AE12)."""
    counts = {str(member): 0 for member in members}
    for value in found:
        counts[str(value)] += 1
    return counts


def categories(scanned: Iterable[ScannedTrack]) -> dict[str, int]:
    """How many tracks landed in each named category, zeroes included (AE12)."""
    return _tally(Readability, (track.readability for track in scanned))


def dispositions(scanned: Iterable[ScannedTrack]) -> dict[str, int]:
    """How many tracks carry each disposition. Derived, zeroes included."""
    return _tally(Disposition, (track.disposition for track in scanned))
