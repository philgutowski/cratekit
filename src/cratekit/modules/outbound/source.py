"""Where an outbound write's items come from: one rekordbox collection export.

THE LIVE DATABASE IS NOT AN OPTION HERE: outside the backup feature it is hands
off. So both outbound verbs read a collection export the operator produced,
through ``cratekit.modules.reports.export.read_export_file``, the one reader
``cli/reports.py`` uses, since two readers would come to disagree about what the
library contains. The file's date is shown in the plan, never refused over
(R-227, :func:`export_age`).

ONE MODULE, NOT TWO COPIES: ``export.playlist`` and ``sync.favorites`` ask the
same question of the same document, and this is the one place that refuses an
absent or empty playlist, since ``core/jobs.py`` reports a job with no items as
SUCCEEDED by design.

THE READER IS BOUND AS ``library_export`` and imported when used, so this module
loads with the ``reports`` toggle off; ``export`` alone would name three
modules.

Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping

from cratekit.acquire import match
from cratekit.core import config, locations, naming, tags
from cratekit.core.cause import Scope, refuse
from cratekit.modules.outbound.export import LocalTrack
from cratekit.modules.outbound.hearts import HeartCandidate

if TYPE_CHECKING:
    from cratekit.modules.reports import export as library_export

_ORIGIN = ("outbound", "source")

#: The favourites playlist this build sweeps unless the caller names another.
#: ``All Favorites``, NOT ``Favorites``: in the live library ``Favorites`` is a
#: folder, which ``LibraryView.playlists`` never holds, so naming it would
#: refuse on the real library while every fixture stayed green.
DEFAULT_FAVORITES_PLAYLIST = "All Favorites"


def __getattr__(name: str) -> Any:
    """``library_export``, the reader, imported only when asked for."""
    if name == "library_export":
        from cratekit.modules.reports import export

        return export
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


@dataclass(frozen=True, slots=True)
class Library:
    """One collection export, read once, its entries indexed by identifier.

    Indexed here because ``LibraryView.entry`` is a linear scan, which per row
    is the N times M shape ``modules/reports/coverage.py`` records removing.
    """

    path: Path
    view: library_export.LibraryView
    entries: Mapping[str, library_export.CollectionEntry]


@dataclass(frozen=True, slots=True)
class ResolvedPlaylist:
    """One library playlist, and everything the derivation had to decide about it.

    ``dangling`` and ``repeated`` are carried so a person is told which track
    is missing and why. ``from_playlist``, ``from_colour`` and ``pink_missing``
    are the favourites sweep's union (R-228), filled by ``favorites.cli`` and
    left at their defaults by ``resolve``.
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
#: just now: exFAT's zoneless local time is up to fourteen hours out, and past
#: a day a date cannot be true.
FUTURE_TOLERANCE = timedelta(days=1)

_SECONDS_PER_DAY = 86_400


@dataclass(frozen=True, slots=True)
class ExportAge:
    """When the export document was last written, against a declared limit.

    ``written`` is the file's modification time, since an export carries no
    date of its own; a copy can make an old export look new, which is why this
    is shown and never decided on. FOUR STATES, one of them recent: unknown
    (``written`` none), future dated past :data:`FUTURE_TOLERANCE`, stale, or
    within the limit, so an unreadable or impossible date never reads as
    fresh. ``written`` and ``judged_at`` are one fact, set together or not at
    all, and the age is derived from them.
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
        """PAST the limit, as a duration, so seven days and an hour is past seven.

        In seconds, since ``timedelta(days=limit_days)`` overflows on a limit
        no duration can hold.
        """
        age = self.age
        return age is not None and age.total_seconds() > self.limit_days * _SECONDS_PER_DAY


def export_age(path: Path, *, limit_days: int, now: datetime | None = None) -> ExportAge:
    """How old the export at ``path`` is. Never raises and never refuses.

    A stat on every call, since the parsed document is memoized and the age is
    about the file now. A time no date can hold raises from ``fromtimestamp``,
    so the conversion sits inside the same guard: an escape would end a whole
    ``sync all`` pass.
    """
    located = Path(path)
    try:
        written = datetime.fromtimestamp(located.stat().st_mtime, tz=timezone.utc)
    except (OSError, OverflowError, ValueError):
        return ExportAge(path=located, limit_days=limit_days)
    return ExportAge(located, limit_days, written, now or datetime.now(timezone.utc))


#: Parsed exports by resolved absolute path, since a job's handler reads the
#: frozen export once per item and an item is one track.
_LIBRARIES: dict[Path, Library] = {}


def forget_libraries() -> None:
    """Drop the parsed exports. For a test that rewrites a file it already read."""
    _LIBRARIES.clear()


def required_path(named: str | None) -> Path:
    """The export document to read, or a refusal naming that none was given.

    A refusal rather than argparse ``required=True``, since status 2 is the
    parser's alone.
    """
    text = str(named or "").strip()
    if not text:
        raise refuse(
            "outbound-export-required",
            "this verb decides what to write from a rekordbox collection "
            "export, and none was named, so it has no work to queue",
            steps=("export the collection from rekordbox and pass the file with --export",),
            scope=Scope.RUN,
            origin=_ORIGIN,
        )
    # ABSOLUTE, LEXICALLY: a resumed child runs in the resuming process's
    # directory, and ``absolute`` reads nothing.
    return Path(text).absolute()


def read_library(path: Path) -> Library:
    """Read one collection export, once per process; the reader's refusals stand."""
    from cratekit.modules.reports import export as library_export

    resolved = Path(path).absolute()
    found = _LIBRARIES.get(resolved)
    if found is not None:
        return found
    view = library_export.read_export_file(resolved)
    library = _LIBRARIES[resolved] = Library(
        resolved, view, {entry.track_id: entry for entry in view.entries}
    )
    return library


def _display_path(playlist: library_export.Playlist) -> str:
    return "/".join(playlist.path)


def playlist_contents(library: Library) -> dict[str, tuple[str, ...]]:
    """Every playlist path this export carries, as a ledger key, with its tracks.

    The same spelling :func:`resolve` gives a key, since the ledger asks of
    each recorded key whether the library still carries it (R-229). Two
    playlists sharing a path pool their tracks.
    """
    pooled: dict[str, tuple[str, ...]] = {}
    for playlist in library.view.playlists:
        key = _display_path(playlist)
        pooled[key] = (*pooled.get(key, ()), *playlist.track_ids)
    return pooled


def resolve(library: Library, identifier: str) -> ResolvedPlaylist:
    """The playlist ``identifier`` names, or a refusal saying which way it failed.

    Unknown, ambiguous and empty send a person three different places, so
    they are three refusals. A folder is unknown, since it carries playlists
    rather than tracks.
    """
    wanted = str(identifier or "").strip()
    if not wanted:
        raise refuse(
            "export-playlist-unknown",
            "no library playlist was named, so there is nothing to resolve",
            steps=("pass the playlist identifier after the verb",),
            scope=Scope.RUN,
            origin=_ORIGIN,
        )

    exact = [p for p in library.view.playlists if _display_path(p) == wanted]
    matched = exact or [p for p in library.view.playlists if p.display == wanted]
    if not matched:
        raise refuse(
            "export-playlist-unknown",
            f"no playlist in {library.path.name} is named {wanted!r}. A folder of that name is "
            f"not a match either, because a folder holds playlists rather than tracks",
            steps=("name the playlist by its display name, or by its full path joined with /",),
            scope=Scope.RUN,
            origin=_ORIGIN,
            detail={"playlist": wanted},
        )
    if len(matched) > 1:
        paths = sorted(_display_path(p) for p in matched)
        raise refuse(
            "export-playlist-ambiguous",
            f"{wanted!r} names {len(matched)} playlists in {library.path.name}, and writing the "
            f"wrong one to a streaming account is not something this build can undo",
            steps=(f"name one of them by its full path: {', '.join(paths)}",),
            scope=Scope.RUN,
            origin=_ORIGIN,
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
            # A TrackID the collection lacks (R-146), reported, not dropped.
            dangling.append(track_id)
            continue
        if track_id in seen:
            # ONE IDENTIFIER IS ONE ITEM, since a job's items are keyed on it.
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
            origin=_ORIGIN,
            detail={"playlist": key, "dangling": dangling},
        )

    return ResolvedPlaylist(
        key=key,
        name=playlist.display,
        track_ids=tuple(kept),
        dangling=tuple(dangling),
        # DEDUPED, so the warning counts distinct tracks.
        repeated=tuple(dict.fromkeys(repeated)),
    )


def _identified(
    library: Library, track_ids: tuple[str, ...] | list[str], cfg: config.Config
) -> list[tuple[str, library_export.CollectionEntry, FileIdentity, str]]:
    """Each row with its file's identity and release title, once the root is checked."""
    rules = prefix_rules(cfg)
    template = _template(cfg)
    _require_root(cfg)
    return [
        (
            track_id,
            entry,
            file_identity(entry, root=cfg.library.root, prefix_map=rules),
            release_title(entry, template=template),
        )
        for track_id, entry in _rows(library, track_ids)
    ]


def local_tracks(
    library: Library, track_ids: tuple[str, ...] | list[str], *, cfg: config.Config
) -> tuple[LocalTrack, ...]:
    """The export engine's input for these identifiers.

    THE ISRC COMES FROM THE AUDIO FILE (R-355), since an export carries none
    and the account matches on nothing else; :func:`isrc_for` says when it is
    empty. ``cfg`` is required, since a default would restore that defect.
    """
    return tuple(
        LocalTrack(track_id, entry.name, entry.artist, found.isrc, title, album=found.album)
        for track_id, entry, found, title in _identified(library, track_ids, cfg)
    )


def heart_candidates(
    library: Library, track_ids: tuple[str, ...] | list[str], *, cfg: config.Config
) -> tuple[HeartCandidate, ...]:
    """The hearts engine's input for these identifiers, read as :func:`local_tracks` reads.

    ``remote_id`` is empty so the engine asks the account to match; the
    release title and artist choose among releases one ISRC names (R-356).
    """
    return tuple(
        HeartCandidate(
            row_id=track_id,
            isrc=found.isrc,
            album=found.album,
            release_title=title,
            artist=entry.artist,
        )
        for track_id, entry, found, title in _identified(library, track_ids, cfg)
    )


def _template(cfg: config.Config) -> naming.NameTemplate:
    """The declared naming shape, ``acquire.match_cli.library_template``'s rule, not its shell."""
    return naming.NameTemplate.lossy_if_marked(cfg.naming.lossy_marker)


def name_template(cfg: config.Config) -> naming.NameTemplate:
    """The declared naming shape, for a caller stripping a title read elsewhere (U130)."""
    return _template(cfg)


def release_title(entry: library_export.CollectionEntry, *, template: naming.NameTemplate) -> str:
    """The row's title as a release spells it, its naming head stripped by the declared template."""
    return naming.strip_heads(entry.name, template=template)


def _require_root(cfg: config.Config) -> None:
    """Refuse when the library root is not there, before any tag is read.

    With the volume unmounted every row would read as untagged and the job
    end succeeded with the whole sweep unmatched (R-355). A present root on
    the wrong volume is doctor's ``library.mounted``.
    """
    root = Path(cfg.library.root)
    if root.is_dir():
        return
    raise refuse(
        "library-volume-unmounted",
        f"the library root {root} is not a directory on this machine, so no track's audio file "
        f"can be read for its ISRC and every row would be reported unmatched; nothing was written",
        steps=("mount the library volume and resume the job",),
        origin=_ORIGIN,
        detail={"library": str(root)},
    )


def prefix_rules(cfg: config.Config) -> list[locations.PrefixRule]:
    """The configured volume prefix map, without which a renamed drive resolves no row (R-372)."""
    return [locations.PrefixRule(prefix, target) for prefix, target in cfg.resolved_prefix_map()]


def isrc_for(
    entry: library_export.CollectionEntry,
    *,
    root: Path | str,
    prefix_map: list[locations.PrefixRule],
) -> str:
    """The ISRC the row's audio file carries, or ``""`` when there is none to trust.

    EMPTY IS THE EXISTING ROUTE, an honest unmatched row, for every way this
    fails, never a refusal over one untagged file; a malformed value is
    dropped, since the provider is queried with exactly this string.
    """
    return file_identity(entry, root=root, prefix_map=prefix_map).isrc


@dataclass(frozen=True, slots=True)
class FileIdentity:
    """What the row's audio file says it is: its ISRC and its album tag (R-572), or empty."""

    isrc: str = ""
    album: str = ""


def file_identity(
    entry: library_export.CollectionEntry,
    *,
    root: Path | str,
    prefix_map: list[locations.PrefixRule],
) -> FileIdentity:
    """:func:`isrc_for` and the file's album tag, through ONE container open (R-572)."""
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
    # THE INDEX'S OWN FOLD AND VALIDATION, so one tag never reads two ways.
    return FileIdentity(match.isrc_token(read["isrc"]), album=str(read["album"] or "").strip())


def _rows(
    library: Library, track_ids: tuple[str, ...] | list[str]
) -> tuple[tuple[str, library_export.CollectionEntry], ...]:
    """The collection rows for these identifiers, skipping any the export lacks.

    Skipping, since :func:`resolve` already refused an all dangling playlist
    and an item's identifier was accepted by the queue.
    """
    entries = library.entries
    return tuple((track_id, entries[track_id]) for track_id in track_ids if track_id in entries)


__all__ = [
    "DEFAULT_FAVORITES_PLAYLIST", "FUTURE_TOLERANCE", "ExportAge", "FileIdentity", "Library",
    "ResolvedPlaylist", "export_age", "file_identity", "forget_libraries", "heart_candidates",
    "isrc_for", "local_tracks", "name_template", "prefix_rules", "release_title",
    "read_library", "required_path", "resolve",
]
