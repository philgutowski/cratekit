"""The rows whose genre a person moved, and the bucket each was moved out of (U339).

``tag set`` gives a row a genre over the one it carried. Adoption then files
the row in the new genre's bucket, and nothing takes it out of the old one:
``adopt move`` never asks a bucket holding a track once, which is right for a
track a person put in a second genre folder by hand (U340). So the verb that
changed the genre says where from, and :mod:`cratekit.adopt.move` asks THAT
bucket for THAT row and no other.

ONE ENTRY PER ROW: the buckets the tree filed it in under a genre ``tag set``
replaced, each run's added to the last's, less the bucket its new genre names.
A bucket is taken off the entry when an ``adopt move`` job reads the row back
out of it, and the entry is spent when none is left; a bucket means nothing
once the row's genre names it again, which the move plan asks before it
removes anything.

COUPLED with the database (:mod:`cratekit.core.state_files`): written inside the
session that changes the genre, after its capture, so a restore of that session
takes the entries back with the rows.

Layer: modules. It reads and writes one state file and opens no database.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.core import config

#: The state entry the moves are kept in, under the library's state.
STATE_KEY = "genre_moves"


def path_of(cfg: config.Config) -> Path:
    return config.state_path(STATE_KEY, cfg)


def read(cfg: config.Config) -> Mapping[str, frozenset[str]]:
    """Every row a genre was moved on, and the buckets it was moved out of.

    AN UNREADABLE FILE READS AS NO ENTRY, which costs a track left in its old
    folder as before this unit, never a membership removed that nobody asked
    for. An entry in another shape is skipped for the same reason.
    """
    try:
        found = json.loads(path_of(cfg).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return MappingProxyType({})
    if not isinstance(found, dict):
        return MappingProxyType({})
    moved: dict[str, frozenset[str]] = {}
    for content_id, buckets in found.items():
        if isinstance(buckets, list) and all(isinstance(one, str) and one for one in buckets):
            moved[str(content_id)] = frozenset(buckets)
    return MappingProxyType(moved)


def _save(cfg: config.Config, moved: Mapping[str, Iterable[str]]) -> None:
    payload = {key: sorted(set(value)) for key, value in sorted(moved.items()) if value}
    config.atomic_write_bytes(
        json.dumps(payload, indent=1, sort_keys=True).encode("utf-8"), path_of(cfg)
    )


def record(cfg: config.Config, moved: Mapping[str, Iterable[str]], *, into: str) -> None:
    """Record the buckets each row was moved out of, beside any its entry still
    holds, less ``into``, the bucket its genre now names: a row moved twice
    before ``adopt move`` ran still sits in the first bucket, and a row moved
    back has nothing to leave there."""
    if not moved:
        return
    kept: dict[str, Any] = {key: set(value) for key, value in read(cfg).items()}
    for content_id, buckets in moved.items():
        kept[str(content_id)] = (kept.get(str(content_id), set()) | set(buckets)) - {into}
    _save(cfg, kept)


def discharge(cfg: config.Config, left: Mapping[str, Iterable[str]]) -> None:
    """Take each bucket a row has now left off its entry, and the entry once empty."""
    if not left:
        return
    kept = {key: set(value) for key, value in read(cfg).items()}
    changed = False
    for content_id, buckets in left.items():
        if content_id not in kept:
            continue
        before = len(kept[content_id])
        kept[content_id] -= set(buckets)
        changed = changed or len(kept[content_id]) != before
    if changed:
        _save(cfg, kept)


__all__ = ["STATE_KEY", "discharge", "path_of", "read", "record"]
