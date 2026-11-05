"""The account mirror step of ``crate organize``: the library side, and the steps (U147).

WHAT IS MIRRORED is what rekordbox holds, read through a read handle as the
account area reads its INSPIRATION listing (U142), with rekordbox open or not:

* EVERY LIVE FOLDER UNDER THE ROUTING TREE'S ADOPTED ROOT, found by the root
  the tree registry records and never by the root's name, as every database
  tree reader finds it. Each becomes a root folder on the account of the same
  name, holding one playlist per live plain playlist in it, titled ``<Folder>
  <Playlist>``, ``Deep House Low``;
* THE FAVORITES FOLDER, the folder holding the playlist every favourite is in
  (``favorites.placement``'s home), mirrored as a root folder of its own name.
  The favourites playlist keeps its own title, ``All Favorites``, and the
  others take the folder's, ``Favorites 2026-10``, ``Favorites Undated``;
* INBOX (U150), the intake tree's adopted root, mirrored as a root folder of
  its own name holding one playlist per LIVE BATCH directly under it,
  ``INBOX 2026-10-31 Defected``, a batch being what ``inbox rotate`` calls one
  (:func:`cratekit.intake.rotate.live_batches`). Old, and every playlist that
  is not a batch, is not mirrored. A batch that leaves INBOX, into Old or
  out, has its mirrored playlist REMOVED at the next refresh, the one
  mirrored playlist the product removes, and only when its title no longer
  sits directly under INBOX at all. An intake tree that is not database
  native or not adopted is listed, named and not mirrored.

EACH ROW'S OWN PROVIDER TRACK IS A LINK (U150). A label landing records the
provider track its manifest names for every row it landed
(``label_filing.PROVIDER_KEY``), and the matcher takes it before asking the
provider anything, so a label batch, which no account playlist holds, fills
from its own tracks with no match request and no ISRC tie to miss on.

A smart playlist and a folder inside a folder hold no membership a mirror
could copy, and are not mirrored. Two rekordbox folders that would take one
account name refuse that name, since which one is the mirror is not something a
name decides, and so do two playlists of one folder taking one title.

ONE STEP PER FOLDER, each its own gate line and digest, so a folder the
account cannot decide refuses alone and the rest are planned. A folder the
ledger records as mirrored that the library no longer holds is LISTED, named
and left on the account: the product never removes a mirrored folder.

UNREAD IS NOT NONE. A library or ledger that cannot be read refuses the whole
kind as one step; a folder whose account side cannot be read refuses that
folder, and no folder is planned over a listing that failed.

AN EDIT MADE ON THE ACCOUNT TO A MIRRORED PLAYLIST IS HELD (U201, U204). Each
mirrored playlist keeps its snapshot, and every playlist of a genre folder, the
Favorites folder and INBOX is read three ways by :func:`read`, once per
organize run for both areas through :class:`Shared`: the rekordbox area's
``mirror-edits`` step takes each edit into the library, its ``mirror-downloads``
step queues a track added there that the library lacks, and the mirror here
neither takes such a track off nor adds it back.

EVERY RUN SAYS ITS REQUEST COUNT AND DURATION: the plan's in the area's facts,
and each applied folder's in its applied totals.

THE PLAN A GATE SHOWS IS THE PLAN ITS APPLY APPLIES (R-1031). A run that asks
its gate records every link and miss its plan found in the ledger, a fact about
a row and a provider track rather than a write to the account, and freezes the
library it read and its matches on the run (:mod:`mirror_frozen`). The run that
answers the gate rebuilds the mirror from them, reading the account listing
alone, so a library write between the two acts no longer moves the digest and
the provider is asked only about rows the frozen plan does not carry. A report
records and freezes nothing.

Layer: modules.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import Cause, CratekitError, Scope, refuse
from cratekit.modules.outbound import ledger, mirror
from cratekit.organize import mirror_frozen
from cratekit.organize.steps import LISTED, NOTHING, PLANNED, Area, Step, refused

#: The step kind ``--only`` names the mirror by.
MIRROR = "mirror"

TITLE = "mirror the genre tree, the Favorites folder and INBOX onto the account"

#: The fact the area shows for the plan's own request count and duration.
PLAN_FACT = "mirror plan"
#: The fact naming the misses a plan reused rather than asked again.
MISSES_FACT = "mirror misses remembered"
#: The fact saying whether the plan was frozen on the run, or rebuilt from one.
FROZEN_FACT = "mirror plan frozen"
#: The fact naming the rows a landing's recorded provider track answered.
KNOWN_FACT = "mirror rows answered by their landing"


@dataclass(frozen=True, slots=True)
class Run:
    """The organize run the mirror is planned on (R-1031).

    ``record`` is a run that asks its gate, so its plan records what it
    learned and freezes itself; a report does neither. ``decided`` is a run
    whose account gate already holds a recorded answer, so the mirror is
    rebuilt from the plan frozen on it. ``rematch`` asks every remembered miss
    again.
    """

    run_id: str
    record: bool = False
    decided: bool = False
    rematch: bool = False

_ORIGIN = ("organize", "account_mirror")


@dataclass(frozen=True, slots=True)
class Library:
    """What the library holds to mirror, and each name it could not decide."""

    folders: tuple[mirror.Folder, ...] = ()
    #: An account name two rekordbox folders, or two playlists, would take.
    refused: dict[str, Cause] = field(default_factory=dict)
    #: Why the Favorites folder is not mirrored, when it is not.
    favorites: str = ""
    #: Why INBOX is not mirrored, when it is not (U150).
    inbox: str = ""


def _rows(db: Any, playlist_id: str, *, timed: bool = False) -> tuple[mirror.Row, ...]:
    from cratekit.acquire import match
    from cratekit.write import playlist_pair

    times = _times(db, playlist_id) if timed else {}
    return tuple(
        mirror.Row(
            content_id=row.content_id,
            title=row.title,
            artist=row.artist,
            isrc=match.isrc_token(row.isrc),
            path=row.path,
            added=times.get(row.content_id, ""),
        )
        for row in playlist_pair.members(db, playlist_id)
    )


def _times(db: Any, playlist_id: str) -> dict[str, str]:
    """When each live membership of one playlist was made, by content row (U201).

    The newest membership of a row held twice, since it is the one a person
    added last. A database whose memberships carry no time, or that refuses the
    read, gives none, which the edit rule reads as unknown, never as a time.
    """
    from sqlalchemy import exc, text

    from cratekit.core import rb_writer
    from cratekit.modules.outbound import mirror_edits

    try:
        found = db.session.execute(
            text(
                f"SELECT ContentID, created_at FROM {rb_writer.MEMBERSHIP_TABLE} "
                f"WHERE PlaylistID = :id "
                f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0"
            ),
            {"id": str(playlist_id)},
        ).fetchall()
    except exc.SQLAlchemyError:
        db.session.rollback()
        return {}
    newest: dict[str, str] = {}
    for content_id, made in found:
        said = "" if made is None else str(made)
        at = mirror_edits.moment(said)
        if at is None:
            continue
        held = mirror_edits.moment(newest.get(str(content_id), ""))
        if held is None or at > held:
            newest[str(content_id)] = said
    return newest


def _children(db: Any, parent_id: str) -> list[Any]:
    """The live rows directly under one node, the binding's query materialized."""
    from cratekit.core import rb_writer

    gone = rb_writer.node_removed
    return [row for row in list(db.get_playlist(ParentID=str(parent_id))) if not gone(row)]


def _plain(row: Any) -> bool:
    return int(getattr(row, "Attribute", -1) or 0) == 0


def _folder(
    db: Any, name: str, parent_id: str, titled: Callable[[str], str], *, edits: str = ""
) -> mirror.Folder | Cause:
    """One rekordbox folder as a mirror, or the refusal of a title two playlists take.

    ``edits`` is the edit rule that reads the folder. A genre folder's rows
    carry their membership times for the later change rule (U201), and the
    Favorites folder's too (U204); an INBOX batch has no such rule to ask.
    """
    from cratekit.modules.outbound import mirror_edits

    playlists = sorted(
        (row for row in _children(db, parent_id) if _plain(row)),
        key=lambda row: (str(row.Name), str(row.ID)),
    )
    sources: list[mirror.Source] = []
    taken: dict[str, int] = {}
    for row in playlists:
        name_of = titled(str(row.Name))
        taken[name_of] = taken.get(name_of, 0) + 1
        timed = edits in (mirror_edits.GENRE, mirror_edits.FAVORITES)
        sources.append(mirror.Source(name=name_of, rows=_rows(db, str(row.ID), timed=timed)))
    twice = sorted(one for one, count in taken.items() if count > 1)
    if twice:
        return _twice(name, f"its playlists {', '.join(repr(one) for one in twice)}")
    return mirror.Folder(name=name, playlists=tuple(sources), edits=edits)


def _twice(name: str, what: str) -> Cause:
    """Two library nodes taking one account name: refused, the remedy in rekordbox."""
    return refuse(
        mirror.AMBIGUOUS_REASON,
        f"the library holds two of {what} under the account name {name!r}, so which "
        f"one the mirror copies is not something a name decides, and nothing was "
        f"planned for it",
        steps=("rename one of them in rekordbox so each carries its own name",),
        scope=Scope.SOURCE,
        origin=_ORIGIN,
        detail={"name": name},
    ).cause


def _inbox(
    cfg: config.Config, db: Any, declared: Any, registry: Any, today: Any = None
) -> tuple[str, mirror.Folder | Cause | str]:
    """INBOX as a retiring mirror folder, the refusal of a title two batches take, or why not.

    Answers ``(name, folder or refusal)``, or ``("", why)`` when the intake
    tree cannot be read as database native, which lists INBOX and mirrors
    nothing of it, so no retirement is planned over a tree nobody read.
    ``today`` is the day a batch's age is read for, the local day by default.
    """
    from datetime import date

    from cratekit.intake import rotate
    from cratekit.modules.outbound import mirror_edits

    try:
        live = rotate.live_batches(
            cfg, db, declared=declared, registry=registry, today=today or date.today()
        )
    except CratekitError as exc:
        return "", f"INBOX is not mirrored: {exc.cause.message}"
    name = live.root_name
    sources: list[mirror.Source] = []
    taken: dict[str, int] = {}
    for playlist_id, batch in live.batches:
        titled = mirror.title(name, batch)
        taken[titled] = taken.get(titled, 0) + 1
        sources.append(mirror.Source(name=titled, rows=_rows(db, playlist_id)))
    twice = sorted(one for one, count in taken.items() if count > 1)
    if twice:
        return name, _twice(name, f"its playlists {', '.join(repr(one) for one in twice)}")
    return name, mirror.Folder(
        name=name,
        playlists=tuple(sources),
        retire=True,
        present=frozenset(mirror.title(name, one) for one in live.present),
        edits=mirror_edits.INBOX,
    )


def read_library(cfg: config.Config) -> Library:
    """Every folder to mirror, read on a read handle that is closed before returning."""
    from cratekit.core import active_taxonomy, rb_writer, tree_registry
    from cratekit.favorites import placement
    from cratekit.modules.outbound import mirror_edits

    declared = active_taxonomy.load(cfg)
    registry = tree_registry.read(cfg)
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        root_id = tree_registry.anchored_root(
            declared.tree.id,
            registry,
            root_exists=lambda root: db.get_playlist(ID=root) is not None,
        )
        found: list[tuple[str, mirror.Folder | Cause]] = []
        for row in sorted(
            (one for one in _children(db, root_id) if rb_writer.is_folder(one)),
            key=lambda one: (str(one.Name), str(one.ID)),
        ):
            name = str(row.Name)
            found.append(
                (
                    name,
                    _folder(
                        db,
                        name,
                        str(row.ID),
                        lambda shown, name=name: mirror.title(name, shown),
                        edits=mirror_edits.GENRE,
                    ),
                )
            )
        favorites = ""
        try:
            home = placement.resolve_home(db, placement.source_name(declared))
        except CratekitError as exc:
            favorites = exc.cause.message
        else:
            if not home.folder_id:
                favorites = (
                    f"the playlist {home.source_name!r} sits at the playlist root, so there "
                    f"is no Favorites folder to mirror"
                )
            else:
                name = home.folder_name

                def titled(shown: str, name: str = name, source: str = home.source_name) -> str:
                    return shown if shown == source else mirror.title(name, shown)

                found.append(
                    (name, _folder(db, name, home.folder_id, titled, edits=mirror_edits.FAVORITES))
                )
        inbox_name, inbox = _inbox(cfg, db, declared, registry)
        inbox_why = ""
        if isinstance(inbox, str):
            inbox_why = inbox
        else:
            found.append((inbox_name, inbox))
    finally:
        rb_writer.close_db(db)
    counted: dict[str, int] = {}
    for name, _held in found:
        counted[name] = counted.get(name, 0) + 1
    folders: list[mirror.Folder] = []
    refusals: dict[str, Cause] = {}
    for name, held in found:
        if counted[name] > 1:
            refusals[name] = _twice(name, "folders")
        elif isinstance(held, Cause):
            refusals[name] = held
        else:
            folders.append(held)
    return Library(folders=tuple(folders), refused=refusals, favorites=favorites, inbox=inbox_why)


def landed_tracks(cfg: config.Config) -> dict[str, str]:
    """Each content row a landing recorded its provider track for, to that track (U150).

    Read from every native landing's session record. A row two records name
    two tracks for is left out, to be matched as any row is, since which
    track it is is not something either record decides. Records that cannot
    be read name nothing, which costs a match request, never a wrong track.
    """
    from cratekit.core import session
    from cratekit.intake import label_filing, native

    records, _unreadable = session.scan_log(cfg)
    named: dict[str, set[str]] = {}
    for record in records:
        if record.workflow != native.WORKFLOW:
            continue
        held = record.detail.get(label_filing.PROVIDER_KEY)
        if not isinstance(held, dict):
            continue
        for content_id, remote in held.items():
            if isinstance(remote, str) and remote.strip():
                named.setdefault(str(content_id), set()).add(remote.strip())
    return {cid: next(iter(found)) for cid, found in named.items() if len(found) == 1}


def identify(cfg: config.Config) -> Callable[[mirror.Row], mirror.Identity]:
    """What a row is matched by: the database code, else the file's, and the bare title.

    ``sync pair``'s reading of one row (U130), so a row means one thing to
    both: the file is read only when the database holds no code for the row.
    """
    from cratekit.core import naming
    from cratekit.modules.outbound import source
    from cratekit.sync import pair_cli

    template = source.name_template(cfg)

    def said(row: mirror.Row) -> mirror.Identity:
        if row.isrc:
            isrc, album, agree = row.isrc, "", False
        else:
            # A CODE READ OFF THE FILE ASKS EVEN ONE TRACK TO AGREE (R-879).
            (isrc, album), agree = pair_cli.file_identity(cfg, row.path), True
        return mirror.Identity(
            isrc=isrc,
            album=album,
            title=naming.strip_heads(row.title, template=template),
            agree=agree,
        )

    return said


def file_signature(cfg: config.Config) -> Callable[[mirror.Row], str]:
    """A row's file as a miss remembers it, its size and mtime, or ``""`` unreadable.

    Resolved as ``pair_cli.file_identity`` resolves the path it reads the code
    from, so a file that gains a code, which changes its mtime, is asked again.
    """
    from cratekit.core import locations
    from cratekit.modules.outbound import source

    rules = source.prefix_rules(cfg)

    def signature(row: mirror.Row) -> str:
        if not row.path:
            return ""
        resolved = locations.resolve_recorded_path(
            row.path, root=cfg.library.root, prefix_map=rules
        )
        if resolved.path is None:
            return ""
        try:
            held = Path(resolved.path).stat()
        except OSError:
            return ""
        return f"{held.st_size}:{held.st_mtime_ns}"

    return signature


def _detail(planned: mirror.FolderPlan) -> str:
    counts = planned.counts()
    if not planned.writes:
        return (
            f"nothing to write: {len(planned.playlists)} playlist(s) already equal "
            f"their rekordbox playlists' account tracks"
            + (f", {counts['unmatched']} row(s) unmatched" if counts["unmatched"] else "")
            + (f", {counts['left']} left as they are" if counts["left"] else "")
        )
    folder = {
        mirror.CREATE: "create the root folder",
        mirror.ADOPT: "adopt the root folder of its name",
        mirror.REUSE: "in its root folder",
        mirror.UNMADE: "no root folder made, since nothing goes in it",
    }[planned.folder_action]
    return (
        f"{folder}, create {counts['create playlist']} playlist(s), add "
        f"{counts['add']} track(s) and remove {counts['remove']}, "
        f"{counts['unmatched']} row(s) unmatched and named"
        + (
            f", remove {counts['remove playlist']} playlist(s) whose batch left it"
            if counts["remove playlist"]
            else ""
        )
    )


def _apply(
    cfg, step: Step, planned: mirror.FolderPlan, account: mirror.Counted, matcher: mirror.Matcher
):
    def apply() -> dict[str, Any]:
        account.lap()
        done = mirror.Applied()
        try:
            # EVERY ROW THE RUN MATCHED OR MISSED, not only this folder's, so
            # a folder with nothing to write leaves no row to be asked again.
            ledger.record_mirror_misses(cfg, matcher.missed)
            mirror.apply(cfg, account, planned, done, links=matcher.fresh)
        finally:
            requests, seconds = account.lap()
        step.warnings.extend(
            {
                "code": "organize-mirror-kept",
                "message": f"{name}: a removal was refused, so nothing was taken off: {why}",
            }
            for name, why in done.kept
        )
        return {**done.totals(), "requests": requests, "seconds": seconds}

    return apply


@dataclass
class Reading:
    """What the mirror read, once per organize run, for both areas (U201).

    The account area's mirror plans from it, and the rekordbox area's step
    that takes an edit made on the account into the library decides from the
    same library, matches and listings, so the two never read two accounts.
    """

    library: Library
    recorded: dict[str, ledger.MirrorFolder]
    account: mirror.Counted
    root: dict[str, str]
    matcher: mirror.Matcher
    started: float
    frozen: Any = None
    unfrozen: str = ""
    #: Every genre playlist's listing read for the edit rule, by remote id.
    listings: dict[str, Any] = field(default_factory=dict)
    #: The edit rule's answer over the genre folders.
    decided: Any = None
    #: Each genre playlist's place, by account title.
    places: dict[str, Any] = field(default_factory=dict)
    #: Why edits made on the account were not read, ``""`` when they were.
    unread: str = ""


def read(cfg: config.Config, account_of: Callable[[], Any], run: Run | None = None) -> Reading:
    """Read the library, the ledger and the account, match every row, and decide the edits.

    Raises the refusal of the whole kind: a library, ledger or account that
    cannot be read.
    """
    from cratekit.modules.outbound import mirror_edits as edits

    started = time.monotonic()
    frozen, unfrozen = None, ""
    if run is not None and run.decided:
        frozen, unfrozen = mirror_frozen.load(cfg, run.run_id)
    library = frozen.library if frozen is not None else read_library(cfg)
    # A FROZEN PLAN CARRIES EVERY ROW'S ANSWER ALREADY, so its rebuild
    # reads no landing record and asks the provider about no row.
    known = landed_tracks(cfg) if frozen is None else {}
    recorded = ledger.mirror_folders(cfg)
    links = ledger.mirror_links(cfg)
    misses = ledger.mirror_misses(cfg)
    account = mirror.Counted(account_of())
    root = account.folders()
    matcher = mirror.Matcher(
        account,
        links,
        identify(cfg),
        misses=misses,
        signature=file_signature(cfg),
        rematch=run is not None and run.rematch,
        seen=frozen.matches if frozen is not None else None,
        known=known,
    )
    # U207. EVERY CODE THE PLANS WILL ASK, screened in batches before the
    # first is asked, so a code the catalogue files nothing under costs no
    # request of its own. A frozen plan's rows are answered already and
    # screen nothing.
    matcher.screen(
        row for folder in library.folders for source in folder.playlists for row in source.rows
    )
    reading = Reading(
        library=library,
        recorded=recorded,
        account=account,
        root=root,
        matcher=matcher,
        started=started,
        frozen=frozen,
        unfrozen=unfrozen,
        decided=edits.Decided(),
    )
    _read_edits(cfg, reading, links)
    return reading


def _read_edits(cfg: config.Config, reading: Reading, links: dict[str, tuple[str, str]]) -> None:
    """Read every edited playlist three ways and decide what a person changed on the account.

    The genre folders, the Favorites folder and INBOX (U201, U204). A taxonomy
    that cannot be read reads no edit, and says so: the mirror then holds
    nothing, as before U201. A playlist whose listing cannot be read is read as
    its snapshot and short, so it carries no edit of its own.
    """
    from cratekit.core import active_taxonomy
    from cratekit.modules.outbound import mirror_edits as edits
    from cratekit.organize import mirror_downloads
    from cratekit.organize import mirror_edits as carry

    edited = [folder for folder in reading.library.folders if folder.edits]
    if not edited:
        return
    try:
        declared = active_taxonomy.load(cfg)
    except CratekitError as exc:
        reading.unread = f"edits made on the account were not read: {exc.cause.message}"
        return
    reading.places = carry.places(declared, edited)
    matcher = reading.matcher
    # EVERY ROW THE MIRROR READS IS MATCHED HERE, the plan's own requests made
    # once, so an account track is owned by any row the library mirrors.
    for folder in reading.library.folders:
        for source in folder.playlists:
            for row in source.rows:
                matcher.match(row)
    owner: dict[str, set[str]] = {}
    seen = matcher.seen
    for content_id, (remote, _isrc, _reason) in seen.items():
        if remote:
            owner.setdefault(remote, set()).add(content_id)
    for content_id, (remote, _isrc) in links.items():
        if content_id not in seen and remote:
            owner.setdefault(remote, set()).add(content_id)
    # A TRACK A MIRROR DOWNLOAD QUEUED IS OWNED BY THE ROW OF ITS ISRC once it
    # lands (U204), even where the matcher broke a tie between releases toward
    # another one, so the addition it was queued for is read and filed, and the
    # row is answered as that track so the mirror never swaps it for another
    # release. Two rows of the code are two owners, which holds the edit.
    for remote, rows in mirror_downloads.landed(cfg, seen).items():
        # A ROW THE LEDGER LINKS TO ANOTHER TRACK was the library's before the
        # download, so it is never relinked: that would swap its release on
        # every playlist it sits in.
        if remote in owner or any(
            links.get(one, ("", ""))[0] not in ("", remote) for one in rows
        ):
            continue
        if len(rows) == 1:
            (content_id,) = rows
            was = seen.get(content_id, ("", "", ""))[0]
            if was and was in owner:
                owner[was].discard(content_id)
            matcher.adopt(content_id, remote)
        owner[remote] = set(rows)
    read: list[edits.Mirrored] = []
    for folder in edited:
        held = reading.recorded.get(folder.name)
        for source in folder.playlists:
            place = reading.places.get(source.name)
            if place is None or place.folder != folder.name:
                continue
            wanted: set[str] = set()
            added: dict[str, str] = {}
            for row in source.rows:
                remote, _reason = matcher.match(row)
                if not remote:
                    continue
                wanted.add(remote)
                newer = edits.moment(row.added)
                if newer is not None and (
                    edits.moment(added.get(remote, "")) is None
                    or newer > edits.moment(added[remote])
                ):
                    added[remote] = row.added
            mine = held.playlists.get(source.name) if held is not None else None
            if mine is None:
                read.append(edits.Mirrored(place=place, rekordbox=frozenset(wanted)))
                continue
            try:
                listing = reading.account.playlist_listing(mine.remote_id)
            except CratekitError:
                read.append(
                    edits.Mirrored(
                        place=place,
                        account=mine.agreed or frozenset(),
                        rekordbox=frozenset(wanted),
                        agreed=mine.agreed,
                        short=True,
                        rekordbox_added=added,
                    )
                )
                continue
            reading.listings[mine.remote_id] = listing
            read.append(
                edits.Mirrored(
                    place=place,
                    account=frozenset(listing.names),
                    rekordbox=frozenset(wanted),
                    agreed=mine.agreed,
                    short=listing.short,
                    account_added=dict(listing.added),
                    rekordbox_added=added,
                )
            )
    reading.decided = edits.decide(read, {remote: sorted(rows) for remote, rows in owner.items()})


def holds_for(reading: Reading, folder: mirror.Folder) -> dict[str, Any] | None:
    """The holds of one folder's playlists, or ``None`` for a folder no edit rule reads.

    By the place's own folder, so a title two folders share never carries one
    folder's hold onto the other's playlist (U204).
    """
    if not folder.edits:
        return None
    return {
        title: hold
        for title, hold in reading.decided.holds.items()
        if (place := reading.places.get(title)) is not None and place.folder == folder.name
    }


class Shared:
    """One account and one :class:`Reading` per organize run, for both areas (U201).

    ``resolve`` resolves the provider seam; its refusal, and the reading's, is
    kept and raised again to every caller, so each area refuses the steps
    that need it with the same reason.
    """

    def __init__(self, cfg: config.Config, resolve: Callable[[], Any], run: Run | None = None) -> None:
        self._cfg = cfg
        self._resolve = resolve
        self._run = run
        self._account: Any = None
        self._account_error: CratekitError | None = None
        self._account_done = False
        self._reading: Reading | None = None
        self._reading_error: CratekitError | None = None

    def account(self) -> Any:
        if not self._account_done:
            self._account_done = True
            try:
                self._account = self._resolve()
            except CratekitError as exc:
                self._account_error = exc
        if self._account_error is not None:
            raise self._account_error
        return self._account

    def reading(self) -> Reading:
        if self._reading is None and self._reading_error is None:
            try:
                self._reading = read(self._cfg, self.account, self._run)
            except CratekitError as exc:
                self._reading_error = exc
        if self._reading_error is not None:
            raise self._reading_error
        assert self._reading is not None
        return self._reading


#: The fact naming what the edit rule read and decided (U201).
EDITS_FACT = "mirror edits made on the account"


def _edits_fact(reading: Reading) -> str:
    from cratekit.modules.outbound import mirror_edits as edits

    if reading.unread:
        return reading.unread
    decisions = reading.decided.decisions
    if not decisions:
        return "no mirrored playlist was changed on the account since the mirror last finished it"
    count = {kind: 0 for kind in (*sorted(edits.CARRIED), edits.HELD, edits.REKORDBOX, edits.AGREED)}
    for one in decisions:
        count[one.outcome] = count.get(one.outcome, 0) + 1
    carried = sum(count[kind] for kind in edits.CARRIED)
    return (
        f"{len(decisions)} edit(s) made on the account: {carried} taken into the "
        f"library by the rekordbox area's mirror-edits step, {count[edits.HELD]} held as "
        f"the account has them ({len(reading.decided.wanted)} of them for the "
        f"mirror-downloads step to queue), {count[edits.REKORDBOX]} where rekordbox's "
        f"change stands, {count[edits.AGREED]} where both sides agree"
    )


def add_steps(
    cfg: config.Config,
    area: Area,
    account_of: Callable[[], Any],
    run: Run | None = None,
    shared: Shared | None = None,
) -> None:
    """Plan every mirrored folder into ``area``, one step each.

    ``account_of`` is the area's own lazy account, so a refusal to resolve it
    is this kind's refusal with its own reason. ``run`` is the organize run,
    or ``None`` for a plan that neither records, freezes nor rebuilds.
    ``shared`` is the run's one reading, which the rekordbox area may have
    read already (U201); without one the mirror reads its own.
    """
    try:
        reading = shared.reading() if shared is not None else read(cfg, account_of, run)
    except CratekitError as exc:
        area.steps.append(refused(MIRROR, TITLE, exc.cause))
        return
    started = reading.started
    frozen, unfrozen = reading.frozen, reading.unfrozen
    library, recorded = reading.library, reading.recorded
    account, root, matcher = reading.account, reading.root, reading.matcher
    settled: list[tuple[str, dict[str, tuple[str, frozenset[str]]]]] = []
    for folder in library.folders:
        key = f"{MIRROR}:{folder.name}"
        title = f"mirror {folder.name} onto the account"
        try:
            planned = mirror.plan(
                folder,
                account,
                recorded=recorded.get(folder.name),
                root=root,
                matcher=matcher,
                holds=holds_for(reading, folder),
                listings=reading.listings,
            )
        except CratekitError as exc:
            area.steps.append(refused(key, title, exc.cause))
            continue
        settled.append((folder.name, mirror.settled(planned)))
        step = Step(
            key=key,
            title=title,
            state=PLANNED if planned.writes else NOTHING,
            detail=_detail(planned),
            digest=digest_of(planned.identity()),
            counts=planned.counts(),
            items=planned.items(),
        )
        if planned.writes:
            step.apply = _apply(cfg, step, planned, account, matcher)
            # EVERY TRACK TAKEN OFF IS NAMED ON THE GATE, U143's line for a
            # removal, so the gate never says nothing is removed over one.
            area.deletes.extend(
                f"{len(one.remove)} track(s) off the mirrored playlist {one.name!r}: "
                + "; ".join(one.removed_names)
                for one in planned.playlists
                if one.remove
            )
            # AND EVERY PLAYLIST REMOVED (U150), the INBOX folder's retired batch.
            area.deletes.extend(
                f"the mirrored playlist {name!r} ({remote_id}) off the account, since "
                f"what it mirrors left {folder.name}"
                for name, remote_id in planned.retire
            )
        area.steps.append(step)
    for name, cause in sorted(library.refused.items()):
        area.steps.append(refused(f"{MIRROR}:{name}", f"mirror {name} onto the account", cause))
    if library.favorites:
        area.steps.append(
            Step(
                key=f"{MIRROR}:favorites",
                title="mirror the Favorites folder onto the account",
                state=LISTED,
                detail=f"not mirrored: {library.favorites}",
            )
        )
    if library.inbox:
        area.steps.append(
            Step(
                key=f"{MIRROR}:inbox",
                title="mirror INBOX onto the account",
                state=LISTED,
                detail=library.inbox,
            )
        )
    held = {folder.name for folder in library.folders} | set(library.refused)
    for name in sorted(set(recorded) - held):
        area.steps.append(
            Step(
                key=f"{MIRROR}:{name}",
                title=f"mirror {name} onto the account",
                state=LISTED,
                detail=(
                    f"the library no longer holds a folder named {name!r}, so its mirror "
                    f"is left on the account as it is and nothing is removed"
                ),
            )
        )
    if run is not None and run.record:
        # THE SNAPSHOT OF EACH PLAYLIST WITH NOTHING TO WRITE (U201), which no
        # apply records. A ledger that cannot take it leaves the snapshot as
        # it was, which reads one more refresh's differences as before.
        try:
            for name, agreed in settled:
                ledger.record_mirror_agreed(cfg, name, agreed)
        except CratekitError as exc:
            area.facts[EDITS_FACT + " snapshot"] = (
                f"not recorded for the playlists with nothing to write: {exc.cause.message}"
            )
    area.facts[EDITS_FACT] = _edits_fact(reading)
    requests, _seconds = account.lap()
    doing = "read the account and rebuild" if frozen is not None else "read the library and the account and plan"
    area.facts[PLAN_FACT] = (
        f"{requests} account request(s) in {round(time.monotonic() - started, 2)} s to "
        f"{doing} {len(library.folders)} folder(s)"
    )
    if matcher.known:
        area.facts[KNOWN_FACT] = (
            f"{matcher.known} row(s) were matched by the provider track their landing "
            f"recorded, with no request"
        )
    if matcher.remembered:
        area.facts[MISSES_FACT] = (
            f"{matcher.remembered} row(s) the mirror could not match before were not "
            f"asked again, since nothing they were asked under changed; --rematch asks them"
        )
    if frozen is not None:
        area.facts[FROZEN_FACT] = f"rebuilt from the plan frozen on run {run.run_id}" + (
            ", whose matches stand, so --rematch on this run asked nothing; give it on "
            "a new run to ask the remembered misses again"
            if run.rematch
            else ""
        )
    elif run is not None and run.record:
        area.facts[FROZEN_FACT] = _record(cfg, run, library, matcher, unfrozen)


def _record(
    cfg: config.Config, run: Run, library: Library, matcher: mirror.Matcher, unfrozen: str
) -> str:
    """Record what the plan learned and freeze it on the run; what the gate says of it.

    NEITHER FAILURE REFUSES THE PLAN. A ledger that cannot take the links
    refuses the apply on its own, and a plan that cannot be frozen is planned
    again by the run that applies, which is what every run did before R-1031.
    """
    said = f"{unfrozen}, so it was planned afresh; " if unfrozen else ""
    try:
        ledger.record_mirror_links(cfg, matcher.fresh)
        ledger.record_mirror_misses(cfg, matcher.missed)
    except CratekitError as exc:
        return f"{said}not frozen: what the plan matched could not be recorded ({exc.cause.message})"
    try:
        return said + mirror_frozen.freeze(cfg, run.run_id, library, matcher.seen)
    except OSError as exc:
        return f"{said}not frozen ({exc}), so the apply plans again"


__all__ = [
    "EDITS_FACT",
    "FROZEN_FACT",
    "KNOWN_FACT",
    "MIRROR",
    "MISSES_FACT",
    "PLAN_FACT",
    "Library",
    "Reading",
    "Run",
    "Shared",
    "add_steps",
    "file_signature",
    "holds_for",
    "identify",
    "landed_tracks",
    "read",
    "read_library",
]
