"""An edit made on the account to a mirrored playlist, taken into the library (U201, U204).

``crate organize``'s rekordbox area step ``mirror-edits``. The account mirror
(U147) reads each genre playlist three ways, the snapshot, the account and
rekordbox, and :mod:`cratekit.modules.outbound.mirror_edits` decides which
track a person changed on the account. This step carries each one the library
takes, and the mirror holds the account as it is meanwhile, so the edit is
never put back:

* a MOVE, a track put on the account in another band playlist, takes the
  genre and energy routing files into that playlist;
* a FOLDER, a track put in another genre's with vox or genre sub playlist,
  takes that genre with its energy kept;
* an UNFILE, a track taken off its band and added to no other genre playlist,
  has its genre and energy cleared and leaves the tree, so ``route unplaced``
  lists it for placing again, Phillip's answer of 2026-11-04. It stays in the
  collection.

THE TAGS ARE CHOSEN BY ROUTING ITSELF, never by restating it. Routing reads a
track's file tags (``rebuild.read_truth``), so the new tags are the nearest pair
``routing.resolve_bucket`` and ``routing.energy_sub`` file into the place the
account names: the current genre when it already files into that folder, else
the folder's own name, else a style source that reaches it; the current energy
when it lands in that band, else the level nearest it that does, and no
reading at all for the sink. A place no pair reaches is refused for that track,
named, and nothing of it is written.

WHAT IS WRITTEN, ONE SESSION FOR EVERY TRACK. The file's ``genre`` and
``energylevel`` tags first, each read back, then in the database the row's
genre where rekordbox already holds a genre of the new name (an unknown one is
named and skipped, never minted), and the track's memberships inside BY GENRE +
ENERGY: it leaves every playlist routing filed it into that the new tags do not,
and joins every one they do that exists (``rebuild.derive_from_taxonomy``,
the rule ``route resort`` writes by). A playlist routing never files into,
the genre Favorites among them, is another engine's and is left, except by an
unfile, which leaves the whole tree so that ``route unplaced`` lists it. The session takes the backup
acknowledgment, the session gates, a verified capture, the guarded commit, and
a read back of every membership. A file whose tag did not take is named and
its row is not touched. Nothing is removed from the collection, and no beat
grid is written: the two tags are the only fields, and the writable field set
refuses a tempo.

THE FAVORITES FOLDER AND INBOX, SINCE U204, in the same session:

* a FAVOURITE, a track put on the account in All Favorites or a month, is
  placed as a heart is placed, through ``favorites.placement``: All Favorites
  and its month, the month made in its slot when absent, Pink on a row with no
  colour and a colour a person chose held. A month is the playlist it was put
  in, else the month of its added time on the account, ``Undated`` when that is
  unknown, and none when it sits in a filing playlist already. A quarter is the
  split's to retire and is never filed into;
* an UNFAVOURITE, a track taken off All Favorites on the account, leaves All
  Favorites and every filing playlist beside it, here and not under
  ``favorites/``, which takes no membership away. Its colour stays, and it stays
  hearted on the account, so the next sync's landing places it again unless it
  is un-hearted there too, Phillip's two step rule of 2026-10-14; the gate says
  so;
* a JOIN or a LEAVE, a track put on or taken off an INBOX batch on the account,
  is added to or taken out of that batch, found live directly under INBOX on
  the handle written, so a batch the rotation moved into Old since is a plan
  that moved and Old is never touched.

THE SNAPSHOT TAKES EACH EDIT THE LIBRARY TOOK (:func:`settle`), once the commit
landed, so the next refresh reads the track as agreed, and a move made in
rekordbox after it is rekordbox's to carry to the account. The month a
FAVOURITE put in All Favorites alone was placed in is recorded beside it as
the library's own placement (U236), since the account does not hold it there
until the mirror's next refresh, and read then as no change made in rekordbox.

THE PLAN A GATE SHOWS IS THE PLAN ITS APPLY WRITES. The apply plans again on its
write handle from the same decisions and refuses ``decision-stale`` when the
library moved between the two.

THE ROW'S GENRE IS NOT CLEARED BY AN UNFILE: the metadata layer has no
operation that empties a row's genre, so rekordbox's Genre column keeps its
word until a reread, and the gate says so. Routing reads the file.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import CratekitError, refuse
from cratekit.modules.outbound import mirror_edits as edits
from cratekit.organize.steps import LISTED, NOTHING, PLANNED, Step, refused

#: The step kind ``--only`` names this by.
KIND = "mirror-edits"

TITLE = "take each edit made on the account to a mirrored playlist into the library"

#: The session workflow the write is recorded under.
WORKFLOW = "organize.mirror-edits"

_ORIGIN = ("organize", "mirror_edits")


def _primary(declared: Any, bucket_id: str) -> frozenset[str]:
    """The band playlists of one bucket, every display ``routing.energy_sub`` answers."""
    from cratekit.core import routing

    bucket = declared.bucket(bucket_id)
    sources = [""]
    if bucket.sub_by_source is not None:
        sources += sorted(bucket.sub_by_source.map)
    levels: list[int | None] = [None, *range(1, int(declared.energy.scale_max) + 1)]
    found: set[str] = set()
    for source in sources:
        for level in levels:
            sub = routing.energy_sub(declared, bucket_id, level, source_genre=source)
            if sub is not None:
                found.add(sub.display)
    return frozenset(found)


def _additive(declared: Any, bucket_id: str) -> frozenset[str]:
    """The additive playlists routing files a track into beside its band.

    A genre sub (U155) and the with vox class, the two ``derive_from_taxonomy``
    writes. A class derived from another playlist, the genre Favorites, is the
    favourites engine's, and any other class is no place routing files a track
    into, so neither is read as an edit here.
    """
    from cratekit.write import trees

    found = {genre.display for genre in declared.bucket(bucket_id).genre_subs}
    found |= {
        entry.display
        for entry in declared.sub_classes
        if entry.id == trees.VOX_SUB_CLASS and entry.additive
    }
    return frozenset(found)


def places(declared: Any, folders: Iterable[Any]) -> dict[str, edits.Place]:
    """Each edited playlist's place by its account title, read by its folder's rule.

    A genre folder's band or additive playlists (U201). A folder whose name is
    no bucket's display, a playlist whose title does not start with its
    folder's name, and a playlist routing never files a track into (the genre
    Favorites among them) have no place: their tracks are read as before U201,
    every difference rekordbox's. The Favorites folder's All Favorites and
    filing playlists, and every INBOX batch (U204).
    """
    found: dict[str, edits.Place] = {}
    for folder in folders:
        if folder.edits == edits.FAVORITES:
            found.update(_favourite_places(declared, folder))
            continue
        if folder.edits == edits.INBOX:
            found.update(_inbox_places(folder))
            continue
        if folder.edits != edits.GENRE:
            continue
        bucket_id = declared.bucket_for_display(folder.name)
        if bucket_id is None:
            continue
        primary = _primary(declared, bucket_id)
        additive = _additive(declared, bucket_id)
        prefix = f"{folder.name} "
        for source in folder.playlists:
            if not source.name.startswith(prefix):
                continue
            playlist = source.name[len(prefix) :]
            if playlist not in primary and playlist not in additive:
                continue
            found[source.name] = edits.Place(
                title=source.name,
                folder=folder.name,
                playlist=playlist,
                primary=playlist in primary,
            )
    return found


def _favourite_places(declared: Any, folder: Any) -> dict[str, edits.Place]:
    """All Favorites, the primary place, and each filing playlist beside it (U204).

    A playlist of any other name in the folder is somebody's, and is mirrored
    one way as before.
    """
    from cratekit.favorites import placeholders, placement

    source = placement.source_name(declared)
    prefix = f"{folder.name} "
    found: dict[str, edits.Place] = {}
    for one in folder.playlists:
        if one.name == source:
            found[one.name] = edits.Place(one.name, folder.name, source, True, edits.FAVORITES)
            continue
        if not one.name.startswith(prefix):
            continue
        name = one.name[len(prefix) :]
        if placeholders.is_filing(name):
            found[one.name] = edits.Place(one.name, folder.name, name, False, edits.FAVORITES)
    return found


def _inbox_places(folder: Any) -> dict[str, edits.Place]:
    """Every INBOX batch the mirror copies, each a place of its own (U204)."""
    prefix = f"{folder.name} "
    return {
        one.name: edits.Place(one.name, folder.name, one.name[len(prefix) :], True, edits.INBOX)
        for one in folder.playlists
        if one.name.startswith(prefix)
    }


def _energies(current: int | None, top: int) -> list[int | None]:
    """Every energy reading, the current one first, then the nearest, then none."""
    middle = current if current is not None else (top + 1) // 2
    levels = sorted(range(1, top + 1), key=lambda level: (abs(level - middle), level))
    ordered: list[int | None] = [current] if current is not None else [None]
    ordered += [level for level in levels if level != current]
    if current is not None:
        ordered.append(None)
    return ordered


def target_tags(
    declared: Any, folder: str, playlist: str | None, genre: str | None, energy: int | None
) -> tuple[str, int | None] | None:
    """The nearest ``(genre, energy)`` routing files into this place, or ``None``.

    ``playlist`` is the band playlist a MOVE names, or ``None`` for a FOLDER,
    which keeps the energy and asks only for the folder.
    """
    from cratekit.core import routing

    bucket_id = declared.bucket_for_display(folder)
    if bucket_id is None:
        return None
    bucket = declared.bucket(bucket_id)
    candidates = [genre or "", bucket.display]
    if bucket.sub_by_source is not None:
        candidates += sorted(bucket.sub_by_source.map)
    for word in dict.fromkeys(one for one in candidates if one):
        if routing.resolve_bucket(declared, word).bucket_id != bucket_id:
            continue
        if playlist is None:
            return word, energy
        for level in _energies(energy, int(declared.energy.scale_max)):
            sub = routing.energy_sub(declared, bucket_id, level, source_genre=word)
            if sub is not None and sub.display == playlist:
                return word, level
    return None


@dataclass(frozen=True, slots=True)
class Change:
    """One track's edit as the library takes it."""

    content_id: str
    track: str
    outcome: str
    shown: str
    path: str
    genre_was: str | None
    genre: str | None
    energy_was: int | None
    energy: int | None
    #: Tree memberships it leaves and joins, ``(playlist id, folder, playlist)``.
    leave: tuple[tuple[str, str, str], ...] = ()
    join: tuple[tuple[str, str, str], ...] = ()
    #: Places the new tags file into that the tree does not hold yet.
    missing: tuple[str, ...] = ()
    why: str = ""
    #: Which tree the edit is in (U204); a genre edit alone writes file tags.
    tree: str = edits.GENRE
    #: A FAVOURITE's month, ``""`` for none, the month's playlist row or
    #: ``""`` when it is to be made, and whether the row takes Pink (U204).
    month: str = ""
    month_id: str = ""
    colour: bool = False

    def identity(self) -> list[Any]:
        return [
            self.content_id,
            self.track,
            self.outcome,
            self.path,
            self.genre,
            self.energy,
            [one[0] for one in self.leave],
            [one[0] for one in self.join],
            [self.month, self.month_id, self.colour],
        ]

    def item(self) -> dict[str, Any]:
        shown: dict[str, Any] = {
            "track": self.shown,
            "content_id": self.content_id,
            "edit": self.outcome,
            "leaves": [f"{folder} / {playlist}" for _pid, folder, playlist in self.leave],
            "joins": [f"{folder} / {playlist}" for _pid, folder, playlist in self.join],
            "why": self.why,
        }
        if self.tree == edits.GENRE:
            shown["genre"] = [self.genre_was, self.genre]
            shown["energy"] = [self.energy_was, self.energy]
        if self.month and not self.month_id:
            shown["makes"] = self.month
        if self.colour:
            shown["colour"] = "Pink"
        if self.outcome == edits.UNFAVOURITE:
            shown["note"] = (
                "it stays hearted on the account, so the next sync's landing places it "
                "again unless it is un-hearted there too; its colour is left as it is"
            )
        if self.missing:
            shown["not in the tree yet"] = list(self.missing)
        if self.outcome == edits.UNFILE:
            shown["note"] = (
                "rekordbox's Genre column keeps its word until a reread; routing reads "
                "the file, whose genre and energy are cleared"
            )
        return shown


@dataclass(frozen=True, slots=True)
class Planned:
    """Every change, and every edit not taken with why, for one gate line."""

    changes: tuple[Change, ...] = ()
    #: Edits the account made that the library does not take now, named.
    named: tuple[dict[str, Any], ...] = field(default=())

    def identity(self) -> dict[str, Any]:
        return {"kind": KIND, "changes": [one.identity() for one in self.changes]}

    #: The Favorites home a FAVOURITE is placed against, the Pink row, and why
    #: no row is coloured when there is none (U204). Not digested: each change
    #: carries the rows it writes.
    home: Any = None
    pink: str = ""
    colour_skipped: str = ""

    def counts(self) -> dict[str, int]:
        count = {
            kind: sum(1 for one in self.changes if one.outcome == kind)
            for kind in (
                edits.MOVE,
                edits.FOLDER,
                edits.UNFILE,
                edits.FAVOURITE,
                edits.UNFAVOURITE,
                edits.JOIN,
                edits.LEAVE,
            )
        }
        return {**count, "named": len(self.named)}


@dataclass(frozen=True, slots=True)
class Tree:
    """The routing tree as the step reads it: every genre playlist by its two names."""

    playlists: Mapping[tuple[str, str], str]
    #: Each tree playlist's names by its id.
    names: Mapping[str, tuple[str, str]]


def read_tree(db: Any, declared: Any, registry: Any) -> Tree:
    """Every plain playlist directly in a folder under the routing tree's adopted root."""
    from cratekit.core import rb_writer, tree_registry

    root_id = tree_registry.anchored_root(
        declared.tree.id, registry, root_exists=lambda root: db.get_playlist(ID=root) is not None
    )
    playlists: dict[tuple[str, str], str] = {}
    names: dict[str, tuple[str, str]] = {}
    for folder in list(db.get_playlist(ParentID=str(root_id))):
        if rb_writer.node_removed(folder) or not rb_writer.is_folder(folder):
            continue
        for row in list(db.get_playlist(ParentID=str(folder.ID))):
            if rb_writer.node_removed(row) or int(getattr(row, "Attribute", -1) or 0) != 0:
                continue
            key = (str(folder.Name), str(row.Name))
            # TWO OF ONE NAME ARE NOT A PLACE A NAME DECIDES: neither is joined.
            playlists[key] = "" if key in playlists else str(row.ID)
            names[str(row.ID)] = key
    return Tree(playlists={key: pid for key, pid in playlists.items() if pid}, names=names)


def _memberships(db: Any, content_id: str, tree: Tree) -> list[str]:
    """The tree playlists one live content row is in, by id, sorted."""
    from sqlalchemy import text

    from cratekit.core import rb_writer

    found = db.session.execute(
        text(
            f"SELECT PlaylistID FROM {rb_writer.MEMBERSHIP_TABLE} WHERE ContentID = :id "
            f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0"
        ),
        {"id": str(content_id)},
    ).fetchall()
    return sorted({str(one[0]) for one in found if str(one[0]) in tree.names})


def _routed(declared: Any) -> Any:
    """Whether a tree playlist, by its two names, is one routing files a track into.

    A band or an additive place of the folder's bucket. Any other playlist in a
    genre folder, the genre Favorites among them, is another engine's, and a
    move leaves the track in it.
    """
    known: dict[str, frozenset[str]] = {}

    def routed(names: tuple[str, str]) -> bool:
        folder, playlist = names
        if folder not in known:
            bucket_id = declared.bucket_for_display(folder)
            known[folder] = (
                frozenset()
                if bucket_id is None
                else _primary(declared, bucket_id) | _additive(declared, bucket_id)
            )
        return playlist in known[folder]

    return routed


def _resolve(cfg: config.Config, recorded: str) -> Path | None:
    from cratekit.core import locations
    from cratekit.modules.outbound import source

    if not recorded:
        return None
    resolved = locations.resolve_recorded_path(
        recorded, root=cfg.library.root, prefix_map=source.prefix_rules(cfg)
    )
    if resolved.path is None:
        return None
    path = Path(resolved.path)
    return path if path.is_file() else None


def plan(
    cfg: config.Config,
    db: Any,
    declared: Any,
    registry: Any,
    decided: edits.Decided,
    vocal_threshold: float | None,
    *,
    today: date | None = None,
) -> Planned:
    """Every carried edit as the library takes it, read on ``db``. Reads only.

    Raises the refusal of the routing tree or of the derivation. ``today`` is
    the day an INBOX batch's age is read for, the local day by default.
    """
    named: list[dict[str, Any]] = [
        one.item() for one in decided.decisions if one.outcome not in edits.CARRIED
    ]
    carried = decided.carried
    if not carried:
        return Planned(named=tuple(named))
    from cratekit.write import playlist_pair

    rows = playlist_pair.content(db, [one.content_id for one in carried])
    changes: list[Change] = []

    def skip(decision: edits.Decision, why: str) -> None:
        named.append({**decision.item(), "outcome": "not taken", "why": f"{decision.why}; {why}"})

    def live(decision: edits.Decision) -> Any:
        row = rows.get(decision.content_id)
        if row is None:
            skip(decision, "its library row is no longer a live row of the collection, so nothing is written")
        return row

    genre = [one for one in carried if one.tree == edits.GENRE]
    if genre:
        changes.extend(_plan_genre(cfg, db, declared, registry, genre, vocal_threshold, live, skip))
    favourites = [one for one in carried if one.tree == edits.FAVORITES]
    found: dict[str, Any] = {}
    if favourites:
        changes.extend(_plan_favourites(db, declared, favourites, live, skip, found))
    inbox = [one for one in carried if one.tree == edits.INBOX]
    if inbox:
        changes.extend(_plan_inbox(cfg, db, declared, registry, inbox, live, skip, today))
    return Planned(
        changes=tuple(changes),
        named=tuple(named),
        home=found.get("home"),
        pink=found.get("pink", ""),
        colour_skipped=found.get("colour_skipped", ""),
    )


def _shown(row: Any) -> str:
    return f"{row.artist} - {row.title}" if row.artist else row.title


def _plan_genre(
    cfg: config.Config,
    db: Any,
    declared: Any,
    registry: Any,
    carried: Sequence[edits.Decision],
    vocal_threshold: float | None,
    live: Any,
    skip: Any,
) -> list[Change]:
    """Every genre edit as the library takes it: the tags routing reads, and the tree (U201)."""
    from cratekit.write import rebuild, routing_pass

    tree = read_tree(db, declared, registry)
    routed = _routed(declared)
    changes: list[Change] = []
    for decision in carried:
        row = live(decision)
        if row is None:
            continue
        path = _resolve(cfg, row.path)
        if path is None:
            skip(decision, "its file could not be found, so neither its tags nor its row is written")
            continue
        truth = rebuild.read_truth(path)
        if decision.outcome == edits.UNFILE:
            genre, energy = None, None
        else:
            assert decision.to is not None
            playlist = decision.to.playlist if decision.outcome == edits.MOVE else None
            target = target_tags(declared, decision.to.folder, playlist, truth.genre, truth.energy)
            if target is None:
                skip(
                    decision,
                    f"no genre and energy routing reads files it into {decision.to.title}, "
                    f"so nothing is written",
                )
                continue
            genre, energy = target
        held = _memberships(db, decision.content_id, tree)
        missing: list[str] = []
        join: list[tuple[str, str, str]] = []
        if decision.outcome == edits.UNFILE:
            leave_ids = held
        else:
            placements, _gaps = rebuild.derive_from_taxonomy(
                declared,
                [rebuild.Truth(location=str(path), genre=genre, energy=energy, voxlevel=truth.voxlevel)],
                vocal_threshold=vocal_threshold,
            )
            wanted: set[str] = set()
            for placement in placements:
                names = routing_pass.destination(declared, placement.bucket, placement.sub)
                pid = tree.playlists.get(names)
                if pid is None:
                    missing.append(f"{names[0]} / {names[1]}")
                    continue
                wanted.add(pid)
            leave_ids = [pid for pid in held if pid not in wanted and routed(tree.names[pid])]
            join = [(pid, *tree.names[pid]) for pid in sorted(wanted) if pid not in held]
        changes.append(
            Change(
                content_id=decision.content_id,
                track=decision.track,
                outcome=decision.outcome,
                shown=_shown(row),
                path=str(path),
                genre_was=truth.genre,
                genre=genre,
                energy_was=truth.energy,
                energy=energy,
                leave=tuple((pid, *tree.names[pid]) for pid in leave_ids),
                join=tuple(join),
                missing=tuple(missing),
                why=decision.why,
            )
        )
    return changes


def _live_in(db: Any, content_id: str) -> frozenset[str]:
    """Every playlist one content row is a live member of, by id."""
    from sqlalchemy import text

    from cratekit.core import rb_writer

    found = db.session.execute(
        text(
            f"SELECT PlaylistID FROM {rb_writer.MEMBERSHIP_TABLE} WHERE ContentID = :id "
            f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0"
        ),
        {"id": str(content_id)},
    ).fetchall()
    return frozenset(str(one[0]) for one in found)


def _plan_favourites(
    db: Any,
    declared: Any,
    carried: Sequence[edits.Decision],
    live: Any,
    skip: Any,
    found: dict[str, Any],
) -> list[Change]:
    """Every Favorites edit as the library takes it, against the home read on ``db`` (U204).

    A library with no one home for the favourites, or one at the playlist root,
    takes none of them, each named.
    """
    from cratekit.favorites import colour, placeholders, placement

    try:
        home = placement.resolve_home(db, placement.source_name(declared))
    except CratekitError as exc:
        for decision in carried:
            skip(decision, f"the favourites have no home here, so nothing is written: {exc.cause.message}")
        return []
    if not home.folder_id:
        for decision in carried:
            skip(
                decision,
                f"{home.source_name!r} sits at the playlist root, so there is no Favorites "
                f"folder to write and nothing is written",
            )
        return []
    pink, colour_skipped = placement.read_pink(db)
    found.update(home=home, pink=pink, colour_skipped=colour_skipped)
    folder = home.folder_name
    filing = sorted(
        (name, pid)
        for name, pid in home.present.items()
        if pid != home.source_id and placeholders.is_filing(name)
    )
    changes: list[Change] = []
    for decision in carried:
        row = live(decision)
        if row is None:
            continue
        held = _live_in(db, decision.content_id)
        base = {
            "content_id": decision.content_id,
            "track": decision.track,
            "outcome": decision.outcome,
            "shown": _shown(row),
            "path": "",
            "genre_was": None,
            "genre": None,
            "energy_was": None,
            "energy": None,
            "why": decision.why,
            "tree": edits.FAVORITES,
        }
        if decision.outcome == edits.UNFAVOURITE:
            leave = [(home.source_id, folder, home.source_name)] if home.source_id in held else []
            leave += [(pid, folder, name) for name, pid in filing if pid in held]
            changes.append(Change(**base, leave=tuple(leave)))
            continue
        assert decision.to is not None
        if decision.to.primary:
            month = "" if decision.filed else placeholders.month_label(edits.moment(decision.when))
        else:
            month = decision.to.playlist
            if placeholders.MONTH_LABEL.fullmatch(month) is None and month != placeholders.UNDATED:
                skip(
                    decision,
                    f"{decision.to.title} is a quarter, which the month split retires, so no "
                    f"favourite is filed into it",
                )
                continue
        join: list[tuple[str, str, str]] = []
        if home.source_id not in held:
            join.append((home.source_id, folder, home.source_name))
        month_id = home.present.get(month, "") if month else ""
        if month_id and month_id in held:
            month, month_id = "", ""
        elif month_id:
            join.append((month_id, folder, month))
        takes = bool(pink) and decision.content_id in colour.sort_rows(db, pink, [decision.content_id]).to_colour
        # A MOVE BETWEEN MONTHS leaves each month it was taken off.
        away = {one.playlist for one in decision.away}
        leave = tuple((pid, folder, name) for name, pid in filing if name in away and pid in held)
        changes.append(
            Change(
                **base,
                join=tuple(join),
                leave=leave,
                month=month,
                month_id=month_id,
                colour=takes,
            )
        )
    return changes


def _plan_inbox(
    cfg: config.Config,
    db: Any,
    declared: Any,
    registry: Any,
    carried: Sequence[edits.Decision],
    live: Any,
    skip: Any,
    today: date | None,
) -> list[Change]:
    """Every INBOX edit as the library takes it, each batch found live under INBOX on ``db`` (U204).

    A batch no longer directly under INBOX, moved into Old or out, is named and
    not written: Old is never touched.
    """
    from cratekit.intake import rotate

    try:
        batches = rotate.live_batches(
            cfg, db, declared=declared, registry=registry, today=today or date.today()
        )
    except CratekitError as exc:
        for decision in carried:
            skip(decision, f"INBOX could not be read, so nothing is written: {exc.cause.message}")
        return []
    named: dict[str, list[str]] = {}
    for pid, name in batches.batches:
        named.setdefault(name, []).append(pid)
    changes: list[Change] = []
    for decision in carried:
        row = live(decision)
        if row is None:
            continue
        assert decision.to is not None
        batch = decision.to.playlist
        found = named.get(batch, [])
        if len(found) != 1:
            skip(
                decision,
                f"{batch!r} is no longer one batch directly under {batches.root_name}, so "
                f"nothing is written to it; Old is never touched",
            )
            continue
        (pid,) = found
        held = pid in _live_in(db, decision.content_id)
        place = ((pid, batches.root_name, batch),)
        changes.append(
            Change(
                content_id=decision.content_id,
                track=decision.track,
                outcome=decision.outcome,
                shown=_shown(row),
                path="",
                genre_was=None,
                genre=None,
                energy_was=None,
                energy=None,
                leave=place if decision.outcome == edits.LEAVE and held else (),
                join=place if decision.outcome == edits.JOIN and not held else (),
                why=decision.why,
                tree=edits.INBOX,
            )
        )
    return changes


def _write_tags(change: Change) -> bool:
    """Write one file's two tags and read them back. ``True`` when the file holds them."""
    from cratekit.core import tags

    path = Path(change.path)
    cleared = [
        name
        for name, value in (("genre", change.genre), ("energylevel", change.energy))
        if value is None
    ]
    written = {
        name: value
        for name, value in (("genre", change.genre), ("energylevel", change.energy))
        if value is not None
    }
    if written and not tags.write_tags(path, written):
        return False
    if cleared and not tags.clear_tags(path, cleared):
        return False
    return (
        (tags.read_genre_from_file(path) or None) == (change.genre or None)
        and tags.read_energy_from_file(path) == change.energy
    )


@dataclass
class Applied:
    """What the write did, for the report."""

    tagged: list[str] = field(default_factory=list)
    untagged: list[str] = field(default_factory=list)
    genre_rows: int = 0
    genre_skipped: list[str] = field(default_factory=list)
    left: int = 0
    joined: int = 0
    session_id: str = ""
    #: Rows coloured Pink with a FAVOURITE, and month playlists made (U204).
    coloured: int = 0
    made: list[str] = field(default_factory=list)
    #: Every edit the library took, ``(content id, tree)``, for the snapshot.
    taken: list[tuple[str, str]] = field(default_factory=list)
    #: Each FAVOURITE the placement wrote into a month, ``(content id, month,
    #: the membership's time)``, the library's own placement (U236).
    months: list[tuple[str, str, str]] = field(default_factory=list)

    def totals(self) -> dict[str, Any]:
        return {
            "tagged": len(self.tagged),
            "untagged": list(self.untagged),
            "genre_rows": self.genre_rows,
            "genre_skipped": list(self.genre_skipped),
            "left": self.left,
            "joined": self.joined,
            "coloured": self.coloured,
            "made": list(self.made),
            "session_id": self.session_id,
        }

    @property
    def wrote(self) -> bool:
        return bool(self.left or self.joined or self.genre_rows or self.coloured or self.made)


def write(
    cfg: config.Config,
    db: Any,
    approved: Planned,
    *,
    tree_id: str,
    registry: Any,
    intake_id: str = "",
) -> Applied:
    """Write every change in one guarded session on the write handle ``db``, and read it back.

    THE TREE'S OWN LATCH FIRST, as every tree writer's
    (``convergence.assert_tree_writable``): a database restored out of band is
    detected before this write's fingerprint overwrites the evidence, and a
    tree marked unconverged is refused before any file or row is written. The
    routing tree's for a genre edit, the intake tree's for an INBOX edit
    (U204); the Favorites folder is nobody's tree, so for it alone the
    restore is detected and marked, as ``favorites backfill`` does.
    """
    from cratekit.core import analysis_store, convergence, rb_writer, session, snapshot
    from cratekit.favorites import placement
    from cratekit.write import metadata, trees

    done = Applied()
    touched = {one.tree for one in approved.changes}
    if edits.GENRE in touched:
        convergence.assert_tree_writable(cfg, db, tree_id, registry)
    if edits.INBOX in touched:
        convergence.assert_tree_writable(cfg, db, intake_id, registry)
    if touched and not touched & {edits.GENRE, edits.INBOX}:
        convergence.detect_out_of_band_restore(cfg, db, registry)
    watched = list(analysis_store.watch_roots(cfg))
    placed: Any = None
    with (
        session.assert_gates(cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD)
        as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record = gates.record
        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)
        # THE FILES FIRST, each read back, and only a file that took has its
        # row written, so the database never says what the file does not. An
        # edit of the Favorites folder or INBOX writes no file (U204).
        taken: list[Change] = []
        for change in approved.changes:
            if change.tree != edits.GENRE:
                taken.append(change)
            elif _write_tags(change):
                taken.append(change)
                done.tagged.append(change.content_id)
            else:
                done.untagged.append(f"{change.shown} ({change.path})")
        try:
            # EVERY ROW TAKING A GENRE IS ASKED, not only one whose file's genre
            # changed: the row may say another genre than its file, and the
            # writer's own policy skips a row that already holds it.
            genres = {one.content_id: one.genre for one in taken if one.genre}
            if genres:
                metadata.enable((metadata.RETAG_GENRE,))
                found = {cid: db.get_content(ID=cid) for cid in genres}
                rows = [row for row in found.values() if row is not None]
                retag = metadata.plan_genre_retag(rows, genres, db=db)
                metadata.assert_within_policy(retag)
                report = metadata.write_plan(retag, {str(row.ID): row for row in rows})
                done.genre_rows = len(report.written)
                done.genre_skipped = [
                    f"{one.content_id}: {one.reason}" for one in report.skipped
                ]
            favourites = [one for one in taken if one.outcome == edits.FAVOURITE]
            for change in taken:
                for pid, _folder, _playlist in change.leave:
                    done.left += len(
                        rb_writer.remove_memberships(db, db.get_playlist(ID=pid), [change.content_id])
                    )
                # A FAVOURITE JOINS THROUGH THE PLACEMENT below, never here.
                if change.outcome == edits.FAVOURITE:
                    continue
                for pid, _folder, _playlist in change.join:
                    done.joined += len(
                        rb_writer.add_memberships(db, db.get_playlist(ID=pid), [change.content_id])
                    )
            if favourites:
                # PLACED AS A HEART IS PLACED (U204): the month found or made in
                # its slot, Pink on a row the plan read with no colour.
                placed = placement.place(
                    db,
                    approved.home,
                    [(one.content_id, one.month or None) for one in favourites],
                    pink=approved.pink,
                    to_colour=[one.content_id for one in favourites if one.colour],
                    colour_skipped=approved.colour_skipped,
                )
                done.joined += placed.added
                done.coloured = len(placed.coloured)
                done.made = list(placed.created)
            db.session.flush()
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
        except BaseException:
            trees._rollback_quietly(db)
            if witness.landed:
                _record_commit(record, cfg, done)
            raise
        _record_commit(record, cfg, done)
        if done.wrote:
            convergence.record_fingerprint(cfg, db)
        done.session_id = record.session_id
    assert_read_back(db, taken, placed=placed, home=approved.home)
    done.taken = [(one.content_id, one.tree) for one in taken]
    # THE MEMBERSHIP EACH MONTH PLACEMENT MADE, by its time as the edit rule
    # reads it (U236), so only that one membership is ever read as the
    # library's. One whose time cannot be read is recorded as nothing.
    from cratekit.organize import account_mirror

    rows = {name: row for name, row, _count in placed.months} if placed is not None else {}
    for one in taken:
        if one.outcome != edits.FAVOURITE or not one.month or one.month not in rows:
            continue
        at = account_mirror.membership_times(db, rows[one.month]).get(one.content_id, "")
        if at:
            done.months.append((one.content_id, one.month, at))
    return done


def _record_commit(record: Any, cfg: config.Config, done: Applied) -> None:
    from cratekit.core import session

    if not done.wrote:
        return
    session.record_commit(
        record,
        KIND,
        session.ChangeSummary(
            (
                session.TreeChange(
                    tree=KIND,
                    created=done.joined + len(done.made),
                    updated=done.left + done.genre_rows + done.coloured,
                ),
            )
        ),
        cfg,
    )


def assert_read_back(
    db: Any, written: Sequence[Change], *, placed: Any = None, home: Any = None
) -> None:
    """Refuse an answer the database does not hold: each track in and out where planned.

    A FAVOURITE is read back in All Favorites and in the month row the
    placement wrote, made or found (U204).
    """
    months = {name: row for name, row, _count in placed.months} if placed is not None else {}
    for change in written:
        found = _live_in(db, change.content_id)
        stayed = [pid for pid, _f, _p in change.leave if pid in found]
        absent = [pid for pid, _f, _p in change.join if pid not in found]
        if change.outcome == edits.FAVOURITE and home is not None:
            wanted = [home.source_id]
            if change.month:
                wanted.append(months.get(change.month, f"{change.month} (not written)"))
            absent += [pid for pid in wanted if pid not in found and pid not in absent]
        if stayed or absent:
            raise refuse(
                "session-committed-unverified",
                f"{change.shown} read back from the database is still in {len(stayed)} "
                f"playlist(s) it was to leave and missing from {len(absent)} it was to "
                f"join; the commit landed and this answer cannot be vouched for",
                origin=_ORIGIN,
                detail={"content_id": change.content_id, "stayed": stayed, "absent": absent},
            )


def settle(
    cfg: config.Config,
    decided: edits.Decided,
    written: Iterable[Any],
    months: Iterable[tuple[str, str, str]] = (),
) -> None:
    """Agree each edit the library took in the snapshot, so it is not read again (U201).

    ``written`` is each edit taken as ``(content id, tree)``, or a bare content
    id for a genre edit. Recorded after the commit and before the mirror's own
    apply, whose record keeps this word for a track it holds. A ledger that
    cannot take it leaves the snapshot as it was: the next refresh reads both
    sides agreeing on the track and settles it then, writing nothing.

    ``months`` is each FAVOURITE the placement wrote into a month, ``(content
    id, month, the membership's time)`` (U236). For one put in All Favorites alone that month is the
    library's choice, which the account does not hold, so it is recorded as
    the library's own placement on that month's account title, mirrored yet
    or not, and the next refresh never reads it as a change made in rekordbox.
    """
    from cratekit.modules.outbound import ledger, mirror

    took = {one if isinstance(one, tuple) else (str(one), edits.GENRE) for one in written}
    month_of = {content_id: (month, at) for content_id, month, at in months}
    carried = [one for one in decided.carried if (one.content_id, one.tree) in took]
    ledger.settle_mirror_tracks(
        cfg,
        [
            (folder, title, decision.track, on)
            for decision in carried
            for folder, title, on in decision.settle
        ],
        placed=[
            (
                decision.to.folder,
                mirror.title(decision.to.folder, month_of[decision.content_id][0]),
                decision.track,
                month_of[decision.content_id][1],
            )
            for decision in carried
            if decision.outcome == edits.FAVOURITE
            and decision.tree == edits.FAVORITES
            and decision.to is not None
            and decision.to.primary
            and month_of.get(decision.content_id)
        ],
    )


def _stale(approved: Planned, now: Planned) -> None:
    if approved.identity() != now.identity():
        raise refuse(
            "decision-stale",
            "the library moved since the plan the gate showed was made, so no edit made "
            "on the account was written; run organize again and approve what it shows now",
            origin=_ORIGIN,
            detail={"approved": approved.identity(), "now": now.identity()},
        )


def add_step(
    cfg: config.Config, declared: Any, registry: Any, shared: Any, *, one_read: Any = None
) -> Step:
    """The rekordbox area's step: plan on a read handle, write on its own (U201).

    ``shared`` is the organize run's one mirror reading. A reading or a tree
    that cannot be read refuses this step alone. ``one_read`` is ``--report``'s
    one read handle (U267), which the plan reads through; the write, which a
    report never runs, opens its own handle to write as before.
    """
    from cratekit.core import rb_writer
    from cratekit.write import metadata_cli

    try:
        reading = shared.reading()
    except CratekitError as exc:
        return refused(KIND, TITLE, exc.cause)
    if reading.unread:
        return Step(key=KIND, title=TITLE, state=LISTED, detail=reading.unread)
    decided = reading.decided
    # EVERY READ THIS STEP MAKES REFUSES THIS STEP ALONE, as each sibling's:
    # the vocal calibration, the read handle and the plan. The calibration is
    # read only for a genre edit, the one that derives a with vox place.
    genre = any(one.tree == edits.GENRE for one in decided.carried)
    try:
        threshold = metadata_cli.load_vocal_threshold(cfg) if genre else None
        db = (
            one_read.handle()
            if one_read is not None
            else rb_writer.open_db(
                rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
            )
        )
    except CratekitError as exc:
        return refused(KIND, TITLE, exc.cause)
    try:
        planned = plan(cfg, db, declared, registry, decided, threshold)
    except CratekitError as exc:
        return refused(KIND, TITLE, exc.cause)
    finally:
        rb_writer.done_reading(db, one_read)
    counts = planned.counts()
    writes = bool(planned.changes)
    detail = (
        f"{counts[edits.MOVE]} track(s) moved, {counts[edits.FOLDER]} given another genre, "
        f"{counts[edits.UNFILE]} unfiled, {counts[edits.FAVOURITE]} favourited, "
        f"{counts[edits.UNFAVOURITE]} unfavourited, {counts[edits.JOIN]} joined to and "
        f"{counts[edits.LEAVE]} taken off an INBOX batch as edited on the account; "
        f"{counts['named']} edit(s) named and not taken"
        if writes or planned.named
        else "no mirrored playlist was changed on the account since the mirror last finished it"
    )
    step = Step(
        key=KIND,
        title=TITLE,
        state=PLANNED if writes else NOTHING,
        detail=detail,
        digest=digest_of(planned.identity()),
        counts=counts,
        items=[one.item() for one in planned.changes] + list(planned.named),
    )
    if writes:

        def apply() -> dict[str, Any]:
            handle = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
            try:
                now = plan(cfg, handle, declared, registry, decided, threshold)
                _stale(planned, now)
                done = write(
                    cfg,
                    handle,
                    now,
                    tree_id=declared.tree.id,
                    registry=registry,
                    intake_id=declared.intake.id,
                )
            finally:
                rb_writer.close_db(handle)
            settle(cfg, decided, done.taken, done.months)
            if done.untagged:
                step.warnings.append(
                    {
                        "code": "organize-mirror-edits-untagged",
                        "message": (
                            f"{len(done.untagged)} file(s) did not take their new tags, so "
                            f"their rows were not written: " + "; ".join(done.untagged)
                        ),
                    }
                )
            return done.totals()

        step.apply = apply
    return step


def deletes(planned_items: Iterable[Mapping[str, Any]]) -> list[str]:
    """Every membership the step takes away, one gate line per track."""
    said = {
        edits.UNFILE: ", and its genre and energy tags are cleared",
        edits.UNFAVOURITE: (
            ", and it stays hearted on the account, so the next sync places it again "
            "unless it is un-hearted there too"
        ),
    }
    return [
        f"{one['track']} leaves {', '.join(one['leaves'])}" + said.get(str(one.get("edit")), "")
        for one in planned_items
        if one.get("leaves") and "edit" in one
    ]


__all__ = [
    "KIND",
    "TITLE",
    "WORKFLOW",
    "Applied",
    "Change",
    "Planned",
    "Tree",
    "add_step",
    "assert_read_back",
    "deletes",
    "places",
    "plan",
    "read_tree",
    "settle",
    "target_tags",
    "write",
]
