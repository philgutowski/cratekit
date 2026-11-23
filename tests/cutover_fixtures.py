"""Making a temporary library one the cutover precheck passes.

Shared by the verbs' suite and the conformance drive: a verified snapshot, a
named Fresh Export and exactly one root folder. The library root is always
the caller's temporary one, since a cutover writes registry state beside it.

Not a test module: pytest does not collect it.
"""

from __future__ import annotations

import json
from pathlib import Path

from cratekit.cli import cutover
from cratekit.core import config, rb_writer, snapshot

#: A capture directory name in the shape the snapshot store writes.
CAPTURE = "2026-08-01T000000Z-deadbeefcafebabe"


def add_folder(cfg: config.Config, name: str, *, under: str | None = None) -> str:
    """Create one playlist folder in the configured database and answer its identifier."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        parent = None if under is None else handle.get_playlist(ID=under)
        row = handle.create_playlist_folder(name, parent=parent)
        handle.session.commit()
        return str(row.ID)
    finally:
        rb_writer.close_db(handle)


def verified_snapshot(cfg: config.Config) -> Path:
    """One capture whose manifest says its integrity check passed."""
    capture = snapshot.store_root(cfg) / CAPTURE
    capture.mkdir(parents=True, exist_ok=True)
    record = snapshot.Capture(
        stamp=capture.name,
        root=capture,
        database=capture / "master.db",
        integrity_verified=True,
    )
    (capture / snapshot.MANIFEST_NAME).write_text(
        json.dumps(record.to_json()) + "\n", encoding="utf-8"
    )
    return capture


def fresh_export(cfg: config.Config) -> Path:
    """A non-empty export document under the configured library."""
    path = Path(cfg.library.root) / "fresh_export.xml"
    path.write_text("<DJ_PLAYLISTS/>\n", encoding="utf-8")
    return path


def one_root(cfg: config.Config, display: str) -> str:
    """The one root folder named ``display``, found through the verb's own reader or created."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        found = cutover.find_roots(handle, display)
    finally:
        rb_writer.close_db(handle)
    if found:
        return found[0].root_id
    return add_folder(cfg, display)


def ready(cfg: config.Config, display: str) -> tuple[Path, str]:
    """Make ``cfg``'s library pass the precheck. Answers the export and the root."""
    verified_snapshot(cfg)
    return fresh_export(cfg), one_root(cfg, display)


__all__ = ["CAPTURE", "add_folder", "fresh_export", "one_root", "ready", "verified_snapshot"]
