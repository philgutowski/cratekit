"""An edit made on the account to a mirrored playlist, taken into the library (U201, U204).

``crate organize``'s rekordbox area step ``mirror-edits``. The edit rule
(:mod:`cratekit.modules.outbound.mirror_edits`) decides which track a person
changed on the account; this step carries each one the library takes, and the
mirror holds the account meanwhile so the edit is never put back. A MOVE or a
FOLDER retags the file to the nearest genre and energy routing itself files into
the named place (refused when none does); an UNFILE clears both so ``route
unplaced`` lists it (2026-11-04); a FAVOURITE is placed as a heart is, through
``favorites.placement``, never into a quarter; an UNFAVOURITE leaves All
Favorites and its filing playlists but stays hearted on the account (the two
step rule of 2026-10-14); a JOIN or LEAVE changes a batch found live directly
under INBOX, never Old.

ONE GUARDED SESSION FOR EVERY TRACK: the file's two tags first, each read back,
then the row's genre where rekordbox already holds that name, then the tree
memberships by the rule ``route resort`` writes by, its vocal sub by the row's
``vox`` My Tag and never the file's score (U127, R-2062), so a membership taken
here is never one the next resort adds back. A file whose tag did not
take keeps its row. Nothing leaves the collection and no beat grid is written:
the two tags are the only fields, and the writable field set refuses a tempo.
An unfile cannot empty the row's genre, so the Genre column keeps its word until
a reread. The snapshot then takes each edit (:func:`settle`), and the apply
refuses ``decision-stale`` when the library moved since the gate.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import CratekitError, refuse
from cratekit.organize.steps import NOTHING, PLANNED, Step, refused

if TYPE_CHECKING:
    from cratekit.modules.outbound import mirror_edits as edits

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
    sources = ["", *(sorted(bucket.sub_by_source.map) if bucket.sub_by_source is not None else ())]
    levels: list[int | None] = [None, *range(1, int(declared.energy.scale_max) + 1)]
    return frozenset(
        sub.display
        for source in sources
        for level in levels
        if (sub := routing.energy_sub(declared, bucket_id, level, source_genre=source)) is not None
    )


def _additive(declared: Any, bucket_id: str) -> frozenset[str]:
    """The additive playlists routing files a track into beside its band: genre subs and with vox."""
    from cratekit.write import trees

    vox = {one.display for one in declared.sub_classes if one.id == trees.VOX_SUB_CLASS and one.additive}
    return frozenset({genre.display for genre in declared.bucket(bucket_id).genre_subs} | vox)


def places(declared: Any, folders: Iterable[Any]) -> dict[str, edits.Place]:
    """Each edited playlist's place by its account title, read by its folder's rule (U201, U204).

    A playlist with no place has every difference read as rekordbox's.
    """
    from cratekit.modules.outbound import mirror_edits as edits

    found: dict[str, edits.Place] = {}
    for folder in folders:
        if folder.edits == edits.FAVORITES:
            found.update(_favourite_places(declared, folder))
        elif folder.edits == edits.INBOX:
            found.update(_inbox_places(folder))
        elif folder.edits == edits.GENRE:
            bucket_id = declared.bucket_for_display(folder.name)
            if bucket_id is None:
                continue
            primary = _primary(declared, bucket_id)
            additive = _additive(declared, bucket_id)
            for source, playlist in _named(folder):
                if playlist in primary or playlist in additive:
                    found[source.name] = edits.Place(source.name, folder.name, playlist, playlist in primary)
    return found


def _named(folder: Any) -> list[tuple[Any, str]]:
    """Each playlist of the folder titled after it, with the title's rest."""
    prefix = f"{folder.name} "
    return [(one, one.name[len(prefix) :]) for one in folder.playlists if one.name.startswith(prefix)]


def _favourite_places(declared: Any, folder: Any) -> dict[str, edits.Place]:
    """All Favorites, the primary place, and each filing playlist beside it (U204)."""
    from cratekit.favorites import placeholders, placement
    from cratekit.modules.outbound import mirror_edits as edits

    source = placement.source_name(declared)
    rest = {one.name: name for one, name in _named(folder)}
    found: dict[str, edits.Place] = {}
    for one in folder.playlists:
        if one.name == source:
            found[one.name] = edits.Place(one.name, folder.name, source, True, edits.FAVORITES)
        elif one.name in rest and placeholders.is_filing(rest[one.name]):
            found[one.name] = edits.Place(one.name, folder.name, rest[one.name], False, edits.FAVORITES)
    return found


def _inbox_places(folder: Any) -> dict[str, edits.Place]:
    """Every INBOX batch the mirror copies, each a place of its own (U204)."""
    from cratekit.modules.outbound import mirror_edits as edits

    return {
        one.name: edits.Place(one.name, folder.name, batch, True, edits.INBOX)
        for one, batch in _named(folder)
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

    ``playlist`` is a MOVE's band, or ``None`` for a FOLDER, which keeps the energy.
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


#: Why an edit on a track filed into two genre folders is not taken (U340).
SECOND_GENRE_EDIT = (
    "it is filed into two genre folders by its genre and its second genre, and "
    "{what}, so which of the two the account changed is not something the account says; "
    "`crate tag second` sets or clears a second genre"
)


#: Why an edit that would leave or wake a folder the account did not touch is
#: not taken (U340): the genres it would write file the track elsewhere.
SECOND_GENRE_ELSEWHERE = (
    "it carries a second genre, and the genres this edit would write file it into "
    "{filed} where the account shows {shown}, so nothing is written; "
    "`crate tag second` sets or clears a second genre"
)


def _folders(declared: Any, buckets: Any) -> str:
    """Genre folders by display, sorted and joined, or ``no genre folder``."""
    shown = sorted(declared.bucket(bucket).display for bucket in buckets if bucket)
    return " and ".join(shown) or "no genre folder"


def _filed_by(declared: Any, genre: str | None, second: str | None) -> frozenset[str]:
    """The genre folders a genre and a second genre file a track into, the
    fallback included for a genre that files by it alone, as rebuild derives."""
    from cratekit.core import routing

    first = routing.resolve_bucket(declared, genre).bucket_id if genre else None
    return frozenset(
        bucket for bucket in (first, routing.second_bucket(declared, genre, second)) if bucket
    )


def left_folders(decision: Any) -> frozenset[str]:
    """The genre folders an edit took a track's band places out of on the account.

    Read off the edit's own record: its band places in the snapshot that the
    account no longer holds, each named to its folder by the playlists the
    edit read in full.
    """
    folder_of = {title: folder for folder, title, _held in decision.settle}
    return frozenset(
        folder_of[title] for title in set(decision.was) - set(decision.account) if title in folder_of
    )


def _second_genre_tags(
    declared: Any, decision: Any, truth: Any, two: str
) -> tuple[str | None, int | None, str | None] | str:
    """The genre, energy and second genre an edit gives a track filed into two folders (U340).

    Or why it is not taken. AN EDIT IN ONE FOLDER LEAVES THE OTHER: a band move
    inside either folder changes the energy alone, which files the track in the
    same band of both; a move out of one folder into a third replaces the genre
    that named the folder it left and keeps the other. An edit that took the
    track out of one folder and left it in the other, that left both, or that
    left neither while adding a third, says nothing about which genre changed,
    and is not taken.
    """
    from cratekit.core import routing
    from cratekit.modules.outbound import mirror_edits as edits

    assert decision.to is not None
    one = routing.resolve_bucket(declared, truth.genre).bucket_id
    to = declared.bucket_for_display(decision.to.folder)
    left = {declared.bucket_for_display(folder) for folder in left_folders(decision)}
    playlist = decision.to.playlist if decision.outcome == edits.MOVE else None
    if to in (one, two):
        other = two if to == one else one
        if other in left:
            return SECOND_GENRE_EDIT.format(
                what=f"the account took it out of {declared.bucket(other).display} only"
            )
        if decision.outcome != edits.MOVE:
            return SECOND_GENRE_EDIT.format(
                what=f"the account put it in a playlist of {decision.to.folder}, which holds it"
            )
        word = truth.genre if to == one else truth.second_genre
        target = target_tags(declared, decision.to.folder, playlist, word, truth.energy)
        if target is None or target[0] != word:
            return (
                f"no energy files it into {decision.to.title} by the genre that names "
                f"{decision.to.folder}, so nothing is written"
            )
        return truth.genre, target[1], truth.second_genre
    if left not in ({one}, {two}):
        return SECOND_GENRE_EDIT.format(
            what=f"the account put it in {decision.to.title} without taking it out of "
            f"exactly one of the two"
        )
    target = target_tags(declared, decision.to.folder, playlist, None, truth.energy)
    if target is None:
        return (
            f"no genre and energy routing reads files it into {decision.to.title}, "
            f"so nothing is written"
        )
    word, energy = target
    found = (word, energy, truth.second_genre) if left == {one} else (truth.genre, energy, word)
    # THE TWO FOLDERS IT ENDS IN ARE THE ONE KEPT AND THE ONE IT WAS PUT IN, or
    # the edit is not taken: a word filing by the fallback alone files no
    # second genre beside it, nor as one (round one's B2).
    kept = two if left == {one} else one
    filed = _filed_by(declared, found[0], found[2])
    if filed != {kept, to}:
        return SECOND_GENRE_ELSEWHERE.format(
            filed=_folders(declared, filed), shown=_folders(declared, {kept, to})
        )
    return found


@dataclass(frozen=True, slots=True)
class Change:
    """One track's edit as the library takes it."""

    content_id: str
    track: str
    outcome: str
    shown: str
    path: str = ""
    genre_was: str | None = None
    genre: str | None = None
    energy_was: int | None = None
    energy: int | None = None
    #: The file's second genre before and after (U340), both None on a track
    #: with one genre, which is written exactly as before.
    second_was: str | None = None
    second: str | None = None
    #: Tree memberships it leaves and joins, ``(playlist id, folder, playlist)``.
    leave: tuple[tuple[str, str, str], ...] = ()
    join: tuple[tuple[str, str, str], ...] = ()
    #: Places the new tags file into that the tree does not hold yet.
    missing: tuple[str, ...] = ()
    #: Held vocal subs kept because the score places the track there and its
    #: row carries no vox My Tag, ``(playlist id, folder, playlist)`` (R-2062).
    untagged: tuple[tuple[str, str, str], ...] = ()
    why: str = ""
    #: Which tree the edit is in (U204); a genre edit alone writes file tags.
    #: Spelled as ``edits.GENRE``'s value, since that module sits behind the toggle.
    tree: str = "genre"
    #: A FAVOURITE's month, ``""`` for none, the month's playlist row or
    #: ``""`` when it is to be made, and whether the row takes Pink (U204).
    month: str = ""
    month_id: str = ""
    colour: bool = False

    def identity(self) -> list[Any]:
        return [
            self.content_id, self.track, self.outcome, self.path, self.genre, self.energy,
            [one[0] for one in self.leave], [one[0] for one in self.join],
            [self.month, self.month_id, self.colour],
            # Only where a second genre is in play (U340), so a one genre
            # change digests as before.
            *([[self.second_was, self.second]] if self.second_was or self.second else []),
        ]

    def item(self) -> dict[str, Any]:
        from cratekit.modules.outbound import mirror_edits as edits

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
            if self.second_was or self.second:
                shown["second genre"] = [self.second_was, self.second]
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
        if self.untagged:
            shown["keeps untagged"] = [f"{folder} / {playlist}" for _pid, folder, playlist in self.untagged]
            shown["untagged"] = (
                "its file clears the vocal cut and its row carries no vox My Tag, so it "
                "stays where it is and converge names it until it is tagged or taken out"
            )
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
        from cratekit.modules.outbound import mirror_edits as edits

        kinds = (edits.MOVE, edits.FOLDER, edits.UNFILE, edits.FAVOURITE, edits.UNFAVOURITE, edits.JOIN, edits.LEAVE)
        count = {kind: sum(1 for one in self.changes if one.outcome == kind) for kind in kinds}
        return {**count, "named": len(self.named)}


@dataclass(frozen=True, slots=True)
class Tree:
    """The routing tree as the step reads it: every genre playlist by its two names."""

    playlists: Mapping[tuple[str, str], str]
    #: Each tree playlist's names by its id.
    names: Mapping[str, tuple[str, str]]


def read_tree(db: Any, declared: Any, registry: Any) -> Tree:
    """Every plain playlist directly in a folder under the routing tree's adopted root."""
    from cratekit.core import rb_writer
    from cratekit.organize import account_mirror as am

    playlists: dict[tuple[str, str], str] = {}
    names: dict[str, tuple[str, str]] = {}
    for folder in am._children(db, am.tree_root(db, declared, registry)):
        if not rb_writer.is_folder(folder):
            continue
        for row in filter(am._plain, am._children(db, folder.ID)):
            key = (str(folder.Name), str(row.Name))
            # TWO OF ONE NAME ARE NOT A PLACE A NAME DECIDES: neither is joined.
            playlists[key] = "" if key in playlists else str(row.ID)
            names[str(row.ID)] = key
    return Tree(playlists={key: pid for key, pid in playlists.items() if pid}, names=names)


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


def _routed(declared: Any) -> Any:
    """Whether a tree playlist, by its two names, is a band or additive place routing files into.

    Any other playlist in a genre folder is another engine's, and a move leaves it.
    """
    known: dict[str, frozenset[str]] = {}

    def routed(names: tuple[str, str]) -> bool:
        folder, playlist = names
        if folder not in known:
            bucket_id = declared.bucket_for_display(folder)
            known[folder] = (
                frozenset() if bucket_id is None else _primary(declared, bucket_id) | _additive(declared, bucket_id)
            )
        return playlist in known[folder]

    return routed


def plan(
    cfg: config.Config, db: Any, declared: Any, registry: Any, decided: edits.Decided,
    vocal_threshold: float | None, *, today: date | None = None,
) -> Planned:
    """Every carried edit as the library takes it, read on ``db``. Reads only.

    Raises the refusal of the routing tree or of the derivation.
    """
    from cratekit.modules.outbound import mirror_edits as edits
    from cratekit.write import playlist_pair

    named: list[dict[str, Any]] = [
        one.item() for one in decided.decisions if one.outcome not in edits.CARRIED
    ]
    carried = decided.carried
    if not carried:
        return Planned(named=tuple(named))
    rows = playlist_pair.content(db, [one.content_id for one in carried])

    def skip(decision: edits.Decision, why: str) -> None:
        named.append({**decision.item(), "outcome": "not taken", "why": f"{decision.why}; {why}"})

    def live(decision: edits.Decision) -> Any:
        row = rows.get(decision.content_id)
        if row is None:
            skip(decision, "its library row is no longer a live row of the collection, so nothing is written")
        return row

    def of(tree: str) -> list[edits.Decision]:
        return [one for one in carried if one.tree == tree]

    changes: list[Change] = []
    if genre := of(edits.GENRE):
        changes.extend(_plan_genre(cfg, db, declared, registry, genre, vocal_threshold, live, skip))
    found: dict[str, Any] = {}
    if favourites := of(edits.FAVORITES):
        changes.extend(_plan_favourites(db, declared, favourites, live, skip, found))
    if inbox := of(edits.INBOX):
        changes.extend(_plan_inbox(cfg, db, declared, registry, inbox, live, skip, today))
    return Planned(changes=tuple(changes), named=tuple(named), **found)


def _shown(row: Any) -> str:
    return f"{row.artist} - {row.title}" if row.artist else row.title


def _plan_genre(
    cfg: config.Config, db: Any, declared: Any, registry: Any, carried: Sequence[edits.Decision],
    vocal_threshold: float | None, live: Any, skip: Any,
) -> list[Change]:
    """Every genre edit as the library takes it: the tags routing reads, and the tree (U201)."""
    from cratekit.core import routing
    from cratekit.modules.outbound import mirror_edits as edits
    from cratekit.organize import account_mirror
    from cratekit.write import rebuild, routing_pass, vox_tag

    tree = read_tree(db, declared, registry)
    routed = _routed(declared)
    # THE VOX MY TAG FILES THE VOCAL SUB (U127, R-2062), as the resort after
    # this reads it: read once for every edit, and only where it could file
    # something. A library with no vox tag carries it on no row.
    reads_tag = rebuild.reads_vox_tag(declared, vocal_threshold)
    tagged = (vox_tag.vox_tagged(db) or frozenset()) if reads_tag else frozenset()
    changes: list[Change] = []
    for decision in carried:
        row = live(decision)
        if row is None:
            continue
        path = account_mirror.resolve_path(cfg, row.path)
        if path is None or not path.is_file():
            skip(decision, "its file could not be found, so neither its tags nor its row is written")
            continue
        truth = rebuild.read_truth(path)
        second_was = truth.second_genre or None
        second = second_was
        two = routing.second_bucket(declared, truth.genre, truth.second_genre)
        if decision.outcome == edits.UNFILE:
            genre, energy, second = None, None, None
        elif two is not None:
            found = _second_genre_tags(declared, decision, truth, two)
            if isinstance(found, str):
                skip(decision, found)
                continue
            genre, energy, second = found
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
            # A SECOND GENRE THE NEW GENRE WOULD WAKE files it into a folder the
            # account never showed it in, so the edit is not taken (U340).
            woken = _filed_by(declared, genre, truth.second_genre)
            if truth.second_genre and len(woken) > 1:
                skip(decision, SECOND_GENRE_ELSEWHERE.format(
                    filed=_folders(declared, woken),
                    shown=_folders(declared, {declared.bucket_for_display(decision.to.folder)}),
                ))
                continue
        held = sorted(pid for pid in _live_in(db, decision.content_id) if pid in tree.names)
        missing: list[str] = []
        join: list[tuple[str, str, str]] = []
        kept: list[str] = []
        if decision.outcome == edits.UNFILE:
            leave_ids = held
        else:
            moved = rebuild.Truth(
                location=str(path), genre=genre, energy=energy, voxlevel=truth.voxlevel,
                second_genre=second,
            )
            placements, _gaps = rebuild.derive_from_taxonomy(
                declared, [moved], vocal_threshold=vocal_threshold,
                carries_vox=_carries(tagged, decision.content_id),
            )
            wanted: set[str] = set()
            for placement in placements:
                names = routing_pass.destination(declared, placement.bucket, placement.sub)
                pid = tree.playlists.get(names)
                if pid is None:
                    missing.append(f"{names[0]} / {names[1]}")
                else:
                    wanted.add(pid)
            kept = _untagged_held(declared, tree, moved, placements, vocal_threshold, held) if reads_tag else []
            leave_ids = [
                pid for pid in held
                if pid not in wanted and pid not in kept and routed(tree.names[pid])
            ]
            join = [(pid, *tree.names[pid]) for pid in sorted(wanted) if pid not in held]
        changes.append(Change(
            decision.content_id, decision.track, decision.outcome, _shown(row), str(path),
            truth.genre, genre, truth.energy, energy,
            second_was=second_was,
            second=second,
            leave=tuple((pid, *tree.names[pid]) for pid in leave_ids),
            join=tuple(join),
            missing=tuple(missing),
            untagged=tuple((pid, *tree.names[pid]) for pid in kept),
            why=decision.why,
            tree=edits.GENRE,
        ))
    return changes


def _untagged_held(
    declared: Any, tree: Tree, moved: Any, placements: Sequence[Any],
    vocal_threshold: float | None, held: Sequence[str],
) -> list[str]:
    """Each held vocal sub the score places the moved track in and its tag does not.

    THE UNTAGGED STATE IS A PERSON'S TO SETTLE (R-2056): the resort keeps such a
    membership and ``converge`` names it ``untagged`` until the row is tagged
    or the track is taken out. An energy moved on the account is neither, so
    the mirror keeps it too (R-2062); it never joins one, since only the tag
    files the vocal sub. The two derivations differ only in vocal places.
    """
    from cratekit.write import rebuild, routing_pass

    scored, _gaps = rebuild.derive_from_taxonomy(declared, [moved], vocal_threshold=vocal_threshold)
    placed = set(placements)
    found = (
        tree.playlists.get(routing_pass.destination(declared, entry.bucket, entry.sub))
        for entry in scored
        if entry not in placed
    )
    return sorted(pid for pid in found if pid is not None and pid in held)


def _carries(tagged: frozenset[str], content_id: str) -> Callable[[str], bool]:
    """The vox My Tag's answer for the edit's own row, whichever file the derivation names."""
    return lambda _location: content_id in tagged


def _tagless(decision: edits.Decision, row: Any, tree: str, **rest: Any) -> Change:
    """A change of a tree whose edit writes no file tag (U204)."""
    return Change(
        decision.content_id, decision.track, decision.outcome, _shown(row), why=decision.why,
        tree=tree, **rest,
    )


def _skip_all(carried: Sequence[edits.Decision], skip: Any, why: str) -> list[Change]:
    for decision in carried:
        skip(decision, why)
    return []


def _plan_favourites(
    db: Any, declared: Any, carried: Sequence[edits.Decision], live: Any, skip: Any,
    found: dict[str, Any],
) -> list[Change]:
    """Every Favorites edit as the library takes it, against the home read on ``db`` (U204)."""
    from cratekit.favorites import colour, placeholders, placement
    from cratekit.modules.outbound import mirror_edits as edits

    try:
        home = placement.resolve_home(db, placement.source_name(declared))
    except CratekitError as exc:
        return _skip_all(
            carried, skip, f"the favourites have no home here, so nothing is written: {exc.cause.message}"
        )
    if not home.folder_id:
        return _skip_all(
            carried,
            skip,
            f"{home.source_name!r} sits at the playlist root, so there is no Favorites "
            f"folder to write and nothing is written",
        )
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
        if decision.outcome == edits.UNFAVOURITE:
            leave = [(home.source_id, folder, home.source_name)] if home.source_id in held else []
            leave += [(pid, folder, name) for name, pid in filing if pid in held]
            changes.append(_tagless(decision, row, edits.FAVORITES, leave=tuple(leave)))
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
        changes.append(_tagless(
            decision, row, edits.FAVORITES,
            join=tuple(join), leave=leave, month=month, month_id=month_id, colour=takes,
        ))
    return changes


def _plan_inbox(
    cfg: config.Config, db: Any, declared: Any, registry: Any, carried: Sequence[edits.Decision],
    live: Any, skip: Any, today: date | None,
) -> list[Change]:
    """Every INBOX edit, each batch found live directly under INBOX on ``db``; Old is never touched (U204)."""
    from cratekit.intake import rotate
    from cratekit.modules.outbound import mirror_edits as edits

    try:
        batches = rotate.live_batches(
            cfg, db, declared=declared, registry=registry, today=today or date.today()
        )
    except CratekitError as exc:
        return _skip_all(carried, skip, f"INBOX could not be read, so nothing is written: {exc.cause.message}")
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
        changes.append(_tagless(
            decision, row, edits.INBOX,
            leave=place if decision.outcome == edits.LEAVE and held else (),
            join=place if decision.outcome == edits.JOIN and not held else (),
        ))
    return changes


def _write_tags(change: Change) -> bool:
    """Write one file's tags and read them back. ``True`` when the file holds them.

    The genre and the energy, and the second genre only where it was there or
    is to be (U340), so a one genre file is written exactly as before.
    """
    from cratekit.core import tags

    path = Path(change.path)
    pairs: list[tuple[str, object]] = [("genre", change.genre), ("energylevel", change.energy)]
    if change.second_was or change.second:
        pairs.append(("secondgenre", change.second))
    written = {name: value for name, value in pairs if value is not None}
    cleared = [name for name, value in pairs if value is None]
    if written and not tags.write_tags(path, written):
        return False
    if cleared and not tags.clear_tags(path, cleared):
        return False
    return (
        (tags.read_genre_from_file(path) or None) == (change.genre or None)
        and tags.read_energy_from_file(path) == change.energy
        and (tags.read_tag(path, "secondgenre") or None) == (change.second or None)
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
            "tagged": len(self.tagged), "untagged": list(self.untagged),
            "genre_rows": self.genre_rows, "genre_skipped": list(self.genre_skipped),
            "left": self.left, "joined": self.joined, "coloured": self.coloured,
            "made": list(self.made), "session_id": self.session_id,
        }

    @property
    def wrote(self) -> bool:
        return bool(self.left or self.joined or self.genre_rows or self.coloured or self.made)


def _month_rows(placed: Any) -> dict[str, str]:
    """Each month the placement wrote, made or found, to its playlist row."""
    return {name: row for name, row, _count in placed.months} if placed is not None else {}


def write(
    cfg: config.Config, db: Any, approved: Planned, *, tree_id: str, registry: Any, intake_id: str = ""
) -> Applied:
    """Write every change in one guarded session on the write handle ``db``, and read it back.

    THE TREE'S OWN LATCH FIRST: the routing tree's for a genre edit, the intake
    tree's for an INBOX edit; the Favorites folder is nobody's tree, so for it alone
    a restore out of band is detected and marked, as ``favorites backfill`` does.
    """
    from cratekit.core import analysis_store, convergence, rb_writer, session
    from cratekit.favorites import placement
    from cratekit.modules.outbound import mirror_edits as edits
    from cratekit.organize import account_mirror
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
        record, capture = trees.attached_capture(gates, cfg, db)
        # THE FILES FIRST, each read back, and only a file that took has its row
        # written, so the database never says what the file does not.
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
            # EVERY ROW TAKING A GENRE IS ASKED, since the row may say another
            # genre than its file; the writer's policy skips one that holds it.
            genres = {one.content_id: one.genre for one in taken if one.genre}
            if genres:
                metadata.enable((metadata.RETAG_GENRE,))
                found = {cid: db.get_content(ID=cid) for cid in genres}
                rows = [row for row in found.values() if row is not None]
                retag = metadata.plan_genre_retag(rows, genres, db=db)
                metadata.assert_within_policy(retag)
                report = metadata.write_plan(retag, {str(row.ID): row for row in rows})
                done.genre_rows = len(report.written)
                done.genre_skipped = [f"{one.content_id}: {one.reason}" for one in report.skipped]
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
                    db, approved.home, [(one.content_id, one.month or None) for one in favourites],
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
            trees.rollback_quietly(db)
            if witness.landed:
                _record_commit(record, cfg, done)
            raise
        _record_commit(record, cfg, done)
        if done.wrote:
            convergence.record_fingerprint(cfg, db)
        done.session_id = record.session_id
    assert_read_back(db, taken, placed=placed, home=approved.home)
    done.taken = [(one.content_id, one.tree) for one in taken]
    # THE MEMBERSHIP EACH MONTH PLACEMENT MADE, by its time (U236), so only that
    # one is ever read as the library's; one with no readable time is not recorded.
    rows = _month_rows(placed)
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
    change = session.TreeChange(
        tree=KIND,
        created=done.joined + len(done.made),
        updated=done.left + done.genre_rows + done.coloured,
    )
    session.record_commit(record, KIND, session.ChangeSummary((change,)), cfg)


def assert_read_back(
    db: Any, written: Sequence[Change], *, placed: Any = None, home: Any = None
) -> None:
    """Refuse an answer the database does not hold: each track in and out where planned (U204)."""
    from cratekit.modules.outbound import mirror_edits as edits

    months = _month_rows(placed)
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
                origin=_ORIGIN, detail={"content_id": change.content_id, "stayed": stayed, "absent": absent},
            )


def settle(
    cfg: config.Config, decided: edits.Decided, written: Iterable[Any],
    months: Iterable[tuple[str, str, str]] = (),
) -> None:
    """Agree each edit the library took in the snapshot, so it is not read again (U201).

    ``written`` is each edit as ``(content id, tree)``, or a bare content id for a
    genre edit. ``months`` is each FAVOURITE placed in a month, ``(content id, month,
    membership time)``: for one put in All Favorites alone it is recorded as the
    library's own placement on the month's title (U236). A ledger that cannot take
    it leaves the snapshot, and the next refresh settles it.
    """
    from cratekit.modules.outbound import ledger, mirror
    from cratekit.modules.outbound import mirror_edits as edits

    took = {one if isinstance(one, tuple) else (str(one), edits.GENRE) for one in written}
    month_of = {content_id: (month, at) for content_id, month, at in months}
    carried = [one for one in decided.carried if (one.content_id, one.tree) in took]
    ledger.settle_mirror_tracks(
        cfg,
        [(folder, title, decision.track, on) for decision in carried for folder, title, on in decision.settle],
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
            origin=_ORIGIN, detail={"approved": approved.identity(), "now": now.identity()},
        )


def add_step(
    cfg: config.Config, declared: Any, registry: Any, shared: Any, *, one_read: Any = None
) -> Step:
    """The rekordbox area's step: plan on a read handle, write on its own (U201).

    A reading or tree that cannot be read refuses this step alone. ``one_read`` is
    ``--report``'s one handle (U267); the write opens its own.
    """
    from cratekit.core import rb_writer
    from cratekit.modules.outbound import mirror_edits as edits
    from cratekit.organize import account_mirror
    from cratekit.write import metadata_cli

    reading = account_mirror.reading_or_step(shared, KIND, TITLE)
    if isinstance(reading, Step):
        return reading
    decided = reading.decided
    # EVERY READ THIS STEP MAKES REFUSES THIS STEP ALONE. The calibration is read
    # only for a genre edit, the one that derives a with vox place.
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
        key=KIND, title=TITLE, state=PLANNED if writes else NOTHING, detail=detail,
        digest=digest_of(planned.identity()), counts=counts,
        items=[one.item() for one in planned.changes] + list(planned.named),
    )
    if writes:

        def apply() -> dict[str, Any]:
            handle = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
            try:
                now = plan(cfg, handle, declared, registry, decided, threshold)
                _stale(planned, now)
                done = write(
                    cfg, handle, now, tree_id=declared.tree.id, registry=registry,
                    intake_id=declared.intake.id,
                )
            finally:
                rb_writer.close_db(handle)
            settle(cfg, decided, done.taken, done.months)
            if done.untagged:
                step.warnings.append({
                    "code": "organize-mirror-edits-untagged",
                    "message": f"{len(done.untagged)} file(s) did not take their new tags, so "
                    f"their rows were not written: " + "; ".join(done.untagged),
                })
            return done.totals()

        step.apply = apply
    return step


def deletes(planned_items: Iterable[Mapping[str, Any]]) -> list[str]:
    """Every membership the step takes away, one gate line per track."""
    from cratekit.modules.outbound import mirror_edits as edits

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
    "KIND", "TITLE", "WORKFLOW", "Applied", "Change", "Planned", "Tree", "add_step",
    "assert_read_back", "deletes", "places", "plan", "read_tree", "settle", "target_tags", "write",
]
