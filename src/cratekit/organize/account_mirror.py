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


def _rows(db: Any, playlist_id: str) -> tuple[mirror.Row, ...]:
    from cratekit.acquire import match
    from cratekit.write import playlist_pair

    return tuple(
        mirror.Row(
            content_id=row.content_id,
            title=row.title,
            artist=row.artist,
            isrc=match.isrc_token(row.isrc),
            path=row.path,
        )
        for row in playlist_pair.members(db, playlist_id)
    )


def _children(db: Any, parent_id: str) -> list[Any]:
    """The live rows directly under one node, the binding's query materialized."""
    from cratekit.core import rb_writer

    gone = rb_writer.node_removed
    return [row for row in list(db.get_playlist(ParentID=str(parent_id))) if not gone(row)]


def _plain(row: Any) -> bool:
    return int(getattr(row, "Attribute", -1) or 0) == 0


def _folder(db: Any, name: str, parent_id: str, titled: Callable[[str], str]) -> mirror.Folder | Cause:
    """One rekordbox folder as a mirror, or the refusal of a title two playlists take."""
    playlists = sorted(
        (row for row in _children(db, parent_id) if _plain(row)),
        key=lambda row: (str(row.Name), str(row.ID)),
    )
    sources: list[mirror.Source] = []
    taken: dict[str, int] = {}
    for row in playlists:
        name_of = titled(str(row.Name))
        taken[name_of] = taken.get(name_of, 0) + 1
        sources.append(mirror.Source(name=name_of, rows=_rows(db, str(row.ID))))
    twice = sorted(one for one, count in taken.items() if count > 1)
    if twice:
        return _twice(name, f"its playlists {', '.join(repr(one) for one in twice)}")
    return mirror.Folder(name=name, playlists=tuple(sources))


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


def _inbox(cfg: config.Config, db: Any, declared: Any, registry: Any) -> tuple[str, mirror.Folder | Cause | str]:
    """INBOX as a retiring mirror folder, the refusal of a title two batches take, or why not.

    Answers ``(name, folder or refusal)``, or ``("", why)`` when the intake
    tree cannot be read as database native, which lists INBOX and mirrors
    nothing of it, so no retirement is planned over a tree nobody read.
    """
    from datetime import date

    from cratekit.intake import rotate

    try:
        live = rotate.live_batches(
            cfg, db, declared=declared, registry=registry, today=date.today()
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
    )


def read_library(cfg: config.Config) -> Library:
    """Every folder to mirror, read on a read handle that is closed before returning."""
    from cratekit.core import active_taxonomy, rb_writer, tree_registry
    from cratekit.favorites import placement

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
                (name, _folder(db, name, str(row.ID), lambda shown, name=name: mirror.title(name, shown)))
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

                found.append((name, _folder(db, name, home.folder_id, titled)))
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


def add_steps(
    cfg: config.Config, area: Area, account_of: Callable[[], Any], run: Run | None = None
) -> None:
    """Plan every mirrored folder into ``area``, one step each.

    ``account_of`` is the area's own lazy account, so a refusal to resolve it
    is this kind's refusal with its own reason. ``run`` is the organize run,
    or ``None`` for a plan that neither records, freezes nor rebuilds.
    """
    started = time.monotonic()
    frozen, unfrozen = None, ""
    if run is not None and run.decided:
        frozen, unfrozen = mirror_frozen.load(cfg, run.run_id)
    try:
        library = frozen.library if frozen is not None else read_library(cfg)
        # A FROZEN PLAN CARRIES EVERY ROW'S ANSWER ALREADY, so its rebuild
        # reads no landing record and asks the provider about no row.
        known = landed_tracks(cfg) if frozen is None else {}
        recorded = ledger.mirror_folders(cfg)
        links = ledger.mirror_links(cfg)
        misses = ledger.mirror_misses(cfg)
        account = mirror.Counted(account_of())
        root = account.folders()
    except CratekitError as exc:
        area.steps.append(refused(MIRROR, TITLE, exc.cause))
        return
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
    for folder in library.folders:
        key = f"{MIRROR}:{folder.name}"
        title = f"mirror {folder.name} onto the account"
        try:
            planned = mirror.plan(
                folder, account, recorded=recorded.get(folder.name), root=root, matcher=matcher
            )
        except CratekitError as exc:
            area.steps.append(refused(key, title, exc.cause))
            continue
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
    requests, _seconds = account.lap()
    read = "read the account and rebuild" if frozen is not None else "read the library and the account and plan"
    area.facts[PLAN_FACT] = (
        f"{requests} account request(s) in {round(time.monotonic() - started, 2)} s to "
        f"{read} {len(library.folders)} folder(s)"
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
    "FROZEN_FACT",
    "KNOWN_FACT",
    "MIRROR",
    "MISSES_FACT",
    "PLAN_FACT",
    "Library",
    "Run",
    "add_steps",
    "file_signature",
    "identify",
    "landed_tracks",
    "read_library",
]
