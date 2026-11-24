"""The account mirror step of ``crate organize``: the library side, and the steps (U147).

WHAT IS MIRRORED is what rekordbox holds, read with rekordbox open or not: every
live folder under the routing tree's adopted root (found by the root the
registry records, never by name) as a root folder of its name holding one
playlist per plain playlist, ``Deep House Low``; the Favorites folder, where
``All Favorites`` keeps its title; and INBOX (U150), one playlist per live batch
directly under it, every other node there named with its reason (U214). A batch
that leaves INBOX has its mirrored playlist removed, the one mirrored playlist
the product removes, and only when its title no longer sits directly under INBOX
at all. And WIP (U959), the top level folder found by its name stripped, as one
root folder ``WIP`` holding every plain playlist directly under it, titled
``WIP <Playlist>``, and in one level of subfolder, titled ``<Subfolder>
<Playlist>``; a playlist a ``sync pair`` keeps (a custom playlist twin is one),
a smart playlist and a folder deeper down are named with their reason, and
with no WIP folder one fact says so. A smart playlist and a folder inside a
folder hold no membership a mirror could copy, and are not mirrored. Two nodes
taking one account name refuse it: a name does not decide which is the mirror.

EACH ROW'S OWN PROVIDER TRACK IS A LINK (U150): a label landing records the
provider track it landed, and the matcher takes it before asking the provider.

ONE STEP PER FOLDER, so a folder the account cannot decide refuses alone; a
recorded folder the library no longer holds is listed and left, since the
product never removes a mirrored folder. UNREAD IS NOT NONE: a library or
ledger that cannot be read refuses the whole kind. Every run says its request
count and duration.

AN EDIT MADE ON THE ACCOUNT IS HELD (U201, U204): :func:`read` reads every edited
playlist three ways once per run for both areas (:class:`Shared`), so the
rekordbox area takes or queues the edit and the mirror never undoes it.

THE PLAN A GATE SHOWS IS THE PLAN ITS APPLY APPLIES (R-1031, U222): a run that
asks its gate records its links and misses and freezes what it read
(:mod:`mirror_frozen`), and the answering run rebuilds from that. A report
records and freezes nothing.

Layer: modules.
"""

from __future__ import annotations

import time
from collections import Counter
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import Cause, CratekitError, Scope, refuse
from cratekit.organize import mirror_frozen
from cratekit.organize.steps import LISTED, NOTHING, PLANNED, Area, Step, refused

if TYPE_CHECKING:
    from cratekit.modules.outbound import ledger, mirror

#: The step kind ``--only`` names the mirror by.
MIRROR = "mirror"

TITLE = "mirror the genre tree, the Favorites folder, INBOX and WIP onto the account"

#: The top level folder of sets in progress the mirror copies (U959), as
#: ``mirror.WIP`` spells it, its name compared stripped.
WIP = "WIP"

#: The fact the area shows for the plan's own request count and duration.
PLAN_FACT = "mirror plan"
#: The fact naming the misses a plan reused rather than asked again.
MISSES_FACT = "mirror misses remembered"
#: The fact saying whether the plan was frozen on the run, or rebuilt from one.
FROZEN_FACT = "mirror plan frozen"
#: The fact naming the rows a landing's recorded provider track answered.
KNOWN_FACT = "mirror rows answered by their landing"
#: The fact naming what the edit rule read and decided (U201).
EDITS_FACT = "mirror edits made on the account"
#: The fact saying why nothing was mirrored for WIP, when nothing was (U959).
WIP_FACT = "mirror WIP"


@dataclass(frozen=True, slots=True)
class Run:
    """The organize run the mirror is planned on (R-1031).

    ``record`` records and freezes the plan; ``decided`` rebuilds from the frozen
    one; ``rematch`` asks every remembered miss again.
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
    #: Why nothing is mirrored for WIP, when the library holds no WIP folder (U959).
    wip: str = ""


def tree_root(db: Any, declared: Any, registry: Any) -> Any:
    """The routing tree's adopted root, found by the root the registry records."""
    from cratekit.core import tree_registry

    return tree_registry.anchored_root(
        declared.tree.id, registry, root_exists=lambda root: db.get_playlist(ID=root) is not None
    )


def resolve_path(cfg: config.Config, recorded: str, rules: Any = None) -> Path | None:
    """A row's recorded path on this machine, as ``pair_cli.file_identity`` resolves it."""
    from cratekit.core import locations
    from cratekit.modules.outbound import source

    if not recorded:
        return None
    rules = source.prefix_rules(cfg) if rules is None else rules
    resolved = locations.resolve_recorded_path(recorded, root=cfg.library.root, prefix_map=rules)
    return None if resolved.path is None else Path(resolved.path)


def keep_newest(newest: dict[str, str], key: str, said: str) -> None:
    """Hold ``said`` under ``key`` when it reads as a time newer than the one held."""
    from cratekit.modules.outbound import mirror_edits

    at = mirror_edits.moment(said)
    held = mirror_edits.moment(newest.get(key, ""))
    if at is not None and (held is None or at > held):
        newest[key] = said


def _rows(db: Any, playlist_id: str, *, timed: bool = False) -> tuple[mirror.Row, ...]:
    from cratekit.acquire import match
    from cratekit.modules.outbound import mirror
    from cratekit.write import playlist_pair

    times = membership_times(db, playlist_id) if timed else {}
    return tuple(
        mirror.Row(row.content_id, row.title, row.artist, match.isrc_token(row.isrc), row.path,
                   times.get(row.content_id, ""))
        for row in playlist_pair.members(db, playlist_id)
    )


def membership_times(db: Any, playlist_id: str) -> dict[str, str]:
    """When each live membership of one playlist was made, the newest per row (U201, U236).

    No time, or a refused read, gives none: unknown to the edit rule, never a time.
    """
    from sqlalchemy import exc, text

    from cratekit.core import rb_writer

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
        keep_newest(newest, str(content_id), "" if made is None else str(made))
    return newest


def _children(db: Any, parent_id: str) -> list[Any]:
    """The live rows directly under one node, the binding's query materialized."""
    from cratekit.core import rb_writer

    gone = rb_writer.node_removed
    return [row for row in list(db.get_playlist(ParentID=str(parent_id))) if not gone(row)]


def _plain(row: Any) -> bool:
    return int(getattr(row, "Attribute", -1) or 0) == 0


def _by_name(row: Any) -> tuple[str, str]:
    return str(row.Name), str(row.ID)


def _sources(name: str, titled_rows: Iterator[tuple[str, Any]]) -> tuple[mirror.Source, ...] | Cause:
    """Each ``(title, rows)`` as a source, or the refusal of a title two of them take."""
    from cratekit.modules.outbound import mirror

    sources = tuple(mirror.Source(name=title, rows=rows) for title, rows in titled_rows)
    twice = sorted(one for one, count in Counter(one.name for one in sources).items() if count > 1)
    if twice:
        return _twice(name, f"its playlists {', '.join(repr(one) for one in twice)}")
    return sources


def _folder(
    db: Any, name: str, parent_id: str, titled: Callable[[str], str], *, edits: str = ""
) -> mirror.Folder | Cause:
    """One rekordbox folder as a mirror, or the refusal of a title two playlists take.

    ``edits`` is the rule that reads it; genre and Favorites rows carry their times.
    """
    from cratekit.modules.outbound import mirror, mirror_edits

    timed = edits in (mirror_edits.GENRE, mirror_edits.FAVORITES)
    playlists = sorted((row for row in _children(db, parent_id) if _plain(row)), key=_by_name)
    sources = _sources(
        name, ((titled(str(row.Name)), _rows(db, str(row.ID), timed=timed)) for row in playlists)
    )
    if isinstance(sources, Cause):
        return sources
    return mirror.Folder(name=name, playlists=sources, edits=edits)


def _twice(name: str, what: str) -> Cause:
    """Two library nodes taking one account name: refused, the remedy in rekordbox."""
    from cratekit.modules.outbound import mirror

    return refuse(
        mirror.AMBIGUOUS_REASON,
        f"the library holds two of {what} under the account name {name!r}, so which "
        f"one the mirror copies is not something a name decides, and nothing was "
        f"planned for it",
        steps=("rename one of them in rekordbox so each carries its own name",),
        scope=Scope.SOURCE, origin=_ORIGIN, detail={"name": name},
    ).cause


def _shared(titles: list[str]) -> Cause:
    """WIP titling a playlist as another mirrored folder does (U959): WIP refused alone."""
    from cratekit.modules.outbound import mirror

    return refuse(
        mirror.AMBIGUOUS_REASON,
        f"{WIP} and another mirrored folder would both hold the account title(s) "
        f"{', '.join(repr(one) for one in titles)}, and an edit on the account is read by "
        f"its title, so which folder it was made in is not something a name decides, and "
        f"nothing was planned for {WIP}",
        steps=("rename the WIP subfolder or playlist in rekordbox so its account title is its own",),
        scope=Scope.SOURCE, origin=_ORIGIN, detail={"name": WIP, "titles": titles},
    ).cause


def _inbox(
    cfg: config.Config, db: Any, declared: Any, registry: Any, today: Any = None
) -> tuple[str, mirror.Folder | Cause | str]:
    """INBOX as a retiring mirror folder, the refusal of a title two batches take, or why not.

    ``("", why)`` when the intake tree cannot be read as database native, so no
    retirement is planned over a tree nobody read.
    """
    from datetime import date

    from cratekit.intake import rotate
    from cratekit.modules.outbound import mirror, mirror_edits

    try:
        live = rotate.live_batches(
            cfg, db, declared=declared, registry=registry, today=today or date.today()
        )
    except CratekitError as exc:
        return "", f"INBOX is not mirrored: {exc.cause.message}"
    name = live.root_name
    sources = _sources(
        name, ((mirror.title(name, batch), _rows(db, pid)) for pid, batch in live.batches)
    )
    if isinstance(sources, Cause):
        return name, sources
    return name, mirror.Folder(
        name=name,
        playlists=tuple(sources),
        retire=True,
        present=frozenset(mirror.title(name, one) for one in live.present),
        edits=mirror_edits.INBOX,
        unmirrored=tuple((node.label(), node.reason) for node in live.left),
    )


def _paired(cfg: config.Config) -> dict[str, tuple[str, str]]:
    """Each rekordbox playlist a sync pair keeps, to how a WIP line names it and why (U959).

    Raises the refusal of a pair record that cannot be read: unread is not none.
    """
    from cratekit.modules.outbound import pairs

    said: dict[str, tuple[str, str]] = {}
    for pair in pairs.PairStore(cfg).all().values():
        if pair.twin:
            said[pair.rekordbox_id] = (
                "a custom playlist twin",
                f"it is a custom playlist twin of the account playlist {pair.account_id}, which "
                f"sync pair keeps the same list, so the mirror does not copy it a second time",
            )
        else:
            said[pair.rekordbox_id] = (
                "paired by sync pair",
                f"it is one side of a sync pair with the account playlist {pair.account_id}, which "
                f"sync pair keeps the same list, so the mirror does not copy it a second time",
            )
    return said


_SMART = (
    "a smart playlist",
    "a smart playlist holds no membership the mirror could copy",
)
_DEEPER = (
    "a folder two levels down",
    "the mirror reads WIP's playlists and one level of subfolder, so nothing inside a "
    "deeper folder is mirrored",
)


def _wip(cfg: config.Config, db: Any) -> mirror.Folder | Cause | str:
    """WIP as a mirror folder, the refusal of a name it cannot decide, or why there is none (U959)."""
    from cratekit.core import rb_writer
    from cratekit.modules.outbound import mirror, mirror_edits

    tops = [
        row
        for row in list(db.get_playlist())
        if rb_writer.is_folder(row)
        and not rb_writer.node_removed(row)
        and str(getattr(row, "ParentID", "") or "") in rb_writer.ROOT_PARENT_SENTINELS
        and str(row.Name or "").strip() == WIP
    ]
    if not tops:
        return f"the library holds no top level folder named {WIP!r}, so nothing is mirrored for it"
    if len(tops) > 1:
        return _twice(WIP, "top level folders")
    try:
        paired = _paired(cfg)
    except CratekitError as exc:
        return exc.cause
    titled: list[tuple[str, str]] = []
    unmirrored: list[tuple[str, str]] = []

    def left(path: str, said: tuple[str, str]) -> None:
        unmirrored.append((f"{path}, {said[0]}", said[1]))

    def take(row: Any, path: str, where: tuple[str, ...]) -> None:
        if not _plain(row):
            left(path, _SMART)
        elif str(row.ID) in paired:
            left(path, paired[str(row.ID)])
        else:
            titled.append((mirror.wip_title((WIP, *where, str(row.Name))), str(row.ID)))

    for row in sorted(_children(db, str(tops[0].ID)), key=_by_name):
        if not rb_writer.is_folder(row):
            take(row, str(row.Name), ())
            continue
        sub = str(row.Name).strip()
        for inner in sorted(_children(db, str(row.ID)), key=_by_name):
            path = f"{sub} / {inner.Name}"
            if rb_writer.is_folder(inner):
                left(path, _DEEPER)
            else:
                take(inner, path, (sub,))
    sources = _sources(WIP, ((title, _rows(db, pid)) for title, pid in titled))
    if isinstance(sources, Cause):
        return sources
    return mirror.Folder(
        name=WIP, playlists=sources, edits=mirror_edits.WIP, unmirrored=tuple(unmirrored)
    )


def read_library(cfg: config.Config, *, one_read: Any = None) -> Library:
    """Every folder to mirror, read on a read handle released before returning."""
    from cratekit.core import active_taxonomy, rb_writer, tree_registry
    from cratekit.favorites import placement
    from cratekit.modules.outbound import mirror, mirror_edits

    declared = active_taxonomy.load(cfg)
    registry = tree_registry.read(cfg)
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
            rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
        )
    )
    try:
        genres = sorted(
            (one for one in _children(db, tree_root(db, declared, registry)) if rb_writer.is_folder(one)),
            key=_by_name,
        )
        found: list[tuple[str, mirror.Folder | Cause]] = [
            (name, _folder(db, name, str(row.ID), lambda shown, name=name: mirror.title(name, shown),
                           edits=mirror_edits.GENRE))
            for row in genres
            for name in (str(row.Name),)
        ]
        try:
            home = placement.resolve_home(db, placement.source_name(declared))
        except CratekitError as exc:
            home, favorites = None, exc.cause.message
        else:
            favorites = "" if home.folder_id else (
                f"the playlist {home.source_name!r} sits at the playlist root, so there "
                f"is no Favorites folder to mirror"
            )
        if home is not None and home.folder_id:
            name = home.folder_name

            def titled(shown: str, name: str = name, source: str = home.source_name) -> str:
                return shown if shown == source else mirror.title(name, shown)

            found.append((name, _folder(db, name, home.folder_id, titled, edits=mirror_edits.FAVORITES)))
        inbox_name, inbox = _inbox(cfg, db, declared, registry)
        if not isinstance(inbox, str):
            found.append((inbox_name, inbox))
        wip = _wip(cfg, db)
        if not isinstance(wip, str):
            found.append((WIP, wip))
    finally:
        rb_writer.done_reading(db, one_read)
    counted = Counter(name for name, _held in found)
    # A TITLE WIP SHARES WITH ANOTHER MIRRORED FOLDER refuses WIP (U959): the
    # edit rule reads a playlist by its title, so the two would read as one.
    elsewhere = {
        source.name
        for name, held in found
        if name != WIP and isinstance(held, mirror.Folder)
        for source in held.playlists
    }
    folders: list[mirror.Folder] = []
    refusals: dict[str, Cause] = {}
    for name, held in found:
        shared = (
            sorted(one.name for one in held.playlists if one.name in elsewhere)
            if name == WIP and isinstance(held, mirror.Folder)
            else []
        )
        if counted[name] > 1:
            refusals[name] = _twice(name, "folders")
        elif shared:
            refusals[name] = _shared(shared)
        elif isinstance(held, Cause):
            refusals[name] = held
        else:
            folders.append(held)
    return Library(
        tuple(folders), refusals, favorites, inbox if isinstance(inbox, str) else "",
        wip if isinstance(wip, str) else "",
    )


def landed_tracks(cfg: config.Config) -> dict[str, str]:
    """Each content row a native landing recorded its provider track for, to that track (U150).

    A row two records disagree on, or an unreadable record, costs a match request,
    never a wrong track.
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
    """What a row is matched by, as ``sync pair`` reads it (U130): its code, else its file's, and the bare title."""
    from cratekit.core import naming
    from cratekit.modules.outbound import mirror, source
    from cratekit.sync import pair_cli

    template = source.name_template(cfg)

    def said(row: mirror.Row) -> mirror.Identity:
        if row.isrc:
            isrc, album, agree = row.isrc, "", False
        else:
            # A CODE READ OFF THE FILE ASKS EVEN ONE TRACK TO AGREE (R-879).
            (isrc, album), agree = pair_cli.file_identity(cfg, row.path), True
        return mirror.Identity(
            isrc=isrc, album=album, title=naming.strip_heads(row.title, template=template), agree=agree
        )

    return said


def file_signature(cfg: config.Config) -> Callable[[mirror.Row], str]:
    """A row's file as a miss remembers it, size and mtime, so a file that gains a code is asked again."""
    from cratekit.modules.outbound import source

    rules = source.prefix_rules(cfg)

    def signature(row: mirror.Row) -> str:
        path = resolve_path(cfg, row.path, rules)
        if path is None:
            return ""
        try:
            held = path.stat()
        except OSError:
            return ""
        return f"{held.st_size}:{held.st_mtime_ns}"

    return signature


def _detail(planned: mirror.FolderPlan, folder: mirror.Folder) -> str:
    """The step's line, with every node the folder leaves off named on it (U214)."""
    from cratekit.modules.outbound import mirror

    counts = planned.counts()
    if not planned.writes:
        said = (
            f"nothing to write: {len(planned.playlists)} playlist(s) already equal "
            f"their rekordbox playlists' account tracks"
            + (f", {counts['unmatched']} row(s) unmatched" if counts["unmatched"] else "")
            + (f", {counts['left']} left as they are" if counts["left"] else "")
        )
    else:
        action = {
            mirror.CREATE: "create the root folder",
            mirror.ADOPT: "adopt the root folder of its name",
            mirror.REUSE: "in its root folder",
            mirror.UNMADE: "no root folder made, since nothing goes in it",
        }[planned.folder_action]
        said = (
            f"{action}, create {counts['create playlist']} playlist(s), add "
            f"{counts['add']} track(s) and remove {counts['remove']}, "
            f"{counts['unmatched']} row(s) unmatched and named"
            + (
                f", remove {counts['remove playlist']} playlist(s) whose batch left it"
                if counts["remove playlist"]
                else ""
            )
        )
    if folder.unmirrored:
        said += (
            f"; {len(folder.unmirrored)} node(s) in {folder.name} not mirrored: "
            + "; ".join(label for label, _reason in folder.unmirrored)
        )
    return said


def _apply(cfg, step: Step, planned: mirror.FolderPlan, account: mirror.Counted, matcher: mirror.Matcher):
    from cratekit.modules.outbound import ledger, mirror

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
            {"code": "organize-mirror-kept",
             "message": f"{name}: a removal was refused, so nothing was taken off: {why}"}
            for name, why in done.kept
        )
        return {**done.totals(), "requests": requests, "seconds": seconds}

    return apply


@dataclass
class Reading:
    """What the mirror read, once per run for both areas, so the two never read two accounts (U201)."""

    library: Library
    recorded: dict[str, ledger.MirrorFolder]
    account: mirror.Counted
    root: dict[str, str]
    matcher: mirror.Matcher
    started: float
    frozen: Any = None
    unfrozen: str = ""
    #: Every edited playlist's listing read for the edit rule, by remote id.
    listings: dict[str, Any] = field(default_factory=dict)
    #: The edit rule's answer.
    decided: Any = None
    #: Each edited playlist's place, by account title.
    places: dict[str, Any] = field(default_factory=dict)
    #: Why edits made on the account were not read, ``""`` when they were.
    unread: str = ""


def _every_row(library: Library) -> Iterator[mirror.Row]:
    return (row for folder in library.folders for source in folder.playlists for row in source.rows)


def read(
    cfg: config.Config, account_of: Callable[[], Any], run: Run | None = None, *, one_read: Any = None
) -> Reading:
    """Read the library, the ledger and the account, match every row, and decide the edits.

    Raises the refusal of the whole kind. ``one_read`` is the report's one handle (U267).
    """
    from cratekit.modules.outbound import ledger, mirror
    from cratekit.modules.outbound import mirror_edits as edits

    started = time.monotonic()
    frozen, unfrozen = None, ""
    if run is not None and run.decided:
        frozen, unfrozen = mirror_frozen.load(cfg, run.run_id)
    library = frozen.library if frozen is not None else read_library(cfg, one_read=one_read)
    # A FROZEN PLAN CARRIES EVERY ROW'S ANSWER, so it reads no landing record.
    known = landed_tracks(cfg) if frozen is None else {}
    recorded = ledger.mirror_folders(cfg)
    if frozen is not None:
        # THE GATE'S SNAPSHOTS beside the gate's library (U222): one the
        # rekordbox area settled between the acts would read its edit as
        # rekordbox's own change.
        recorded = mirror_frozen.overlay(recorded, frozen)
    links = ledger.mirror_links(cfg)
    misses = ledger.mirror_misses(cfg)
    account = mirror.Counted(account_of())
    root = account.folders()
    matcher = mirror.Matcher(
        account, links, identify(cfg), misses=misses, signature=file_signature(cfg),
        rematch=run is not None and run.rematch,
        seen=frozen.matches if frozen is not None else None,
        known=known,
    )
    # EVERY CODE THE PLANS WILL ASK, screened in batches first (U207), so a code
    # the catalogue files nothing under costs no request of its own.
    matcher.screen(_every_row(library))
    reading = Reading(
        library, recorded, account, root, matcher, started, frozen, unfrozen, decided=edits.Decided()
    )
    _read_edits(cfg, reading, links)
    return reading


def _read_edits(cfg: config.Config, reading: Reading, links: dict[str, tuple[str, str]]) -> None:
    """Read every edited playlist three ways and decide what a person changed on the account.

    A taxonomy that cannot be read reads no edit and says so. A playlist whose
    listing cannot be read is read as its snapshot and short, carrying no edit.
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
    # EVERY ROW THE MIRROR READS IS MATCHED HERE, so an account track is owned
    # by any row the library mirrors.
    for row in _every_row(reading.library):
        matcher.match(row)
    seen = matcher.seen
    remote_of = {content_id: held[0] for content_id, held in seen.items()}
    remote_of.update((cid, held[0]) for cid, held in links.items() if cid not in seen)
    owner: dict[str, set[str]] = {}
    for content_id, remote in remote_of.items():
        if remote:
            owner.setdefault(remote, set()).add(content_id)
    # A TRACK A MIRROR DOWNLOAD QUEUED IS OWNED BY THE ROW OF ITS ISRC once it
    # lands (U204), even where the matcher tied it to another release, so the
    # addition is filed and the mirror never swaps the release. Two rows of the
    # code are two owners, which holds the edit.
    for remote, rows in mirror_downloads.landed(cfg, seen).items():
        # A ROW THE LEDGER LINKS TO ANOTHER TRACK was the library's before the
        # download, and is never relinked.
        if remote in owner or any(links.get(one, ("", ""))[0] not in ("", remote) for one in rows):
            continue
        if len(rows) == 1:
            (content_id,) = rows
            was = seen.get(content_id, ("", "", ""))[0]
            if was and was in owner:
                owner[was].discard(content_id)
            matcher.adopt(content_id, remote)
        owner[remote] = set(rows)
    read: list[edits.Mirrored] = []
    #: Each recorded remote playlist read here, to its title (U230).
    titled: dict[str, str] = {}
    for folder in edited:
        held = reading.recorded.get(folder.name)
        for source in folder.playlists:
            # THE LIBRARY'S OWN PLACEMENTS ON IT (U236), by title.
            recorded_placed = held.placed.get(source.name, {}) if held is not None else {}
            place = reading.places.get(source.name)
            if place is None or place.folder != folder.name:
                continue
            wanted: set[str] = set()
            added: dict[str, str] = {}
            for row in source.rows:
                remote, _reason = matcher.match(row)
                if remote:
                    wanted.add(remote)
                    keep_newest(added, remote, row.added)
            # ONLY WHILE REKORDBOX HOLDS IT BY THE MEMBERSHIP THE WRITE MADE, read
            # by its time, so one a person took off and put back is theirs (U236).
            ours = frozenset(
                remote for remote, at in recorded_placed.items() if at and added.get(remote) == at
            )
            mine = held.playlists.get(source.name) if held is not None else None
            if mine is not None and mine.remote_id:
                titled[mine.remote_id] = source.name
            if mine is None:
                read.append(edits.Mirrored(place=place, rekordbox=frozenset(wanted), placed=ours))
                continue
            try:
                listing = reading.account.playlist_listing(mine.remote_id)
            except CratekitError:
                listing = None
            else:
                reading.listings[mine.remote_id] = listing
            read.append(edits.Mirrored(
                place=place,
                account=(mine.agreed or frozenset()) if listing is None else frozenset(listing.names),
                rekordbox=frozenset(wanted),
                agreed=mine.agreed,
                short=True if listing is None else listing.short,
                account_added={} if listing is None else dict(listing.added),
                rekordbox_added=added,
                placed=ours,
            ))
    # AND WHERE EACH QUEUED TRACK'S LANDING FILED ITS ROW BY ITS TAGS (U227), read
    # as the landing's filing so the edit it was queued for is carried.
    landings = mirror_downloads.filed(cfg, declared, owner)
    # AND WHICH PLAYLIST'S JOB QUEUED EACH (U230), whose base is read as it stood
    # at the queue while the landing's filing stands.
    queued_on = {
        remote: frozenset(titled[one] for one in sources if one in titled)
        for remote, sources in mirror_downloads.queued_from(cfg).items()
        if remote in landings
    }
    reading.decided = edits.decide(
        read, {remote: sorted(rows) for remote, rows in owner.items()}, landings, queued_on
    )


def holds_for(reading: Reading, folder: mirror.Folder) -> dict[str, Any] | None:
    """The holds of one folder's playlists by the place's own folder (U204), ``None`` when no rule reads it."""
    if not folder.edits:
        return None
    return {
        title: hold
        for title, hold in reading.decided.holds.items()
        if (place := reading.places.get(title)) is not None and place.folder == folder.name
    }


class Shared:
    """One account and one :class:`Reading` per organize run, for both areas (U201).

    A refusal to resolve or read is kept and raised to every caller, so each area
    refuses with the same reason.
    """

    def __init__(
        self, cfg: config.Config, resolve: Callable[[], Any], run: Run | None = None, *, one_read: Any = None
    ) -> None:
        self._cfg, self._resolve, self._run, self._one_read = cfg, resolve, run, one_read
        self._held: dict[str, tuple[Any, CratekitError | None]] = {}

    def _once(self, key: str, make: Callable[[], Any]) -> Any:
        if key not in self._held:
            try:
                self._held[key] = (make(), None)
            except CratekitError as exc:
                self._held[key] = (None, exc)
        value, error = self._held[key]
        if error is not None:
            raise error
        return value

    def account(self) -> Any:
        return self._once("account", self._resolve)

    def reading(self) -> Reading:
        return self._once(
            "reading", lambda: read(self._cfg, self.account, self._run, one_read=self._one_read)
        )


def reading_or_step(shared: Shared, kind: str, title: str) -> Reading | Step:
    """The run's one reading for a rekordbox area step, or the step it refuses or lists."""
    try:
        reading = shared.reading()
    except CratekitError as exc:
        return refused(kind, title, exc.cause)
    if reading.unread:
        return Step(key=kind, title=title, state=LISTED, detail=reading.unread)
    return reading


def _edits_fact(reading: Reading) -> str:
    from cratekit.modules.outbound import mirror_edits as edits

    if reading.unread:
        return reading.unread
    decisions = reading.decided.decisions
    if not decisions:
        return "no mirrored playlist was changed on the account since the mirror last finished it"
    count = Counter(one.outcome for one in decisions)
    carried = sum(count[kind] for kind in edits.CARRIED)
    return (
        f"{len(decisions)} edit(s) made on the account: {carried} taken into the "
        f"library by the rekordbox area's mirror-edits step, {count[edits.HELD]} held as "
        f"the account has them ({len(reading.decided.wanted)} of them for the "
        f"mirror-downloads step to queue), {count[edits.REKORDBOX]} where rekordbox's "
        f"change stands, {count[edits.AGREED]} where both sides agree"
    )


def _title(name: str) -> str:
    return f"mirror {name} onto the account"


def _listed(name: str, title: str, detail: str) -> Step:
    return Step(key=f"{MIRROR}:{name}", title=title, state=LISTED, detail=detail)


def add_steps(
    cfg: config.Config, area: Area, account_of: Callable[[], Any], run: Run | None = None,
    shared: Shared | None = None,
) -> None:
    """Plan every mirrored folder into ``area``, one step each.

    ``account_of`` is the area's lazy account; ``run`` is ``None`` for a plan that
    neither records, freezes nor rebuilds; ``shared`` is the run's one reading.
    """
    from cratekit.modules.outbound import ledger, mirror

    try:
        reading = shared.reading() if shared is not None else read(cfg, account_of, run)
    except CratekitError as exc:
        area.steps.append(refused(MIRROR, TITLE, exc.cause))
        return
    frozen, library, recorded = reading.frozen, reading.library, reading.recorded
    account, matcher = reading.account, reading.matcher
    settled: list[tuple[str, dict[str, tuple[str, frozenset[str]]]]] = []
    for folder in library.folders:
        key, title = f"{MIRROR}:{folder.name}", _title(folder.name)
        try:
            planned = mirror.plan(
                folder, account, recorded=recorded.get(folder.name), root=reading.root,
                matcher=matcher, holds=holds_for(reading, folder), listings=reading.listings,
            )
        except CratekitError as exc:
            area.steps.append(refused(key, title, exc.cause))
            continue
        settled.append((folder.name, mirror.settled(planned)))
        step = Step(
            key=key, title=title, state=PLANNED if planned.writes else NOTHING,
            detail=_detail(planned, folder), digest=digest_of(planned.identity()),
            counts=planned.counts(), items=planned.items(),
        )
        if planned.writes:
            step.apply = _apply(cfg, step, planned, account, matcher)
            # EVERY TRACK TAKEN OFF IS NAMED ON THE GATE (U143), and every
            # playlist removed, the INBOX folder's retired batch (U150).
            area.deletes.extend(
                f"{len(one.remove)} track(s) off the mirrored playlist {one.name!r}: "
                + "; ".join(one.removed_names)
                for one in planned.playlists
                if one.remove
            )
            area.deletes.extend(
                f"the mirrored playlist {name!r} ({remote_id}) off the account, since "
                f"what it mirrors left {folder.name}"
                for name, remote_id in planned.retire
            )
        area.steps.append(step)
    for name, cause in sorted(library.refused.items()):
        area.steps.append(refused(f"{MIRROR}:{name}", _title(name), cause))
    if library.favorites:
        area.steps.append(_listed(
            "favorites", "mirror the Favorites folder onto the account", f"not mirrored: {library.favorites}"
        ))
    if library.inbox:
        area.steps.append(_listed("inbox", "mirror INBOX onto the account", library.inbox))
    if library.wip:
        area.facts[WIP_FACT] = library.wip
    held = {folder.name for folder in library.folders} | set(library.refused)
    for name in sorted(set(recorded) - held):
        area.steps.append(_listed(
            name, _title(name), f"the library no longer holds a folder named {name!r}, so its mirror "
            f"is left on the account as it is and nothing is removed",
        ))
    if run is not None and run.record:
        # THE SNAPSHOT OF EACH PLAYLIST WITH NOTHING TO WRITE (U201), which no
        # apply records. A ledger that cannot take it leaves it as it was.
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
        f"{requests} account request(s) in {round(time.monotonic() - reading.started, 2)} s to "
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
        area.facts[FROZEN_FACT] = _record(cfg, run, reading, area)
    if run is not None and run.decided:
        area.stale.extend(_stale(area, frozen))


def _stale(area: Area, frozen: mirror_frozen.Frozen | None) -> list[str]:
    """What a stale answer says beside the digests (U222): each step that moved, and how the plan was made."""
    said: list[str] = []
    if frozen is not None and not frozen.shown:
        said.append(
            "what moved cannot be named: the plan frozen on this run was planned afresh "
            "by a run that applies, not shown by its gate"
        )
    elif frozen is not None:
        moved = mirror_frozen.moved(area.steps, frozen)
        said.append(
            "moved since the gate showed it: " + "; ".join(moved)
            if moved
            else "every step plans as the gate showed it"
        )
    said.extend(f"{name}: {area.facts[name]}" for name in (FROZEN_FACT, PLAN_FACT) if name in area.facts)
    return said


def _record(cfg: config.Config, run: Run, reading: Reading, area: Area) -> str:
    """Record what the plan learned and freeze it on the run; what the gate says of it.

    NEITHER FAILURE REFUSES THE PLAN: the apply refuses an unrecorded link itself,
    and an unfrozen plan is planned again. What is frozen is what the plan read and
    every step the gate shows (U222).
    """
    from cratekit.modules.outbound import ledger

    said = f"{reading.unfrozen}, so it was planned afresh; " if reading.unfrozen else ""
    matcher = reading.matcher
    try:
        ledger.record_mirror_links(cfg, matcher.fresh)
        ledger.record_mirror_misses(cfg, matcher.missed)
    except CratekitError as exc:
        return f"{said}not frozen: what the plan matched could not be recorded ({exc.cause.message})"
    try:
        return said + mirror_frozen.freeze(
            cfg, run.run_id, reading.library, matcher.seen,
            recorded=reading.recorded,
            steps=area.steps,
            # A RUN THAT APPLIES PLANNED THIS AFRESH, so no gate showed it.
            shown=not run.decided,
        )
    except OSError as exc:
        return f"{said}not frozen ({exc}), so the apply plans again"


__all__ = [
    "EDITS_FACT", "FROZEN_FACT", "KNOWN_FACT", "MIRROR", "MISSES_FACT", "PLAN_FACT", "WIP", "WIP_FACT",
    "Library", "Reading", "Run", "Shared", "add_steps", "file_signature", "holds_for",
    "identify", "landed_tracks", "read", "read_library",
]
