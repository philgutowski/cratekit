"""The steps :func:`cratekit.intake.native.apply_rows` runs, and the read back after its commit.

Every name here is reached through :mod:`cratekit.intake.native` as well.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from cratekit.adopt import placements as adopt_placements
from cratekit.core import config, convergence, rb_writer, tree_registry
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.intake.native import (
    _ORIGIN,
    ALBUM_ARTIST,
    ALBUM_COLUMN,
    ANALYZE,
    ARTIST_COLUMN,
    DYN_CATEGORY,
    DYN_VALUE,
    GENRE_COLUMN,
    LANDED_COLUMNS,
    LANDED_UUID_KEY,
    LEFT_EMPTY,
    MINTED,
    YEAR_COLUMN,
    NativePlan,
    RowPlan,
    Word,
    logger,
)
from cratekit.intake.native_plan import _lookup_class, _Resolver, anchored_intake_root
from cratekit.intake.native_read import analyze_playlist, content_ids_for, dyn_marked
from cratekit.write import metadata_cli


def _read_back(db: Any, content_id: str) -> tuple[dict[str, Any], str, str, str, int | None]:
    """The analysis columns, title, path, file id and link of one row, from SQL after the commit."""
    from sqlalchemy import text

    selected = ", ".join(LEFT_EMPTY)
    row = db.session.execute(
        text(
            f"SELECT Title, FolderPath, {rb_writer.FILE_ID_COLUMN}, "
            f"{rb_writer.CONTENT_LINK_COLUMN}, {selected} "
            f"FROM djmdContent WHERE ID = :id"
        ),
        {"id": content_id},
    ).first()
    if row is None:
        raise refuse(
            "internal-error",
            f"the content row {content_id!r} was committed and could not be read "
            f"back, so the landing cannot say what it holds",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"content_id": content_id},
        )
    values = dict(zip(LEFT_EMPTY, row[4:]))
    return (
        values,
        str(row[0] or ""),
        str(row[1] or ""),
        str(row[2] or ""),
        None if row[3] is None else int(row[3]),
    )


def _words_back(db: Any, content_id: str) -> dict[str, Any]:
    """One row's artist, album, album artist, genre and year, from SQL after the commit (U163).

    THROUGH ACTIVE LOOKUP ROWS ONLY, so a row linked to a tombstone reads as
    carrying no word, which is what rekordbox shows for it.
    """
    from sqlalchemy import text

    active = f"{rb_writer.SOFT_DELETE_COLUMN} = 0"
    row = db.session.execute(
        text(
            f"SELECT a.Name, al.Name, aa.Name, g.Name, c.{YEAR_COLUMN} "
            f"FROM {rb_writer.CONTENT_TABLE} c "
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} a ON a.ID = c.{ARTIST_COLUMN} AND a.{active} "
            f"LEFT JOIN {rb_writer.ALBUM_TABLE} al ON al.ID = c.{ALBUM_COLUMN} AND al.{active} "
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} aa ON aa.ID = al.{ALBUM_ARTIST} AND aa.{active} "
            f"LEFT JOIN {rb_writer.GENRE_TABLE} g ON g.ID = c.{GENRE_COLUMN} AND g.{active} "
            f"WHERE c.ID = :id"
        ),
        {"id": content_id},
    ).first()
    if row is None:
        return {}
    return {
        ARTIST_COLUMN: str(row[0] or ""),
        ALBUM_COLUMN: str(row[1] or ""),
        ALBUM_ARTIST: str(row[2] or ""),
        GENRE_COLUMN: str(row[3] or ""),
        YEAR_COLUMN: int(row[4]) if row[4] else None,
    }


def _resolved_now(resolver: _Resolver, word: Word) -> Word | None:
    """``word`` resolved again on the apply's handle, by the plan's own rule."""
    if word.table == rb_writer.ALBUM_TABLE:
        artist = (
            resolver.word(rb_writer.ARTIST_TABLE, word.album_artist.name)
            if word.album_artist is not None
            else None
        )
        return resolver.album(word.name, artist)
    return resolver.word(word.table, word.name)


def _rows_of(word: Word | None) -> tuple[str, str]:
    """The rows a word takes, its own and an album's artist, empty for a mint."""
    if word is None:
        return ("", "")
    artist = word.album_artist.row_id if word.album_artist is not None else ""
    return (word.row_id, artist)


def _assert_words_unmoved(db: Any, rows: Sequence[RowPlan]) -> None:
    """Refuse when a word resolves to another row now than the plan found (U163).

    The plan is what was approved and is not rebuilt: a lookup row minted,
    retired or renamed since changes what the screen showed.
    """
    resolver = _Resolver(db)
    moved = []
    for row in rows:
        for word in (row.artist, row.album, row.genre):
            if word is None:
                continue
            now = _resolved_now(resolver, word)
            if _rows_of(now) != _rows_of(word):
                moved.append(
                    f"{row.target.name}: {word.table} {word.name!r} was "
                    f"{word.row_id or MINTED} and is {(now.row_id if now else '') or MINTED}"
                )
    if moved:
        raise refuse(
            "decision-stale",
            "a word a row would carry resolves to another lookup row than the plan "
            "found, so nothing was written; plan the landing again: " + "; ".join(moved),
            origin=_ORIGIN,
            detail={"moved": moved},
        )


class _Mints:
    """The lookup rows one commit mints, each once per word, and the links to them (U163).

    BY HAND, NOT THROUGH ``add_artist`` AND KIN, which refuse a name even a
    tombstone holds. MINTED AND LINKED IN ONE COMMIT, because rekordbox
    garbage collects a lookup row nothing references (A4).
    """

    def __init__(self, db: Any) -> None:
        self._db = db
        self._made: dict[tuple[str, str, str], str] = {}

    def tables(self) -> tuple[str, ...]:
        """The lookup tables this commit minted a row in, to name in ``creations``."""
        return tuple(sorted({table for table, _name, _artist in self._made}))

    def link(self, content: Any, row: RowPlan) -> None:
        """Link the content row to each of its words' rows, minting a word's once, and write its year."""
        for column, word in row.linked():
            if word is not None:
                setattr(content, column, self.id_of(word))
        if row.year is not None:
            setattr(content, YEAR_COLUMN, row.year)

    def id_of(self, word: Word) -> str:
        """The row ``word`` links: the plan's active row, or the one this commit minted for it."""
        if word.row_id:
            return word.row_id
        key = word.key()
        if key not in self._made:
            self._made[key] = self._mint(word)
        return self._made[key]

    def _mint(self, word: Word) -> str:
        from uuid import uuid4

        kind = _lookup_class(word.table)
        # TEXT, AS THE STORED ROWS ARE (U153): the binding mints an int.
        columns: dict[str, Any] = {
            "ID": str(self._db.generate_unused_id(kind)),
            "Name": word.name,
            "UUID": str(uuid4()),
        }
        if word.table != rb_writer.GENRE_TABLE:
            columns["SearchStr"] = word.search
        if word.table == rb_writer.ALBUM_TABLE:
            columns[ALBUM_ARTIST] = (
                self.id_of(word.album_artist) if word.album_artist is not None else None
            )
        made = kind.create(**columns)
        self._db.add(made)
        # FLUSHED AT ONCE, so the next mint's unused id is drawn against this one.
        self._db.flush()
        return str(made.ID)


def _taken_since_the_plan(db: Any, cfg: config.Config, rows: Sequence[RowPlan]) -> dict[str, str]:
    """Each planned target a row has taken since the plan was made, by target.

    The one question the apply asks again, since its answer can change under
    an approval: a row that appeared is counted present rather than doubled.
    Asked before the first row is added, so the read flushes nothing pending.
    """
    return content_ids_for(db, cfg, [row.target for row in rows])


def _tag_vox(db: Any, added: Sequence[tuple[RowPlan, str]]) -> int:
    """Give each added row the plan tagged the vox My Tag (U127). Answers how many were written."""
    content_ids = [content_id for row, content_id in added if row.vox]
    return _tag(db, content_ids, metadata_cli.CATEGORY, metadata_cli.VALUE_VOX)


def _tag_dyn(db: Any, added: Sequence[tuple[RowPlan, str]]) -> int:
    """Give each added row the plan tagged the dyn My Tag (U157). Answers how many were written."""
    return _tag(db, [content_id for row, content_id in added if row.dyn], DYN_CATEGORY, DYN_VALUE)


def _tag(db: Any, content_ids: Sequence[str], category: str, name: str) -> int:
    """Give each row the My Tag ``name`` under ``category``, pending on the landing's handle.

    THE VOCALS VERB'S OWN WRITER, so the category and value are found or made
    as ``metadata mytags-vocals`` makes them and an association there is kept.
    """
    if not content_ids:
        return 0
    value = rb_writer.ensure_my_tag_value(db, category, name)
    return sum(1 for content_id in content_ids if rb_writer.add_my_tag(db, value, content_id))


def _dyn_read_back(db: Any) -> tuple[frozenset[str], str]:
    """Every row carrying the dyn My Tag as the check reads it, after the commit (U157).

    A refusal is the answer's reason, not a failure: the commit has landed.
    """
    try:
        return dyn_marked(db), ""
    except CratekitError as exc:
        return frozenset(), exc.cause.message


def _vox_read_back(db: Any) -> tuple[frozenset[str], str]:
    """Every row carrying the vox My Tag as adoption reads it, after the commit (U127).

    ADOPTION'S OWN READER, since the promise is that the next ``adopt apply``
    files the row. A refusal is the answer's reason, not a failure: the
    commit has landed.
    """
    try:
        tagged = adopt_placements.vox_tagged(db)
    except CratekitError as exc:
        return frozenset(), exc.cause.message
    return tagged or frozenset(), ""


def _batch_playlist_row(db: Any, plan: NativePlan, anchor: Any) -> Any:
    """The INBOX playlist the batch members go in: the recorded one, else found or made.

    THE RECORDED PLAYLIST of a set landing (U135) is checked live again. A
    removed playlist is never found: rekordbox soft deletes one a person
    removes, and memberships written into it are seen by nobody.
    """
    if plan.batch_playlist_id:
        row = db.get_playlist(ID=plan.batch_playlist_id)
        if row is None or rb_writer.is_folder(row) or rb_writer.node_removed(row):
            raise refuse(
                "decision-stale",
                f"the INBOX playlist {plan.playlist!r} (row {plan.batch_playlist_id}) "
                f"the plan adds to is not live any more, so nothing was written",
                origin=_ORIGIN,
                detail={"playlist": plan.batch_playlist_id, "name": plan.playlist},
            )
        return row
    parent_id = str(anchor.ID)
    for row in list(db.get_playlist(Name=plan.playlist)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
            return row
    return db.create_playlist(plan.playlist, parent=anchor)


def _analyze_row(db: Any, plan: NativePlan, anchor: Any) -> Any:
    """The :data:`ANALYZE` playlist the added rows join: found live under the root, else made.

    FOUND AGAIN AT THE WRITE, so one another landing made since is joined,
    never made twice, and one removed since is not written into.
    """
    del plan
    found = analyze_playlist(db, str(anchor.ID))
    return found if found is not None else db.create_playlist(ANALYZE, parent=anchor)


def _plain(value: Any) -> Any:
    return value if value is None or isinstance(value, (int, float)) else str(value)


def _landed_rows(
    db: Any,
    plan: NativePlan,
    added_ids: Sequence[tuple[RowPlan, str]],
    joined: Iterable[str],
    *,
    before: frozenset[str],
) -> dict[str, Any] | None:
    """What :data:`LANDED_ROWS_KEY` records of a committed landing, read back from the database.

    THE ROWS AS THE DATABASE HOLDS THEM after the commit, with the update
    count it left, each row's UUID (R-1844), and the playlists of ``joined``
    this landing MADE, those not in ``before``: no database from before the
    landing holds one, which tells a removal from a rollback.

    A READ THAT FAILS RECORDS NOTHING and says so: the landing has committed,
    and a record naming no row only keeps the files.
    """
    if not added_ids:
        return None
    try:
        rows = []
        for _row, content_id in added_ids:
            content = db.get_content(ID=content_id)
            if content is None:
                raise LookupError(f"the row {content_id!r} could not be read back")
            rows.append(
                {
                    "content_id": str(content_id),
                    "columns": {name: _plain(getattr(content, name, None)) for name in LANDED_COLUMNS},
                    LANDED_UUID_KEY: str(getattr(content, "UUID", None) or ""),
                }
            )
        sequence = int(db.get_local_usn())
    except Exception as exc:  # noqa: BLE001 - any read failure records nothing
        logger.warning(
            "the rows this landing made could not be read back for its record (%s), so "
            "the deletion pass will not offer their files if they are removed in rekordbox",
            exc,
        )
        return None
    playlists = sorted({str(one) for one in joined if one and str(one) not in before})
    return {
        "database_identity": plan.master_db_id,
        "sequence": sequence,
        "playlists": playlists,
        "rows": rows,
    }


def _assert_unchanged(
    cfg: config.Config, db: Any, plan: NativePlan, analysis_roots: Iterable[Path | str]
) -> list[Path]:
    """The roots to watch, once the intake tree is still anchored where the plan found it.

    ``analysis_roots`` has no default: a watch that watches nothing reports
    every session clean.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    registry = tree_registry.read(cfg)
    root_id = anchored_intake_root(db, plan.tree_id, registry)
    if root_id != plan.root_id:
        raise refuse(
            "decision-stale",
            f"the intake tree {plan.tree_id!r} is anchored to root {root_id!r} and the "
            f"plan was made against {plan.root_id!r}, so nothing was written",
            origin=_ORIGIN,
            detail={"planned": plan.root_id, "anchored": root_id},
        )
    convergence.assert_tree_writable(cfg, db, plan.tree_id, registry)
    return watched


def _batch_order(plan: NativePlan, by_target: Mapping[str, str], claimed: set[str]) -> list[str]:
    """The batch playlist's rows, each once: what no account playlist claimed, in the plan's order.

    IN SET ORDER FIRST FOR A SET LANDING (U135), so both landings' rows read in
    set order on the joined INBOX playlist; the set's members carry positions
    and landing files alone sort by name.
    """
    members = plan.set_playlist.members if plan.set_playlist is not None else ()
    targets = [str(member.target) for member in members if member.target]
    targets += [str(row.target) for row in plan.rows]
    return list(
        dict.fromkeys(by_target[one] for one in targets if one in by_target and one not in claimed)
    )
