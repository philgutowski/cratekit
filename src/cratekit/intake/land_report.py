"""What ``intake land`` shows and reports: gate screens, payloads, the landed report and its notes.

Split out of :mod:`cratekit.intake.land_cli`, which re-exports every name a
caller reads there. ONE WORDING FOR EVERY VERB THAT ADDS A ROW (R-770):
``intake file`` reads the facts and the warnings here, so the two verbs
cannot say the same thing two ways.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config, drift, rb_writer
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.intake import account_playlists, filing, label_filing, landing, native, set_playlist
from cratekit.write import metadata_cli

_ORIGIN = ("intake.land_cli",)

#: The action every planned file carries until the apply reports on it.
LAND = "land"
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
#: What a label playlist written, and a label row filed under none, are marked.
FILED = "filed"
UNFILED = "unfiled"

#: The notes a native landing carries about its hearts (U120).
FAVORITES_PLACED = "favorites-placed"
FAVORITES_SKIPPED = "favorites-placement-skipped"
#: A heart's row a person coloured otherwise, left and named (U153).
FAVORITES_COLOUR_HELD = "favorites-colour-held"

#: The warning a native landing carries: the rows are in the collection and
#: rekordbox has not analysed them, which it does on request and not on sight.
AWAITING_ANALYSIS = "rows-await-analysis"
#: The warnings a native write carries about the vox My Tag (U127): a file
#: whose score could not be read, and a landing that wrote no tag at all.
VOX_UNSCORED = "vox-unscored"
VOX_NOT_WRITTEN = "vox-not-written"
#: On the GATE SCREEN when more than half the added rows carry no voxlevel
#: (U181): the shape of a batch analysed while the vocal model could not load.
VOX_MOSTLY_UNSCORED = "vox-mostly-unscored"
#: A row whose drift read as variable and carries no dyn My Tag after the
#: commit (U157), named so the person still runs it with Dynamic.
DYN_NOT_WRITTEN = "dyn-not-written"

#: What the bridge's gate screen says of the vox My Tag (U127), on a
#: calibrated library; :func:`bridge_vox_fact` says the rest.
BRIDGE_VOX_NONE = "not written, the xml bridge carries no My Tag"
BRIDGE_VOX_OWED = (
    f"{BRIDGE_VOX_NONE}; once rekordbox has imported the batch, run crate metadata "
    f"mytags-vocals --apply to tag its vocal tracks"
)


def _payload(
    planned: landing.Plan,
    *,
    target: Path,
    destination: Path,
    export: Path,
    manifest: landing.LabelManifest | None = None,
    split: tuple[account_playlists.Claimed, ...] = (),
    emptied: tuple[tuple[str, account_playlists.Left], ...] = (),
) -> dict:
    items = [
        {"action": LAND, "from": str(item), "to": str(target / item.name)} for item in planned.items
    ]
    identity = {
        "kind": "land",
        "folder": str(planned.folder),
        "batch": planned.batch,
        "target": str(target),
        "destination": str(destination),
        "export": str(export),
        "files": planned.digest,
    }
    if manifest is not None:
        # Only when one is given, so a landing without a manifest is compared
        # exactly as it was before the manifest existed.
        # The bytes and not only the path: a manifest rewritten under the same
        # name files other tracks under other labels, and a digest of the name
        # would call that the plan the person saw.
        identity["manifest"] = str(manifest.path)
        identity["manifest_bytes"] = manifest.digest
    if split:
        # Only when there is one, for the manifest's reason: a landing that
        # splits nothing is compared exactly as it was before U113. Another
        # split, or another name for one playlist, is another plan.
        identity["playlists"] = [claimed.identity() for claimed in split]
    if emptied:
        # The left rows of an account playlist that holds nothing (U128).
        identity["unplanned_left"] = [[name, row.identity()] for name, row in emptied]
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {"count": len(items)},
        "chunk": None,
    }


def _shown(
    planned: landing.Plan,
    *,
    cfg: config.Config,
    target: Path,
    destination: Path,
    manifest: landing.LabelManifest | None = None,
    split: tuple[account_playlists.Claimed, ...] = (),
    emptied: int = 0,
) -> dict[str, Any]:
    """What the gate screen puts in front of the person, one line per fact."""
    shown: dict[str, Any] = {
        "folder": str(planned.folder),
        "lands in": str(target),
        "playlist": planned.batch,
        "intake file": str(destination),
        "count": len(planned.items),
        "files": [item.name for item in planned.items],
        # U127: the xml bridge carries no My Tag, so the vox tag a native
        # landing writes is a step this one leaves owed, said before the
        # approval rather than discovered in a with vox playlist missing it.
        "vox My Tag": bridge_vox_fact(cfg),
    }
    if split:
        shown.update(
            split_facts(
                [(one.name, one.account_name, len(one.members), one.owned) for one in split],
                len(account_playlists.unclaimed(planned.items, split)),
                left=sum(len(one.left) for one in split) + emptied,
            )
        )
    if manifest is not None:
        # What the manifest ASKS for, since which rows have a file in this
        # batch is known only once the batch folder can be indexed.
        shown["labels filed from"] = str(manifest.path)
        shown["label playlists named"] = [
            f"{name} ({count} listed)" for name, count in sorted(manifest.playlists().items())
        ]
    return shown


def bridge_vox_fact(cfg: config.Config) -> str:
    """What the bridge's gate screen says of the vox My Tag (U127), by the calibration.

    THE STEP OWED IS ONLY NAMED WHERE IT WOULD TAG FROM A FITTED CUT. The vocals
    verb tags from the default cut on a library with none, which the native
    landing refuses to do (R-276), so an uncalibrated library is told to
    calibrate first, and an unreadable calibration is named, never refused:
    the bridge writes no tag either way.
    """
    try:
        cut = metadata_cli.load_vocal_threshold(cfg)
    except CratekitError as exc:
        return f"{BRIDGE_VOX_NONE}, and " + native.VOX_UNREADABLE.format(why=exc.cause.message)
    if cut is None:
        return f"{BRIDGE_VOX_NONE}, and {native.VOX_UNCALIBRATED}"
    return BRIDGE_VOX_OWED


def split_facts(
    entries: list[tuple[str, str, int, int]], rest: int, *, left: int = 0
) -> dict[str, Any]:
    """The account playlists on a gate screen, each by the name it lands as (U113).

    ``entries`` are each playlist's name, the account's own name for it, how
    many tracks it holds and how many of those the library already owned
    (U128); ``rest`` is how many files the batch playlist keeps and ``left``
    how many rows of the account playlists no INBOX playlist holds. ONE
    WORDING FOR BOTH MEDIA, so the same split reads the same on either screen.
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


def _split_items(split: tuple[tuple[account_playlists.Claimed, int], ...]) -> list[dict[str, Any]]:
    """One item per account playlist an intake file was given, with what it holds."""
    return [
        {
            "action": PLAYLIST,
            "playlist": claimed.name,
            "account": claimed.playlist_id,
            "count": count,
        }
        for claimed, count in split
    ]


def _reported(payload: dict, landed: landing.Landed) -> dict:
    """The plan, each item marked with what the apply actually did to it."""
    refused = {str(entry.path): entry for entry in landed.refused}
    items: list[dict[str, Any]] = []
    for item in payload["items"]:
        entry = refused.get(item["from"])
        if entry is None:
            items.append({**item, "action": LANDED})
        else:
            items.append({**item, "action": REFUSED, "reason": entry.reason, "why": entry.sentence})
    totals = {
        "count": payload["totals"]["count"],
        "landed": len(landed.moved),
        "refused": len(landed.refused),
    }
    items.extend(_split_items(landed.split))
    if landed.labelled or landed.unlabelled:
        # IN ``items`` AND ``totals``, because the plan surface is closed at
        # four fields and a fifth is a schema break for every consumer. A label
        # playlist written and a label row left out are both things this run
        # did to the plan it was shown, which is what an item is.
        items.extend(
            {
                "action": FILED,
                "label": entry.label,
                "year": entry.year,
                "playlist": entry.playlist,
                "count": len(entry.track_ids),
            }
            for entry in landed.labelled
        )
        items.extend(
            {
                "action": UNFILED,
                "id": entry.ref,
                "artist": entry.artist,
                "title": entry.title,
                "label": entry.label,
                "year": entry.year,
                "reason": entry.reason,
                "why": entry.sentence,
            }
            for entry in landed.unlabelled
        )
        totals["filed"] = len(landed.labelled)
        totals["unfiled"] = len(landed.unlabelled)
    return {**payload, "items": items, "totals": totals}


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
    """The plan as the approval gate shows it: one item per file, with its row.

    EVERY COLUMN THE ROW WOULD CARRY IS ON THE ITEM, and the digest is taken
    over the files, the folder, the batch and the collection plan together, so
    an answer given for one folder, one batch name, one library or one set of
    rows is stale for another. The engine's own digest already covers the rows,
    the root and the library's device and master id, and not the database's
    path, which the screen shows (U161); the files' fingerprint covers what is
    on disk.
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
            "action": row.action,
            "from": str(item),
            "to": str(row.target),
            "row": row.columns(),
        }
        if row.content_id is not None:
            entry["content_id"] = row.content_id
        if row.why:
            entry["why"] = row.why
        if str(row.target) in hearts:
            entry["heart"] = hearts[str(row.target)] or "month left to the backfill"
        if rows.labels is not None:
            # U156: the label playlist each file is filed in, or none, which
            # the screen's facts say why for.
            entry["label"] = filed.get(str(row.target), "none")
        if row.action == native.ADD and rows.vox_cut is not None and not rows.vox_blocked:
            # U127: the score each added row was read at and whether it is tagged.
            entry["voxlevel"] = row.voxlevel
            entry["vox"] = row.vox
        if row.action == native.ADD and row.drift_verdict not in ("", drift.UNSCORED):
            # U157: the drift each added row was read at, its verdict and
            # whether it is tagged dyn. A file with no reading is the fact
            # line's to count, so a batch from before U157 shows as it did.
            entry["drift"] = row.drift
            entry["drift_verdict"] = row.drift_verdict
            entry["dyn"] = row.dyn
        if str(row.target) in sorted_into:
            entry["files into"] = sorted_into[str(row.target)].shown()
        items.append(entry)
    identity = _native_identity(planned, rows, target=target)
    if rows.favorites is not None and rows.favorites.skipped:
        # THE SKIP IS AN ITEM OF THE PLAN, since the payload's keys are closed
        # (``plan/1``) and the apply reports it back unchanged.
        items.append(
            {
                "action": FAVORITES,
                "playlist": rows.favorites.source_name,
                "skipped": rows.favorites.skipped,
            }
        )
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {"count": len(planned.items)},
        "chunk": None,
    }


def favorites_facts(plan: native.FavoritesPlan) -> dict[str, Any]:
    """The hearts on a gate screen, one line per fact (U120)."""
    if plan.skipped:
        return {"hearts": f"none placed, {plan.skipped}"}
    where = (
        f"{plan.source_name!r} under {plan.folder_name!r}"
        if plan.folder_name
        else repr(plan.source_name)
    )

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
    # THE COLOUR (U153): every landed heart's row and each uncoloured owned
    # heart takes Pink, a row a person coloured is held, no Pink row is said.
    if plan.colour_skipped:
        facts["rows to colour Pink"] = f"none, {plan.colour_skipped}"
    else:
        facts["rows to colour Pink"] = len(plan.items) + len(plan.colour)
    if plan.held:
        facts["colour held"] = [one.said() for one in plan.held]
    return facts


def collection_facts(rows: native.NativePlan) -> dict[str, Any]:
    """What a native plan writes, one line per fact, for any verb's gate screen.

    SHARED WITH ``intake file`` (R-770), which asks the same kind of question
    over the same engine's plan: where the playlist hangs, which database is
    written, which device the rows are stamped with, how the path is stored,
    and what is left for rekordbox.
    """
    stored = (
        f"under the base drive {rows.base_drive}, which rekordbox maps to {rows.current_drive}"
        if rows.base_drive and rows.current_drive and rows.base_drive != rows.current_drive
        else "under the mounted path"
    )
    facts = {
        "playlist": f"{rows.playlist} under {rows.root_name} (row {rows.root_id})",
        "reads and writes": str(rows.database),
        "device": f"{rows.device_id} (master {rows.master_db_id})",
        "paths stored": stored,
        # U126: the value every added row is given, and the count that makes
        # it the library's, so the person approves the number and its source.
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
            (
                f"{rows.root_name} / {native.ANALYZE}, every added row, "
                + (
                    f"found (row {rows.analyze_playlist_id})"
                    if rows.analyze_playlist_id
                    else "made"
                )
            )
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
        facts["inbox leftovers"] = "not joined automatically: " + ", ".join(
            repr(name) for name in rows.inbox_leftovers
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

    One file in nineteen with no score is a file the model could not hear and
    is said on the vox line. Most of a batch with no score is a batch analysed
    with no model loaded, so it is a warning with its own code that a verb
    running the landing lifts onto its own envelope, rather than a clause a
    person has to notice at the end of a line.
    """
    adding = rows.to_add()
    unscored = rows.vox_unscored()
    if not adding or 2 * len(unscored) <= len(adding):
        return []
    return [
        {
            "code": VOX_MOSTLY_UNSCORED,
            "message": (
                f"{len(unscored)} of the {len(adding)} row(s) this landing adds carry "
                f"no voxlevel, so they join with no vox My Tag; a batch this unscored "
                f"was analysed with no vocal model loaded. Check crate doctor's "
                f"install.extras row, score them with crate analyze vocals --unscored "
                f"{folder}, then plan the landing again"
            ),
        }
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
        "action": PLAYLIST,
        "playlist": collection.playlist,
        "id": collection.playlist_id,
        "tree": collection.tree_id,
        "session": collection.session_id,
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
                [
                    (one.name, one.account_name, len(one.members), one.owned)
                    for one in rows.playlists
                ],
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
    made = [one for one in planned if not one.why]
    left = [one for one in planned if one.why]
    said = [f"{one.folder.name} / {one.name}" for one in made]
    said.extend(f"{one.account_name} gets none: {one.why}" for one in left)
    return "; ".join(said)


def _twin_notes(cfg: config.Config, rows, collection: native.NativeLanded) -> list[dict[str, str]]:
    """Pair each twin the commit wrote (U149), and name each planned twin it could not make."""
    from cratekit.sync import twins

    notes = twins.pair_landed(cfg, collection.twins)
    left = [one for one in (rows.twins if rows is not None else ()) if one.why]
    if left:
        notes.append(
            {
                "code": TWINS_LEFT,
                "message": (
                    f"{len(left)} account playlist(s) got no custom playlist twin: "
                    + "; ".join(f"{one.account_name}: {one.why}" for one in left)
                ),
            }
        )
    return notes


def _native_reported(payload: dict, landed: landing.LandedNative) -> dict:
    """The plan, each item marked with what the apply actually did to it."""
    refused = {str(entry.path): entry for entry in landed.refused}
    added = {str(row.target): row for row in landed.collection.added}
    present = {str(row.target): row for row in landed.collection.present}
    items: list[dict[str, Any]] = []
    for item in payload["items"]:
        if item.get("action") == FAVORITES or item.get("area") == "account-archive":
            # Favourites (U120) and the account archive folded into this landing
            # (U129) are not file moves: they have no "from", so carry them through.
            items.append(item)
            continue
        entry = refused.get(item["from"])
        if entry is not None:
            items.append({**item, "action": REFUSED, "reason": entry.reason, "why": entry.sentence})
            continue
        row = added.get(item["to"])
        if row is not None:
            items.append(
                {
                    **item,
                    "action": LANDED,
                    "content_id": row.content_id,
                    "row": {
                        **item["row"],
                        "Title": row.title,
                        "FolderPath": row.folder_path,
                        rb_writer.FILE_ID_COLUMN: row.file_id,
                        rb_writer.CONTENT_LINK_COLUMN: row.content_link,
                    },
                    "left_empty": sorted(row.empty),
                    **({"vox": row.vox} if "vox" in item else {}),
                    **({"dyn": row.dyn} if "dyn" in item else {}),
                }
            )
            continue
        held = present.get(item["to"])
        items.append(
            {
                **item,
                "action": LANDED,
                "content_id": held.content_id if held is not None else item.get("content_id"),
                "already_present": True,
            }
        )
    totals = {
        "count": payload["totals"]["count"],
        "landed": len(landed.moved),
        "refused": len(landed.refused),
        "added": len(landed.collection.added),
        "already present": len(landed.collection.present),
        "memberships": landed.collection.memberships_added,
    }
    # WHAT ADOPTION READS BACK, not what the writer counted (U127): a tag
    # written under a category rekordbox removed is no tag a person sees.
    voxed = sum(1 for row in landed.collection.added if row.vox)
    if voxed:
        totals["vox tagged"] = voxed
    # AND WHAT THE CHECK READS BACK (U157), on the same reading.
    dyned = sum(1 for row in landed.collection.added if row.dyn)
    if dyned:
        totals["dyn tagged"] = dyned
    if landed.collection.playlist_id:
        items.append(playlist_item(landed.collection))
    items.extend(
        {
            "action": PLAYLIST,
            "playlist": written.name,
            "id": written.playlist_id,
            "account": written.account,
            "count": written.tracks,
            "tree": landed.collection.tree_id,
            "session": landed.collection.session_id,
        }
        for written in landed.collection.playlists
    )
    items.extend(
        {
            "action": TWIN,
            "playlist": f"{twin.folder} / {twin.name}",
            "id": twin.playlist_id,
            "account_id": twin.account_id,
            "count": twin.tracks,
            "session": landed.collection.session_id,
        }
        for twin in landed.collection.twins
    )
    placed = landed.collection.favorites
    if placed is not None:
        totals["hearts placed"] = placed.added
        items.append(
            {
                "action": FAVORITES,
                "playlist": placed.source_name,
                "id": placed.source_id,
                "count": placed.added_source,
                "session": landed.collection.session_id,
            }
        )
        items.extend(
            {
                "action": FAVORITES,
                "playlist": name,
                "id": row,
                "count": count,
                "created": name in placed.created,
                "session": landed.collection.session_id,
            }
            for name, row, count in placed.months
        )
    kept = landed.collection.set_playlist
    if kept is not None:
        if kept.playlist_id:
            items.append(set_playlist_item(kept, session_id=landed.collection.session_id))
        totals = {
            **totals,
            "set playlist tracks": kept.members,
            "set playlist left out": len(kept.left),
        }
    filed = landed.collection.labels
    if filed is not None:
        items.extend(
            label_filing.item(one, tree=filed.tree_id, session_id=landed.collection.session_id)
            for one in filed.years
        )
        totals = {
            **totals,
            "label playlists": len(filed.years),
            "label memberships": filed.added(),
            "filed under no label": len(filed.left),
        }
    return {**payload, "items": items, "totals": totals}


def set_playlist_item(kept: set_playlist.Written, *, session_id: str) -> dict[str, Any]:
    """The one item a write appends for the set's permanent playlist (U121)."""
    return {
        "action": PLAYLIST,
        "playlist": kept.name,
        "id": kept.playlist_id,
        "folder": kept.folder_id,
        "folder_created": kept.folder_created,
        "playlist_created": kept.playlist_created,
        "count": kept.members,
        "added": kept.added,
        "left": [one.identity() for one in kept.left],
        "session": session_id,
    }


def _with_filing(reported: dict, filed: filing.Filed) -> dict:
    """The landed payload with what the filing after it did, in its totals (U165)."""
    totals = {**reported["totals"], "filing": filed.state}
    if filed.state == filing.FILED:
        totals = {
            **totals,
            "filed": filed.filed,
            "filing memberships": filed.memberships,
            "placed nowhere": len(filed.nowhere),
        }
    # EACH ITEM ALREADY SAYS WHERE IT FILES, or why nowhere, in its
    # ``files into``; the payload's keys are closed (``plan/1``).
    return {**reported, "totals": totals}


def favorites_notes(payload: dict, collection: native.NativeLanded) -> list[dict[str, str]]:
    """What a person reads about the hearts a landing placed, or did not (U120).

    ON THE WARNINGS CHANNEL, for R-424's reason: the default renderer prints
    a verb's outcome, its warnings and its run id, so a fact only the json
    block states is a fact a person never reads. A skipped placement is said
    with the home's own words; a placement is said with its counts.
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
    return [{"code": FAVORITES_PLACED, "message": placed.said()}, *_colour_notes(placed)]


def _colour_notes(placed) -> list[dict[str, str]]:
    """The colour's notes (U153), from what the write knew, so the apply reports
    the held rows and the missing Pink row the gate screen showed. The same two
    whether the hearts came with files or the owned hearts were placed alone."""
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
            {
                "code": FAVORITES_COLOUR_HELD,
                "message": (
                    f"{len(placed.held)} row(s) carry a colour a person chose and keep it: "
                    + "; ".join(one.said() for one in placed.held)
                ),
            }
        )
    return notes


#: The visit's short path (U319), which A33's probe at sitting 101 measured:
#: with Auto Analysis on, a launch brought to the front raises one dialog whose
#: OK analyses every row waiting, with no selection, on the fields and the mode
#: the preference holds, so a dyn row still takes Dynamic. Said after the
#: Analyze Tracks selections it stands in for, so "as above" names them, and
#: ONE WORDING for every sentence that offers it: ``cli.tail`` spells the same
#: for the step ``crate sync land`` prints, held to this by a test, since a
#: lower package imports no feature module. Nothing here or in the visit turns
#: Auto Analysis on: it is the person's.
AUTO_ANALYSIS_STEP = (
    "or, with Auto Analysis on, open rekordbox with its window in front and press OK "
    "on its Auto Analysis dialog only when it shows every one of those Normal "
    "settings with Vocal and CUE off and no field set otherwise, else Cancel it and "
    "select as above; Auto Analysis runs on its preference's own mode, so the rows "
    f"carrying the dyn My Tag still take Analyze Tracks with {drift.DYNAMIC_SETTINGS}"
)


def awaiting_analysis(collection: native.NativeLanded) -> list[dict[str, str]]:
    """The warning a native write carries when rows joined the collection, else none.

    ONE SENTENCE FOR EVERY VERB THAT ADDS A ROW (R-770). ``intake file`` adds
    one through the same engine and owes the person the same next step, and a
    second wording of it is how one of the two goes stale.
    """
    if not collection.added:
        return []
    # ONE PLAYLIST, ANALYZE (U166), which holds every row still waiting and
    # only those, so the visit is one selection rather than one per batch.
    # TWO SELECTIONS IN IT (U157), each with its count and its settings: the
    # rows without the dyn My Tag take Normal and the rows with it Dynamic.
    # TWO PATHS TO THEM (U319): the selections with Auto Analysis off, and
    # with it on the one dialog a launch in front raises, said in the one
    # wording above, which leaves the dyn rows to their own Dynamic run.
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

    SHARED WITH ``intake file`` for :func:`awaiting_analysis`' reason. A row
    whose drift read as variable and carries no mark would be analysed with
    Normal by a person who selects by the mark, so each is named, with why,
    and the step owed is to run it with Dynamic by hand. A file with no drift
    reading is the screen's to count and not a warning: every batch analysed
    before U157 is one, and Normal is what each of its rows always took.
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
        {
            "code": DYN_NOT_WRITTEN,
            "message": (
                f"{len(untagged)} row(s) whose tempo moves do not carry the dyn My Tag, "
                f"so select them by name and run Analyze Tracks on them with "
                f"{drift.DYNAMIC_SETTINGS}: {names}; {why}"
            ),
        }
    ]


def vox_warnings(collection: native.NativeLanded) -> list[dict[str, str]]:
    """What a person reads about the vox My Tag a native write gave its rows, or did not (U127).

    SHARED WITH ``intake file`` for :func:`awaiting_analysis`' reason. A file
    with no score is named, never tagged on a guess; a landing that could tag
    nothing says why and names the step owed. A row tagged is the report's.
    """
    if not collection.added:
        return []
    warnings: list[dict[str, str]] = []
    if collection.vox_missing:
        # PLANNED, WRITTEN, AND NOT WHAT ADOPTION READS: said, never reported
        # as tagged, so a person is not told a row reaches with vox when the
        # next adoption will not file it there.
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
            {
                "code": VOX_NOT_WRITTEN,
                "message": (
                    f"{len(collection.vox_missing)} row(s) planned for the vox My Tag "
                    f"do not carry it, so they reach no with vox playlist: {names}; {why}"
                ),
            }
        )
    if collection.vox_blocked:
        return [
            *warnings,
            {
                "code": VOX_NOT_WRITTEN,
                "message": (
                    f"no row joined with the vox My Tag, so none reaches a with vox "
                    f"playlist: {collection.vox_blocked}"
                ),
            },
        ]
    if not collection.vox_unscored:
        return warnings
    names = ", ".join(path.name for path in collection.vox_unscored)
    return [
        *warnings,
        {
            "code": VOX_UNSCORED,
            "message": (
                f"{len(collection.vox_unscored)} file(s) carry no voxlevel to read, so "
                f"their rows got no vox My Tag: {names}; run crate analyze vocals on "
                f"them and then crate metadata mytags-vocals --apply"
            ),
        },
    ]
