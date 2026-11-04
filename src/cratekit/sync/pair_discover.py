"""The playlists ``crate sync pair`` finds for itself: every one the author made in rekordbox (U198).

Decided by Phillip on 2026-11-04: every plain playlist he made himself in
rekordbox, outside ARCHIVE, is on the account and stays the same list on both
sides, with no pair named by hand. This module answers which playlists those
are, and what each is called on the account. It reads one database handle and
writes nothing.

**WHAT IS FOUND.** Every live plain playlist, walked down from the top of the
playlist tree through live folders only, so a playlist under a folder that was
removed is not found. Left out, and never listed, because each is another
writer's list or no list at all:

* a node under one of Cratekit's own trees, which is a node the tree registry
  records as a root or a top level node carrying a name the taxonomy declares
  for one of its trees, the rule the pair scope already refuses by
  (``pair_cli.generated_tops``);
* the Favorites folder and the favourites playlist itself, found by the
  playlist the taxonomy names as the favourites (``placement.source_name``).
  Every live plain playlist of that name is taken as a home, so a library
  holding two of them leaves both homes out rather than guessing;
* another app's folder at the top level (U185);
* a custom playlist twins' folder, ``Custom Playlists <year>`` (U149), whose
  playlists the product made and pairs itself;
* a rekordbox playlist a pair already holds, which the pair syncs.

**WHAT IS LISTED, NEVER WRITTEN.** A playlist under a folder the configuration
names to skip (``outbound.pair_skip_folders``, ARCHIVE by default), a smart
playlist, which holds no list a pair could keep, a playlist whose account side
a person deleted, which is released and not made again, and two playlists
that would take one account title, which refuse that title, since which one
the account playlist copies is not something a name decides.

**THE ACCOUNT LAYOUT.** Each rekordbox top folder becomes one root folder of
the same name on the account, holding one private playlist per rekordbox
playlist under it, titled as the mirror titles its playlists, ``<Folder>
<Playlist>``. A playlist in a subfolder takes its path below the top folder,
``GIG READY Halloween Opener``. A playlist at the rekordbox root goes in the
root folder ``Playlists``.

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from cratekit.core import rb_writer
from cratekit.modules.outbound import mirror

#: The account root folder a playlist at the rekordbox root goes in.
ROOT_FOLDER = "Playlists"

#: A custom playlist twins' folder (U149), ``Custom Playlists 2026``.
TWIN_FOLDER = re.compile(r"Custom Playlists [0-9]{4}")

#: Why a playlist is listed and not found.
SKIPPED = "skipped"
SMART = "smart"
TWICE = "twice"
RELEASED = "released"
#: Found, and left out by the account side: its folder or its title is taken there.
TAKEN = "taken"

#: Every reason a playlist is listed, in the order the gate shows them.
LISTED_KINDS = (SKIPPED, SMART, RELEASED, TWICE, TAKEN)

#: How a warning counts each kind.
SAID = {
    SKIPPED: "skipped",
    SMART: "smart playlist(s) listed and not paired",
    RELEASED: "released, its account playlist deleted",
    TWICE: "refused, two taking one account title",
    TAKEN: "left, the account already holds its folder or title for something else",
}

#: The attributes a playlist row carries: a plain playlist and a folder.
PLAIN = 0
FOLDER = 1


@dataclass(frozen=True, slots=True)
class Found:
    """One plain rekordbox playlist the author made, and what it is called on the account."""

    rekordbox_id: str
    name: str
    #: The account root folder it goes in.
    folder: str
    #: Its account title, ``<Folder> <path below> <Playlist>``.
    title: str
    #: Where it sits in rekordbox, top folder first, the playlist last.
    path: tuple[str, ...]

    @property
    def where(self) -> str:
        return " / ".join(self.path)


@dataclass(frozen=True, slots=True)
class Listed:
    """One playlist left out and named: skipped, smart, released or twice titled."""

    rekordbox_id: str
    name: str
    path: tuple[str, ...]
    kind: str
    why: str

    @property
    def where(self) -> str:
        return " / ".join(self.path)

    def shown(self) -> dict[str, str]:
        return {
            "rekordbox_id": self.rekordbox_id,
            "name": self.name,
            "where": self.where,
            "why": self.why,
        }


@dataclass(frozen=True, slots=True)
class Discovery:
    """Every playlist found to pair, and every one left out and named."""

    found: tuple[Found, ...] = ()
    listed: tuple[Listed, ...] = ()


def title_of(path: tuple[str, ...]) -> tuple[str, str]:
    """The account root folder and title for a rekordbox path, top folder first.

    A path of one name is a playlist at the rekordbox root.
    """
    if len(path) == 1:
        return ROOT_FOLDER, mirror.title(ROOT_FOLDER, path[0])
    return path[0], mirror.title(path[0], " ".join(path[1:]))


def _attribute(row: Any) -> int:
    return int(getattr(row, "Attribute", 0) or 0)


def _order(row: Any) -> tuple[int, str, str]:
    return (int(getattr(row, "Seq", 0) or 0), str(getattr(row, "Name", "") or ""), str(row.ID))


def discover(
    db: Any,
    *,
    tops: tuple[frozenset[str], frozenset[str]],
    favorites: str,
    skip: Iterable[str],
    paired: Iterable[str],
    released: Iterable[str],
) -> Discovery:
    """Walk the live playlist tree once and say what a sync of every pair should make.

    ``tops`` is ``pair_cli.generated_tops``'s answer, ``favorites`` the name of
    the playlist every favourite is in, ``skip`` the top folder names to list
    and never write, ``paired`` every rekordbox playlist a pair holds, and
    ``released`` every one whose account side was deleted.
    """
    from cratekit.core import foreign_tree

    roots, names = tops
    skipped = frozenset(str(one) for one in skip)
    held = frozenset(str(one) for one in paired)
    gone = frozenset(str(one) for one in released)
    every = list(db.get_playlist())
    live = [row for row in every if not rb_writer.node_removed(row)]
    children: dict[str, list[Any]] = {}
    for row in live:
        parent = str(getattr(row, "ParentID", "") or "")
        if parent in rb_writer.ROOT_PARENT_SENTINELS:
            parent = ""
        children.setdefault(parent, []).append(row)

    # EVERY HOME THE FAVOURITES COULD HAVE, so two of them leave both out.
    homes: set[str] = set()
    for row in live:
        if _attribute(row) == PLAIN and str(getattr(row, "Name", "") or "") == favorites:
            homes.add(str(row.ID))
            parent = str(getattr(row, "ParentID", "") or "")
            if parent not in rb_writer.ROOT_PARENT_SENTINELS:
                homes.add(parent)
    foreign = {str(row.ID) for row in foreign_tree.roots_in(live)}

    found: list[Found] = []
    listed: list[Listed] = []

    def walk(row: Any, path: tuple[str, ...], skip_why: str) -> None:
        node_id = str(row.ID)
        name = str(getattr(row, "Name", "") or "")
        if node_id in roots or node_id in homes:
            return
        here = (*path, name)
        attribute = _attribute(row)
        if attribute == FOLDER:
            for child in sorted(children.get(node_id, ()), key=_order):
                walk(child, here, skip_why)
            return
        if node_id in held:
            return
        if skip_why:
            listed.append(Listed(node_id, name, here, SKIPPED, skip_why))
            return
        if attribute != PLAIN:
            listed.append(
                Listed(
                    node_id,
                    name,
                    here,
                    SMART,
                    "a smart playlist holds no list a pair could keep, so it is not paired",
                )
            )
            return
        if node_id in gone:
            listed.append(
                Listed(
                    node_id,
                    name,
                    here,
                    RELEASED,
                    "its account playlist was deleted, so it was unpaired and is not made "
                    "again; pair it by hand with crate sync pair to sync it once more",
                )
            )
            return
        folder, title = title_of(here)
        found.append(Found(node_id, name, folder, title, here))

    for top in sorted(children.get("", ()), key=_order):
        top_id = str(top.ID)
        top_name = str(getattr(top, "Name", "") or "")
        if top_id in roots or top_name in names or top_id in foreign:
            continue
        if _attribute(top) == FOLDER and TWIN_FOLDER.fullmatch(top_name):
            continue
        why = ""
        if _attribute(top) == FOLDER and top_name in skipped:
            why = (
                f"it sits under {top_name!r}, a folder outbound.pair_skip_folders names, "
                f"so it stays in rekordbox only"
            )
        walk(top, (), why)

    # TWO PLAYLISTS TAKING ONE TITLE REFUSE THAT TITLE, and only that one.
    counted: dict[str, int] = {}
    for one in found:
        counted[one.title] = counted.get(one.title, 0) + 1
    kept: list[Found] = []
    for one in found:
        if counted[one.title] > 1:
            listed.append(
                Listed(
                    one.rekordbox_id,
                    one.name,
                    one.path,
                    TWICE,
                    f"{counted[one.title]} rekordbox playlists would take the account title "
                    f"{one.title!r}, so which one it copies is not something a name decides; "
                    f"rename one of them in rekordbox",
                )
            )
        else:
            kept.append(one)
    return Discovery(found=tuple(kept), listed=tuple(listed))


def by_kind(listed: Iterable[Listed]) -> Mapping[str, tuple[Listed, ...]]:
    """The listed playlists grouped by why, in :data:`LISTED_KINDS` order."""
    grouped: dict[str, list[Listed]] = {kind: [] for kind in LISTED_KINDS}
    for one in listed:
        grouped.setdefault(one.kind, []).append(one)
    return {kind: tuple(rows) for kind, rows in grouped.items() if rows}


__all__ = [
    "FOLDER",
    "LISTED_KINDS",
    "PLAIN",
    "RELEASED",
    "ROOT_FOLDER",
    "SKIPPED",
    "SAID",
    "SMART",
    "TAKEN",
    "TWICE",
    "TWIN_FOLDER",
    "Discovery",
    "Found",
    "Listed",
    "by_kind",
    "discover",
    "title_of",
]
