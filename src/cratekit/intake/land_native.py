"""The native medium of ``intake land`` (R-746): its gate screen, payload, write order and report.

``land_cli._land_native`` runs these steps in order: the planner, the write in
:func:`ask_then_write`'s order, the account archive, the owned hearts and the
notes a person reads after. ONE WORDING FOR EVERY VERB THAT ADDS A ROW (R-770):
``intake file`` reads the facts and the warnings here, through :mod:`land_cli`,
which answers every name of this module.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Callable, TypeVar

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import analysis_store, config, jobs, rb_writer, session
from cratekit.core.cause import CratekitError, Outcome, Remedy, refuse
from cratekit.intake import (
    account_playlists,
    batch_name,
    drift,
    filing,
    ingest,
    label_filing,
    landing,
    native,
    set_playlist,
    shelve,
)

_ORIGIN = ("intake.land_cli",)

#: What the apply marks each planned file.
LANDED = "landed"
REFUSED = "refused"

#: The one item a native landing appends for the batch playlist it wrote.
PLAYLIST = "playlist"

#: The item a native landing appends for each custom playlist twin it wrote (U149).
TWIN = "twin"

#: A planned twin the landing could not make, named with why (U149).
TWINS_LEFT = "custom-playlist-twins-left"

#: The item a native write appends for each favourites playlist it placed hearts in (U120).
FAVORITES = "favorites"

#: The notes a native landing carries about its hearts (U120).
FAVORITES_PLACED = "favorites-placed"
FAVORITES_SKIPPED = "favorites-placement-skipped"

#: A heart's row a person coloured otherwise, left and named (U153).
FAVORITES_COLOUR_HELD = "favorites-colour-held"

#: The rows are in the collection and rekordbox has not analysed them, which
#: it does on request and not on sight.
AWAITING_ANALYSIS = "rows-await-analysis"

#: The vox My Tag (U127): a file whose score could not be read, and a landing
#: that wrote no tag at all.
VOX_UNSCORED = "vox-unscored"
VOX_NOT_WRITTEN = "vox-not-written"

#: On the gate screen when more than half the added rows carry no voxlevel
#: (U181): the shape of a batch analysed while the vocal model could not load.
VOX_MOSTLY_UNSCORED = "vox-mostly-unscored"

#: A variable row with no dyn My Tag after the commit (U157), named so the
#: person still runs it with Dynamic.
DYN_NOT_WRITTEN = "dyn-not-written"

#: Why a set landing's account archive did not finish after the rows wrote (U129).
LAND_ARCHIVE_FAILED = "intake-land-archive-failed"

#: What a native write's answer is pinned to outside its digest (U161): the
#: database file the handle opened.
DATABASE_PIN = "database"


def _note(code: str, message: str) -> dict[str, str]:
    """One warning a person reads, by its code."""
    return {"code": code, "message": message}


def _plan(identity: dict[str, Any], items: list, count: int) -> dict[str, Any]:
    """A plan payload, closed at the four keys of ``plan/1``."""
    return {"digest": digest_of(identity), "items": items, "totals": {"count": count}, "chunk": None}


def split_facts(
    entries: list[tuple[str, str, int, int]], rest: int, *, left: int = 0
) -> dict[str, Any]:
    """The account playlists on a gate screen, each by the name it lands as (U113).

    ``entries`` are (name, account name, tracks, already owned); ``rest`` is
    what the batch playlist keeps and ``left`` the rows no INBOX playlist
    holds. ONE WORDING FOR BOTH MEDIA.
    """
    facts: dict[str, Any] = {
        "account playlists": [
            f"{name} ({count} file(s)"
            + (f", {owned} already in the library" if owned else "")
            + ")"
            + (f", the account's {account}" if account and name != account else "")
            for name, account, count, owned in entries
        ],
        "batch playlist holds": (
            f"{rest} file(s) no account playlist claimed"
            if rest
            else "nothing, so it is not written"
        ),
    }
    if left:
        facts["account playlist tracks left out"] = (
            f"{left} no INBOX playlist will hold, each named with why after the landing"
        )
    return facts


def _folder(rows: native.NativePlan) -> Path:
    """The folder a native landing's plan chose for its files (U164)."""
    if rows.folder is None:
        raise refuse(
            "internal-error",
            "a native landing's plan carries no folder to land in, so nothing was moved",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
        )
    return rows.folder


def _native_identity(
    planned: landing.Plan, rows: native.NativePlan, *, target: Path
) -> dict[str, Any]:
    """What the native gate digests: the folder, batch, target, files and rows."""
    return {
        "kind": "land-native",
        "folder": str(planned.folder),
        "batch": planned.batch,
        "target": str(target),
        "files": planned.digest,
        "collection": rows.digest,
    }


def _native_payload(planned: landing.Plan, rows: native.NativePlan, *, target: Path) -> dict:
    """The plan as the approval gate shows it: one item per file, with every column of its row.

    The digest covers the files, folder, batch and collection plan together,
    so an answer for one is stale for another. The database's path is not in
    it but on the screen and pinned (U161).
    """
    by_target = {str(row.target): row for row in rows.rows}
    hearts = (
        {str(one.target): one.month for one in rows.favorites.items}
        if rows.favorites is not None
        else {}
    )
    filed = label_filing.label_of(rows.labels) if rows.labels is not None else {}
    # U165: where adoption files each new row after the commit, by target.
    sorted_into = {str(one.target): one for one in rows.filing or ()}
    items = []
    for item in planned.items:
        row = by_target[str(target / item.name)]
        entry: dict[str, Any] = {
            "action": row.action, "from": str(item), "to": str(row.target), "row": row.columns()
        }
        if row.content_id is not None:
            entry["content_id"] = row.content_id
        if row.why:
            entry["why"] = row.why
        if str(row.target) in hearts:
            entry["heart"] = hearts[str(row.target)] or "month left to the backfill"
        if rows.labels is not None:
            # U156: the label playlist each file is filed in, or none.
            entry["label"] = filed.get(str(row.target), "none")
        if row.action == native.ADD and rows.vox_cut is not None and not rows.vox_blocked:
            # U127: the score each added row was read at and whether it is tagged.
            entry.update(voxlevel=row.voxlevel, vox=row.vox)
        if row.action == native.ADD and row.drift_verdict not in ("", drift.UNSCORED):
            # U157: the drift reading, its verdict and dyn tag; a file with no
            # reading is the fact line's to count.
            entry.update(drift=row.drift, drift_verdict=row.drift_verdict, dyn=row.dyn)
        if str(row.target) in sorted_into:
            entry["files into"] = sorted_into[str(row.target)].shown()
        items.append(entry)
    if rows.favorites is not None and rows.favorites.skipped:
        # THE SKIP IS AN ITEM OF THE PLAN, since ``plan/1``'s keys are closed.
        skipped = rows.favorites
        items.append(
            {"action": FAVORITES, "playlist": skipped.source_name, "skipped": skipped.skipped}
        )
    return _plan(_native_identity(planned, rows, target=target), items, len(planned.items))


def favorites_facts(plan: native.FavoritesPlan) -> dict[str, Any]:
    """The hearts on a gate screen, one line per fact (U120)."""
    if plan.skipped:
        return {"hearts": f"none placed, {plan.skipped}"}
    where = f"{plan.source_name!r} under {plan.folder_name!r}" if plan.folder_name else repr(plan.source_name)

    def counted(month: str) -> str:
        files = sum(1 for item in plan.items if item.month == month)
        held = sum(1 for one in plan.owned if one.month == month)
        said = f"{files} file(s)" + (f", {held} owned" if held else "")
        return f"{month} ({said})" + (", made" if month in plan.creates else "")

    hearts = f"{len(plan.items)} file(s) the account hearts"
    if plan.owned:
        hearts += f" and {len(plan.owned)} owned track(s)"
    facts: dict[str, Any] = {
        "hearts": f"{hearts}, into {where} and their month",
        "month playlists": [counted(month) for month in plan.months],
    }
    if plan.owned:
        # U146: the hearts on tracks the library already held, by title.
        facts["owned hearts"] = [f"{one.title}, {one.month}" for one in plan.owned]
    if plan.unknown:
        facts["month left to the backfill"] = (
            f"{plan.unknown} file(s) whose job froze no date, which join "
            f"{plan.source_name!r} here and take their month from crate favorites backfill"
        )
    # THE COLOUR (U153): landed hearts and uncoloured owned ones take Pink.
    if plan.colour_skipped:
        facts["rows to colour Pink"] = f"none, {plan.colour_skipped}"
    else:
        facts["rows to colour Pink"] = len(plan.items) + len(plan.colour)
    if plan.held:
        facts["colour held"] = [one.said() for one in plan.held]
    return facts


def collection_facts(rows: native.NativePlan) -> dict[str, Any]:
    """What a native plan writes, one line per fact, shared with ``intake file`` (R-770)."""
    stored = (
        f"under the base drive {rows.base_drive}, which rekordbox maps to {rows.current_drive}"
        if rows.base_drive and rows.current_drive and rows.base_drive != rows.current_drive
        else "under the mounted path"
    )
    analyze = f"found (row {rows.analyze_playlist_id})" if rows.analyze_playlist_id else "made"
    facts = {
        "playlist": f"{rows.playlist} under {rows.root_name} (row {rows.root_id})",
        "reads and writes": str(rows.database),
        "device": f"{rows.device_id} (master {rows.master_db_id})",
        "paths stored": stored,
        # U126: the value every added row is given, and the count behind it.
        "content link": (
            f"{rows.link.value}, carried by {rows.link.carriers} of the library's "
            f"{rows.link.rows} live rows"
            if rows.link is not None
            else "none, since no row is added"
        ),
        "left empty for rekordbox": list(native.LEFT_EMPTY),
        "adds": len(rows.to_add()),
        "already present": len(rows.present()),
        "vox My Tag": vox_fact(rows),
        "dyn My Tag": dyn_fact(rows),
        # U166: the one playlist every added row joins for the rekordbox visit.
        "analyze": (
            f"{rows.root_name} / {native.ANALYZE}, every added row, {analyze}"
            if rows.to_add()
            else "nothing, since no row is added"
        ),
    }
    if rows.set_job_id:
        facts["inbox playlist"] = rows.playlist
        if rows.batch_playlist_id:
            facts["inbox"] = (
                f"adds to the playlist an earlier landing of this set made "
                f"(row {rows.batch_playlist_id})"
            )
        elif rows.inbox_found_by_name:
            facts["inbox"] = "found live by name, not recorded"
        else:
            facts["inbox"] = "made"
    if rows.inbox_leftovers:
        facts["inbox leftovers"] = (
            "not joined automatically: "
            + ", ".join(repr(name) for name in rows.inbox_leftovers)
        )
    return facts


def vox_fact(rows: native.NativePlan) -> str:
    """The vox My Tag a native plan writes, in one line, for any verb's gate screen (U127)."""
    adding = rows.to_add()
    if not adding:
        return "none, since no row is added"
    if rows.vox_blocked:
        return f"none, {rows.vox_blocked}"
    unscored = len(rows.vox_unscored())
    return (
        f"{len(rows.vox_tagged())} of {len(adding)} added row(s), each whose voxlevel "
        f"is at or above the cut {rows.vox_cut:g}"
        + (f"; {unscored} file(s) carry no score and get no tag" if unscored else "")
    )


def vox_plan_warnings(rows: native.NativePlan, *, folder: Path) -> list[dict[str, str]]:
    """The gate screen's warning when most added rows carry no score, else none (U181).

    Most of a batch unscored is a batch analysed with no vocal model loaded,
    so it is a warning with its own code a caller can lift.
    """
    adding = rows.to_add()
    unscored = rows.vox_unscored()
    if not adding or 2 * len(unscored) <= len(adding):
        return []
    return [
        _note(
            VOX_MOSTLY_UNSCORED,
            f"{len(unscored)} of the {len(adding)} row(s) this landing adds carry "
            f"no voxlevel, so they join with no vox My Tag; a batch this unscored "
            f"was analysed with no vocal model loaded. Check crate doctor's "
            f"install.extras row, score them with crate analyze vocals --unscored "
            f"{folder}, then plan the landing again",
        )
    ]


def dyn_fact(rows: native.NativePlan) -> str:
    """The dyn My Tag a native plan writes, in one line, for any verb's gate screen (U157)."""
    adding = rows.to_add()
    if not adding:
        return "none, since no row is added"
    variable = len(rows.drift_variable())
    unscored = len(rows.drift_unscored())
    said = (
        f"{len(rows.dyn_tagged())} of {len(adding)} added row(s), each whose drift is at "
        f"or above the cut {rows.drift_cut:g} percent"
    )
    if rows.dyn_blocked:
        said = f"none of the {variable} variable row(s), {rows.dyn_blocked}"
    if unscored:
        said += f"; {unscored} file(s) carry no drift reading and get no tag"
    return said


def playlist_item(collection: native.NativeLanded) -> dict[str, Any]:
    """The one item a native write appends for the batch playlist it wrote."""
    return {
        "action": PLAYLIST, "playlist": collection.playlist, "id": collection.playlist_id,
        "tree": collection.tree_id, "session": collection.session_id,
    }


def _native_shown(rows: native.NativePlan, *, folder: Path, target: Path) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per fact."""
    shown = {
        "folder": str(folder),
        "lands in": str(target),
        **collection_facts(rows),
        "left in staging": len(rows.unsupported()),
    }
    if rows.set_playlist is not None:
        shown.update(set_playlist.facts(rows.set_playlist))
    if rows.playlists:
        claimed = {str(t) for one in rows.playlists for t in one.targets}
        written = [row for row in rows.rows if row.action != native.UNSUPPORTED]
        shown.update(
            split_facts(
                [(one.name, one.account_name, len(one.members), one.owned) for one in rows.playlists],
                sum(1 for row in written if str(row.target) not in claimed),
                left=sum(len(one.left) for one in rows.playlists) + len(rows.unplanned_left),
            )
        )
    if rows.favorites is not None:
        shown.update(favorites_facts(rows.favorites))
    if rows.labels is not None:
        shown.update(label_filing.facts(rows.labels))
    warned = vox_plan_warnings(rows, folder=folder)
    if warned:
        shown["warnings"] = warned
    if rows.twins:
        shown["custom playlist twins"] = twin_facts(rows.twins)
    return shown


def twin_facts(planned) -> str:
    """The landing's custom playlist twins (U149), one line: each made, each left and why."""
    said = [f"{one.folder.name} / {one.name}" for one in planned if not one.why]
    said.extend(f"{one.account_name} gets none: {one.why}" for one in planned if one.why)
    return "; ".join(said)


def _twin_notes(cfg: config.Config, rows, collection: native.NativeLanded) -> list[dict[str, str]]:
    """Pair each twin the commit wrote (U149), and name each planned twin it could not make."""
    from cratekit.sync import twins

    notes = twins.pair_landed(cfg, collection.twins)
    left = [one for one in (rows.twins if rows is not None else ()) if one.why]
    if left:
        notes.append(
            _note(
                TWINS_LEFT,
                f"{len(left)} account playlist(s) got no custom playlist twin: "
                + "; ".join(f"{one.account_name}: {one.why}" for one in left),
            )
        )
    return notes


def _native_reported(payload: dict, landed: landing.LandedNative) -> dict:
    """The plan, each item marked with what the apply actually did to it."""
    collection = landed.collection
    session_id = collection.session_id
    refused = {str(entry.path): entry for entry in landed.refused}
    added = {str(row.target): row for row in collection.added}
    present = {str(row.target): row for row in collection.present}
    items: list[dict[str, Any]] = []
    for item in payload["items"]:
        if item.get("action") == FAVORITES or item.get("area") == "account-archive":
            # Favourites (U120) and the archive (U129) are not file moves.
            items.append(item)
            continue
        entry = refused.get(item["from"])
        if entry is not None:
            items.append(
                {**item, "action": REFUSED, "reason": entry.reason, "why": entry.sentence}
            )
            continue
        row = added.get(item["to"])
        if row is not None:
            columns = {
                **item["row"], "Title": row.title, "FolderPath": row.folder_path,
                rb_writer.FILE_ID_COLUMN: row.file_id,
                rb_writer.CONTENT_LINK_COLUMN: row.content_link,
            }
            items.append(
                {
                    **item, "action": LANDED, "content_id": row.content_id, "row": columns,
                    "left_empty": sorted(row.empty),
                    **({"vox": row.vox} if "vox" in item else {}),
                    **({"dyn": row.dyn} if "dyn" in item else {}),
                }
            )
            continue
        held = present.get(item["to"])
        held_id = held.content_id if held is not None else item.get("content_id")
        items.append({**item, "action": LANDED, "content_id": held_id, "already_present": True})
    totals = {
        "count": payload["totals"]["count"], "landed": len(landed.moved),
        "refused": len(landed.refused), "added": len(collection.added),
        "already present": len(collection.present), "memberships": collection.memberships_added,
    }
    # WHAT ADOPTION READS BACK, not what the writer counted (U127, U157).
    voxed = sum(1 for row in landed.collection.added if row.vox)
    if voxed:
        totals["vox tagged"] = voxed
    dyned = sum(1 for row in collection.added if row.dyn)
    if dyned:
        totals["dyn tagged"] = dyned
    if collection.playlist_id:
        items.append(playlist_item(collection))
    items.extend(
        {
            "action": PLAYLIST, "playlist": written.name, "id": written.playlist_id,
            "account": written.account, "count": written.tracks, "tree": collection.tree_id,
            "session": session_id,
        }
        for written in collection.playlists
    )
    items.extend(
        {
            "action": TWIN, "playlist": f"{twin.folder} / {twin.name}", "id": twin.playlist_id,
            "account_id": twin.account_id, "count": twin.tracks, "session": session_id,
        }
        for twin in collection.twins
    )
    placed = collection.favorites
    if placed is not None:
        totals["hearts placed"] = placed.added
        items.append(
            {
                "action": FAVORITES, "playlist": placed.source_name, "id": placed.source_id,
                "count": placed.added_source, "session": session_id,
            }
        )
        items.extend(
            {
                "action": FAVORITES, "playlist": name, "id": row, "count": count,
                "created": name in placed.created, "session": session_id,
            }
            for name, row, count in placed.months
        )
    kept = collection.set_playlist
    if kept is not None:
        if kept.playlist_id:
            items.append(set_playlist_item(kept, session_id=session_id))
        totals["set playlist tracks"] = kept.members
        totals["set playlist left out"] = len(kept.left)
    filed = collection.labels
    if filed is not None:
        items.extend(
            label_filing.item(one, tree=filed.tree_id, session_id=session_id)
            for one in filed.years
        )
        totals["label playlists"] = len(filed.years)
        totals["label memberships"] = filed.added()
        totals["filed under no label"] = len(filed.left)
    return {**payload, "items": items, "totals": totals}


def set_playlist_item(kept: set_playlist.Written, *, session_id: str) -> dict[str, Any]:
    """The one item a write appends for the set's permanent playlist (U121)."""
    return {
        "action": PLAYLIST, "playlist": kept.name, "id": kept.playlist_id,
        "folder": kept.folder_id, "folder_created": kept.folder_created,
        "playlist_created": kept.playlist_created, "count": kept.members, "added": kept.added,
        "left": [one.identity() for one in kept.left], "session": session_id,
    }


def _with_filing(reported: dict, filed: filing.Filed) -> dict:
    """The landed payload with what the filing after it did, in its totals (U165);
    each item already says where it files in its ``files into``."""
    totals = {**reported["totals"], "filing": filed.state}
    if filed.state == filing.FILED:
        totals.update(
            {
                "filed": filed.filed,
                "filing memberships": filed.memberships,
                "placed nowhere": len(filed.nowhere),
            }
        )
    return {**reported, "totals": totals}


def favorites_notes(payload: dict, collection: native.NativeLanded) -> list[dict[str, str]]:
    """What a person reads about the hearts a landing placed, or did not (U120).

    ON THE WARNINGS CHANNEL, since the default renderer prints no json block
    (R-424).
    """
    skipped = next(
        (
            str(item.get("skipped") or "")
            for item in payload.get("items", ())
            if item.get("action") == FAVORITES and item.get("skipped")
        ),
        "",
    )
    if skipped:
        return [
            {
                "code": FAVORITES_SKIPPED,
                "message": (
                    f"the batch landed and no heart was placed: {skipped}; run crate "
                    f"favorites backfill once the playlist exists"
                ),
            }
        ]
    placed = collection.favorites
    if placed is None:
        return []
    return [_note(FAVORITES_PLACED, placed.said()), *_colour_notes(placed)]


def _colour_notes(placed) -> list[dict[str, str]]:
    """The colour's notes (U153): the held rows and the missing Pink row the
    gate screen showed, with files or owned hearts alone."""
    from cratekit.favorites import colour as colour_mod  # noqa: PLC0415 - favorites is toggleable

    notes = []
    if placed.colour_skipped:
        notes.append(
            {
                "code": colour_mod.PINK_COLOUR_MISSING,
                "message": (
                    f"no row is coloured: {placed.colour_skipped}; the hearts are "
                    f"placed all the same, and crate favorites backfill colours them "
                    f"once the library carries Pink again"
                ),
            }
        )
    if placed.held:
        notes.append(
            _note(
                FAVORITES_COLOUR_HELD,
                f"{len(placed.held)} row(s) carry a colour a person chose and keep it: "
                + "; ".join(one.said() for one in placed.held),
            )
        )
    return notes


#: The visit's short path (U319): with Auto Analysis on, a launch in front
#: raises one dialog whose OK analyses every waiting row on the preference's
#: own mode, so a dyn row still takes Dynamic. Said after the selections, so
#: "as above" names them. ``cli.tail`` spells the same, held to this by a test.
AUTO_ANALYSIS_STEP = (
    "or, with Auto Analysis on, open rekordbox with its window in front and press OK "
    "on its Auto Analysis dialog only when it shows every one of those Normal "
    "settings with Vocal and CUE off and no field set otherwise, else Cancel it and "
    "select as above; Auto Analysis runs on its preference's own mode, so the rows "
    f"carrying the dyn My Tag still take Analyze Tracks with {drift.DYNAMIC_SETTINGS}"
)


def awaiting_analysis(collection: native.NativeLanded) -> list[dict[str, str]]:
    """The warning a native write carries when rows joined the collection, else none.

    ONE PLAYLIST, ANALYZE (U166), holding every waiting row; TWO SELECTIONS in
    it, Normal and Dynamic by the dyn My Tag (U157); and the Auto Analysis
    path beside them (U319).
    """
    if not collection.added:
        return []
    dyned = sum(1 for row in collection.added if row.dyn)
    normal = len(collection.added) - dyned
    selections = (
        f"run Analyze Tracks on the {normal} row(s) without the dyn My Tag with "
        f"{drift.NORMAL_SETTINGS}, and on the {dyned} row(s) carrying it with "
        f"{drift.DYNAMIC_SETTINGS}"
    )
    return [
        {
            "code": AWAITING_ANALYSIS,
            "message": (
                f"{len(collection.added)} row(s) joined the collection with no "
                f"tempo, grid, key or waveform, and rekordbox analyses nothing on its "
                f"own with Auto Analysis off; open rekordbox, select the "
                f"{collection.analyze_name} playlist, which holds every row waiting "
                f"for analysis, and {selections}; {AUTO_ANALYSIS_STEP}; then "
                f"crate inbox analyzed takes out each row rekordbox analysed"
            ),
        }
    ]


def dyn_warnings(collection: native.NativeLanded) -> list[dict[str, str]]:
    """What a person reads when a variable row did not get the dyn My Tag (U157), else none.

    Such a row would take Normal from a person selecting by the mark, so each
    is named with why. A file with no drift reading is the screen's to count.
    """
    if not collection.added:
        return []
    untagged = set(collection.dyn_missing)
    if collection.dyn_blocked:
        untagged.update(collection.dyn_variable)
    if not untagged:
        return []
    if collection.dyn_blocked:
        why = collection.dyn_blocked
    elif collection.dyn_unread:
        why = f"the tag could not be read back as crate analyze check reads it: {collection.dyn_unread}"
    else:
        why = (
            f"the {native.DYN_VALUE} value it was written under is one rekordbox removed; "
            f"check the {native.DYN_CATEGORY} My Tag category in rekordbox"
        )
    names = ", ".join(path.name for path in collection.dyn_variable if path in untagged)
    return [
        _note(
            DYN_NOT_WRITTEN,
            f"{len(untagged)} row(s) whose tempo moves do not carry the dyn My Tag, "
            f"so select them by name and run Analyze Tracks on them with "
            f"{drift.DYNAMIC_SETTINGS}: {names}; {why}",
        )
    ]


def vox_warnings(collection: native.NativeLanded) -> list[dict[str, str]]:
    """What a person reads about the vox My Tag a native write gave its rows, or did not (U127).

    A file with no score is named, never tagged on a guess; a landing that
    could tag nothing says why and names the step owed.
    """
    if not collection.added:
        return []
    warnings: list[dict[str, str]] = []
    if collection.vox_missing:
        # PLANNED, WRITTEN, AND NOT WHAT ADOPTION READS: said, never reported.
        why = (
            f"the tag could not be read back as adoption reads it: {collection.vox_unread}"
            if collection.vox_unread
            else (
                "the Vocals My Tag category or its vox value it was written under "
                "is one rekordbox removed; check the Vocals category in rekordbox"
            )
        )
        names = ", ".join(path.name for path in collection.vox_missing)
        warnings.append(
            _note(
                VOX_NOT_WRITTEN,
                f"{len(collection.vox_missing)} row(s) planned for the vox My Tag "
                f"do not carry it, so they reach no with vox playlist: {names}; {why}",
            )
        )
    if collection.vox_blocked:
        said = "no row joined with the vox My Tag, so none reaches a with vox playlist: "
        return [*warnings, _note(VOX_NOT_WRITTEN, said + collection.vox_blocked)]
    if not collection.vox_unscored:
        return warnings
    names = ", ".join(path.name for path in collection.vox_unscored)
    return [
        *warnings,
        _note(
            VOX_UNSCORED,
            f"{len(collection.vox_unscored)} file(s) carry no voxlevel to read, so "
            f"their rows got no vox My Tag: {names}; run crate analyze vocals on "
            f"them and then crate metadata mytags-vocals --apply",
        ),
    ]


def unfiled_reason(ctx, medium: ingest.IntakeMedium) -> str:
    """Why the landing files nothing after it, empty when it files (U165).

    Asked with ``--land-only``, or a routing tree still on the bridge, where no
    database writer may write its membership and a filing could only end refused.
    """
    declared = medium.declared
    return (
        "asked with --land-only"
        if getattr(ctx.args, "land_only", False)
        else (
            ""
            if medium.files_natively
            else (
                f"the tree {declared.tree.id!r} is on the xml bridge; cut it over with "
                f"crate tree cutover {declared.tree.id}"
            )
        )
    )


def read_set(ctx) -> tuple[jobs.Job | None, set_playlist.SetWords | None, tuple[dict, ...]]:
    """The set job, its words and its reports, read before the gate (U121).

    A job that is not a finished set, and a name the page and the flags cannot
    complete, refuse with the files still in staging and nothing shown.
    """
    if not ctx.args.set_job:
        return None, None, ()
    with jobs.open_store() as store:
        set_job = set_playlist.set_job_or_refuse(store, str(ctx.args.set_job))
        words = set_playlist.words_for(
            set_job, dj=ctx.args.dj, set_name=ctx.args.set_name, set_date=ctx.args.set_date
        )
        return set_job, words, set_playlist.reports_of(store, set_job)


def native_planner(
    ctx, medium: ingest.IntakeMedium, *, manifest: landing.LabelManifest | None,
    label: str | None, label_from_tags: bool, claims: tuple[account_playlists.Claim, ...],
    hearted: tuple[account_playlists.Hearted, ...], owned: tuple[account_playlists.HeartRow, ...],
    unfiled: str, set_job: jobs.Job | None, words: set_playlist.SetWords | None,
    reports: tuple[dict[str, Any], ...], set_planned: list[set_playlist.SetPlaylistPlan],
) -> Callable[[config.Config, landing.Plan], Callable[[Any], native.NativePlan]]:
    """The landing's planner: given a library and its staged files, a plan made on a handle.

    ONE PLANNER, TWO PLACES (U162): the live landing and its rehearsal's
    scratch area plan through this same code. Each set plan made is appended
    to ``set_planned``.
    """
    declared, registry = medium.declared, medium.registry
    tree_id = declared.intake.id

    def planner(cfg: config.Config, planned: landing.Plan) -> Callable[[Any], native.NativePlan]:
        def set_plan(db, files) -> set_playlist.SetPlaylistPlan | None:
            if set_job is None or words is None:
                return None
            made = set_playlist.plan_for_landing(
                cfg, db, declared, set_job, words, reports, files=files,
                posted=getattr(ctx.args, "posted", None),
            )
            set_planned.append(made)
            return made

        def label_plan(db, files) -> label_filing.LabelPlan | None:
            # A MANIFEST WITH NO LABEL ROW FILES NOTHING, as on the bridge.
            if manifest is not None and manifest.rows:
                return label_filing.plan_for_manifest(
                    cfg, db, medium, manifest=manifest, files=files
                )
            if label is not None:
                return label_filing.plan_for_label(db, medium, label=label, files=files)
            if label_from_tags:
                return label_filing.plan_for_tags(db, medium, files=files)
            return None

        def plan(db) -> native.NativePlan:
            # THE FILED FOLDER, CHOSEN ON THIS HANDLE (U164), so every row
            # carries its final FolderPath from the first commit.
            target = shelve.landing_target(cfg, db, planned.batch, on=batch_name.today())
            files = [(item, target / item.name) for item in planned.items]
            # THE INBOX PLAYLIST FOR A SET (U135): named for the set, and an
            # earlier landing's playlist of the job is added to; the batch
            # folder keeps the landing's own name, so only the playlist joins.
            inbox_name, batch_playlist_id, set_job_id = planned.batch, "", ""
            leftovers: tuple[str, ...] = ()
            inbox_found_by_name = False
            if set_job is not None and words is not None:
                set_job_id = set_job.job_id
                root_id = native.anchored_intake_root(db, tree_id, registry)
                recorded = native.recorded_inbox_playlist(cfg, db, set_job_id, root_id)
                if recorded is not None:
                    batch_playlist_id, inbox_name = recorded
                else:
                    inbox_name = set_playlist.frozen_name(set_job) or set_playlist.playlist_name(
                        words
                    )
                    inbox_found_by_name = native.live_inbox_named(db, inbox_name, root_id)
                leftovers = native.leftover_set_inbox(
                    cfg, db, set_job_id, root_id, inbox_name, keep_id=batch_playlist_id
                )
            split, emptied = _native_split(
                db, cfg, claims, tree_id=tree_id, registry=registry, batch=inbox_name, target=target
            )
            # EACH UNPAIRED ACCOUNT PLAYLIST'S TWIN (U149), on this handle.
            from cratekit.favorites import backfill, placement  # noqa: PLC0415 - toggleable
            from cratekit.modules.outbound import pairs
            from cratekit.sync import twins

            landing_twins = twins.plan_landing(
                db, [(one.account, one.account_name or one.name) for one in split],
                year=batch_name.today().year, paired=pairs.PairStore(cfg).all(),
            )
            made = native.plan_rows(
                cfg, db, tree_id=tree_id, registry=registry, batch=inbox_name, files=files,
                split=split, unplanned_left=emptied, pass_name=ctx.args.pass_name,
                hearts=tuple(
                    native.HeartItem(target=target / one.path.name, month=one.month, ref=one.ref)
                    for one in hearted
                ),
                favorites_source=placement.source_name(declared),
                owned_hearts=tuple(
                    native.OwnedHeartItem(
                        content_id=one.content_id, month=one.month, ref=one.ref, title=one.title
                    )
                    for one in backfill.owned_in_library(cfg, db, owned)
                ),
                set_plan=set_plan(db, files), batch_playlist_id=batch_playlist_id,
                set_job_id=set_job_id, inbox_leftovers=leftovers,
                inbox_found_by_name=inbox_found_by_name, labels=label_plan(db, files),
                twins=landing_twins,
            )
            made = replace(made, folder=target, batch=planned.batch)
            # WHERE EACH NEW ROW WILL BE FILED (U165), digested, so the one
            # answer covers the filing after the commit.
            if unfiled:
                return made
            return native.with_filing(made, filing.predict(declared, made.to_add()))

        return plan

    return planner


def landed_warnings(
    cfg: config.Config, payload: dict, landed: landing.LandedNative, *,
    applied: list[native.NativePlan], archive_notes: list[dict[str, str]],
    set_planned: list[set_playlist.SetPlaylistPlan],
) -> list[dict[str, str]]:
    """What a person reads after a native landing wrote, in the order it is said."""
    warnings = [_note(entry.reason, entry.sentence) for entry in landed.refused]
    warnings.extend(account_playlists.left_warning(landed.collection.left))
    warnings.extend(_twin_notes(cfg, applied[-1] if applied else None, landed.collection))
    warnings.extend(awaiting_analysis(landed.collection))
    warnings.extend(vox_warnings(landed.collection))
    warnings.extend(dyn_warnings(landed.collection))
    warnings.extend(favorites_notes(payload, landed.collection))
    warnings.extend(archive_notes)
    if set_planned:
        # ONCE PER RUN, from the first plan: the write takes the plan again.
        warnings.extend(set_playlist.ignored_note(set_planned[0]))
    kept = landed.collection.set_playlist
    if kept is not None and kept.playlist_id:
        set_playlist.assert_read_back(kept)
        warnings.extend(set_playlist.written_note(kept))
        warnings.extend(set_playlist.left_warning(kept.left))
    elif kept is not None and set_planned:
        # NOTHING WRITTEN; the left rows are the write's own answer.
        warnings.extend(set_playlist.nothing_note(set_planned[0], left=len(kept.left)))
        warnings.extend(set_playlist.left_warning(kept.left))
    filed = landed.collection.labels
    if filed is not None:
        label_filing.assert_read_back(filed)
        warnings.extend(label_filing.unfiled_warning(filed.left))
    return warnings


def _native_split(
    db, cfg: config.Config, claims: tuple[account_playlists.Claim, ...], *, tree_id: str,
    registry, batch: str, target: Path,
) -> tuple[tuple[native.PlaylistPlan, ...], tuple[tuple[str, account_playlists.Left], ...]]:
    """Each account playlist named against the database's INBOX, on the write handle.

    AND EACH OWNED TRACK'S ROW FOUND BY PATH ON THE SAME HANDLE (U128), so the
    digest names the rows the apply adds. Answers the playlists and the left
    rows of the ones left holding nothing.
    """
    if not claims:
        return (), ()
    held = native.inbox_held(db, native.anchored_intake_root(db, tree_id, registry))
    named = account_playlists.named(claims, held, batch=batch)
    names = {Path(path).name for one in named for member in one.members for path in member.paths}
    resolved, emptied = account_playlists.resolve_owned(
        cfg, named, native.candidate_rows(db, names)
    )
    return (
        tuple(
            native.PlaylistPlan(
                name=claimed.name, account=claimed.playlist_id, account_name=claimed.account_name,
                left=claimed.left, members=tuple(
                    native.PlaylistMember(target=target / member.file.name, member=member)
                    if member.file is not None
                    else native.PlaylistMember(content_id=member.row, member=member)
                    for member in claimed.members
                ),
            )
            for claimed in resolved
        ),
        emptied,
    )


def _apply_landing_archive(cfg, archived) -> list[dict[str, str]]:
    """Apply the account archive after the landing wrote. Failures are warnings,
    since the rows are already in the library."""
    if archived is None or not archived.writes:
        return []
    from cratekit.export import set_cli

    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:
        message = (
            exc.cause.message if isinstance(exc, CratekitError) else f"{type(exc).__name__}: {exc}"
        )
        return [
            {
                "code": LAND_ARCHIVE_FAILED,
                "message": (
                    f"the account archive could not finish after the landing wrote "
                    f"({message}); the batch is in the library, run crate export "
                    f"archive over the set once the account can be reached"
                ),
            }
        ]
    return list(warnings)


def _with_archive(payload: dict, archived) -> dict:
    """Fold the archive plan into the landing's digest and items so one approval covers both."""
    if archived is None:
        return payload
    identity = {
        "land": payload["digest"],
        "archive": archived.payload["digest"],
    }
    items = list(payload.get("items") or [])
    items.extend({**item, "area": "account-archive"} for item in archived.payload.get("items") or [])
    totals = {**(payload.get("totals") or {}), "archive_writes": bool(archived.writes)}
    return {**payload, "digest": digest_of(identity), "items": items, "totals": totals}


#: What a native write plans: a landing's rows, or the owned hearts alone (U146).
_Planned = TypeVar("_Planned")


def ask_then_write(
    ctx, cfg: config.Config, spec, *, plan: Callable[[Any], _Planned],
    payload: Callable[[_Planned], dict], shown: Callable[[_Planned], dict[str, Any]],
    write: Callable[[Any, _Planned], Any],
) -> tuple[dict, Any | None]:
    """The order every native intake write keeps, held once. Answers (payload, written).

    Shared by the landing, its owned hearts (U146) and ``intake file`` (R-770),
    because the order is the contract:

    * THE DATABASE IS OPENED WITH WRITE INTENT BEFORE THE PLAN, so a running
      rekordbox refuses before anything is shown;
    * THE ACKNOWLEDGMENT IS READ BEFORE THE GATE (R-733), so an approval is
      never refused by what could have been read first;
    * only ``apply`` writes, and the handle is closed whatever happened;
    * THE ANSWER IS PINNED TO THE FILE THE HANDLE OPENED (U161), since the
      digest names the library, not the file.

    ``written`` is None when the answer was not ``apply``.
    """
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        rows = plan(db)
        data = payload(rows)
        session.assert_backup_acknowledged(cfg)
        opened = rb_writer.handle_path(db) or rb_writer.live_db_path(cfg)
        option = ctx.gate.require(
            spec, plan=data, context=shown(rows), pinned={DATABASE_PIN: str(opened)}
        )
        if option != "apply":
            return data, None
        return data, write(db, rows)
    finally:
        rb_writer.close_db(db)


def _place_owned(
    ctx, cfg: config.Config, spec, *, declared, owned: tuple[account_playlists.HeartRow, ...],
    empty: dict,
) -> Envelope:
    """The pass's owned hearts All Favorites lacks, placed when no file was downloaded (U146).

    THE LANDING'S GATE AND THE BACKFILL'S WRITER. Asked first of a read handle,
    so a pass whose hearts are all placed opens nothing to write and ends
    NO_OP; otherwise in :func:`ask_then_write`'s order. A library with no All
    Favorites, or two, is not a refusal: the pass ends NO_OP and says why.
    """
    from cratekit.favorites import backfill, placement  # noqa: PLC0415 - favorites is toggleable

    source = placement.source_name(declared)
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        first = backfill.plan_owned(cfg, db, source=source, rows=owned)
    except CratekitError as exc:
        if exc.cause.reason != placement.SOURCE_MISSING:
            raise
        return ctx.envelope(
            data=empty,
            outcome=Outcome.NO_OP,
            warnings=[
                _note(
                    FAVORITES_SKIPPED,
                    f"nothing to land and no owned heart was placed: "
                    f"{exc.cause.message}; run crate favorites backfill once the "
                    f"playlist exists",
                )
            ],
        )
    finally:
        rb_writer.close_db(db)
    if not first.writes:
        return ctx.envelope(data=empty, outcome=Outcome.NO_OP)

    def written(db, approved: backfill.BackfillPlan) -> backfill.Backfilled:
        return backfill.apply(
            cfg, db, approved, source=source, analysis_roots=analysis_store.watch_roots(cfg)
        )

    payload, done = ask_then_write(
        ctx, cfg, spec, plan=lambda db: backfill.plan_owned(cfg, db, source=source, rows=owned),
        payload=lambda planned: backfill.payload(planned, cfg), shown=backfill.landing_facts,
        write=written,
    )
    if done is None:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    backfill.assert_read_back(done)
    placed = done.placed
    totals = {**payload["totals"], "hearts placed": placed.added}
    said = (
        f"{placed.said()}, for {len(payload['items'])} owned heart(s); no file "
        f"was landed; undo with a restore of session {done.session_id}"
    )
    warnings = [_note(FAVORITES_PLACED, said), *_colour_notes(placed)]
    return ctx.envelope(data={**payload, "totals": totals}, warnings=warnings)
