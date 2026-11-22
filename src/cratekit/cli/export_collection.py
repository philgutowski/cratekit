"""``crate export collection``: a collection export without rekordbox's menus (R-745).

The database is read through a disposable copy and never written, refused
while rekordbox or its agent runs since such a copy misses whatever was mid
write. The destination is created exclusively and never replaces a file, since
a kept export is what a cutover walks back to. Cheap refusals come before the
expensive copy. There is no gate, as the run only adds one file. No tempo data
is written. Locations under a ``library.location_prefix_map`` rule are written
under its target, as rekordbox's own export would (R-773).
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit import __version__
from cratekit.cli import registry
from cratekit.cli.output import Envelope
from cratekit.core import config, locations, rb_writer, tree_registry
from cratekit.core.cause import CratekitError, refuse
from cratekit.write import collection_export

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context


def _now() -> datetime:
    """The moment the file says it was written, a seam for tests."""
    return datetime.now(timezone.utc)


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    """Declare the one argument, the file to write.

    No default, since it would put an export somewhere nobody chose, and no
    overwrite flag, since that would be the one path where something is lost.
    """
    del entry
    parser.add_argument(
        "file",
        metavar="FILE",
        help="where to write the export; a file that already exists is refused",
    )
    parser.set_defaults(_handler=export_collection)


def _refuse_destination(destination: Path) -> None:
    """Refuse a destination that is taken, or named as a pending intake file.

    A pending intake name is refused because the cutover and the import proof
    read it as un-imported work and would refuse the export.
    """
    name = destination.name
    for suffix in tree_registry.PENDING_XML_SUFFIXES:
        if name.endswith(suffix):
            raise refuse(
                "library-export-unusable",
                f"{name} ends in {suffix}, which is how an intake file waiting "
                f"on an import is named, so the verbs that take an export would "
                f"refuse this one; no export was written",
                steps=("name the export without that ending",),
                origin=("cli.export_collection",),
                detail={"destination": str(destination), "suffix": suffix},
            )
    if os.path.lexists(destination):
        raise _taken(destination)
    _refuse_unwritable_folder(destination)


def _taken(destination: Path) -> CratekitError:
    return refuse(
        "output-exists",
        f"{destination} already exists, and an export somebody kept is "
        f"never replaced; no export was written",
        steps=("name a file that does not exist yet, or move the existing one",),
        origin=("cli.export_collection",),
        detail={"destination": str(destination)},
    )


def _unwritable(destination: Path, blocked: Path, why: str) -> CratekitError:
    return refuse(
        "path-permission-denied",
        f"the export cannot be written to {destination}, because {blocked} "
        f"{why}; no export was written",
        steps=("name a file in a folder that exists and can be written to",),
        origin=("cli.export_collection",),
        detail={"destination": str(destination), "blocked": str(blocked)},
    )


def _refuse_unwritable_folder(destination: Path) -> None:
    """Refuse a destination whose folder could not hold it, before the copy.

    The nearest existing folder is asked, since the write makes the ones
    under it, so the database is never copied for a file that cannot land.
    """
    nearest = destination.parent
    while not os.path.lexists(nearest) and nearest != nearest.parent:
        nearest = nearest.parent
    if not nearest.is_dir():
        raise _unwritable(destination, nearest, "is not a folder")
    if not os.access(nearest, os.W_OK | os.X_OK):
        raise _unwritable(destination, nearest, "cannot be written to")


def _make_folders(folder: Path) -> list[Path]:
    """Make ``folder`` and whatever it lacks above it, answering what was made."""
    missing: list[Path] = []
    cursor = folder
    while not os.path.lexists(cursor) and cursor != cursor.parent:
        missing.append(cursor)
        cursor = cursor.parent
    made: list[Path] = []
    for path in reversed(missing):
        try:
            path.mkdir()
        except FileExistsError:
            continue
        made.append(path)
    return made


def _write_new(destination: Path, content: bytes) -> None:
    """Create ``destination`` holding ``content``, or refuse, and never replace.

    The exclusive create is the guard, the earlier check only a courtesy. A
    failed write leaves nothing, since a truncated export reads as a smaller
    library, so the file is removed and so is every folder made, while empty.
    """
    made: list[Path] = []
    created = False
    try:
        try:
            made = _make_folders(destination.parent)
            handle = open(destination, "xb")  # noqa: SIM115 - closed by the with below
        except FileExistsError as exc:
            raise _taken(destination) from exc
        except OSError as exc:
            raise _unwritable(
                destination, destination.parent, f"refused the write: {exc}"
            ) from exc
        created = True
        with handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        if created:
            try:
                destination.unlink()
            except OSError:
                pass
        for path in reversed(made):
            try:
                path.rmdir()
            except OSError:
                break
        raise


def _read(cfg: config.Config) -> tuple[collection_export.Document, str | None]:
    """Read the copy and render it, answering the document and the schema version."""
    database = rb_writer.live_db_path(cfg)
    with rb_writer.read_only_copy(database, cfg=cfg) as db:
        schema = rb_writer.db_schema_version(db)
        tracks, unrated = collection_export.read_tracks(db)
        nodes = collection_export.read_nodes(db)
    provenance = collection_export.Provenance(
        writer=f"cratekit {__version__}",
        written=_now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        schema=schema,
        installed=rb_writer.read_installed_app_version(cfg=cfg),
        pinned=rb_writer.pinned_app_version(cfg),
    )
    document = collection_export.render(
        tracks,
        nodes,
        provenance,
        root=cfg.library.root,
        prefix_map=[
            locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()
        ],
        unreadable_ratings=unrated,
    )
    return document, schema


#: How many prefixes the unmapped rows warning names; the rest are counted.
_NAMED_PREFIXES = 3


def _warnings(omitted: collection_export.Omitted) -> list[dict[str, str]]:
    """One warning per kind of thing the database held and the file does not."""
    found: list[dict[str, str]] = []

    def names(values: tuple[str, ...]) -> str:
        shown = ", ".join(repr(value) for value in values[:5])
        return shown if len(values) <= 5 else f"{shown} and {len(values) - 5} more"

    if omitted.smart_playlists:
        found.append(
            {
                "code": "export-smart-playlist-omitted",
                "message": (
                    f"{len(omitted.smart_playlists)} smart playlist(s) are not in "
                    f"the export, because the database stores their rule and not "
                    f"their tracks: {names(omitted.smart_playlists)}"
                ),
            }
        )
    if omitted.unreadable_kinds:
        found.append(
            {
                "code": "export-node-kind-unreadable",
                "message": (
                    f"{len(omitted.unreadable_kinds)} playlist row(s) are neither a "
                    f"folder nor a playlist as this build reads them, and are not "
                    f"in the export: {names(omitted.unreadable_kinds)}"
                ),
            }
        )
    if omitted.unreachable_nodes:
        found.append(
            {
                "code": "export-node-unreachable",
                "message": (
                    f"{len(omitted.unreachable_nodes)} playlist row(s) sit under a "
                    f"parent the export does not carry, and are not in it: "
                    f"{names(omitted.unreachable_nodes)}"
                ),
            }
        )
    if omitted.dangling_members:
        found.append(
            {
                "code": "export-member-not-in-collection",
                "message": (
                    f"{omitted.dangling_members} playlist membership(s) name a "
                    f"track the collection no longer holds, and are not in the "
                    f"export"
                ),
            }
        )
    if omitted.unreadable_ratings:
        found.append(
            {
                "code": "export-rating-unreadable",
                "message": (
                    f"{len(omitted.unreadable_ratings)} track(s) hold a rating that "
                    f"is neither a star count nor an export value, and are "
                    f"written as unrated: rows {names(omitted.unreadable_ratings)}"
                ),
            }
        )
    if omitted.normalised_text:
        found.append(
            {
                "code": "export-text-normalised",
                "message": (
                    f"{len(omitted.normalised_text)} row(s) or playlist name(s) "
                    f"hold a tab, a line break or a character no XML document "
                    f"may carry, each written as a space: "
                    f"{names(omitted.normalised_text)}"
                ),
            }
        )
    if omitted.not_file_paths:
        found.append(
            {
                "code": "export-location-not-a-file",
                "message": (
                    f"{len(omitted.not_file_paths)} track(s) record no file on "
                    f"this machine, a streamed track or a row with no path, and "
                    f"their location is copied as the database holds it: rows "
                    f"{names(omitted.not_file_paths)}"
                ),
            }
        )
    if omitted.unmapped_paths:
        shown = omitted.unmapped_prefixes[:_NAMED_PREFIXES]
        listed = ", ".join(f"{count} under {prefix}" for prefix, count in shown)
        more = len(omitted.unmapped_prefixes) - len(shown)
        if more > 0:
            listed += f", and {more} other prefix{'es' if more > 1 else ''}"
        found.append(
            {
                "code": "export-location-unmapped",
                "message": (
                    f"{len(omitted.unmapped_paths)} track(s) record a path under "
                    f"neither the library root nor any library.location_prefix_map "
                    f"rule ({listed}), and their location is written as the "
                    f"database holds it, so a verb reading this file finds each "
                    f"one only if it is at that path on this machine; doctor's "
                    f"library.paths_resolved counts the same rows, which are rows "
                    f"{names(omitted.unmapped_paths)}"
                ),
            }
        )
    return found


def _check(key: str, title: str, detail: str, *, status: str = "ok") -> dict[str, Any]:
    return {"key": key, "title": title, "status": status, "detail": detail, "remedy": None}


def export_collection(ctx: "Context") -> Envelope:
    """Write one collection export from a disposable copy of the database."""
    cfg = config.load()
    destination = Path(ctx.args.file).expanduser().resolve()
    _refuse_destination(destination)

    document, schema = _read(cfg)
    _write_new(destination, document.content)

    omitted = document.omitted
    left_out = (
        len(omitted.smart_playlists)
        + len(omitted.unreadable_kinds)
        + len(omitted.unreachable_nodes)
    )
    checks = [
        _check(
            "export.collection",
            "collection",
            f"{document.tracks} active track(s) written, tombstones omitted",
        ),
        _check(
            "export.playlists",
            "playlists",
            f"{document.folders} folder(s) and {document.playlists} playlist(s) "
            f"written, holding {document.memberships} membership(s)",
            status="ok" if not left_out and not omitted.dangling_members else "info",
        ),
        _check(
            "export.locations",
            "locations",
            f"{document.remapped} location(s) written where a "
            f"library.location_prefix_map rule places them, "
            f"{len(omitted.left_to_rule)} left to a rule that points outside "
            f"what a reader of this file resolves, and "
            f"{len(omitted.unmapped_paths)} under no rule, both written as the "
            f"database holds them",
            status="ok" if not omitted.unmapped_paths else "info",
        ),
        _check(
            "export.tempo",
            "tempo",
            "no tempo data was written: every track carries the gridless "
            "constant and no grid, whatever the database holds",
        ),
        _check(
            "export.provenance",
            "provenance",
            f"the file says cratekit {__version__} wrote it, from a database "
            f"whose schema version is {schema or 'unknown'}",
        ),
    ]
    return ctx.envelope(
        data={
            "checks": checks,
            "summary": {
                "export": str(destination),
                "database": str(rb_writer.live_db_path(cfg)),
                "tracks": document.tracks,
                "folders": document.folders,
                "playlists": document.playlists,
                "memberships": document.memberships,
                "bytes": len(document.content),
                "smart_playlists_omitted": len(omitted.smart_playlists),
                "nodes_omitted": len(omitted.unreadable_kinds)
                + len(omitted.unreachable_nodes),
                "memberships_omitted": omitted.dangling_members,
                "tracks_without_a_file": len(omitted.not_file_paths),
                "locations_remapped": document.remapped,
                "locations_left_to_a_rule": len(omitted.left_to_rule),
                "tracks_under_no_rule": len(omitted.unmapped_paths),
                "rows_normalised": len(omitted.normalised_text),
            },
        },
        warnings=tuple(_warnings(omitted)),
    )


__all__ = ["build", "export_collection"]
