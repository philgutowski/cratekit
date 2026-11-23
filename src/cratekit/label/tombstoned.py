"""Which tracks of a label's catalogue the library removed on purpose (U243).

A track confirmed in ``crate delete review`` is tombstoned. The label sweep
asks the tombstone store about a release; this asks it about each track a
label's catalogue read carries, so ``label playlists`` never adds a removed
track and ``label prune`` takes one off a year playlist this product made.

One record of removals: the same store, kinds and identity the deletion pass
writes, through :mod:`cratekit.core.tombstone` and :mod:`cratekit.core.review`
only, since the deletion package is a toggleable module.

A track's identity is its own words as the downloader tags a file: the billed
artists joined by a comma and a space, and the title with its version. Asked
under the version kind first and the credited deletion's companion second.

The store is read once and lazily, on the first track with words to ask about,
and an unreadable store refuses rather than reading as empty.

Layer: modules.
"""

from __future__ import annotations

from typing import Any

from cratekit.core import config, review, tombstone
from cratekit.core.review import DecisionStore


def track_artist(track: Any) -> str:
    """The artists a provider track bills, joined as the downloader tags them."""
    names: list[str] = []
    for entry in getattr(track, "artists", None) or ():
        name = entry if isinstance(entry, str) else getattr(entry, "name", "")
        if isinstance(name, str) and name.strip():
            names.append(name.strip())
    if names:
        return ", ".join(names)
    lead = getattr(track, "artist", None)
    if isinstance(lead, str):
        return lead.strip()
    name = getattr(lead, "name", None)
    return name.strip() if isinstance(name, str) else ""


def track_title(track: Any) -> str:
    """The title with its version, as the provider spells the whole of it."""
    for attribute in ("full_name", "name", "title"):
        value = getattr(track, attribute, None)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


class Tombstoned:
    """Whether an artist and title is a version the library removed, one store read."""

    def __init__(self, cfg: config.Config) -> None:
        self._cfg = cfg
        self._snapshot: frozenset[str] | None = None

    def _standing(self) -> frozenset[str]:
        if self._snapshot is None:
            store = DecisionStore(tombstone.STORE_KEY, self._cfg)
            # SUPPRESSING RECORDS ONLY: a revoked tombstone stays in the document
            # and must not take a track off, which is what lifting it asked for.
            self._snapshot = frozenset(
                record.suppression_id for record in store.suppressions()
            )
        return self._snapshot

    def __call__(self, artist: str, title: str) -> bool:
        if not tombstone.fold(artist) and not tombstone.fold(title):
            # NOTHING TO ASK UNDER. ``version_identity`` refuses an identity
            # with neither field, since it would collide every unnamed track.
            return False
        standing = self._standing()
        if not standing:
            return False
        identity = tombstone.version_identity(artist=artist, title=title)
        for kind in (tombstone.KIND_VERSION, tombstone.KIND_VERSION_UNCREDITED):
            if review.suppression_id_for(tombstone.STORE_KEY, kind, identity) in standing:
                return True
        return False


__all__ = ["Tombstoned", "track_artist", "track_title"]
