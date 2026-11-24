"""The playlists ``crate sync pair`` finds for itself: every one the author made in rekordbox (U198).

Every plain playlist the author made in rekordbox, outside ARCHIVE, is kept
the same list on the account with no pair named by hand. This says which
playlists those are and their account names. It reads one database handle
and writes nothing.

**WHAT IS FOUND.** Every live plain playlist under live folders only. Left
out, and never listed, as another writer's list or no list:

* a node under one of Cratekit's own trees (``pair_model.generated_tops``);
* the favourites playlist and its folder (``placement.source_name``); two of
  that name leave both out rather than guess;
* another app's top level folder (U185);
* a twins' folder, ``Custom Playlists <year>`` (U149), which pairs itself;
* a playlist a pair already holds.

**WHAT IS LISTED, NEVER WRITTEN.** A playlist under a skipped folder
(``outbound.pair_skip_folders``), a smart playlist, one whose account side a
person deleted, and two that would take one account title, since a name
cannot decide which one the account copies.

**THE ACCOUNT LAYOUT.** Each rekordbox top folder becomes a root folder of the
same name, one private playlist per playlist titled as the mirror titles
them, ``<Folder> <path below> <Playlist>``. The rekordbox root goes in
``Playlists``.

**AND THE WAY BACK (U202).** :func:`home_of` inverts :func:`title_of`, and
refuses, in words a gate shows, any place a name cannot decide or discovery
would never pair.

**ONLY WHAT WAS MADE AFTER THE SYNC (U216).** An account playlist comes back
only when made after its root folder was synced (:func:`before_adoption`,
every unknown read as held), and never as a downloaded copy of one a pair in
the same folder holds (:func:`downloaded_copy`).

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from cratekit.core import rb_writer
from cratekit.write import playlist_pair

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
#: U216. An account playlist its root folder held before a sync adopted the folder.
BEFORE = "before"
#: U216. An account playlist that is a ``DOWNLOADED `` copy of one a pair holds.
COPY = "copy"

#: Every reason a playlist is listed, in the order the gate shows them.
LISTED_KINDS = (SKIPPED, SMART, RELEASED, TWICE, TAKEN, BEFORE, COPY)

#: How a warning counts each kind.
SAID = {
    SKIPPED: "skipped",
    SMART: "smart playlist(s) listed and not paired",
    RELEASED: "released, its account playlist deleted",
    TWICE: "refused, two taking one account title",
    TAKEN: "left, the account already holds its folder or title for something else",
    BEFORE: "left, its account folder held it before a sync adopted the folder",
    COPY: "left, a downloaded copy of a playlist a pair already holds",
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
    """One playlist left out and named: skipped, smart, released or twice titled.

    ``account_id`` is set for an account playlist not brought to rekordbox
    (U202); its ``path`` is then its root folder and title.
    """

    rekordbox_id: str
    name: str
    path: tuple[str, ...]
    kind: str
    why: str
    account_id: str = ""

    @property
    def where(self) -> str:
        return " / ".join(self.path)

    def shown(self) -> dict[str, str]:
        block = {
            "rekordbox_id": self.rekordbox_id,
            "name": self.name,
            "where": self.where,
            "why": self.why,
        }
        if self.account_id:
            block["account_id"] = self.account_id
        return block


@dataclass(frozen=True, slots=True)
class Discovery:
    """Every playlist found to pair, and every one left out and named."""

    found: tuple[Found, ...] = ()
    listed: tuple[Listed, ...] = ()


def title_of(path: tuple[str, ...]) -> tuple[str, str]:
    """The account root folder and title for a rekordbox path, top folder first.

    A path of one name is a playlist at the rekordbox root.
    """
    from cratekit.modules.outbound import mirror
    if len(path) == 1:
        return ROOT_FOLDER, mirror.title(ROOT_FOLDER, path[0])
    return path[0], mirror.title(path[0], " ".join(path[1:]))


@dataclass(frozen=True, slots=True)
class Home:
    """Where an account playlist's rekordbox side is made (U202), the inverse of :func:`title_of`."""

    #: The account root folder the account playlist sits in.
    folder: str
    #: The rekordbox playlist's name.
    name: str
    #: The live rekordbox folder it is made in, empty for the rekordbox root.
    parent_id: str
    #: Where it goes, top folder first, the playlist last.
    path: tuple[str, ...]

    @property
    def parent(self) -> str:
        """The parent as a playlist row records it, ``root`` at the top."""
        return self.parent_id or playlist_pair.ROOT_PARENT

    @property
    def where(self) -> str:
        return " / ".join(self.path)

    def identity(self) -> dict[str, str]:
        return {
            "folder": self.folder,
            "name": self.name,
            "parent_id": self.parent_id,
            "where": self.where,
        }


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

    ``tops`` is ``pair_model.generated_tops``'s answer, ``favorites`` the
    favourites playlist's name, ``skip`` the top folders to list and never
    write, ``paired`` the rekordbox playlists pairs hold, and ``released``
    those whose account side was deleted.
    """
    from cratekit.core import active_taxonomy

    roots, names = tops
    skipped = frozenset(str(one) for one in skip)
    held = frozenset(str(one) for one in paired)
    gone = frozenset(str(one) for one in released)
    every, live, children = _live_children(db)

    foreign = {str(row.ID) for row in active_taxonomy.foreign_roots_in(live)}
    # THE FAVOURITES' HOME, by placement's rule, and its folder. Two of them are
    # no home a name decides, so every playlist there is LISTED, never hidden.
    named = [
        row
        for row in active_taxonomy.outside_foreign(
            [r for r in live if _attribute(r) == PLAIN and str(getattr(r, "Name", "") or "") == favorites],
            every,
        )
    ]
    homes: set[str] = set()
    for row in named:
        homes.add(str(row.ID))
        parent = str(getattr(row, "ParentID", "") or "")
        if parent not in rb_writer.ROOT_PARENT_SENTINELS:
            homes.add(parent)
    unsure = (
        f"{len(named)} playlists are named {favorites!r}, so which folder is Favorites is not "
        f"something a name decides, and none of them is paired; rename the extra ones"
        if len(named) > 1
        else ""
    )

    found: list[Found] = []
    listed: list[Listed] = []

    def walk(row: Any, path: tuple[str, ...], skip_why: str) -> None:
        node_id = str(row.ID)
        name = str(getattr(row, "Name", "") or "")
        if node_id in roots:
            return
        if node_id in homes:
            if not unsure:
                return
            skip_why = skip_why or unsure
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


def left_behind(db: Any, playlist: Any, *, favorites: str, skip: Iterable[str]) -> str:
    """Why a made pair's rekordbox playlist now sits where no pair is kept, or ``""``.

    U198. Moved where discovery would never find it, its pair is let go
    rather than synced there.
    """
    from cratekit.core import active_taxonomy

    if not playlist.ancestors:
        return ""
    top_id, top_name = playlist.top
    if top_name in set(str(one) for one in skip):
        return f"moved under {top_name!r}, a folder the configuration skips"
    live = [row for row in db.get_playlist() if not rb_writer.node_removed(row)]
    if top_id in {str(row.ID) for row in active_taxonomy.foreign_roots_in(live)}:
        return f"moved into {top_name!r}, another app's folder"
    above = {node_id for node_id, _name in playlist.ancestors}
    for row in live:
        if (
            _attribute(row) == PLAIN
            and str(getattr(row, "Name", "") or "") == favorites
            and str(getattr(row, "ParentID", "") or "") in above
        ):
            return "moved into the folder that holds the favourites"
    return ""


def name_of(folder: str, title: str) -> str:
    """An account title less its root folder's prefix, or the title when it has none.

    ``GIG READY Opener`` in ``GIG READY`` is ``Opener``; the folder's name alone is ``""``.
    """
    text = str(title or "").strip()
    head = f"{folder} "
    if text.startswith(head):
        return text[len(head) :].strip()
    return "" if text == folder else text


def home_of(
    db: Any,
    folder: str,
    title: str,
    *,
    tops: tuple[frozenset[str], frozenset[str]],
    favorites: str,
    skip: Iterable[str],
) -> Home | str:
    """Where an account playlist in one root folder goes in rekordbox, or why it goes nowhere.

    U202, the inverse of :func:`title_of`. ``Playlists`` is the rekordbox
    root; any other folder is the one live top folder of its name. Below it,
    a live subfolder whose name and a space begin the rest of the title is
    descended into, longest name first, so ``GIG READY Halloween Opener`` is
    ``Opener`` in ``GIG READY / Halloween`` when that exists. Every place a
    name cannot decide or discovery would never pair is refused.
    """
    from cratekit.core import active_taxonomy

    name = name_of(folder, title)
    if not name:
        return (
            f"its title {title!r} is only its folder's name, so a rekordbox playlist "
            f"made for it would have no name; rename it on the account"
        )
    _every, live, children = _live_children(db)

    def named(row: Any) -> str:
        return str(getattr(row, "Name", "") or "")

    parent_id = ""
    path: tuple[str, ...] = ()
    if folder != ROOT_FOLDER:
        roots, declared = tops
        if folder in set(str(one) for one in skip):
            return (
                f"its folder {folder!r} is one outbound.pair_skip_folders names, so it "
                f"stays on the account only"
            )
        if folder in declared or TWIN_FOLDER.fullmatch(folder):
            return (
                f"rekordbox's {folder!r} is a folder Cratekit or the twins keep, so no "
                f"playlist of a pair is made in it"
            )
        top = [
            row
            for row in children.get("", ())
            if _attribute(row) == FOLDER and named(row) == folder
        ]
        if not top:
            return (
                f"rekordbox holds no live top level folder named {folder!r}, so it is not "
                f"made there; make the folder in rekordbox and the next sync fills it"
            )
        if len(top) > 1:
            return (
                f"rekordbox holds {len(top)} top level folders named {folder!r}, so which "
                f"one it goes in is not something a name decides"
            )
        top_id = str(top[0].ID)
        foreign = {str(row.ID) for row in active_taxonomy.foreign_roots_in(live)}
        if top_id in roots or top_id in foreign:
            return (
                f"rekordbox's {folder!r} is one of Cratekit's trees or another app's "
                f"folder, so no playlist of a pair is made in it"
            )
        parent_id, path = top_id, (folder,)
        while True:
            fits = [
                row
                for row in children.get(parent_id, ())
                if _attribute(row) == FOLDER
                and name.startswith(f"{named(row)} ")
                and name[len(named(row)) + 1 :].strip()
            ]
            if not fits:
                break
            longest = max(len(named(row)) for row in fits)
            best = [row for row in fits if len(named(row)) == longest]
            if len(best) > 1:
                return (
                    f"{' / '.join(path)!r} holds {len(best)} folders named "
                    f"{named(best[0])!r}, so which one it goes in is not something a "
                    f"name decides"
                )
            name = name[longest + 1 :].strip()
            parent_id, path = str(best[0].ID), (*path, named(best[0]))
        above = {parent_id, *(_chain(live, parent_id))}
        if any(
            _attribute(row) == PLAIN
            and named(row) == favorites
            and str(getattr(row, "ParentID", "") or "") in above
            for row in live
        ):
            return (
                f"rekordbox's {' / '.join(path)!r} holds the favourites, so no playlist "
                f"of a pair is made in it"
            )
    here = [row for row in children.get(parent_id, ()) if named(row) == name]
    if here:
        where = " / ".join(path) or "the rekordbox root"
        return (
            f"{where} already holds a node named {name!r} that no pair made for this "
            f"playlist, so it is left as it is and nothing is made beside it; pair the "
            f"two by hand with crate sync pair, or rename one"
        )
    return Home(folder=folder, name=name, parent_id=parent_id, path=(*path, name))


# ---------------------------------------------------------------------------
# U216: what an account folder held before a sync, and the DOWNLOADED copies
# ---------------------------------------------------------------------------

#: The step for syncing a left out playlist anyway; the rekordbox side is theirs (U216).
BY_HAND = (
    "to sync it anyway, make or choose its rekordbox playlist and pair the two by hand "
    "with crate sync pair ACCOUNT_ID --rekordbox PLAYLIST_ID"
)


def adoption_moment(marks: Iterable[str]) -> datetime | None:
    """When a sync adopted a root folder, as the earliest readable mark of a pair made in it.

    U216. The adoption is reserved just before the first playlist in it is
    marked, so the earliest mark bounds it. A mark without a zone is passed over.
    """
    found: list[datetime] = []
    for mark in marks:
        try:
            moment = datetime.fromisoformat(str(mark or ""))
        except ValueError:
            continue
        if moment.tzinfo is not None:
            found.append(moment)
    return min(found) if found else None


def before_adoption(
    account_id: str,
    *,
    held: frozenset[str] | None,
    created: bool,
    folder: str,
    made: datetime | None,
    adopted: datetime | None,
) -> str:
    """Why an account playlist in a recorded root folder is one the folder held before the sync, or ``""``.

    U216. ``held``, when recorded, answers alone; a ``created`` folder held
    nothing; otherwise ``made`` is read against ``adopted``. Every unknown
    answers held, since one read as new makes a duplicate in rekordbox and
    one read as held is only named.
    """
    if held is not None:
        if account_id in held:
            return (
                f"the account's {folder!r} folder already held it when a sync adopted the "
                f"folder, so it is the account's own and not made in rekordbox; {BY_HAND}"
            )
        return ""
    if created:
        return ""
    unrecorded = (
        f"the account's {folder!r} folder was adopted before a sync recorded what it held"
    )
    if adopted is None:
        return (
            f"{unrecorded}, and no playlist made in it dates the adoption, so this may be "
            f"one it held before and is not made in rekordbox; {BY_HAND}"
        )
    if made is None or made.tzinfo is None:
        return (
            f"{unrecorded}, and the account gave no creation time for this playlist, so it "
            f"may be one the folder held before and is not made in rekordbox; {BY_HAND}"
        )
    if made <= adopted:
        return (
            f"the account says it was made at {made.isoformat()}, not after a sync adopted "
            f"the {folder!r} folder at {adopted.isoformat()}, so the folder held it before "
            f"and it is not made in rekordbox; {BY_HAND}"
        )
    return ""


def downloaded_copy(
    folder: str, title: str, paired: Iterable[str], *, taken: bool = False
) -> str:
    """The paired account title ``title`` is a downloaded copy of, or ``""``.

    U216. Both are read less the folder's prefix (:func:`name_of`), ignoring
    case, so ``DOWNLOADED Techno`` copies ``Genre Trivia! Techno`` in
    ``Genre Trivia!``.

    ``taken`` IS WHETHER CRATEKIT'S RECORD HOLDS THE PLAYLIST AS TAKEN (U242):
    once ``crate sync strip`` took the prefix off, only the record says it is
    a copy. One with neither prefix nor record is never a copy.
    """
    from cratekit.sync.playlists import SWEPT_PREFIX, untaken_name

    text = str(title or "")
    prefixed = text[: len(SWEPT_PREFIX)].casefold() == SWEPT_PREFIX.casefold()
    if not prefixed and not taken:
        return ""
    rest = text[len(SWEPT_PREFIX) :] if prefixed else text
    wanted = name_of(folder, untaken_name(rest)).casefold()
    if not wanted:
        return ""
    for one in sorted(str(each) for each in paired):
        if name_of(folder, one).casefold() == wanted:
            return one
    return ""


def copy_candidates(
    fresh: Iterable[tuple[str, str]], account_id: str, title: str, taken: Iterable[str]
) -> list[str]:
    """The titles beside ``account_id`` it may be a downloaded copy of, as :func:`downloaded_copy` reads them.

    TWO TAKEN PLAYLISTS OF ONE NAME ARE NOT EACH OTHER'S COPY (U242). A title
    still carrying the prefix reads every one beside it.
    """
    from cratekit.sync.playlists import is_swept_name

    held = frozenset(taken)
    plain_taken = account_id in held and not is_swept_name(title)
    return [
        other
        for other_id, other in fresh
        if other_id != account_id and not (plain_taken and other_id in held)
    ]


def _chain(live: Iterable[Any], node_id: str) -> tuple[str, ...]:
    """Every folder above ``node_id``, nearest first, through live rows."""
    parent_of = {
        str(row.ID): str(getattr(row, "ParentID", "") or "") for row in live
    }
    found: list[str] = []
    at = parent_of.get(node_id, "")
    while at and at not in rb_writer.ROOT_PARENT_SENTINELS and at not in found:
        found.append(at)
        at = parent_of.get(at, "")
    return tuple(found)


def by_kind(listed: Iterable[Listed]) -> Mapping[str, tuple[Listed, ...]]:
    """The listed playlists grouped by why, in :data:`LISTED_KINDS` order."""
    grouped: dict[str, list[Listed]] = {kind: [] for kind in LISTED_KINDS}
    for one in listed:
        grouped.setdefault(one.kind, []).append(one)
    return {kind: tuple(rows) for kind, rows in grouped.items() if rows}


__all__ = [
    "BEFORE", "BY_HAND", "COPY", "FOLDER", "LISTED_KINDS", "PLAIN", "RELEASED", "ROOT_FOLDER",
    "SKIPPED", "SAID", "SMART", "TAKEN", "TWICE", "TWIN_FOLDER", "Discovery", "Found", "Home",
    "Listed", "adoption_moment", "before_adoption", "by_kind", "copy_candidates", "discover",
    "downloaded_copy", "home_of", "left_behind", "name_of", "title_of"
]


def _live_children(db) -> tuple[list[Any], list[Any], dict[str, list[Any]]]:
    """Every node, the live ones, and each parent's live children, the root as ``""``."""
    every = list(db.get_playlist())
    live = [row for row in every if not rb_writer.node_removed(row)]
    children: dict[str, list[Any]] = {}
    for row in live:
        parent = str(getattr(row, "ParentID", "") or "")
        if parent in rb_writer.ROOT_PARENT_SENTINELS:
            parent = ""
        children.setdefault(parent, []).append(row)
    return every, live, children
