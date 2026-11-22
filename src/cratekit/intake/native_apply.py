"""The apply half of a native landing: the plan written in one guarded commit, and recorded.

Imported through :mod:`cratekit.intake.native`, which re-exports every name here.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Mapping, Sequence

from cratekit.adopt import placements as adopt_placements
from cratekit.core import config, convergence, drift, rb_writer, session, tree_registry
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.favorites import placement
from cratekit.intake import ingest, label_filing, native, set_playlist
from cratekit.intake.native import (
    _ORIGIN,
    ALBUM_ARTIST,
    ALBUM_COLUMN,
    ANALYZE,
    ARTIST_COLUMN,
    BATCH_PLAYLIST_KEY,
    DYN_CATEGORY,
    DYN_CHANGE_KEY,
    DYN_VALUE,
    FILED_BATCH_KEY,
    GENRE_COLUMN,
    INBOX_JOB_KEY,
    INBOX_PLAYLISTS_KEY,
    LANDED_COLUMNS,
    LANDED_ROWS_KEY,
    LANDED_UUID_KEY,
    LEFT_EMPTY,
    MINTED,
    NOT_LANDED,
    PASS_KEY,
    PRESENT,
    WORKFLOW,
    YEAR_COLUMN,
    AddedRow,
    NativeLanded,
    NativePlan,
    RowPlan,
    Word,
    WrittenPlaylist,
    analyze_playlist,
    assert_names_still_free,
    content_ids_for,
    dyn_marked,
    logger,
)
from cratekit.intake.native_plan import _lookup_class, _Resolver, anchored_intake_root
from cratekit.write import metadata_cli, trees

if TYPE_CHECKING:
    from cratekit.intake.account_playlists import Left

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

    The plan is what was approved and it is not rebuilt. A lookup row minted,
    retired or renamed since then changes which row a word links or whether
    it is minted, which the screen showed, so the answer is stale for it.
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

    BY HAND, NOT THROUGH THE BINDING'S ``add_artist`` AND KIN, which refuse a
    name any row holds, a tombstone included, and so would refuse exactly the
    word whose only namesake rekordbox retired. MINTED AND LINKED IN ONE
    COMMIT, because rekordbox garbage collects a lookup row nothing references
    (A4): a mint is pending on the landing's handle beside the row that links
    it, and a refusal rolls both back.
    """

    def __init__(self, db: Any) -> None:
        self._db = db
        self._made: dict[tuple[str, str, str], str] = {}

    def tables(self) -> tuple[str, ...]:
        """The lookup tables this commit minted a row in, to name in ``creations``."""
        return tuple(sorted({table for table, _name, _artist in self._made}))

    def link(self, content: Any, row: RowPlan) -> None:
        """Link the content row to each of its words' rows, minting a word's once, and write its year."""
        for column, word in (
            (ARTIST_COLUMN, row.artist),
            (ALBUM_COLUMN, row.album),
            (GENRE_COLUMN, row.genre),
        ):
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
        # FLUSHED AT ONCE, as the binding's own writers flush, so the next
        # mint's unused id is drawn against this one.
        self._db.flush()
        return str(made.ID)

def _taken_since_the_plan(db: Any, cfg: config.Config, rows: Sequence[RowPlan]) -> dict[str, str]:
    """Each planned target a row has taken since the plan was made, by target.

    The plan is what was approved and it is not rebuilt, so the one thing the
    apply asks the database again is the question whose answer can change
    under an approval: whether the file is in the collection now. A row that
    appeared is counted present rather than doubled. Asked before the first
    row is added, so nothing pending is flushed by the read, and asked of the
    candidate rows rather than the whole collection.
    """
    return content_ids_for(db, cfg, [row.target for row in rows])


def apply_rows(
    cfg: config.Config,
    db: Any,
    plan: NativePlan,
    *,
    analysis_roots: Iterable[Path | str],
) -> NativeLanded:
    """Write the plan: the rows, the playlist under the root, the memberships.

    THE SESSION SPINE IS CALLED, NOT REBUILT, and it is the one the membership
    writers use: the three gates in their argued order with a record kept, a
    capture the commit happens behind, the analysis watch over the roots named,
    the commit witness, and the guarded commit. The one thing this commit says
    that no other does is ``creations``, which names the content table and
    admits the rows the whitelist would otherwise refuse (R-760).

    ALL OR NOTHING IN THE DATABASE. Every row and every membership is pending on
    one handle until one commit, and a refusal anywhere before it rolls the
    handle back, so a failure on the second of three files leaves the table as
    it was. The files are in the library by then, which the caller reports.

    ``analysis_roots`` has no default for the reason the membership writer
    gives: a watch that watches nothing reports every session clean.
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

    added_ids: list[tuple[RowPlan, str]] = []
    present: list[RowPlan] = list(plan.present())
    memberships = 0
    vox_written = 0
    dyn_written = 0
    analyze_id = ""
    analyze_added = 0
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record, capture = trees.attached_capture(gates, cfg, db)

        anchor = db.get_playlist(ID=plan.root_id)
        if anchor is None:
            raise tree_registry.RegistrySkew(
                f"the adopted intake root {plan.root_id!r} was reported present and "
                f"could not be read back, so the batch playlist has nothing to hang "
                f"from and would be created beside the tree instead",
                tree_id=plan.tree_id,
                root_id=plan.root_id,
            )
        playlist_id = ""
        # EVERY PLAYLIST ROW BEFORE THIS LANDING WRITES ONE (R-1037), so its
        # record names only the playlists it MADE: a rollback to before the
        # landing cannot hold one of those, and a removal leaves them.
        playlists_before = frozenset(str(row.ID) for row in db.get_playlist())
        written: list[WrittenPlaylist] = []
        left: list[tuple[str, Left]] = [
            *plan.unplanned_left,
            *((one.name, row) for one in plan.playlists for row in one.left),
        ]
        placed: placement.Placed | None = None
        set_written: set_playlist.Written | None = None
        labels_written: label_filing.Written | None = None
        twins_written: tuple[Any, ...] = ()
        try:
            # BEFORE THE FIRST ROW, so a refusal adds nothing. A name the plan
            # chose free that INBOX holds now would show two playlists of one
            # name, and an account playlist is created rather than found.
            assert_names_still_free(db, plan)
            if plan.twins:
                from cratekit.sync import twins as twin_mod

                twin_mod.recheck_landing(db, plan.twins)
            to_add = plan.to_add()
            taken = _taken_since_the_plan(db, cfg, to_add)
            # THE WORDS ARE ASKED AGAIN BEFORE THE FIRST ROW (U163), as the
            # targets are, so a lookup row made or retired since the approval
            # refuses rather than linking what nobody approved.
            _assert_words_unmoved(db, [row for row in to_add if str(row.target) not in taken])
            mints = _Mints(db)
            for row in to_add:
                held = taken.get(str(row.target))
                if held is not None:
                    present.append(replace(row, action=PRESENT, content_id=held))
                    continue
                content = db.add_content(row.target, Title=row.title)
                native._restamp(content, row, plan)
                mints.link(content, row)
                added_ids.append((row, str(content.ID)))
            # THE VOX MY TAG, IN THE SAME COMMIT (U127), on the rows this
            # landing made and only those the plan tagged. Additive: the writer
            # adds an association it does not find and removes none.
            vox_written = _tag_vox(db, added_ids)
            # THE DYN MY TAG, IN THE SAME COMMIT (U157), on the rows this
            # landing made whose drift read as variable, the same writer.
            dyn_written = _tag_dyn(db, added_ids)
            # In listing order: the files the plan named, in the order it named
            # them, whether the row is new or was already there.
            by_target = {str(row.target): content_id for row, content_id in added_ids}
            by_target.update({str(row.target): row.content_id for row in present if row.content_id})
            claimed = {str(target) for one in plan.playlists for target in one.targets}
            # IN THE ACCOUNT PLAYLIST'S ORDER (U128), a new row by its target and
            # an owned row by the id the plan found for it. A member whose file
            # made no row is left, and named, rather than silently absent.
            accounts = []
            for one in plan.playlists:
                ids: list[str] = []
                for member in one.members:
                    held = (
                        member.content_id
                        if member.target is None
                        else by_target.get(str(member.target), "")
                    )
                    if held:
                        ids.append(held)
                    elif member.member is not None:
                        left.append((one.name, member.member.left(NOT_LANDED)))
                if ids:
                    accounts.append((one, ids))
            # IN SET ORDER WHEN THIS IS A SET LANDING (U135): the brief asks
            # for both landings' rows in set order on the joined INBOX playlist.
            # Landing files alone sort by name; the set's members carry positions.
            if plan.set_playlist is not None:
                ordered = []
                seen: set[str] = set()
                for member in plan.set_playlist.members:
                    target = str(member.target) if member.target else ""
                    if not target or target not in by_target or target in claimed:
                        continue
                    held = by_target[target]
                    if held in seen:
                        continue
                    ordered.append(held)
                    seen.add(held)
                for row in plan.rows:
                    target = str(row.target)
                    if target not in by_target or target in claimed:
                        continue
                    held = by_target[target]
                    if held in seen:
                        continue
                    ordered.append(held)
                    seen.add(held)
            else:
                ordered = [
                    by_target[str(row.target)]
                    for row in plan.rows
                    if str(row.target) in by_target and str(row.target) not in claimed
                ]
            # THE BATCH PLAYLIST HOLDS WHAT NO ACCOUNT PLAYLIST CLAIMED, and is
            # not written when that is nothing, as the intake file does it.
            # A SET LANDING ADDS TO THE RECORDED INBOX PLAYLIST (U135) when an
            # earlier landing of the same job left one live under the root.
            if ordered or not accounts:
                playlist = _batch_playlist_row(db, plan, anchor)
                memberships = len(rb_writer.add_memberships(db, playlist, ordered))
                playlist_id = str(playlist.ID)
            for one, ids in accounts:
                created = db.create_playlist(one.name, parent=anchor)
                count = len(rb_writer.add_memberships(db, created, ids))
                memberships += count
                written.append(
                    WrittenPlaylist(
                        name=one.name,
                        playlist_id=str(created.ID),
                        account=one.account,
                        tracks=count,
                    )
                )
            # EACH ACCOUNT PLAYLIST'S TWIN, IN THE SAME COMMIT (U149): the rows
            # its INBOX playlist was given, under Custom Playlists <year>, the
            # copy that stays when the INBOX one rotates out.
            if plan.twins:
                from cratekit.sync import twins as twin_mod

                twins_written = twin_mod.write_landing(
                    db, plan.twins, {one.account: ids for one, ids in accounts}
                )
            # EVERY ROW THIS LANDING MADE JOINS ANALYZE (U166), in the same
            # commit and in the plan's order, so the visit selects one playlist.
            # A row already held is not added: rekordbox has had it.
            if added_ids:
                analyze = _analyze_row(db, plan, anchor)
                analyze_id = str(analyze.ID)
                analyze_added = len(
                    rb_writer.add_memberships(
                        db, analyze, [content_id for _row, content_id in added_ids]
                    )
                )
            # THE HEARTS, IN THE SAME COMMIT (U120): into All Favorites and
            # each one's month, a row already present as much as a row
            # added, so a heart landed twice is one membership. And the
            # pass's owned hearts All Favorites lacked (U146), by their rows.
            if plan.favorites is not None and (plan.favorites.items or plan.favorites.owned):
                pairs: list[tuple[str, str | None]] = [
                    (by_target[str(item.target)], item.month)
                    for item in plan.favorites.items
                    if str(item.target) in by_target
                ]
                pairs.extend((one.content_id, one.month) for one in plan.favorites.owned)
                # AND PINK ON EACH (U153): every row this landing made for a
                # heart, which carries no colour by construction, and the
                # owned hearts the plan read as uncoloured.
                to_colour = [
                    by_target[str(item.target)]
                    for item in plan.favorites.items
                    if str(item.target) in by_target
                ]
                to_colour.extend(plan.favorites.colour)
                placed = placement.place(
                    db,
                    plan.favorites.home(),
                    pairs,
                    pink=plan.favorites.pink,
                    to_colour=to_colour,
                    held=plan.favorites.held,
                    colour_skipped=plan.favorites.colour_skipped,
                )
            # THE SET'S PERMANENT PLAYLIST, IN THE SAME COMMIT (U121): the rows
            # this landing made are keyed by target, and a member the landing
            # could not make a row for is left and listed, never guessed.
            if plan.set_playlist is not None:
                set_written = set_playlist.write_members(db, plan.set_playlist, by_target=by_target)
            # THE LABEL FILING, IN THE SAME COMMIT (U156): appended under the
            # Record Labels tree by target, a member whose file made no row
            # left and named, nothing found there removed.
            if plan.labels is not None:
                labels_written = label_filing.write(db, plan.labels, by_target=by_target)
            # THE LOOKUP TABLES ONLY WHEN A WORD WAS MINTED (U163), so a
            # landing that links every word admits what it did before.
            rb_writer.commit_guarded(
                db, creations=(rb_writer.CONTENT_TABLE, *mints.tables())
            )
        except BaseException:
            trees.rollback_quietly(db)
            if witness.landed:
                _record_landing_commit(
                    record,
                    plan,
                    len(added_ids),
                    memberships + analyze_added,
                    cfg,
                    landed=_landed_rows(
                        db, plan, added_ids, (playlist_id, *(one.playlist_id for one in written)),
                        before=playlists_before,
                    ),
                    playlist_id=playlist_id,
                    written=written,
                    placed=placed,
                    set_written=set_written,
                    vox_written=vox_written,
                    dyn_written=dyn_written,
                    labels_written=labels_written,
                    twins_written=twins_written,
                )
            raise

        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships + analyze_added,
            cfg,
            landed=_landed_rows(
                db, plan, added_ids, (playlist_id, *(one.playlist_id for one in written)),
                before=playlists_before,
            ),
            playlist_id=playlist_id,
            written=written,
            placed=placed,
            set_written=set_written,
            vox_written=vox_written,
            dyn_written=dyn_written,
            labels_written=labels_written,
            twins_written=twins_written,
        )
        convergence.record_fingerprint(cfg, db)
        if set_written is not None and set_written.playlist_id:
            set_written = replace(
                set_written, read_back=set_playlist.read_back(db, set_written.playlist_id)
            )
        if labels_written is not None:
            labels_written = label_filing.read_back(db, labels_written)

        landed = []
        # ONLY WHEN A TAG WAS PLANNED: a row this landing just made carries no
        # tag it did not write, so there is nothing else to read back.
        voxed, vox_unread = (
            _vox_read_back(db) if any(row.vox for row, _ in added_ids) else (frozenset(), "")
        )
        dyned, dyn_unread = (
            _dyn_read_back(db) if any(row.dyn for row, _ in added_ids) else (frozenset(), "")
        )
        for row, content_id in added_ids:
            values, title, folder_path, file_id, link = _read_back(db, content_id)
            landed.append(
                AddedRow(
                    target=row.target,
                    content_id=content_id,
                    title=title,
                    folder_path=folder_path,
                    empty=values,
                    file_id=file_id,
                    content_link=link,
                    vox=content_id in voxed,
                    dyn=content_id in dyned,
                    words=_words_back(db, content_id),
                    planned=row.words(),
                )
            )
        session_id = record.session_id

    unscored = {row.target for row in plan.vox_unscored()}
    return NativeLanded(
        tree_id=plan.tree_id,
        playlist=plan.playlist,
        playlist_id=playlist_id,
        added=tuple(landed),
        present=tuple(present),
        memberships_added=memberships,
        session_id=session_id,
        playlists=tuple(written),
        favorites=placed,
        set_playlist=set_written,
        labels=labels_written,
        content_link=plan.link.value if plan.link is not None else None,
        left=tuple(left),
        vox_written=vox_written,
        vox_unscored=tuple(
            row.target for row, _content_id in added_ids if row.target in unscored
        ),
        vox_blocked=plan.vox_blocked if added_ids else "",
        vox_missing=tuple(
            row.target for row, content_id in added_ids if row.vox and content_id not in voxed
        ),
        vox_unread=vox_unread,
        dyn_written=dyn_written,
        dyn_variable=tuple(
            row.target for row, _content_id in added_ids if row.drift_verdict == drift.VARIABLE
        ),
        dyn_unscored=tuple(
            row.target for row, _content_id in added_ids if row.drift_verdict == drift.UNSCORED
        ),
        dyn_blocked=plan.dyn_blocked if added_ids else "",
        dyn_missing=tuple(
            row.target for row, content_id in added_ids if row.dyn and content_id not in dyned
        ),
        dyn_unread=dyn_unread,
        analyze_id=analyze_id,
        analyze_name=f"{plan.root_name} / {ANALYZE}" if analyze_id else "",
        analyze_added=analyze_added,
        twins=twins_written,
    )

def _tag_vox(db: Any, added: Sequence[tuple[RowPlan, str]]) -> int:
    """Give each added row the plan tagged the vox My Tag. Answers how many were written.

    THE VOCALS VERB'S OWN WRITER (U127), so the category and the value are
    found or made exactly as ``metadata mytags-vocals`` makes them, and an
    association already there is left as it is. Pending on the landing's
    handle, committed or rolled back with its rows.
    """
    content_ids = [content_id for row, content_id in added if row.vox]
    if not content_ids:
        return 0
    value = rb_writer.ensure_my_tag_value(db, metadata_cli.CATEGORY, metadata_cli.VALUE_VOX)
    return sum(1 for content_id in content_ids if rb_writer.add_my_tag(db, value, content_id))


def _tag_dyn(db: Any, added: Sequence[tuple[RowPlan, str]]) -> int:
    """Give each added row the plan tagged the dyn My Tag (U157). Answers how many were written.

    The vocals verb's writer, as :func:`_tag_vox` uses it, under
    :data:`DYN_CATEGORY`, found by name or made, and :data:`DYN_VALUE` inside
    it. Pending on the landing's handle, committed or rolled back with its rows.
    """
    content_ids = [content_id for row, content_id in added if row.dyn]
    if not content_ids:
        return 0
    value = rb_writer.ensure_my_tag_value(db, DYN_CATEGORY, DYN_VALUE)
    return sum(1 for content_id in content_ids if rb_writer.add_my_tag(db, value, content_id))


def _dyn_read_back(db: Any) -> tuple[frozenset[str], str]:
    """Every row carrying the dyn My Tag as the check reads it, after the commit (U157).

    A refusal the reader raises is the answer's reason and not the landing's
    failure, as :func:`_vox_read_back` says: the commit has landed by now.
    """
    try:
        return dyn_marked(db), ""
    except CratekitError as exc:
        return frozenset(), exc.cause.message


def _vox_read_back(db: Any) -> tuple[frozenset[str], str]:
    """Every row carrying the vox My Tag as adoption reads it, after the commit (U127).

    ADOPTION'S OWN READER, :func:`cratekit.adopt.placements.vox_tagged`, and
    not a second reading of the table, because what the landing promises is
    that the next ``adopt apply`` files the row, and a tag the writer put under
    a category rekordbox removed is one that reader does not answer. A
    refusal it raises, a marker no row can state, is the answer's reason and
    not the landing's failure: the commit has landed by now. Answers the rows
    and the reason, empty when it read.
    """
    try:
        tagged = adopt_placements.vox_tagged(db)
    except CratekitError as exc:
        return frozenset(), exc.cause.message
    return tagged or frozenset(), ""


def _batch_playlist_row(db: Any, plan: NativePlan, anchor: Any) -> Any:
    """The INBOX playlist the batch members go in: the recorded one, else found or made.

    THE RECORDED PLAYLIST, when a set landing names one (U135), was checked
    live at the plan and is checked again here. Otherwise a live playlist of
    the name under the intake root is taken, and a new one made when none is
    live. A removed playlist is not found: rekordbox soft deletes a playlist a
    person removes, and :func:`rb_writer.ensure_playlist` matches name and
    parent alone, so a playlist deleted in rekordbox and written into would
    hold memberships nobody can see. The INSPIRATION path guards the same way.
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

    FOUND AGAIN AT THE WRITE rather than taken from the plan, so a playlist
    made by another landing since this plan was read is joined and never made
    a second time. The plan's identifier is what the screen said; a playlist
    removed since is not written into, and a new one is made in its place.
    """
    del plan
    found = analyze_playlist(db, str(anchor.ID))
    return found if found is not None else db.create_playlist(ANALYZE, parent=anchor)


def _record_landing_commit(
    record: session.SessionRecord,
    plan: NativePlan,
    rows: int,
    memberships: int,
    cfg: config.Config,
    *,
    playlist_id: str,
    landed: Mapping[str, Any] | None = None,
    written: Sequence[WrittenPlaylist] = (),
    placed: placement.Placed | None = None,
    set_written: set_playlist.Written | None = None,
    vox_written: int = 0,
    dyn_written: int = 0,
    labels_written: label_filing.Written | None = None,
    twins_written: Sequence[Any] = (),
) -> None:
    """Record the commit on the session, once anything landed.

    TWO COUNTS UNDER TWO NAMES. The intake tree's entry is the memberships, the
    number ``restore list`` asks for and the one ``tree cutover`` reads to
    refuse a revert after a native write. The content table's entry is the rows,
    kept apart because a restore that discards them discards tracks, not
    memberships, and a person weighing that should see the difference.
    """
    hearts = placed.added if placed is not None else 0
    coloured = len(placed.coloured) if placed is not None else 0
    if (
        rows <= 0
        and memberships <= 0
        and hearts <= 0
        and coloured <= 0
        and not (set_written and set_written.playlist_id)
        and not (labels_written and labels_written.changed())
    ):
        return
    # THE BATCH PLAYLIST IS NAMED ON THE RECORD (U111), by identifier as well
    # as by name, so ``inbox rotate`` ages a batch from the day it landed
    # rather than from whatever the playlist row says. Written with the commit,
    # by the call that persists it.
    if playlist_id:
        kept = {"id": playlist_id, "name": plan.playlist}
        if plan.set_job_id:
            kept[INBOX_JOB_KEY] = plan.set_job_id
        record.detail[BATCH_PLAYLIST_KEY] = kept
    # AND THE BATCH AND ITS FILED FOLDER (U164), so the next landing of the
    # same name goes back to the folder and the name stays taken.
    if plan.folder is not None and plan.batch:
        record.detail[FILED_BATCH_KEY] = {"batch": plan.batch, "folder": str(plan.folder)}
    # AND EVERY ROW IT MADE (R-1037), so the deletion pass offers a landed
    # row's file once rekordbox has deleted the row outright. Persisted by the
    # content table's commit below, which is recorded whenever a row landed.
    if landed is not None:
        record.detail[LANDED_ROWS_KEY] = dict(landed)
    # AND THE PASS (R-777), which is what ``sync mark --pass`` reads as the
    # proof this pass landed. Only with the commit, never for a plan.
    if plan.pass_name:
        record.detail[PASS_KEY] = plan.pass_name
    # AND EACH ACCOUNT PLAYLIST (U113), by identifier, so it is aged from this
    # record with the batch and never by its name, whose date (U175) is a label.
    if written:
        record.detail[INBOX_PLAYLISTS_KEY] = [
            {
                "id": one.playlist_id,
                "name": one.name,
                ingest.INBOX_ACCOUNT_KEY: one.account,
                ingest.INBOX_PASS_KEY: plan.pass_name or "",
            }
            for one in written
        ]
    # AND EACH LABEL ROW'S PROVIDER TRACK (U150), what its manifest row names,
    # so the account mirror fills this batch's INBOX playlist from its own
    # tracks. Persisted by whichever commit below records anything.
    if labels_written is not None and labels_written.provider:
        record.detail[label_filing.PROVIDER_KEY] = dict(labels_written.provider)
    # AND THE HEARTS PLACED (U120), under their own key, since the Favorites
    # folder is nobody's registered tree and a restore weighing the intake
    # tree's memberships should see these apart from them.
    if placed is not None and (hearts > 0 or coloured > 0):
        record.detail[placement.PLACED_KEY] = placed.to_json()
    changes = []
    if memberships > 0:
        changes.append(session.TreeChange(tree=plan.tree_id, created=memberships))
    if rows > 0:
        changes.append(session.TreeChange(tree=rb_writer.CONTENT_TABLE, created=rows))
    # ONLY A TREE THAT CHANGED IS RECORDED COMMITTED. A landing whose every
    # file was present and in the batch already, with only the set's playlist
    # or the hearts written, leaves the intake tree as it was, and a record
    # saying the tree committed with no change would tell a restore and a
    # revert otherwise.
    if changes:
        session.record_commit(record, plan.tree_id, session.ChangeSummary(tuple(changes)), cfg)
    # AND THE HEARTS PLACED (U120), under the favourites key, so the record
    # counts the batch's memberships and the hearts' apart, as the backfill
    # records its own.
    if hearts > 0 or coloured > 0:
        session.record_commit(
            record,
            placement.RECORD_KEY,
            session.ChangeSummary(
                (
                    session.TreeChange(
                        tree=placement.RECORD_KEY, created=hearts, updated=coloured
                    ),
                )
            ),
            cfg,
        )
    # AND THE SET'S PLAYLIST (U121), under the declared folder's own id, so
    # the record counts the batch's memberships and the set's apart.
    if set_written is not None and plan.set_playlist is not None:
        set_playlist.record_commit(record, set_written, plan.set_playlist, cfg)
    # AND THE LABEL FILING (U156), under the catalogue tree's own id, so the
    # record counts the batch's memberships and the labels' apart.
    if labels_written is not None:
        label_filing.record_commit(record, labels_written, cfg)
    # AND THE CUSTOM PLAYLIST TWINS (U149), named on the record and counted
    # under their own key, since the twin folder is nobody's registered tree.
    if twins_written:
        from cratekit.sync import twins as twin_mod

        record.detail[twin_mod.RECORD_KEY] = [
            {"id": one.playlist_id, "name": one.name, ingest.INBOX_ACCOUNT_KEY: one.account_id}
            for one in twins_written
        ]
        session.record_commit(
            record,
            twin_mod.RECORD_KEY,
            session.ChangeSummary(
                (
                    session.TreeChange(
                        tree=twin_mod.RECORD_KEY,
                        created=len(twins_written) + sum(one.tracks for one in twins_written),
                    ),
                )
            ),
            cfg,
        )
    # AND THE VOX TAGS (U127), under the vocals verb's own key, so a restore
    # counts the tag associations apart from the rows they hang on.
    if vox_written > 0:
        session.record_commit(
            record,
            metadata_cli.CHANGE_KEY,
            session.ChangeSummary(
                (session.TreeChange(tree=metadata_cli.CHANGE_KEY, created=vox_written),)
            ),
            cfg,
        )
    # AND THE DYN TAGS (U157), under their own key, apart from the vox tags.
    if dyn_written > 0:
        session.record_commit(
            record,
            DYN_CHANGE_KEY,
            session.ChangeSummary((session.TreeChange(tree=DYN_CHANGE_KEY, created=dyn_written),)),
            cfg,
        )


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

    THE ROWS AS THE DATABASE HOLDS THEM, read after the commit, so a column
    the binding filled differently from the plan is recorded as it is. The
    update count is the one the commit left. The playlists are the ones the
    rows joined that this landing MADE, every id in ``joined`` that was not a
    playlist row ``before`` it wrote: a removal in rekordbox leaves them (A178,
    A185), and no database from before the landing holds one. Each row's UUID
    is kept beside its columns (R-1844), since a person deleting the playlist
    in rekordbox deletes its row outright (A200) and the rows the landing made
    are then what tells a removal from a rollback, whatever put the database
    back.

    A READ THAT FAILS RECORDS NOTHING and says so: the landing has committed,
    so refusing here would report a landing that happened as failed, and a
    record naming no row only keeps the files, since the deletion pass offers
    nothing it does not name.
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


