"""The plan of a native landing: one row per file, planned against the open database.

Every name here is reached through :mod:`cratekit.intake.native` as well.
"""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, Any, Sequence

from cratekit.cli.output import digest_of
from cratekit.core import config, drift, locations, rb_writer, tags, tree_registry
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.favorites import colour as colour_mod
from cratekit.favorites import placement
from cratekit.intake import ingest, label_filing, native, set_playlist
from cratekit.intake.native import (
    _ORIGIN,
    ADD,
    ALBUM_ARTIST,
    ANALYZE,
    DYN_NO_CATEGORY,
    NOT_LANDED,
    PRESENT,
    UNSUPPORTED,
    VOX_NO_CATEGORY,
    VOX_UNCALIBRATED,
    VOX_UNREADABLE,
    FavoritesPlan,
    HeartItem,
    NativePlan,
    OwnedHeartItem,
    PlaylistPlan,
    RowPlan,
    Word,
)
from cratekit.intake.native_read import _holding, analyze_playlist
from cratekit.write import metadata, metadata_cli, routing_pass, row_link, trees

if TYPE_CHECKING:
    from cratekit.intake.account_playlists import Left


def _property(db: Any) -> Any:
    from pyrekordbox.db6 import tables

    return db.session.query(tables.DjmdProperty).first()


def choose_device(db: Any) -> tuple[str, str]:
    """The device whose ``MasterDBID`` is the library's own, as (device id, master id).

    ASSERTED, NEVER TRUSTED: ``add_content`` stamps the first device the query
    returns, and a library holds one per machine that opened it. Several
    matches take the lowest identifier, so query order cannot decide.
    """
    from pyrekordbox.db6 import tables

    property_row = _property(db)
    dbid = None if property_row is None else str(getattr(property_row, "DBID", "") or "")
    devices = list(db.session.query(tables.DjmdDevice).all())
    matching = sorted(
        (device for device in devices if dbid and str(device.MasterDBID) == dbid),
        key=lambda device: str(device.ID),
    )
    if not matching:
        raise refuse(
            "collection-unreadable",
            f"no device row in the database carries the library's own identifier "
            f"{dbid!r}, so a content row could not be stamped with the device that "
            f"owns this library; {len(devices)} device row(s) were read",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"dbid": dbid, "devices": [str(device.ID) for device in devices]},
        )
    return str(matching[0].ID), str(matching[0].MasterDBID)


def stored_folder_path(path: Path, *, base_drive: str | None, current_drive: str | None) -> str:
    """The ``FolderPath`` rekordbox's own rows would carry for a mounted ``path``.

    UNDER THE BASE DRIVE, NOT THE MOUNTED ONE: rekordbox remaps the drive the
    database was made on at runtime, so a path under the current drive takes
    the base drive's prefix. NFC, as rekordbox stores, since one byte of
    difference is a second row for one file (KTD27).
    """
    text = locations.norm_for_compare(str(path))
    if base_drive and current_drive and base_drive != current_drive:
        current = locations.norm_for_compare(current_drive).rstrip("/\\")
        if text == current or text.startswith(current + os.sep):
            return locations.norm_for_compare(base_drive).rstrip("/\\") + text[len(current) :]
    return text


def file_type_of(path: Path) -> int | None:
    """The binding's file type for ``path``'s suffix, or None when it has none.

    Asked at plan time, since the binding raises the wrong exception class on
    an unknown suffix. None rather than a refusal: the file is planned as
    :data:`UNSUPPORTED` and stays in staging, and the batch still lands.
    """
    from pyrekordbox.db6.tables import FileType

    name = path.suffix.lstrip(".").upper()
    found = getattr(FileType, name, None) if name else None
    return None if found is None else int(found.value)


def anchored_intake_root(db: Any, tree_id: str, registry: tree_registry.Registry) -> str:
    """The intake tree's adopted root, or the refusal that names ``tree cutover``.

    THROUGH THE SHARED ASSERTION. A tree still on the bridge is rephrased with
    the verb that fixes it, since here it means the person has not cut over yet.
    """
    try:
        return tree_registry.anchored_root(
            tree_id, registry, root_exists=lambda root_id: db.get_playlist(ID=root_id) is not None
        )
    except tree_registry.TreeModeRefused as exc:
        if exc.cause.reason != "tree-unconverged" or exc.mode != tree_registry.Mode.XML:
            raise
        raise refuse(
            "tree-unconverged",
            f"the intake tree {tree_id!r} is still on the xml bridge, so a landing "
            f"adds nothing to the collection through the database; the xml landing "
            f"takes --export, or cut the intake tree over first",
            remedy=Remedy.COMPLETE_PENDING_ACTION,
            steps=(
                f"run crate tree cutover {tree_id} --export with a Fresh Export to "
                f"move the intake tree to the database",
                "or land with --export to splice the batch into that export as before",
            ),
            origin=_ORIGIN,
            detail={"tree_id": tree_id, "mode": str(exc.mode)},
            inner=exc.cause,
        ) from exc


def plan_rows(
    cfg: config.Config,
    db: Any,
    *,
    tree_id: str,
    registry: tree_registry.Registry,
    batch: str,
    files: Sequence[tuple[Path, Path]],
    split: Sequence[PlaylistPlan] = (),
    unplanned_left: Sequence[tuple[str, Left]] = (),
    pass_name: str | None = None,
    hearts: Sequence[HeartItem] = (),
    favorites_source: str | None = None,
    owned_hearts: Sequence[OwnedHeartItem] = (),
    set_plan: set_playlist.SetPlaylistPlan | None = None,
    batch_playlist_id: str = "",
    set_job_id: str = "",
    inbox_leftovers: Sequence[str] = (),
    inbox_found_by_name: bool = False,
    labels: label_filing.LabelPlan | None = None,
    twins: Sequence[Any] = (),
) -> NativePlan:
    """Plan one row per file and one playlist, against the open database.

    ``files`` pairs where each file is now with where the landing puts it: the
    row is planned for the target, the title read off the source. The caller
    plans the account playlists (``split``, U113), their ``unplanned_left``
    (U128), ``set_plan`` (U121), ``labels`` (U156) and ``twins`` (U149) on
    this handle; each is digested, less what this plan leaves in staging.
    ``hearts`` and ``owned_hearts`` (U120, U146) are placed under
    ``favorites_source``; a home that cannot be resolved SKIPS the placement
    and says why, never refusing the landing.

    A FILE THE COLLECTION HOLDS IS PRESENT, NOT ADDED TWICE, matched through
    one index resolved on this machine; two active rows on one path count as
    present too, since a third is not the answer to a duplicate.
    """
    # THE QUEUE'S NAME IS RESERVED (U166): a batch of it would be rotated into
    # Old with every row still waiting in it.
    if batch == ANALYZE:
        raise refuse(
            "intake-list-unusable",
            f"the batch name {batch!r} is the playlist under INBOX every landing "
            f"fills with the rows awaiting analysis, so no batch may take it and "
            f"nothing was planned; land with another --name, or rename the file",
            origin=_ORIGIN,
            detail={"batch": batch},
        )
    root_id = anchored_intake_root(db, tree_id, registry)
    root = db.get_playlist(ID=root_id)
    device_id, master_db_id = choose_device(db)
    base_drive, current_drive = rb_writer.recorded_db_drives(db)
    prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
    index = trees.index_active_rows(
        routing_pass.content_rows(db), root=cfg.library.root, prefix_map=prefix_map
    )
    matches = trees.match_indexed_rows(
        [target for _source, target in files], index, root=cfg.library.root, prefix_map=prefix_map
    )
    rows: list[RowPlan] = []
    for (source, target), match in zip(files, matches):
        if match.outcome is trees.MatchOutcome.UNRESOLVED:
            # NOT ABSENT, UNASKED (R-770): the matcher never looked for a row,
            # so an add here could be a second row for a file already held.
            raise refuse(
                "intake-list-unusable",
                f"{target} resolves nowhere under the library at "
                f"{cfg.library.root} or its prefix rules, so the collection could "
                f"not be asked whether it already holds that file and no row was "
                f"planned for it",
                origin=_ORIGIN,
                detail={"target": str(target), "root": str(cfg.library.root)},
            )
        held = _holding(match)
        file_type = file_type_of(target)
        if file_type is None:
            action, why = (
                UNSUPPORTED,
                (
                    f"{target.name} has a suffix rekordbox's database has no file type "
                    f"for, so no content row can name it and it was left in staging; "
                    f"convert it, or land it through the xml bridge"
                ),
            )
        else:
            action, why = (ADD if held is None else PRESENT), ""
        rows.append(
            RowPlan(
                source=source,
                target=target,
                action=action,
                title=str(ingest.file_meta(source, cfg=cfg)["name"]),
                folder_path=stored_folder_path(
                    target, base_drive=base_drive, current_drive=current_drive
                ),
                file_name=target.name,
                file_size=source.stat().st_size,
                file_type=file_type or 0,
                content_link=None,
                content_id=held,
                why=why,
            )
        )
    # ONLY WHEN A ROW IS ADDED (U126): a landing of memberships alone needs no value.
    link = (
        row_link.library_link(db) if any(row.action == ADD for row in rows) else None
    )  # fmt: skip
    if link is not None:
        rows = [replace(row, content_link=link.value) if row.action == ADD else row for row in rows]
    rows, vox_cut, vox_blocked = _vox_plan(cfg, db, rows)
    rows, drift_cut, dyn_blocked = _dyn_plan(cfg, db, rows)
    rows = _words_plan(db, rows)
    kept, dropped = _supported_only(split, rows)
    written_for = {one.account for one in kept}
    if labels is not None:
        labels = label_filing.supported_only(
            labels, {str(row.target) for row in rows if row.action != UNSUPPORTED}
        )
    planned = NativePlan(
        tree_id=tree_id,
        root_id=str(root_id),
        root_name=str(getattr(root, "Name", "") or ""),
        playlist=batch,
        database=Path(rb_writer.handle_path(db) or rb_writer.live_db_path(cfg)),
        device_id=device_id,
        master_db_id=master_db_id,
        base_drive=base_drive,
        current_drive=current_drive,
        rows=tuple(rows),
        link=link,
        digest="",
        playlists=kept,
        unplanned_left=(*unplanned_left, *dropped),
        pass_name=pass_name,
        favorites=_favorites_plan(db, hearts, rows, source=favorites_source, owned=owned_hearts),
        set_playlist=set_plan,
        labels=labels,
        batch_playlist_id=batch_playlist_id,
        set_job_id=set_job_id,
        inbox_leftovers=tuple(inbox_leftovers),
        inbox_found_by_name=inbox_found_by_name,
        vox_cut=vox_cut,
        vox_blocked=vox_blocked,
        drift_cut=drift_cut,
        dyn_blocked=dyn_blocked,
        twins=tuple(one for one in twins if one.account_id in written_for),
    )
    found = analyze_playlist(db, str(root_id))
    if found is not None:
        planned = replace(planned, analyze_playlist_id=str(found.ID))
    return replace(planned, digest=digest_of(native.identity(planned)))


def _vox_plan(
    cfg: config.Config, db: Any, rows: list[RowPlan]
) -> tuple[list[RowPlan], float | None, str]:
    """Each row to be added with its file's score and whether it is given the vox My Tag (U127).

    THE TAG OWNS THE VOCAL SUB (R-841), so it is written from the cut and the
    comparison the vocals verb uses, :mod:`cratekit.write.metadata_cli`'s.
    Only on a row this landing adds; a held row is the repair's (A37).

    NEVER A GUESS: no calibration or no My Tag category plans no tag and says
    why; an unreadable score is no tag, named. Answers rows, cut and reason.
    """
    if not any(row.action == ADD for row in rows):
        return rows, None, ""
    try:
        cut = metadata_cli.load_vocal_threshold(cfg)
    except CratekitError as exc:
        # AN UNREADABLE CALIBRATION BLOCKS THE TAG, NOT THE LANDING. The
        # vocals verb is where it is repaired; holding the batch over it
        # would cost the whole intake.
        return rows, None, VOX_UNREADABLE.format(why=exc.cause.message)
    if cut is None:
        return rows, None, VOX_UNCALIBRATED
    if not rb_writer.my_tag_writable(db):
        return rows, cut, VOX_NO_CATEGORY
    scored: list[RowPlan] = []
    for row in rows:
        if row.action != ADD:
            scored.append(row)
            continue
        level = tags.read_vox_from_file(row.source)
        values = metadata_cli.vocal_tag_values(level, None, cut)
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
    return scored, cut, ""


#: The tags a row's words are read from, in one container open (U163).
_WORD_TAGS: tuple[str, ...] = ("artist", "album", "albumartist", "genre", "date")

#: The two file tags a drift reading is read from (U157).
_DRIFT_TAGS = ("driftlevel", "drift")


def _dyn_plan(
    cfg: config.Config, db: Any, rows: list[RowPlan]
) -> tuple[list[RowPlan], float | None, str]:
    """Each row to be added with its file's drift, its verdict and whether it is tagged dyn (U157).

    AGAINST THE CUT CONFIGURED NOW, ``analysis.drift_cut``, so a changed cut
    moves the digest. Too little pulse reads steady; no reading reads unscored
    and gets no tag. Only on a row this landing adds, and the category is
    asked only when a row reads variable. Answers rows, cut and reason.
    """
    if not any(row.action == ADD for row in rows):
        return rows, None, ""
    cut = float(cfg.analysis.drift_cut)
    read: list[RowPlan] = []
    for row in rows:
        if row.action != ADD:
            read.append(row)
            continue
        values = tags.read_tags(row.source, _DRIFT_TAGS)
        score, verdict = drift.reading(values["driftlevel"], values["drift"], cut)
        read.append(replace(row, drift=score, drift_verdict=verdict))
    variable = [row for row in read if row.drift_verdict == drift.VARIABLE]
    if not variable:
        return read, cut, ""
    if not rb_writer.my_tag_writable(db):
        return read, cut, DYN_NO_CATEGORY
    return [replace(row, dyn=row.drift_verdict == drift.VARIABLE) for row in read], cut, ""


def _words_plan(db: Any, rows: list[RowPlan]) -> list[RowPlan]:
    """Each row to be added with its artist, album and genre words and its year (U163).

    THE LANDING WRITES WHAT RELOAD TAGS WROTE (R-921), so the visit is Analyze
    Tracks alone. Never ``KeyID``, which is rekordbox's analysis. Only on a row
    this landing adds; a held row is ``crate tag rows``' to repair.
    """
    if not any(row.action == ADD for row in rows):
        return rows
    resolver = _Resolver(db)
    planned: list[RowPlan] = []
    for row in rows:
        if row.action != ADD:
            planned.append(row)
            continue
        read = tags.read_tags(row.source, _WORD_TAGS)
        artist = resolver.word(rb_writer.ARTIST_TABLE, _word(read["artist"]))
        album_artist = resolver.word(rb_writer.ARTIST_TABLE, _word(read["albumartist"]))
        planned.append(
            replace(
                row,
                artist=artist,
                album=resolver.album(_word(read["album"]), album_artist),
                genre=resolver.word(rb_writer.GENRE_TABLE, _word(read["genre"])),
                year=year_of(read["date"]),
            )
        )
    return planned


def _word(value: str | None) -> str:
    """A tag's first value as a lookup row's name, empty for a tag that holds only space.

    THE FIRST VALUE IN EVERY CONTAINER: ID3 joins a multi-value frame on NUL,
    and a NUL joined name is a lookup row no other row will ever share.
    """
    first = (value or "").split("\x00")[0]
    if not first.strip():
        return ""
    return first


def year_of(date: str | None) -> int | None:
    """The year a date tag opens with, as rekordbox's ``ReleaseYear`` holds it, else None (U163).

    The first four characters when they are digits naming a year after zero;
    anything else is no year rather than a guess.
    """
    head = (date or "").strip()[:4]
    if len(head) != 4 or not head.isdigit() or int(head) == 0:
        return None
    return int(head)


class _Resolver:
    """The plan's lookup reads for one handle: each word resolved once, each table's convention read once (U163)."""

    def __init__(self, db: Any) -> None:
        self._db = db
        self._found: dict[tuple[str, str, str], str] = {}
        self._search: dict[str, str] = {}

    def word(self, table: str, name: str) -> Word | None:
        """The word for ``name`` in ``table``, linked or minted, or None for no name."""
        if not name:
            return None
        row_id = self._resolved((table, name, ""), lambda: _active_id(self._db, table, name))
        return self._shaped(Word(table=table, name=name, row_id=row_id))

    def album(self, name: str, album_artist: Word | None) -> Word | None:
        """The album word for ``name`` by ``album_artist``, or None for no name."""
        if not name:
            return None
        key = (rb_writer.ALBUM_TABLE, name, album_artist.name if album_artist else "")
        row_id = self._resolved(key, lambda: _active_album_id(self._db, name, album_artist))
        return self._shaped(
            Word(table=rb_writer.ALBUM_TABLE, name=name, row_id=row_id, album_artist=album_artist)
        )

    def _resolved(self, key: tuple[str, str, str], find: Any) -> str:
        if key not in self._found:
            self._found[key] = find()
        return self._found[key]

    def _shaped(self, word: Word) -> Word:
        """A mint given what its table stores in ``SearchStr``, a link as it is."""
        if word.row_id or word.table == rb_writer.GENRE_TABLE:
            return word
        if word.table not in self._search:
            self._search[word.table] = search_convention(self._db, word.table)
        convention = self._search[word.table]
        return replace(word, search=word.name if convention == SEARCH_NAME else convention)


def _lookup_class(table: str) -> Any:
    from pyrekordbox.db6 import tables

    return {
        rb_writer.ARTIST_TABLE: tables.DjmdArtist,
        rb_writer.ALBUM_TABLE: tables.DjmdAlbum,
        rb_writer.GENRE_TABLE: tables.DjmdGenre,
    }[table]


def _active_id(db: Any, table: str, name: str) -> str:
    """The first active row of ``table`` named exactly ``name``, as text, else empty."""
    rows = db.session.query(_lookup_class(table)).filter_by(Name=name)
    found = metadata.first_active_id(rows, table=table, name=name)
    return "" if found is None else str(found)


def _active_album_id(db: Any, name: str, album_artist: Word | None) -> str:
    """The first active album named ``name`` whose album artist is ``album_artist``'s row, else empty.

    An album artist the commit mints has no album yet, so its album is minted
    too. No album artist matches an album whose artist is empty.
    """
    if album_artist is not None and not album_artist.row_id:
        return ""
    want = album_artist.row_id if album_artist is not None else ""
    rows = [
        row
        for row in db.session.query(_lookup_class(rb_writer.ALBUM_TABLE)).filter_by(Name=name)
        if str(getattr(row, ALBUM_ARTIST, None) or "") == want
    ]
    found = metadata.first_active_id(rows, table=rb_writer.ALBUM_TABLE, name=name)
    return "" if found is None else str(found)


#: The ``SearchStr`` conventions :func:`search_convention` answers (U163), or NULL.
SEARCH_NAME = "name"
SEARCH_EMPTY = ""


def search_convention(db: Any, table: str) -> str | None:
    """What most active rows of ``table`` store in ``SearchStr``: their name, empty, or NULL (U163).

    UNMEASURED IN REKORDBOX, SO THE LIBRARY IS ASKED: a mint follows the
    majority of its rows, tombstones included. A tie or no counted row
    answers NULL, the binding's own default.
    """
    from collections import Counter

    counted: Counter[str | None] = Counter()
    for row in db.session.query(_lookup_class(table)):
        stored = getattr(row, "SearchStr", None)
        if stored is None:
            counted[None] += 1
        elif stored == "":
            counted[SEARCH_EMPTY] += 1
        elif stored == getattr(row, "Name", None):
            counted[SEARCH_NAME] += 1
    ranked = counted.most_common()
    if not ranked or (len(ranked) > 1 and ranked[0][1] == ranked[1][1]):
        return None
    return ranked[0][0]


def _favorites_plan(
    db: Any,
    hearts: Sequence[HeartItem],
    rows: Sequence[RowPlan],
    *,
    source: str | None,
    owned: Sequence[OwnedHeartItem] = (),
) -> FavoritesPlan | None:
    """Where the landing's hearts go, or None when it places none (U120, U146).

    AN OWNED HEART JOINS WHEN ALL FAVORITES DOES NOT HOLD IT LIVE (U146): one
    taken out by hand and still hearted joins again, since dropping a
    favourite takes both hand steps.
    """
    writable = {str(row.target) for row in rows if row.action != UNSUPPORTED}
    kept = tuple(item for item in hearts if str(item.target) in writable)
    if not (kept or owned) or not source:
        return None
    try:
        home = placement.resolve_home(db, source)
    except CratekitError as exc:
        # THE ONE REFUSAL A LANDING ABSORBS: no source, or two. Anything else
        # refuses, or a fail closed check would become a note.
        if exc.cause.reason != placement.SOURCE_MISSING:
            raise
        return FavoritesPlan(
            source_name=source,
            source_id="",
            folder_id="",
            folder_name="",
            items=(),
            skipped=exc.cause.message,
        )
    in_source = placement.members(db, home.source_id) if owned else frozenset()
    joining: list[OwnedHeartItem] = []
    seen: set[str] = set()
    for one in owned:
        if one.content_id in in_source or one.content_id in seen:
            continue
        seen.add(one.content_id)
        joining.append(one)
    if not kept and not joining:
        return None
    # THE COLOUR, READ NOW (U153): only a row with none takes Pink, and a row
    # a person coloured is held.
    pink, colour_skipped = placement.read_pink(db)
    to_colour: tuple[str, ...] = ()
    held: tuple[colour_mod.Held, ...] = ()
    if pink and joining:
        sorted_rows = colour_mod.sort_rows(db, pink, [one.content_id for one in joining])
        to_colour, held = sorted_rows.to_colour, sorted_rows.held
    return FavoritesPlan(
        source_name=home.source_name,
        source_id=home.source_id,
        folder_id=home.folder_id,
        folder_name=home.folder_name,
        items=kept,
        present=tuple(sorted(home.present)),
        owned=tuple(joining),
        pink=pink,
        colour_skipped=colour_skipped,
        colour=to_colour,
        held=held,
    )


def _supported_only(
    split: Sequence[PlaylistPlan], rows: Sequence[RowPlan]
) -> tuple[tuple[PlaylistPlan, ...], tuple[tuple[str, Left], ...]]:
    """The account playlists over only the targets a row can be written for, and what was dropped.

    An ``UNSUPPORTED`` file stays in staging, so it is listed as left. A
    playlist holding nothing else is not planned, and its left rows are
    answered by its name, so the landing still names it.
    """
    unsupported = {str(row.target) for row in rows if row.action == UNSUPPORTED}
    kept: list[PlaylistPlan] = []
    dropped: list[tuple[str, Left]] = []
    for one in split:
        members = tuple(
            member
            for member in one.members
            if member.target is None or str(member.target) not in unsupported
        )
        left = (
            *one.left,
            *(
                member.member.left(NOT_LANDED)
                for member in one.members
                if member.target is not None
                and str(member.target) in unsupported
                and member.member is not None
            ),
        )
        if members:
            kept.append(replace(one, members=members, left=left))
        else:
            dropped.extend((one.name, row) for row in left)
    return tuple(kept), tuple(dropped)


def with_filing(plan: NativePlan, predicted: Sequence[Any]) -> NativePlan:
    """``plan`` with where adoption would file its rows, digested again (U165)."""
    filed = replace(plan, filing=tuple(predicted))
    return replace(filed, digest=digest_of(native.identity(filed)))
