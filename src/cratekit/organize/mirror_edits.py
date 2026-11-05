"""An edit made on the account to a mirrored genre playlist, taken into the library (U201).

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

THE SNAPSHOT TAKES EACH EDIT THE LIBRARY TOOK (:func:`settle`), once the commit
landed, so the next refresh reads the track as agreed, and a move made in
rekordbox after it is rekordbox's to carry to the account.

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
from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import CratekitError, refuse
from cratekit.modules.outbound import mirror_edits as edits
from cratekit.organize.steps import LISTED, NOTHING, PLANNED, Step, refused

#: The step kind ``--only`` names this by.
KIND = "mirror-edits"

TITLE = "take each edit made on the account to a mirrored genre playlist into the library"

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
    """Each genre playlist's place by its account title, band or additive.

    A folder whose name is no bucket's display, a playlist whose title does not
    start with its folder's name, and a playlist routing never files a track
    into (the genre Favorites among them) have no place: their tracks are read
    as before U201, every difference rekordbox's.
    """
    found: dict[str, edits.Place] = {}
    for folder in folders:
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
        ]

    def item(self) -> dict[str, Any]:
        shown: dict[str, Any] = {
            "track": self.shown,
            "content_id": self.content_id,
            "edit": self.outcome,
            "genre": [self.genre_was, self.genre],
            "energy": [self.energy_was, self.energy],
            "leaves": [f"{folder} / {playlist}" for _pid, folder, playlist in self.leave],
            "joins": [f"{folder} / {playlist}" for _pid, folder, playlist in self.join],
            "why": self.why,
        }
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

    def counts(self) -> dict[str, int]:
        return {
            "move": sum(1 for one in self.changes if one.outcome == edits.MOVE),
            "folder": sum(1 for one in self.changes if one.outcome == edits.FOLDER),
            "unfile": sum(1 for one in self.changes if one.outcome == edits.UNFILE),
            "named": len(self.named),
        }


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
) -> Planned:
    """Every carried edit as the library takes it, read on ``db``. Reads only.

    Raises the refusal of the routing tree or of the derivation.
    """
    from cratekit.write import playlist_pair, rebuild, routing_pass

    named: list[dict[str, Any]] = [
        one.item() for one in decided.decisions if one.outcome not in edits.CARRIED
    ]
    carried = decided.carried
    if not carried:
        return Planned(named=tuple(named))
    tree = read_tree(db, declared, registry)
    routed = _routed(declared)
    rows = playlist_pair.content(db, [one.content_id for one in carried])
    changes: list[Change] = []
    for decision in carried:

        def skip(why: str, decision: edits.Decision = decision) -> None:
            named.append({**decision.item(), "outcome": "not taken", "why": f"{decision.why}; {why}"})

        row = rows.get(decision.content_id)
        if row is None:
            skip("its library row is no longer a live row of the collection, so nothing is written")
            continue
        shown = f"{row.artist} - {row.title}" if row.artist else row.title
        path = _resolve(cfg, row.path)
        if path is None:
            skip("its file could not be found, so neither its tags nor its row is written")
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
                    f"no genre and energy routing reads files it into {decision.to.title}, "
                    f"so nothing is written"
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
                shown=shown,
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
    return Planned(changes=tuple(changes), named=tuple(named))


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

    def totals(self) -> dict[str, Any]:
        return {
            "tagged": len(self.tagged),
            "untagged": list(self.untagged),
            "genre_rows": self.genre_rows,
            "genre_skipped": list(self.genre_skipped),
            "left": self.left,
            "joined": self.joined,
            "session_id": self.session_id,
        }


def write(cfg: config.Config, db: Any, approved: Planned) -> Applied:
    """Write every change in one guarded session on the write handle ``db``, and read it back."""
    from cratekit.core import analysis_store, convergence, rb_writer, session, snapshot
    from cratekit.write import metadata, trees

    done = Applied()
    watched = list(analysis_store.watch_roots(cfg))
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
        # row written, so the database never says what the file does not.
        taken: list[Change] = []
        for change in approved.changes:
            if _write_tags(change):
                taken.append(change)
                done.tagged.append(change.content_id)
            else:
                done.untagged.append(f"{change.shown} ({change.path})")
        try:
            genres = {
                one.content_id: one.genre
                for one in taken
                if one.genre and one.genre != one.genre_was
            }
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
            for change in taken:
                for pid, _folder, _playlist in change.leave:
                    done.left += len(
                        rb_writer.remove_memberships(db, db.get_playlist(ID=pid), [change.content_id])
                    )
                for pid, _folder, _playlist in change.join:
                    done.joined += len(
                        rb_writer.add_memberships(db, db.get_playlist(ID=pid), [change.content_id])
                    )
            db.session.flush()
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
        except BaseException:
            trees._rollback_quietly(db)
            if witness.landed:
                _record_commit(record, cfg, done)
            raise
        _record_commit(record, cfg, done)
        if done.left or done.joined or done.genre_rows:
            convergence.record_fingerprint(cfg, db)
        done.session_id = record.session_id
    assert_read_back(db, taken)
    return done


def _record_commit(record: Any, cfg: config.Config, done: Applied) -> None:
    from cratekit.core import session

    if not (done.left or done.joined or done.genre_rows):
        return
    session.record_commit(
        record,
        KIND,
        session.ChangeSummary(
            (
                session.TreeChange(
                    tree=KIND, created=done.joined, updated=done.left + done.genre_rows
                ),
            )
        ),
        cfg,
    )


def assert_read_back(db: Any, written: Sequence[Change]) -> None:
    """Refuse an answer the database does not hold: each track in and out where planned."""
    from sqlalchemy import text

    from cratekit.core import rb_writer

    for change in written:
        found = {
            str(one[0])
            for one in db.session.execute(
                text(
                    f"SELECT PlaylistID FROM {rb_writer.MEMBERSHIP_TABLE} WHERE ContentID = :id "
                    f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0"
                ),
                {"id": change.content_id},
            ).fetchall()
        }
        stayed = [pid for pid, _f, _p in change.leave if pid in found]
        absent = [pid for pid, _f, _p in change.join if pid not in found]
        if stayed or absent:
            raise refuse(
                "session-committed-unverified",
                f"{change.shown} read back from the database is still in {len(stayed)} "
                f"playlist(s) it was to leave and missing from {len(absent)} it was to "
                f"join; the commit landed and this answer cannot be vouched for",
                origin=_ORIGIN,
                detail={"content_id": change.content_id, "stayed": stayed, "absent": absent},
            )


def settle(cfg: config.Config, decided: edits.Decided, written: Iterable[str]) -> None:
    """Agree each edit the library took in the snapshot, so it is not read again (U201).

    Recorded after the commit and before the mirror's own apply, whose record
    keeps this word for a track it holds. A ledger that cannot take it leaves
    the snapshot as it was: the next refresh reads both sides agreeing on the
    track and settles it then, writing nothing.
    """
    from cratekit.modules.outbound import ledger

    took = set(written)
    ledger.settle_mirror_tracks(
        cfg,
        [
            (folder, title, decision.track, on)
            for decision in decided.carried
            if decision.content_id in took
            for folder, title, on in decision.settle
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


def add_step(cfg: config.Config, declared: Any, registry: Any, shared: Any) -> Step:
    """The rekordbox area's step: plan on a read handle, write on its own (U201).

    ``shared`` is the organize run's one mirror reading. A reading or a tree
    that cannot be read refuses this step alone.
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
    threshold = metadata_cli.load_vocal_threshold(cfg)
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        planned = plan(cfg, db, declared, registry, decided, threshold)
    except CratekitError as exc:
        return refused(KIND, TITLE, exc.cause)
    finally:
        rb_writer.close_db(db)
    counts = planned.counts()
    writes = bool(planned.changes)
    detail = (
        f"{counts['move']} track(s) moved, {counts['folder']} given another genre and "
        f"{counts['unfile']} unfiled as edited on the account; {counts['named']} edit(s) "
        f"named and not taken"
        if writes or planned.named
        else "no genre playlist was changed on the account since the mirror last finished it"
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
                _stale(planned, plan(cfg, handle, declared, registry, decided, threshold))
                done = write(cfg, handle, planned)
            finally:
                rb_writer.close_db(handle)
            settle(cfg, decided, done.tagged)
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
    return [
        f"{one['track']} leaves {', '.join(one['leaves'])}"
        + (", and its genre and energy tags are cleared" if one.get("edit") == edits.UNFILE else "")
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
