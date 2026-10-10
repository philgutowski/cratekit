"""Where an outbound write's items come from: one rekordbox collection export.

THE LIVE DATABASE IS NOT AN OPTION HERE and that is a product constraint rather
than a gap. Outside the backup feature the live rekordbox database is hands off,
and no collection reader against it has landed, which is the same reason
``R-203`` gives for ``adopt.scan`` being unbound. So both outbound verbs read a
collection export the operator produced, through
:func:`cratekit.modules.reports.export.read_export_file`, which is the one reader
``cli/reports.py`` already uses. A second reader would be a second answer to
"what does this library contain", and two answers is how they come to disagree.
The operator cost of reading a document somebody has to make by hand is R-227.
That a stale one used to resolve, queue and write with nothing said is the half
of R-227 :func:`export_age` answers: the file's date is read here and shown in
the plan a person confirms, and nothing is refused over it.

**WHY THIS MODULE EXISTS RATHER THAN TWO COPIES.** ``export.playlist`` and
``sync.favorites`` ask the same question, "which library rows is this write made
of", and answer it against the same document. Two implementations would disagree
about what an absent playlist is, which is precisely the decision the zero item
rule turns on: ``core/jobs.py`` reports a job with no items as SUCCEEDED by
design, so a verb that queues an empty job reports a clean success over work it
never did. This module is the one place that refuses instead.

**THE IMPORT IS ALIASED, ALWAYS.** Three modules in this tree are called
``export``: ``cratekit.export.cli`` is the verb, ``cratekit.modules.outbound.export``
is the engine that writes a remote playlist, and
``cratekit.modules.reports.export`` is the reader below. Both outbound shells now
name two of the three, so the reader is bound as ``library_export`` here and the
engine as ``outbound_export`` at its call sites. One symbol meaning two things in
two modules is the defect ``docs/METHOD.md`` says to hunt once a suite is green.

Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Mapping

from cratekit.acquire import match
from cratekit.core import config, locations, naming, tags
from cratekit.core.cause import Scope, refuse
from cratekit.modules.outbound.export import LocalTrack
from cratekit.modules.outbound.hearts import HeartCandidate
from cratekit.modules.reports import export as library_export

#: The favourites playlist this build sweeps unless the caller names another.
#:
#: ``All Favorites`` RATHER THAN ``Favorites``, and the difference is the whole
#: value of this constant. In the live library ``Favorites`` is a FOLDER, created
#: by the source system through ``ensure_folder(db, "Favorites")``, and its track
#: bearing children are ``All Favorites`` and the quarter playlists.
#: ``LibraryView.playlists`` holds playlists only, so a folder never appears in
#: it, and a default naming the folder would refuse ``export-playlist-unknown``
#: on the operator's real library on every run while every fixture in this
#: repository stayed green, because a fixture names a playlist directly.
DEFAULT_FAVORITES_PLAYLIST = "All Favorites"


@dataclass(frozen=True, slots=True)
class Library:
    """One collection export, read once, with its entries indexed by identifier.

    THE INDEX IS BUILT HERE RATHER THAN ASKED FOR PER ROW.
    ``LibraryView.entry`` is a linear scan and says so in its own docstring, so
    calling it once per track is a walk of the collection per track, which is
    the N times M shape ``modules/reports/coverage.py`` records this repository
    shipping and then removing.
    """

    path: Path
    view: library_export.LibraryView
    entries: Mapping[str, library_export.CollectionEntry]


@dataclass(frozen=True, slots=True)
class ResolvedPlaylist:
    """One library playlist, and everything the derivation had to decide about it.

    ``dangling`` and ``repeated`` are carried rather than dropped because both
    are things the document said that this build declined to act on, and a person
    who exports twenty nine of thirty tracks should be told which one is missing
    and why.

    ``from_playlist``, ``from_colour`` and ``pink_missing`` are the favourites
    sweep's union fields (R-228). ``resolve`` leaves them at their defaults of
    zero and empty; ``favorites.cli`` always fills them after reading pink rows
    from a read only open. An export verb never shows these fields.
    """

    key: str
    name: str
    track_ids: tuple[str, ...]
    dangling: tuple[str, ...] = ()
    repeated: tuple[str, ...] = ()
    from_playlist: int = 0
    from_colour: int = 0
    pink_missing: tuple[str, ...] = ()


#: How far ahead of the clock a file may be dated and still be read as written
#: just now. A network volume whose clock runs ahead is seconds out, and exFAT
#: stores local time with no zone, which is up to fourteen hours. Past a day it
#: is no longer a clock, it is a date that cannot be true.
FUTURE_TOLERANCE = timedelta(days=1)

_SECONDS_PER_DAY = 86_400


@dataclass(frozen=True, slots=True)
class ExportAge:
    """When the export document was last written, against a declared limit.

    ``written`` IS THE FILE'S MODIFICATION TIME, because a rekordbox collection
    export carries no date of its own: its header names the product and the
    version and nothing else. That makes it a proxy with a known weakness, which
    is stated rather than hidden. A copy made without preserving times, or a sync
    client that rewrites the file, gives an old export a new date, so a recent
    date is weaker evidence than an old one. It is why this is shown to a person
    and never decided on.

    FOUR STATES, AND ONLY ONE OF THEM IS "RECENT". ``written`` is none when the
    file could not be asked. It is set and :attr:`future_dated` when the date is
    further ahead of the clock than :data:`FUTURE_TOLERANCE`, which cannot be
    true and so cannot be judged. Otherwise the age is a duration and is either
    past the limit or within it. "I could not read a date" folded into "the date
    is recent" is the first recurring defect pattern in ``docs/METHOD.md``, and
    a future date clamped to an age of nothing was that pattern arriving by a
    second route: it read as the freshest export there could be until the clock
    caught up with it.

    THE AGE IS DERIVED, never stored beside the date. ``written`` and
    ``judged_at`` are set together or not at all, and the constructor refuses
    anything else, so no caller can build a date that looks known and carries no
    age to be stale by.
    """

    path: Path
    limit_days: int
    written: datetime | None = None
    judged_at: datetime | None = None

    def __post_init__(self) -> None:
        if (self.written is None) != (self.judged_at is None):
            raise ValueError(
                "an export's date and the instant it is judged at are one fact: "
                "set both or neither"
            )

    @property
    def known(self) -> bool:
        return self.written is not None

    @property
    def future_dated(self) -> bool:
        if self.written is None or self.judged_at is None:
            return False
        return self.written - self.judged_at > FUTURE_TOLERANCE

    @property
    def age(self) -> timedelta | None:
        """How long ago it was written, or none when that cannot be said."""
        if self.written is None or self.judged_at is None or self.future_dated:
            return None
        return max(self.judged_at - self.written, timedelta(0))

    @property
    def age_days(self) -> int | None:
        """Whole days, floored. For display; :attr:`stale` compares durations."""
        age = self.age
        return None if age is None else age.days

    @property
    def stale(self) -> bool:
        """PAST the limit, as a duration. Seven days exactly is not past seven.

        Not ``age_days > limit_days``: floored days read seven days and twenty
        three hours as seven, which is fresh for a day longer than the key says.
        COMPARED IN SECONDS rather than against ``timedelta(days=limit_days)``,
        which raises ``OverflowError`` on a limit no duration can hold.
        Validation bounds the configured key, and this holds for a value built
        in code that never touched a file.
        """
        age = self.age
        return age is not None and age.total_seconds() > self.limit_days * _SECONDS_PER_DAY


def export_age(path: Path, *, limit_days: int, now: datetime | None = None) -> ExportAge:
    """How old the export at ``path`` is. Never raises and never refuses.

    A STAT RATHER THAN A FIELD ON :class:`Library`, because the parsed document
    is memoized for the life of the process and the age is a question about the
    file as it is now. ``limit_days`` is required for the reason ``cfg`` is on
    :func:`local_tracks`: a default would let a caller that forgot the
    configuration warn on somebody else's number.

    THE CONVERSION IS INSIDE THE SAME GUARD AS THE STAT. A modification time no
    date can hold, which a damaged FAT volume or a network share can return,
    raises from ``fromtimestamp`` rather than from ``stat``. Either way the
    answer is that the date could not be read, never a traceback: this is not a
    ``CratekitError``, so escaping from here would end a whole ``sync all`` pass.
    """
    located = Path(path)
    try:
        written = datetime.fromtimestamp(located.stat().st_mtime, tz=timezone.utc)
    except (OSError, OverflowError, ValueError):
        return ExportAge(path=located, limit_days=limit_days)
    return ExportAge(
        path=located,
        limit_days=limit_days,
        written=written,
        judged_at=now or datetime.now(timezone.utc),
    )


#: Parsed exports, keyed on the resolved absolute path.
#:
#: MEMOIZED BECAUSE AN ITEM IS ONE TRACK. ``cli.handlers.run_job`` drives every
#: item of a job inside one process and the handler reads the frozen export on
#: each call, so a hundred item job would locate and parse every track element in
#: the whole document a hundred times. The key is the resolved path rather than
#: the argument, so two spellings of one file are one entry.
_LIBRARIES: dict[Path, Library] = {}


def forget_libraries() -> None:
    """Drop the parsed exports. For a test that rewrites a file it already read."""
    _LIBRARIES.clear()


def required_path(named: str | None) -> Path:
    """The export document to read, or a refusal naming that none was given.

    A REFUSAL RATHER THAN AN ARGPARSE ``required=True``, because status 2 belongs
    to the argument parser and to nothing else, which is the rule
    ``export-playlist-unknown`` and ``tag-retag-folder-unknown`` already follow.
    The parser accepts the invocation; what is missing is an input the verb needs
    before it can decide what its work is.
    """
    text = str(named or "").strip()
    if not text:
        raise refuse(
            "outbound-export-required",
            "this verb decides what to write from a rekordbox collection "
            "export, and none was named, so it has no work to queue",
            steps=(
                "export the collection from rekordbox and pass the file with "
                "--export",
            ),
            scope=Scope.RUN,
            origin=("outbound", "source"),
        )
    # ABSOLUTE, LEXICALLY. ``jobs.spawn`` starts the resumed child with the
    # RESUMING process's working directory, so a relative path frozen into a
    # payload names different files in different directories. ``absolute``
    # resolves nothing and stats nothing, so it does not turn this into a read.
    return Path(text).absolute()


def read_library(path: Path) -> Library:
    """Read one collection export, once per process.

    The refusal for a path that is not readable, is not an export, or is a
    truncated one comes from the reader itself, so every consumer in the product
    says the same sentence about the same file.
    """
    resolved = Path(path).absolute()
    found = _LIBRARIES.get(resolved)
    if found is not None:
        return found
    view = library_export.read_export_file(resolved)
    library = Library(
        path=resolved,
        view=view,
        entries={entry.track_id: entry for entry in view.entries},
    )
    _LIBRARIES[resolved] = library
    return library


def _display_path(playlist: library_export.Playlist) -> str:
    return "/".join(playlist.path)


def playlist_contents(library: Library) -> dict[str, tuple[str, ...]]:
    """Every playlist path this export carries, as a ledger key, with its tracks.

    THE SAME SPELLING :func:`resolve` GIVES ``ResolvedPlaylist.key``, from the
    same function, because the outbound ledger asks of each recorded key
    whether the library still carries it (R-229) and a second spelling would
    answer no for every crate there is. The tracks ride along because a path
    can be reused for a different crate, and only its contents say so.

    TWO PLAYLISTS CAN SHARE ONE PATH, which :func:`resolve` refuses as ambiguous
    when it is the one asked for. Here their tracks are pooled, so a record
    under that path stays a living crate's while either of them carries it.
    """
    pooled: dict[str, tuple[str, ...]] = {}
    for playlist in library.view.playlists:
        key = _display_path(playlist)
        pooled[key] = (*pooled.get(key, ()), *playlist.track_ids)
    return pooled


def resolve(library: Library, identifier: str) -> ResolvedPlaylist:
    """The playlist ``identifier`` names, or a refusal saying which way it failed.

    THREE REFUSALS RATHER THAN ONE, because they send a person to three different
    places. Nothing carries that name; several things do; the thing is there and
    is empty. A single "cannot export that" would make a person who typed a
    folder name and a person whose crate is genuinely empty read the same
    sentence, and only one of them has a playlist to look at.

    A FOLDER RESOLVES AS UNKNOWN, and that is the reader's shape rather than a
    decision taken here: ``LibraryView.playlists`` holds nodes that carry tracks,
    and a folder carries nodes. It is worth stating because the live library's
    ``Favorites`` is a folder, which is why
    :data:`DEFAULT_FAVORITES_PLAYLIST` names its child.
    """
    wanted = str(identifier or "").strip()
    if not wanted:
        raise refuse(
            "export-playlist-unknown",
            "no library playlist was named, so there is nothing to resolve",
            steps=("pass the playlist identifier after the verb",),
            scope=Scope.RUN,
            origin=("outbound", "source"),
        )

    exact = [p for p in library.view.playlists if _display_path(p) == wanted]
    matched = exact or [p for p in library.view.playlists if p.display == wanted]
    if not matched:
        raise refuse(
            "export-playlist-unknown",
            f"no playlist in {library.path.name} is named {wanted!r}. A folder "
            f"of that name is not a match either, because a folder holds "
            f"playlists rather than tracks",
            steps=(
                "name the playlist by its display name, or by its full path "
                "joined with /",
            ),
            scope=Scope.RUN,
            origin=("outbound", "source"),
            detail={"playlist": wanted},
        )
    if len(matched) > 1:
        paths = sorted(_display_path(p) for p in matched)
        raise refuse(
            "export-playlist-ambiguous",
            f"{wanted!r} names {len(matched)} playlists in {library.path.name}, "
            f"and writing the wrong one to a streaming account is not something "
            f"this build can undo",
            steps=(f"name one of them by its full path: {', '.join(paths)}",),
            scope=Scope.RUN,
            origin=("outbound", "source"),
            detail={"playlist": wanted, "paths": paths},
        )

    playlist = matched[0]
    key = _display_path(playlist)
    kept: list[str] = []
    seen: set[str] = set()
    dangling: list[str] = []
    repeated: list[str] = []
    for track_id in playlist.track_ids:
        if track_id not in library.entries:
            # R-146: the reader accepts a playlist naming a TrackID the
            # COLLECTION does not carry, so this is reachable input rather than
            # a hypothetical. Reported rather than dropped, because a person
            # whose export is short one track needs to know which one.
            dangling.append(track_id)
            continue
        if track_id in seen:
            # ONE IDENTIFIER IS ONE ITEM. ``job_items`` is keyed on
            # ``(job_id, item_id)``, so handing the same identifier to
            # ``jobs.enqueue`` twice raises an IntegrityError that reaches a
            # person as ``internal-error`` with the report-defect remedy, over a
            # document the reader accepted.
            repeated.append(track_id)
            continue
        seen.add(track_id)
        kept.append(track_id)

    if not kept:
        raise refuse(
            "export-playlist-empty",
            f"{key!r} in {library.path.name} carries no track this export "
            f"can write, so the job would queue with nothing to claim and be "
            f"reported as a success over work it never did",
            steps=("add tracks to the playlist and export the collection again",),
            scope=Scope.RUN,
            origin=("outbound", "source"),
            detail={"playlist": key, "dangling": dangling},
        )

    return ResolvedPlaylist(
        key=key,
        name=playlist.display,
        track_ids=tuple(kept),
        dangling=tuple(dangling),
        # DEDUPED, so the count and the joined list in the warning describe
        # distinct tracks. A playlist naming one track three times appended it
        # twice and reported "2 track(s) appear more than once", naming one.
        repeated=tuple(dict.fromkeys(repeated)),
    )


def local_tracks(
    library: Library,
    track_ids: tuple[str, ...] | list[str],
    *,
    cfg: config.Config,
) -> tuple[LocalTrack, ...]:
    """The export engine's input for these identifiers.

    THE ISRC COMES FROM THE AUDIO FILE, NOT THE EXPORT (R-355). A rekordbox
    collection export carries no ISRC attribute, and the account matches on
    nothing else a row has, so without the file's own tag every live export
    matched nothing and reported a clean job. See :func:`isrc_for` for how the
    file is found and when the answer is empty. The title and artist are carried
    anyway, because ``export.plan`` puts them on an ``Unmatched`` row and an
    unmatched row with no name is unreportable.

    ``cfg`` IS REQUIRED, never defaulted. A default of none would restore the
    defect for any caller that forgot it, silently, as a job that hearts nothing.
    """
    rules = prefix_rules(cfg)
    template = _template(cfg)
    _require_root(cfg)
    return tuple(
        LocalTrack(
            identity=track_id,
            title=entry.name,
            artist=entry.artist,
            isrc=found.isrc,
            album=found.album,
            release_title=release_title(entry, template=template),
        )
        for track_id, entry in _rows(library, track_ids)
        for found in (file_identity(entry, root=cfg.library.root, prefix_map=rules),)
    )


def heart_candidates(
    library: Library,
    track_ids: tuple[str, ...] | list[str],
    *,
    cfg: config.Config,
) -> tuple[HeartCandidate, ...]:
    """The hearts engine's input for these identifiers.

    ``remote_id`` is left empty so the engine asks the account to match, and the
    ISRC is read from the file exactly as :func:`local_tracks` reads it, so the
    two engines cannot come to disagree about one row's identity. The release
    title and the artist are carried for the same reason and from the same
    function: they are what the account chooses by when one ISRC names several
    releases, and a sweep that carried neither left every such favourite
    unmatched (R-356).
    """
    rules = prefix_rules(cfg)
    template = _template(cfg)
    _require_root(cfg)
    return tuple(
        HeartCandidate(
            row_id=track_id,
            isrc=found.isrc,
            album=found.album,
            release_title=release_title(entry, template=template),
            artist=entry.artist,
        )
        for track_id, entry in _rows(library, track_ids)
        for found in (file_identity(entry, root=cfg.library.root, prefix_map=rules),)
    )


def _template(cfg: config.Config) -> naming.NameTemplate:
    """The declared naming shape, on ``acquire.match_cli.library_template``'s rule.

    A configuration with no marker text is one where no file carries a marker,
    and a marker rule with an empty literal is refused at construction, so the
    rule is left out rather than the whole item refused over a naming policy.
    Built here rather than imported because that module is a verb's shell.
    """
    marker = (cfg.naming.lossy_marker or "").strip()
    if not marker:
        return naming.NameTemplate()
    return naming.NameTemplate(
        markers=(naming.MarkerRule(field="lossy", literal=marker),)
    )


def release_title(
    entry: library_export.CollectionEntry, *, template: naming.NameTemplate
) -> str:
    """The row's title as a release spells it, the library's naming head off.

    ``CollectionEntry.name`` is the rekordbox display field and carries the key
    and tempo head this library writes, so compared as it stands it agrees with
    no provider title at all. Stripped through the DECLARED template, never a
    pattern of this module's own, for the reason that class's docstring gives.
    """
    return naming.strip_heads(entry.name, template=template)


def _require_root(cfg: config.Config) -> None:
    """Refuse when the library root is not there, before any tag is read.

    :func:`isrc_for` reads a file that is not there as no ISRC, which is the
    honest answer for ONE untagged or moved file. With the volume unmounted it is
    the answer for EVERY row, and the job would end succeeded with the whole sweep
    unmatched, which is R-355's symptom arriving by a second route. So an absent
    root stops the item rather than reading as a library of untagged files.

    A root that is present but holds a different volume is not caught here; that
    is ``library.mounted`` in doctor, which the registry already declares.
    """
    root = Path(cfg.library.root)
    if root.is_dir():
        return
    raise refuse(
        "library-volume-unmounted",
        f"the library root {root} is not a directory on this machine, so no "
        f"track's audio file can be read for its ISRC and every row would be "
        f"reported unmatched; nothing was written",
        steps=("mount the library volume and resume the job",),
        origin=("outbound", "source"),
        detail={"library": str(root)},
    )


def prefix_rules(cfg: config.Config) -> list[locations.PrefixRule]:
    """The configured volume prefix map, as the resolver takes it.

    Without it a library whose drive was renamed resolves no row at all, which
    R-372 measured on the live library as 0 of 9937.
    """
    return [
        locations.PrefixRule(source_prefix, target)
        for source_prefix, target in cfg.resolved_prefix_map()
    ]


#: Twelve characters: country, registrant, year, designation. Hyphens and spaces
#: are presentation and are folded away before this is asked.
def isrc_for(
    entry: library_export.CollectionEntry,
    *,
    root: Path | str,
    prefix_map: list[locations.PrefixRule],
) -> str:
    """The ISRC the row's audio file carries, or ``""`` when there is none to trust.

    EMPTY IS NOT A GUESS, IT IS THE EXISTING ROUTE. An empty ISRC makes the
    account fall back to an exact provider reference and otherwise report the row
    unmatched, which is what every row did before this read existed. So each way
    this can fail, a location that is not a local file, a prefix no rule maps, a
    file that is gone, a container with no tag, a value that is not an ISRC, ends
    in the same honest unmatched row rather than a refusal that would fail the
    item over one untagged file.

    A MALFORMED VALUE IS DROPPED rather than passed on, because the account
    queries the provider with exactly this string, and a tag holding a catalogue
    number or a stray label would be a lookup of something that is not a
    recording's identity.
    """
    return file_identity(entry, root=root, prefix_map=prefix_map).isrc


@dataclass(frozen=True, slots=True)
class FileIdentity:
    """What the row's audio file says it is: its ISRC and the release it names.

    ``album`` is the file's own album tag, stripped, or ``""`` when it carries
    none (R-572). It is a statement about which release the file was cut from,
    and the account reads it only to choose among releases one ISRC already
    named, never to search.
    """

    isrc: str = ""
    album: str = ""


def file_identity(
    entry: library_export.CollectionEntry,
    *,
    root: Path | str,
    prefix_map: list[locations.PrefixRule],
) -> FileIdentity:
    """:func:`isrc_for` and the file's album tag, through ONE container open.

    Every way :func:`isrc_for` answers empty answers an empty identity here,
    for the reasons that function gives. The album is read in the same open as
    the ISRC (R-572), so a single and its album cut sharing one code can be
    told apart by the release the file names, and no row pays a second read.
    """
    if not entry.location:
        return FileIdentity()
    try:
        recorded = locations.location_to_path(entry.location)
    except locations.LocationDecodeError:
        return FileIdentity()
    resolved = locations.resolve_recorded_path(recorded, root=root, prefix_map=prefix_map)
    if resolved.path is None:
        return FileIdentity()
    path = Path(resolved.path)
    if not path.is_file():
        return FileIdentity()
    read = tags.read_tags(path, ("isrc", "album"))
    # THE INDEX'S OWN FOLD AND VALIDATION, so the hearts export and the
    # library index cannot read one tag two ways.
    return FileIdentity(
        isrc=match.isrc_token(read["isrc"]),
        album=str(read["album"] or "").strip(),
    )


def _rows(
    library: Library, track_ids: tuple[str, ...] | list[str]
) -> tuple[tuple[str, library_export.CollectionEntry], ...]:
    """The collection rows for these identifiers, skipping any the export lacks.

    Skipping rather than refusing, because :func:`resolve` already refused the
    playlist whose every identifier is dangling, and a handler running ONE item
    is asking about an identifier the queue already accepted. A refusal here
    would turn a stale export into an internal error on the item's row.
    """
    return tuple(
        (track_id, library.entries[track_id])
        for track_id in track_ids
        if track_id in library.entries
    )


__all__ = [
    "DEFAULT_FAVORITES_PLAYLIST",
    "FUTURE_TOLERANCE",
    "ExportAge",
    "FileIdentity",
    "Library",
    "ResolvedPlaylist",
    "export_age",
    "file_identity",
    "forget_libraries",
    "heart_candidates",
    "isrc_for",
    "local_tracks",
    "prefix_rules",
    "release_title",
    "read_library",
    "required_path",
    "resolve",
]
