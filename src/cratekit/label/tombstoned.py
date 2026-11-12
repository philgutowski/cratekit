"""Which tracks of a label's catalogue the library removed on purpose (U243).

A track confirmed in ``crate delete review`` is tombstoned, which is the
record that the library stopped holding that version and should never acquire
it again. The label sweep already asks the tombstone store about a RELEASE;
this asks it about each TRACK a label's catalogue read carries, so ``label
playlists`` never adds a removed track to a year playlist and ``label prune``
takes one off a year playlist this product made.

ONE RECORD OF REMOVALS, NOT TWO. The question is asked of the same store the
deletion pass writes and the acquisition passes read, under the same kinds and
the same identity, through :mod:`cratekit.core.tombstone` and
:mod:`cratekit.core.review` only. The deletion package is a toggleable module,
so a label verb never imports it.

THE TRACK'S OWN WORDS ARE ITS IDENTITY, read as the downloader tags a file: the
artists the provider bills, joined by a comma and a space, and the title with
its version, which is what a removed row records in rekordbox for a track this
product acquired. Asked under the version kind first and the companion a
credited deletion writes second, as the acquisition consult asks.

THE STORE IS READ ONCE AND LAZILY, on the first track that has words to ask
about, so a run with nothing to judge never reads it, and an unreadable store
refuses (``DecisionStore`` refuses a document it cannot recognise rather than
reading it as empty, which would put every removed track back).

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
