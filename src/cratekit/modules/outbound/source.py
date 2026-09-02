"""Where an outbound write's items come from: one rekordbox collection export.

THE LIVE DATABASE IS NOT AN OPTION HERE and that is a product constraint rather
than a gap. Outside the backup feature the live rekordbox database is hands off,
and no collection reader against it has landed, which is the same reason
``R-203`` gives for ``adopt.scan`` being unbound. So both outbound verbs read a
collection export the operator produced, through
:func:`cratekit.modules.reports.export.read_export_file`, which is the one reader
``cli/reports.py`` already uses. A second reader would be a second answer to
"what does this library contain", and two answers is how they come to disagree.
The operator cost of reading a document somebody has to make by hand, and the
fact that nothing warns when it is stale, are R-227.

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
from pathlib import Path
from typing import Mapping

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
    """

    key: str
    name: str
    track_ids: tuple[str, ...]
    dangling: tuple[str, ...] = ()
    repeated: tuple[str, ...] = ()


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
    library: Library, track_ids: tuple[str, ...] | list[str]
) -> tuple[LocalTrack, ...]:
    """The export engine's input for these identifiers.

    THE ISRC IS EMPTY AND THAT IS THE FORMAT RATHER THAN AN OMISSION. A rekordbox
    collection export carries no ISRC attribute, so there is none to read and
    inventing one would hand the provider seam a fabricated identity. The title
    and artist are carried anyway, because ``export.plan`` puts them on an
    ``Unmatched`` row and an unmatched row with no name is unreportable.
    """
    return tuple(
        LocalTrack(
            identity=track_id,
            title=entry.name,
            artist=entry.artist,
        )
        for track_id, entry in _rows(library, track_ids)
    )


def heart_candidates(
    library: Library, track_ids: tuple[str, ...] | list[str]
) -> tuple[HeartCandidate, ...]:
    """The hearts engine's input for these identifiers.

    ``remote_id`` is left empty so the engine asks the account to match, which is
    the only route this build has: see :func:`local_tracks` about the ISRC.
    """
    return tuple(
        HeartCandidate(row_id=track_id)
        for track_id, _entry in _rows(library, track_ids)
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
    "Library",
    "ResolvedPlaylist",
    "forget_libraries",
    "heart_candidates",
    "local_tracks",
    "read_library",
    "required_path",
    "resolve",
]
