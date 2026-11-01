"""``intake.land``: a staged batch moves into the library behind one gate.

R-413's verb half. ``acquire download`` commits files to download staging,
``tag folder`` and ``name apply`` work on them there, and nothing moved them
out, so no downloaded track ever reached an importable file. The engine is
:mod:`cratekit.intake.landing`, and this shell owns the plan, the gate and
what a person is told afterwards.

THE PLAN IS SHOWN BEFORE ANYTHING MOVES. The first run lists the folder, puts
the list, the batch folder and the intake file in front of the person on the
gate screen, and stops. An answer recorded against that plan is refused as
stale if the folder, the batch or the intake file changed since, because the
digest covers all of them and not only the files.

THE IMPORT IS THE PERSON'S, AND THE RUN SAYS SO. A landed batch is one intake
file rekordbox has not seen. :func:`cratekit.intake.ingest.place_files` leaves
its intake session ``awaiting-import`` with a ``rekordbox_import`` pending
action PERSISTED ON THAT RECORD, and the envelope carries that same action, not
a second one built here, so what the screen said and what the session log holds
cannot differ. Its steps run end to end: import the file, import the batch
playlist on its own and drag it from the playlist root into the intake folder
(R-687), take a Fresh Export, run ``intake imported``, which proves the import,
retires the file and settles the run (R-501). It BLOCKS NOTHING. A blocking
action makes every verb it names refuse, and no consequence of an unimported
landing was driven that would justify that.

THE SESSION RECORD IS WHERE IT IS REMEMBERED, NOT THE RUN RECORD. The action is
not put on this run's own state, because nothing would ever clear it there and
doctor would report the run as waiting for ever. Doctor's session check names
every run still ``awaiting-import``.

``--manifest`` FILES LABEL TRACKS IN THE SAME FILE. The manifest is the
provenance ``label approved`` wrote beside its list. Its bytes are part of what
the gate compares, so an answer given against one manifest is stale for
another. A label row that no landed file matches is a warning that names the
track, never a failure: the file, if there is one, is in the intake playlist.
On a database native intake tree the same rows, or one label named with
``--label`` and each file's date tag, are filed under the Record Labels tree in
the landing's own commit (U156, :mod:`cratekit.intake.label_filing`).
"""

from __future__ import annotations

import re
from dataclasses import replace
from pathlib import Path
from typing import Any, Callable, TypeVar

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import analysis_store, config, jobs, rb_writer, rehearsal, session
from cratekit.core.cause import CratekitError, Outcome, Remedy, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import backfill, placement
from cratekit.favorites import colour as colour_mod
from cratekit.intake import (
    account_playlists,
    batch_name,
    filing,
    ingest,
    label_filing,
    landing,
    native,
    set_playlist,
    shelve,
)
from cratekit.intake import cli as intake_cli
from cratekit.write import metadata_cli

#: The action every planned file carries until the apply reports on it.
LAND = "land"
LANDED = "landed"
REFUSED = "refused"
#: The one item a native landing appends for the batch playlist it wrote.
PLAYLIST = "playlist"
#: The item a native write appends for each favourites playlist it placed hearts in (U120).
FAVORITES = "favorites"

#: The notes a native landing carries about its hearts (U120).
FAVORITES_PLACED = "favorites-placed"
FAVORITES_SKIPPED = "favorites-placement-skipped"
#: A heart's row a person coloured otherwise, left and named (U153).
FAVORITES_COLOUR_HELD = "favorites-colour-held"

#: The two gates, one per medium. The xml one answers inline as it always has;
#: the native one is explicit, because a content row in the collection is a
#: new kind of write and R34 forbids a blanket answer for it.
XML_GATE = "intake.land.confirm"
NATIVE_GATE = "intake.land.native"
#: The fact a native write's answer is pinned to outside its digest (U161):
#: the database file the handle opened, as the screen's reads and writes line
#: names it.
DATABASE_PIN = "database"

#: The warning a native landing carries: the rows are in the collection and
#: rekordbox has not analysed them, which it does on request and not on sight.
AWAITING_ANALYSIS = "rows-await-analysis"

#: The warnings a native write carries about the vox My Tag (U127): a file
#: whose score could not be read, and a landing that wrote no tag at all.
VOX_UNSCORED = "vox-unscored"
VOX_NOT_WRITTEN = "vox-not-written"

#: What the bridge's gate screen says of the vox My Tag (U127), on a
#: calibrated library; :func:`bridge_vox_fact` says the rest.
BRIDGE_VOX_NONE = "not written, the xml bridge carries no My Tag"
BRIDGE_VOX_OWED = (
    f"{BRIDGE_VOX_NONE}; once rekordbox has imported the batch, run crate metadata "
    f"mytags-vocals --apply to tag its vocal tracks"
)

_ORIGIN = ("intake.land_cli",)

#: What a label playlist written, and a label row filed under none, are marked.
FILED = "filed"
UNFILED = "unfiled"

#: The verb that proves an intake file imported. One spelling, beside the
#: session it is persisted on, and named here for the callers that read it.
VERIFY_VERB = ingest.VERIFY_VERB

INTAKE_SUFFIX = "_inboxed.xml"

#: What an intake file's name gains once its import is proven (R-501). It ends
#: the name, so the cutover precheck's scan, which walks ``*.xml``, stops seeing
#: the file. A second file retired under a name already taken gains ``-2``.
RETIRED_SUFFIX = ".imported"

_RETIRED_TAIL = re.compile(re.escape(RETIRED_SUFFIX) + r"(-[0-9]+)?$")


def unretired_name(name: str) -> str:
    """An intake file's name as it was written, retired or not.

    ONE PLACE KNOWS BOTH SPELLINGS. A verb that finds its pass from an intake
    file's name is handed the retired name by anybody who proved the import
    first, and it must read the same pass off it.
    """
    return _RETIRED_TAIL.sub("", name)


def default_name(run_id: str) -> str:
    """A run's identifier as a file name: what an intake file is named for.

    The run's own identifier WITHOUT ITS COLONS. A run id spells the time as
    ``19:34:38``, and a colon cannot be in a file name on the exFAT volumes a
    library commonly sits on, and reads as a slash in Finder on the others.

    NOT THE BATCH'S NAME SINCE U110. The batch folder and its playlist are named
    for the date and the source (:mod:`cratekit.intake.batch_name`); this names
    the intake file of a landing given neither ``--pass`` nor ``--name``, and
    the pass ``intake missing --run`` and ``label sync --go`` tell a person to
    land under.
    """
    return run_id.replace(":", "")


def intake_stem(*, pass_name: str | None, name: str | None, run_id: str) -> str:
    """What a landing's intake file is named for, before ``_inboxed.xml``.

    THE PASS FIRST, because the file's name is how ``sync mark`` finds the pass
    and how ``label mark``, ``export archive`` and ``sync unmark`` key what they
    record. Then ``--name``, which is what the file was named for before
    ``--pass`` existed, so a landing typed the old way still writes the file a
    later mark reads. Then the landing's own run.
    """
    if pass_name is not None:
        return pass_name
    if name is not None:
        return name
    return default_name(run_id)


def _check_pass(pass_name: str | None) -> None:
    """Refuse a ``--pass`` that is not one plain file name at the library root."""
    if pass_name is None:
        return
    if not landing.plain_name(pass_name):
        raise refuse(
            "intake-list-unusable",
            f"{pass_name!r} is not a pass this landing can name its intake file for, "
            f"because it must be one plain file name beside the library; nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=("pass the name crate intake missing --run or crate label sync --go printed",),
            origin=_ORIGIN,
            detail={"pass": pass_name},
        )


def intake_file(cfg: config.Config, stem: str) -> Path:
    """Where a landing's intake file is written, beside the library, not in staging.

    ``stem`` is what :func:`intake_stem` names it for, which is the batch's
    own name only when ``--name`` was given and ``--pass`` was not.

    Staging is the folder a person cleans, and the file has to outlive that
    until rekordbox has imported it. The suffix is one the pending intake scan
    already walks, so an unimported landing is visible to the cutover check.
    """
    return Path(cfg.library.root) / f"{stem}{INTAKE_SUFFIX}"


def _still_free(cfg: config.Config, batch: str) -> None:
    """Refuse a default name another landing took since this one chose it.

    UNDER THE BATCH LOCK, because the name was chosen before the gate and two
    landings that both found it free would otherwise land into one folder and,
    on the native medium, one playlist. Only a name this run chose: one a person
    gave with ``--name`` is theirs to land into again.
    """
    if batch_name.taken(cfg, batch):
        raise refuse(
            "decision-stale",
            f"the batch name {batch!r} was taken by another landing after this one "
            f"chose it, so nothing was moved; run the landing again and it takes "
            f"the next free name",
            origin=_ORIGIN,
            detail={"batch": batch},
        )


def build_land(parser, entry) -> None:
    parser.add_argument(
        "folder",
        nargs="?",
        default=None,
        metavar="FOLDER",
        help="the folder of acquired files to land (default: download staging)",
    )
    parser.add_argument(
        "--export",
        default=None,
        metavar="XML",
        help=(
            "a Fresh Export of the collection to splice the landed files into; "
            "required while the intake tree is on the xml bridge, and refused "
            "once it is database native, where the files join the collection "
            "through the database"
        ),
    )
    parser.add_argument(
        "--name",
        default=None,
        metavar="NAME",
        help=(
            "the batch folder under the music folder and the batch playlist under "
            "INBOX (default: the landing's date and its source, for example "
            "'2026-10-03 Tidal playlists', with ' 2' added when that is taken)"
        ),
    )
    parser.add_argument(
        "--pass",
        dest="pass_name",
        default=None,
        metavar="PASS",
        help=(
            "the pass these files were acquired under, as crate intake missing --run "
            "or crate label sync --go printed it; the intake file is named for it, so "
            "sync mark finds the pass, and the batch is named for the pass's sources"
        ),
    )
    parser.add_argument(
        "--manifest",
        default=None,
        metavar="JSON",
        help=(
            "the manifest written beside the list these files were acquired "
            "from; its label rows are filed under the record labels tree"
        ),
    )
    parser.add_argument(
        "--label",
        default=None,
        metavar="NAME",
        help=(
            "file every landed file under this label in the record labels tree, in "
            "the year its date tag names, for a label batch with no manifest such as "
            "a Bandcamp purchase from the label's own account (database native intake "
            "trees only; a file with no date tag is named and filed nowhere)"
        ),
    )
    parser.add_argument(
        "--set",
        dest="set_job",
        default=None,
        metavar="JOB",
        help=(
            "the intake set job these files were downloaded for; the landing then "
            "also writes the whole set, owned and landed tracks in set order, as one "
            "permanent playlist under the INSPIRATION folder, in the same commit as "
            "the batch (database native intake trees only)"
        ),
    )
    parser.add_argument(
        "--rehearse",
        action="store_true",
        help=(
            "rehearse the landing instead of asking to apply it: copy the database "
            "and the library state to a scratch area of this run's own, apply the "
            "landing there over clones of the staged files, read the copy back, "
            "report the plan's digest, and remove the area; nothing live is "
            "written or moved, and the live landing then says whether its plan "
            "equals this rehearsal's (database native intake trees only)"
        ),
    )
    parser.add_argument(
        "--land-only",
        action="store_true",
        help=(
            "land the files and write their rows without filing them into the "
            "library tree afterwards; by default a database native landing shows "
            "where adoption would file each new row, and files them under the "
            "same answer when the plan after the commit agrees"
        ),
    )
    set_playlist.add_word_arguments(parser)
    parser.set_defaults(_handler=intake_land)


def _label_flag(
    given: str | None,
    *,
    manifest: landing.LabelManifest | None,
    medium: ingest.IntakeMedium,
    cfg: config.Config,
) -> str | None:
    """The label ``--label`` names, or a refusal before the gate with nothing moved (U156).

    NATIVE ONLY: the bridge files labels into its intake file from a manifest
    alone, and a flag it would ignore is a label batch landed filed under
    nothing. NOT BESIDE A MANIFEST, whose rows name their own labels, since
    two answers to one question is a guess at which one wins. NOT BLANK, since
    a playlist named for nothing sits in the tree for good. AND NOT ON A
    LIBRARY WHOSE ROOT IS NOT THERE, said as that: the medium was not read, so
    telling the person their tree is on the bridge, and to drop the flag, would
    land the batch filed under nothing once the volume is back.
    """
    if given is None:
        return None
    flag = "--label"
    if not given.strip():
        raise refuse(
            "intake-list-unusable",
            f"{flag} names no label, so there is nothing to file the batch under; "
            f"name the label or drop {flag}, nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
        )
    if manifest is not None:
        raise refuse(
            "intake-list-unusable",
            f"{flag} and --manifest both say which label each file is filed under, and "
            f"the manifest's rows name their own; pass one of them, nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"label": given, "manifest": str(manifest.path)},
        )
    if medium.declared is None:
        raise refuse(
            "library-root-unreachable",
            f"the library root {cfg.library.root} is not reachable, so its taxonomy and "
            f"its intake tree could not be read and {flag} has no tree to file the "
            f"batch under; mount the library volume and run it again, nothing was moved",
            origin=_ORIGIN,
            detail={"root": str(cfg.library.root), "label": given},
        )
    if not medium.native:
        raise refuse(
            "intake-list-unusable",
            f"{flag} files the batch under its label through the database, and this "
            f"library's intake tree is on the xml bridge, whose landing files labels "
            f"from a manifest alone; land with --manifest or without {flag}, "
            f"nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"label": given},
        )
    return given.strip()


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
        {"action": LAND, "from": str(item), "to": str(target / item.name)}
        for item in planned.items
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


def _planned(folder: Path, cfg: config.Config, batch: str) -> landing.Plan:
    """The engine's plan, or a plan of nothing for a folder with nothing in it.

    AN EMPTY FOLDER IS A PLAN, NOT A REFUSAL, on the precedent ``name apply``
    and ``route inbox`` set: download staging is empty on a fresh install and
    after every landing, and a person running the step then is told there is
    nothing to move, not that something failed. The empty plan is never handed
    to :func:`landing.apply`, so no folder and no intake file is made for it.
    Anything that is not a folder still goes to the engine, which refuses it.
    """
    if folder.is_dir() and not landing.listing(folder):
        return landing.Plan(folder=folder, batch=batch, items=(), digest="")
    return landing.plan(folder, cfg, batch)


def _reported(payload: dict, landed: landing.Landed) -> dict:
    """The plan, each item marked with what the apply actually did to it."""
    refused = {str(entry.path): entry for entry in landed.refused}
    items: list[dict[str, Any]] = []
    for item in payload["items"]:
        entry = refused.get(item["from"])
        if entry is None:
            items.append({**item, "action": LANDED})
        else:
            items.append(
                {**item, "action": REFUSED, "reason": entry.reason, "why": entry.sentence}
            )
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


def _xml_split(
    cfg: config.Config,
    claims: tuple[account_playlists.Claim, ...],
    export: Path,
    *,
    batch: str,
    declared,
    registry,
) -> tuple[account_playlists.Claimed, ...]:
    """Each account playlist named against the export it is spliced into, and the pending files.

    The export's intake tree and playlist root (:func:`landing.inbox_held`), and
    every account playlist an intake file still waiting on its import names,
    which no export holds yet. An export that cannot be read names against the
    pending files only: the preflight refuses it before anything moves.
    """
    if not claims:
        return ()
    held: tuple[str, ...] | str = ()
    if declared is not None and registry is not None:
        held = landing.inbox_held(export, landing.Checked(registry=registry, declared=declared))
    taken = (*(held if isinstance(held, tuple) else ()), *account_playlists.pending_names(cfg))
    return account_playlists.named(claims, taken, batch=batch)


def gate_named(entry, name: str):
    """One of a verb's gates by name, never by position.

    Two gates on the landing since R-746, one per medium, and the shared cloud
    sync one is raised by the guarded writer rather than asked by a verb, so
    indexing would bind a medium to the order the gates happen to be written
    in. ``intake file`` looks its native gate up the same way (R-770).
    """
    for spec in entry.gates:
        if spec.name == name:
            return spec
    raise refuse(
        "internal-error",
        f"{entry.name} declares no gate named {name!r}, so there is no question "
        f"to ask before it writes",
        remedy=Remedy.REPORT_DEFECT,
        origin=_ORIGIN,
        detail={"verb": entry.name, "gate": name},
    )


def intake_land(ctx) -> Envelope:
    cfg = intake_cli._load()
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.paths.download_staging)
    pass_name = ctx.args.pass_name
    _check_pass(pass_name)
    # READ BEFORE THE GATE, so a file that is not a manifest refuses before
    # anybody spends an answer on it, and the screen can say what it names.
    manifest = (
        landing.read_label_manifest(Path(ctx.args.manifest)) if ctx.args.manifest else None
    )
    # TWO NAMES SINCE U110. The batch, its folder and its playlist, is what a
    # person reads in INBOX: the date and the source unless ``--name`` says
    # otherwise. The intake file keeps the identifier the marks read.
    batch = (
        ctx.args.name
        if ctx.args.name is not None
        else batch_name.readable(
            cfg,
            label_rows=manifest.rows if manifest is not None else (),
            pass_name=pass_name,
        )
    )
    stem = intake_stem(pass_name=pass_name, name=ctx.args.name, run_id=ctx.run.run_id)
    planned = _planned(folder, cfg, batch)
    target = landing.target_dir(cfg, batch)
    # WHICH PLAYLIST ON THE ACCOUNT ASKED FOR EACH FILE (U113), read from the
    # pass's own jobs before the gate, so the screen can say where every file
    # goes. Named per medium below, against what that medium's INBOX holds.
    claims = account_playlists.split(cfg, pass_name, planned.items)
    # THE MEDIUM IS THE INTAKE TREE'S MODE, the way the routing verbs choose
    # theirs (R-746). A tree the database owns takes the files into the
    # collection through the guarded writer and no export is involved; a tree
    # on the bridge is spliced into the export it always was. The registry
    # lives under the library root, so an unreachable root decides nothing
    # here: the xml path is taken as it was before the medium existed, and
    # its preflight names the library, before the gate, under the R-677
    # contract that a recorded abort is still honoured over it. THE SWITCH IS
    # ``ingest.intake_medium`` AND NO COPY OF IT (R-770): ``intake file`` reads
    # the same one, so the two verbs cannot choose by two rules.
    medium = ingest.intake_medium(cfg)
    declared, registry = medium.declared, medium.registry
    # THE SET PLAYLIST IS A DATABASE WRITE (U121), one more node in the native
    # landing's commit, and the bridge landing splices an export and opens no
    # database. Refused by name before the gate rather than landing the batch
    # and quietly writing no playlist. AND A WORD WITHOUT THE SET IS REFUSED
    # TOO, since nothing would read it and the person would find no playlist.
    words_given = [
        flag
        for flag, value in (
            ("--dj", ctx.args.dj),
            ("--set-name", ctx.args.set_name),
            ("--set-date", ctx.args.set_date),
        )
        if value is not None
    ]
    if words_given and not ctx.args.set_job:
        raise refuse(
            "intake-list-unusable",
            f"{', '.join(words_given)} name{'s' if len(words_given) == 1 else ''} the "
            f"set's playlist and --set names the set it is made from, so without "
            f"--set nothing would read {'it' if len(words_given) == 1 else 'them'}; "
            f"pass --set JOB or drop {'it' if len(words_given) == 1 else 'them'}, "
            f"nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"given": words_given},
        )
    if ctx.args.set_job:
        set_playlist.assert_native(medium, landing=True)
    label = _label_flag(ctx.args.label, manifest=manifest, medium=medium, cfg=cfg)
    rehearse = bool(getattr(ctx.args, "rehearse", False))
    if rehearse and not medium.native:
        raise refuse(
            "intake-list-unusable",
            "--rehearse rehearses a landing into the database on a copy of it, and "
            "this intake tree is on the xml bridge, where a landing writes no "
            "database; drop --rehearse, nothing was copied",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"tree_id": declared.intake.id if declared is not None else None},
        )
    if medium.native:
        # AND WHICH FILES ARE HEARTS (U120), read from the same jobs the same
        # way, each with the month the account dated it into. The native
        # medium alone, since the bridge writes an export and places none, so
        # the match over the planned files is not made for nothing there.
        hearted = account_playlists.hearted(cfg, pass_name, planned.items)
        # AND WHICH HEARTS THE LIBRARY ALREADY HELD (U146), with the files the
        # job's reports named, so the landing places them too, files or none.
        owned = account_playlists.owned_hearts(cfg, pass_name)
        return _land_native(
            ctx,
            cfg,
            planned,
            declared=declared,
            registry=registry,
            manifest=manifest,
            label=label,
            medium=medium,
            claims=claims,
            hearted=hearted,
            owned=owned,
            rehearse=rehearse,
        )
    if ctx.args.export is None and declared is not None:
        raise refuse(
            "library-export-unusable",
            f"the intake tree {declared.intake.id!r} is on the xml bridge, so a "
            f"landing splices the batch into a Fresh Export and --export has to name "
            f"one; nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=(
                "export the collection from rekordbox and pass that file as --export",
                f"or run crate tree cutover {declared.intake.id} --export with it, after "
                f"which a landing adds the files to the collection directly",
            ),
            origin=_ORIGIN,
            detail={"tree_id": declared.intake.id},
        )
    # With no export named and no library to read, the engine's preflight
    # below refuses on the library first, so the name here is never opened.
    export = (
        Path(ctx.args.export)
        if ctx.args.export is not None
        else Path(cfg.library.root) / "collection.xml"
    )
    destination = intake_file(cfg, stem)
    split = _xml_split(cfg, claims, export, batch=batch, declared=declared, registry=registry)
    # EACH OWNED TRACK FOUND IN THE EXPORT BEFORE THE GATE (U128), so the screen
    # counts and the digest covers what the intake file will hold.
    split, emptied = landing.owned_in_export(cfg, split, export)
    # THE ENGINE'S PRE-MOVE CHECKS ARE ASKED BEFORE THE GATE TOO (R-677), for
    # the manifest's reason. A plan over an export that is not there, or not a
    # collection, or a library that is not mounted, could never run, and the
    # engine says so without moving anything. Only when something would move,
    # since a plan of nothing splices nothing.
    unusable: CratekitError | None = None
    if planned.items:
        try:
            landing.preflight(
                planned,
                cfg=cfg,
                export=export,
                destination=destination,
                label_rows=manifest.rows if manifest is not None else (),
                names=[claimed.name for claimed in split],
            )
        except CratekitError as exc:
            unusable = exc
    payload = _payload(
        planned,
        target=target,
        destination=destination,
        export=export,
        manifest=manifest,
        split=split,
        emptied=emptied,
    )
    spec = gate_named(ctx.entry, XML_GATE)
    try:
        option = ctx.gate.require(
            spec,
            digest=payload["digest"],
            context=_shown(
                planned,
                cfg=cfg,
                target=target,
                destination=destination,
                manifest=manifest,
                split=split,
                emptied=len(emptied),
            ),
        )
    except CratekitError as exc:
        # THE REFUSAL TAKES THE PLACE OF AN UNANSWERED GATE ONLY, the refusal
        # whose remedy is to answer it. An answer already given is honored
        # exactly as it was before the check existed, so an abort still ends in
        # nothing done, and an apply reaches the engine, which asks the same
        # checks again before its first move. Read off the remedy because this
        # layer cannot import the gate's own class.
        if unusable is not None and exc.cause.remediation.remedy is Remedy.ANSWER_DECISION:
            raise unusable from None
        raise
    if option != "apply" or not planned.items:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    # The engine lists the folder again and refuses a fingerprint that moved,
    # so the gap between this plan and the moves is its to close, not this
    # shell's. What the gate compared is what the person was shown.
    #
    # ONE LANDING PER BATCH NAME, HELD ACROSS THE WHOLE APPLY (R-432). The
    # engine checks a target free and then renames over it, and checks the
    # intake file absent long before it is written, so a second landing into
    # the same batch folder is refused at the door rather than waited for. Only
    # here, after the answer: a plan and a gate screen move nothing and a held
    # name does not stop anybody reading one.
    # AND ONE LANDING PER INTAKE FILE (U110), since the file is named for the
    # pass and the batch for the date, and either can be shared by a landing
    # the other lock does not see.
    with landing.batch_lock(batch), landing.intake_lock(stem):
        if ctx.args.name is None:
            _still_free(cfg, batch)
        landed = landing.apply(
            planned,
            cfg=cfg,
            export=export,
            destination=destination,
            manifest=manifest.path if manifest is not None else None,
            manifest_digest=manifest.digest if manifest is not None else None,
            split=split,
            pass_name=pass_name,
        )
    return ctx.envelope(
        data=_reported(payload, landed),
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=ingest.persisted_pending(cfg, landed.placed),
        warnings=[
            *(
                {"code": entry.reason, "message": entry.sentence}
                for entry in (*landed.refused, *landed.unlabelled)
            ),
            *account_playlists.left_warning((*emptied, *landed.left)),
        ],
    )


# ---------------------------------------------------------------------------
# The native medium (R-746)
# ---------------------------------------------------------------------------


def _filed_watch(cfg: config.Config, planned: landing.Plan) -> tuple[Path, ...]:
    """The live folders a native landing could file its batch in, which a rehearsal watches.

    The year folder the batch name or today names, where a new folder would
    appear, and for a batch landed into again by its name the folder recorded
    for it and that folder's own year folder, which may be another year's.
    """
    when, _said = shelve.filed_parts(planned.batch, on=batch_name.today())
    watched = [shelve.processed_root(cfg) / f"{when.year}"]
    again = batch_name.filed_folders(cfg).get(planned.batch)
    if again is not None:
        watched.extend((Path(again).parent, Path(again)))
    return tuple(dict.fromkeys(watched))


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
    return shown


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
            items.append(
                {**item, "action": REFUSED, "reason": entry.reason, "why": entry.sentence}
            )
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


def _land_native(
    ctx,
    cfg: config.Config,
    planned: landing.Plan,
    *,
    declared,
    registry,
    manifest: landing.LabelManifest | None,
    label: str | None = None,
    medium: ingest.IntakeMedium,
    claims: tuple[account_playlists.Claim, ...] = (),
    hearted: tuple[account_playlists.Hearted, ...] = (),
    owned: tuple[account_playlists.HeartRow, ...] = (),
    rehearse: bool = False,
) -> Envelope:
    """Plan the rows against the database, ask, then move, write and file.

    THE ORDER IS :func:`ask_then_write`'s, which ``intake file`` shares: the
    database opened with write intent before the plan, the acknowledgment read
    before the gate (R-733), the write only on ``apply``. A PLAN OF NOTHING IS
    NOT ASKED: download staging is empty after every landing, and an explicit
    gate, which takes a separate recorded act, is the price of a new kind of
    write and not of learning there is nothing to move. Nothing is written
    for it, so the envelope says so and stops.

    THE GATE TAKES NO INLINE ANSWER. This is a new kind of write, content rows
    in the collection, and it is answered by a separate recorded act with an
    actor, the way the adoption is (R34).

    AN EMPTY STAGING FOLDER STILL PLACES THE PASS'S OWNED HEARTS (U146): a
    heart on a track the library holds joins All Favorites whether or not a
    file was downloaded, under this same gate, through :func:`_place_owned`.

    A MANIFEST OR A ``--label`` FILES THE BATCH UNDER ITS LABEL (U156), planned
    on the same handle by :mod:`cratekit.intake.label_filing` and written in the
    same commit, so the batch and its label playlists land together or not at
    all.
    """
    tree_id = declared.intake.id
    # WHY THE LANDING FILES NOTHING AFTER IT, empty when it files (U165): asked,
    # or a routing tree still on the bridge, where no database writer may write
    # its membership and a filing could only end refused.
    unfiled = (
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
    if ctx.args.export is not None:
        raise refuse(
            "intake-list-unusable",
            f"the intake tree {tree_id!r} is database native, so a landing adds the "
            f"files to the collection through the database and there is no export "
            f"to splice; drop --export, nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"tree_id": tree_id, "export": str(ctx.args.export)},
        )
    spec = gate_named(ctx.entry, NATIVE_GATE)
    if not planned.items:
        identity = {"kind": "land-native", "folder": str(planned.folder), "batch": planned.batch}
        empty = {"digest": digest_of(identity), "items": [], "totals": {"count": 0}, "chunk": None}
        if rehearse:
            # NOTHING TO REHEARSE, and never the owned hearts' write instead: a
            # rehearsal asks no gate, so it must not reach one (U162).
            if owned:
                raise refuse(
                    "intake-list-unusable",
                    f"{planned.folder} holds no file to land, and a rehearsal of the "
                    f"pass's {len(owned)} owned heart(s) alone is not built; run the "
                    f"landing without --rehearse to plan them, nothing was copied",
                    remedy=Remedy.FIX_COMMAND_LINE,
                    origin=_ORIGIN,
                    detail={"folder": str(planned.folder), "owned_hearts": len(owned)},
                )
            return ctx.envelope(data=empty, outcome=Outcome.NO_OP)
        if owned:
            return _place_owned(ctx, cfg, spec, declared=declared, owned=owned, empty=empty)
        return ctx.envelope(data=empty, outcome=Outcome.NO_OP)

    # THE LIBRARY CHECKS BEFORE THE DATABASE IS OPENED, so an unmounted volume
    # is named as the volume and a staging folder on another device refuses
    # without a snapshot copy of anything. Once here, and again by the engine
    # before its first move, as the xml landing's preflight is.
    landing.preflight_native(planned, cfg=cfg)
    # THE SET AND ITS NAME BEFORE THE GATE (U121): a job that is not a finished
    # set, and a name the page and the flags cannot complete, refuse with the
    # files still in staging and nothing shown.
    set_job: jobs.Job | None = None
    words: set_playlist.SetWords | None = None
    reports: tuple[dict[str, Any], ...] = ()
    if ctx.args.set_job:
        with jobs.open_store() as store:
            set_job = set_playlist.set_job_or_refuse(store, str(ctx.args.set_job))
            words = set_playlist.words_for(
                set_job, dj=ctx.args.dj, set_name=ctx.args.set_name, set_date=ctx.args.set_date
            )
            reports = set_playlist.reports_of(store, set_job)

    set_planned: list[set_playlist.SetPlaylistPlan] = []
    # U129. The account playlist's archive rides on this landing's gate when the
    # set already has one recorded under the frozen INSPIRATION name.
    archive_planned = _plan_set_archive(
        cfg,
        set_job=set_job,
        words=words,
        pass_name=ctx.args.pass_name or planned.batch,
    )

    def planner(cfg: config.Config, planned: landing.Plan) -> Callable[[Any], native.NativePlan]:
        # ONE PLANNER, TWO PLACES (U162): the live landing plans its own staging
        # folder and music folder, and a rehearsal plans the same files again at
        # its scratch area, through this same code, to apply them there.

        def set_plan(db, files) -> set_playlist.SetPlaylistPlan | None:
            if set_job is None or words is None:
                return None
            made = set_playlist.plan_for_landing(
                cfg,
                db,
                declared,
                set_job,
                words,
                reports,
                files=files,
                posted=getattr(ctx.args, "posted", None),
            )
            set_planned.append(made)
            return made

        def label_plan(db, files) -> label_filing.LabelPlan | None:
            # A MANIFEST WITH NO LABEL ROW FILES NOTHING, and asks nothing of the
            # catalogue tree, as the bridge's own check returns early on it.
            if manifest is not None and manifest.rows:
                return label_filing.plan_for_manifest(
                    cfg, db, medium, manifest=manifest, files=files
                )
            if label is not None:
                return label_filing.plan_for_label(db, medium, label=label, files=files)
            return None

        def plan(db) -> native.NativePlan:
            # THE FILED FOLDER, CHOSEN ON THIS HANDLE (U164): the batch lands
            # where a shelve would have filed it, so every row carries its
            # final FolderPath from the first commit and no shelve follows.
            target = shelve.landing_target(cfg, db, planned.batch, on=batch_name.today())
            files = [(item, target / item.name) for item in planned.items]
            # THE INBOX PLAYLIST FOR A SET (U135): named for the set, and an earlier
            # landing of the same job's playlist is added to under its first name.
            # The batch folder stays the dated (or --name) landing name so two
            # landings never share a folder; only the playlist joins.
            inbox_name = planned.batch
            batch_playlist_id = ""
            set_job_id = ""
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
                db,
                cfg,
                claims,
                tree_id=tree_id,
                registry=registry,
                batch=inbox_name,
                target=target,
            )
            made = native.plan_rows(
                cfg,
                db,
                tree_id=tree_id,
                registry=registry,
                batch=inbox_name,
                files=files,
                split=split,
                unplanned_left=emptied,
                pass_name=ctx.args.pass_name,
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
                set_plan=set_plan(db, files),
                batch_playlist_id=batch_playlist_id,
                set_job_id=set_job_id,
                inbox_leftovers=leftovers,
                inbox_found_by_name=inbox_found_by_name,
                labels=label_plan(db, files),
            )
            made = replace(made, folder=target, batch=planned.batch)
            # WHERE EACH NEW ROW WILL BE FILED, BEFORE IT EXISTS (U165), shown
            # and digested, so the one answer covers the filing after the commit.
            if unfiled:
                return made
            return native.with_filing(made, filing.predict(declared, made.to_add()))

        return plan

    archive_notes: list[dict[str, str]] = []
    applied: list[native.NativePlan] = []

    def write(db, rows: native.NativePlan) -> landing.LandedNative:
        applied.append(rows)
        # ONE LANDING PER BATCH NAME, HELD ACROSS THE WHOLE APPLY (R-432), as on
        # the bridge: the engine checks a target free and then renames over it.
        with landing.batch_lock(planned.batch):
            if ctx.args.name is None:
                _still_free(cfg, planned.batch)
            landed_native = landing.apply_native(
                planned, cfg=cfg, db=db, rows=rows, declared=declared
            )
        # THE LANDING IS THE PROOF. Archive after the batch is in the library.
        # A failure here must not fail a landing that already wrote: it becomes
        # a warning on the landed envelope, and so does apply_archive's own
        # "not renamed" return (U129).
        archive_notes.extend(_apply_landing_archive(cfg, archive_planned))
        return landed_native

    def payload_of(rows: native.NativePlan) -> dict:
        data = _native_payload(planned, rows, target=_folder(rows))
        return _with_archive(data, archive_planned)

    def shown_of(rows: native.NativePlan) -> dict[str, Any]:
        shown = _native_shown(rows, folder=planned.folder, target=_folder(rows))
        shown["files after landing"] = filing.fact(rows.filing, why=unfiled, tree=declared.tree.id)
        if archive_planned is not None:
            shown["account archive"] = archive_planned.shown
        # THE REHEARSAL THIS PLAN IS COMPARED AGAINST (U162), named, and equal
        # or not; a plan that differs prints the lines that differ.
        shown.update(
            rehearsal_facts(
                planned,
                digest=payload_of(rows)["digest"],
                plan=plan_lines(planned, rows, target=_folder(rows), archived=archive_planned),
            )
        )
        return shown

    plan = planner(cfg, planned)

    if rehearse:
        return _rehearse_native(
            ctx,
            cfg,
            planned,
            planner=planner,
            payload_of=payload_of,
            archived=archive_planned,
            declared=declared,
        )

    payload, landed = ask_then_write(
        ctx,
        cfg,
        spec,
        plan=plan,
        payload=payload_of,
        shown=shown_of,
        write=write,
    )
    if landed is None:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    native.assert_rows_gridless(landed.collection)
    native.assert_rows_identified(landed.collection)
    warnings = [{"code": entry.reason, "message": entry.sentence} for entry in landed.refused]
    warnings.extend(account_playlists.left_warning(landed.collection.left))
    warnings.extend(awaiting_analysis(landed.collection))
    warnings.extend(vox_warnings(landed.collection))
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
        # NOTHING WRITTEN, and the left rows are the write's own answer: the
        # members whose files did not land as well as the plan's left rows.
        warnings.extend(set_playlist.nothing_note(set_planned[0], left=len(kept.left)))
        warnings.extend(set_playlist.left_warning(kept.left))
    filed = landed.collection.labels
    if filed is not None:
        label_filing.assert_read_back(filed)
        warnings.extend(label_filing.unfiled_warning(filed.left))
    reported = _native_reported(payload, landed)
    predicted = applied[-1].filing if applied else None
    if predicted is not None:
        # THE FILING, AFTER EVERY READ BACK OF THE LANDING (U165), under the
        # actor who answered its gate. It never fails the landing it follows.
        sorted_in = filing.file_landed(
            cfg,
            declared,
            predicted,
            landed.collection,
            actor=_gate_actor(ctx, spec),
        )
        warnings.extend(filing.warnings(sorted_in))
        reported = _with_filing(reported, sorted_in)
    return ctx.envelope(data=reported, warnings=warnings)


def _gate_actor(ctx, spec) -> str:
    """Who the run record says answered the landing's gate, as the adopt verb reads it."""
    decision = ctx.run.decisions.get(spec.name)
    return decision.actor if decision is not None else ""


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


#: The verb a rehearsal record names, so a live landing reads only its own (U162).
REHEARSAL_VERB = "intake land"

#: The warning a set landing's rehearsal carries: its account archive was not rehearsed.
REHEARSAL_ARCHIVE_SKIPPED = "intake-rehearsal-archive-skipped"

#: At most this many differing lines on a live gate screen; the rest are counted.
REHEARSAL_LINES_SHOWN = 40


def rehearsal_key(planned: landing.Plan) -> dict[str, str]:
    """What a live landing and its rehearsal share: the staging folder and the batch."""
    return {"folder": str(planned.folder.resolve()), "batch": planned.batch}


def plan_lines(
    planned: landing.Plan, rows: native.NativePlan, *, target: Path, archived=None
) -> list[str]:
    """The native plan as ``path = value`` lines: the gate's identity and the engine's."""
    return rehearsal.lines(plan_identity(planned, rows, target=target, archived=archived))


def plan_identity(
    planned: landing.Plan, rows: native.NativePlan, *, target: Path, archived=None
) -> dict[str, Any]:
    """What :func:`plan_lines` prints, as values, so a rehearsal maps them before they are text.

    MAPPED AS VALUES, NEVER AS LINES (U188). Each line is a JSON value, which
    escapes every character outside ASCII and every quote, so a path with an
    accent in it is spelled in a line as no pair of real paths is, and a
    rehearsal of a batch named with one refused on every path it held.
    """
    # NOT THE ENGINE'S OWN DIGEST, which is a hash of the plan lines below and
    # so names every path in a form no mapping back can reach.
    gate = {
        key: value
        for key, value in _native_identity(planned, rows, target=target).items()
        if key != "collection"
    }
    if archived is not None:
        gate = {**gate, "archive": archived.payload["digest"]}
    return {"gate": gate, "plan": native.identity(rows)}


def rehearsal_facts(planned: landing.Plan, *, digest: str, plan: list[str]) -> dict[str, Any]:
    """The gate screen's lines naming the rehearsal a live plan is compared against, or none.

    THE NEWEST REHEARSAL OF THE SAME FOLDER AND BATCH, named by its run and
    time, and whether its digest equals this plan's. When it does not, the
    lines only the rehearsal had and the lines only this plan has, so the
    session reading the screen sees what moved and not merely that it moved.
    No line at all when no rehearsal was kept: the screen is as it was.
    """
    found = rehearsal.latest(verb=REHEARSAL_VERB, key=rehearsal_key(planned))
    if found is None:
        return {}
    equal = found.get("digest") == digest
    facts: dict[str, Any] = {
        "rehearsal": (
            f"run {found.get('run_id')} at {found.get('at')}: digest {found.get('digest')}, "
            + ("equal to this plan's" if equal else f"differs from this plan's {digest}")
        )
    }
    if not equal:
        lines = rehearsal.differing(found["plan"], plan)
        shown = lines[:REHEARSAL_LINES_SHOWN]
        if len(lines) > len(shown):
            shown.append(f"and {len(lines) - len(shown)} more line(s)")
        facts["differs from the rehearsal"] = shown
    return facts


def _active_rows(db) -> int:
    from sqlalchemy import text

    return int(
        db.session.execute(
            text("SELECT COUNT(*) FROM djmdContent WHERE rb_local_deleted = 0")
        ).scalar()
    )


def _rehearse_native(
    ctx,
    cfg: config.Config,
    planned: landing.Plan,
    *,
    planner: Callable[..., Callable[[Any], native.NativePlan]],
    payload_of: Callable[[native.NativePlan], dict],
    archived,
    declared,
) -> Envelope:
    """Rehearse the landing on a scratch area of this run's own, then remove it (U162).

    THE LIVE PLAN IS MADE FIRST, over the live staging folder and music folder
    and against the database copy, so its digest is the one the live landing
    will show; it is what the rehearsal reports and records. THEN THE SAME
    FILES ARE PLANNED AGAIN AT THE AREA, over their clones and the area's music
    folder, and applied there. The area's plan with every scratch path mapped
    back to its live one must read line for line as the live plan, or nothing
    is applied and the lines that differ are named: what the rehearsal applied
    is the plan the live run will be asked, not a plan like it.

    NOTHING LIVE IS WRITTEN OR MOVED. The live database file set is hashed and
    the live staging and music folders listed before and after, and a change
    is refused as the defect it would be. The account archive of a set
    landing is account side and is never rehearsed; the report says so.

    A FAILURE KEEPS THE AREA AND NAMES IT, so whoever reads the refusal can
    look at what the rehearsal saw. A rehearsal that ends removes it.
    """
    before = rehearsal.witness(
        cfg,
        (
            planned.folder,
            Path(cfg.library.root) / cfg.library.music_dir,
            *_filed_watch(cfg, planned),
        ),
    )
    area = rehearsal.open_area(cfg, ctx.run.run_id, files=planned.items, staging=planned.folder)
    try:
        facts, payload, lines = _rehearse_in(
            cfg,
            planned,
            area=area,
            planner=planner,
            payload_of=payload_of,
            archived=archived,
            declared=declared,
        )
    except CratekitError as exc:
        rehearsal.assert_untouched(before, kept=area.paths)
        inner = exc.cause
        raise refuse(
            inner.reason,
            f"{inner.message}; the rehearsal area is kept at "
            f"{', '.join(str(path) for path in area.paths)}",
            remedy=inner.remediation.remedy,
            steps=inner.remediation.steps,
            origin=_ORIGIN,
            detail={**dict(inner.detail), "rehearsal_area": [str(path) for path in area.paths]},
            inner=inner,
        ) from exc
    except KeyboardInterrupt as exc:
        rehearsal.assert_untouched(before, kept=area.paths)
        raise refuse(
            "cancelled",
            f"the rehearsal was interrupted; the rehearsal area is kept at "
            f"{', '.join(str(path) for path in area.paths)}",
            origin=_ORIGIN,
            detail={"rehearsal_area": [str(path) for path in area.paths]},
        ) from exc
    except Exception as exc:
        rehearsal.assert_untouched(before, kept=area.paths)
        raise refuse(
            "internal-error",
            f"the rehearsal failed ({exc}); the rehearsal area is kept at "
            f"{', '.join(str(path) for path in area.paths)}",
            origin=_ORIGIN,
            detail={"rehearsal_area": [str(path) for path in area.paths]},
        ) from exc
    rehearsal.assert_untouched(before, kept=area.paths)
    rehearsal.remove(area)
    facts["area removed"] = True
    recorded = rehearsal.record(
        ctx.run.run_id,
        verb=REHEARSAL_VERB,
        key=rehearsal_key(planned),
        digest=payload["digest"],
        plan=lines,
        facts=facts,
    )
    facts["record"] = str(recorded)
    data = {**payload, "totals": {**payload["totals"], "rehearsal": facts}}
    warnings = []
    if archived is not None:
        warnings.append(
            {
                "code": REHEARSAL_ARCHIVE_SKIPPED,
                "message": "the account archive this set landing would rename was planned "
                "and digested and not rehearsed, since it is a write to the account",
            }
        )
    return ctx.envelope(data=data, warnings=warnings)


def _rehearse_in(
    cfg: config.Config,
    planned: landing.Plan,
    *,
    area: rehearsal.Area,
    planner,
    payload_of,
    archived,
    declared,
) -> tuple[dict[str, Any], dict, list[str]]:
    """Plan live, plan at the area, compare, apply at the area, read back. Answers the facts."""
    db = rb_writer.open_db(area.database, require_closed=True, cfg=area.cfg)
    try:
        rows = planner(cfg, planned)(db)
        target = _folder(rows)
        payload = payload_of(rows)
        lines = plan_lines(planned, rows, target=target, archived=archived)
        # THE AREA'S PLAN IS MADE OUTSIDE THE REDIRECTION, reading the same
        # installation state the live plan read (a pass's jobs, a set's job),
        # so the only difference between the two plans is where the files are.
        staged = landing.plan(area.staging, area.cfg, planned.batch)
        scratch_rows = planner(area.cfg, staged)(db)
        scratch_target = _folder(scratch_rows)
        pairs = _mapped_back(
            area,
            planned,
            target=target,
            scratch_target=scratch_target,
            rows=rows,
            scratch_rows=scratch_rows,
        )
        back = rehearsal.lines(
            rehearsal.mapped(
                plan_identity(staged, scratch_rows, target=scratch_target, archived=archived),
                pairs,
            )
        )
        differ = rehearsal.differing(back, lines)
        if differ:
            raise refuse(
                "decision-stale",
                f"the plan made at the rehearsal area is not the live plan in "
                f"{len(differ)} line(s), in {', '.join(_fields_of(differ))}, so nothing "
                f"was applied there; the area's paths were compared after mapping "
                + ", ".join(f"{scratch} to {live}" for scratch, live in pairs)
                + "; a line only the area's plan has is marked -, one only the live plan has +: "
                + "; ".join(differ[:REHEARSAL_LINES_SHOWN]),
                origin=_ORIGIN,
                detail={"differs": differ, "mapped": [list(pair) for pair in pairs]},
            )
        # A NAME THE LIVE BATCH FOLDER ALREADY HOLDS IS HELD AT THE AREA TOO,
        # by an empty file of that name, so the area's move refuses the same
        # files the live move will and the facts say so. Occupancy is asked at
        # the move and not in the plan, so the plans alone cannot see it.
        for item in staged.items:
            if (target / item.name).exists() or (target / item.name).is_symlink():
                scratch_target.mkdir(parents=True, exist_ok=True)
                (scratch_target / item.name).touch()
        with rehearsal.redirected(area):
            session.assert_backup_acknowledged(area.cfg)
            rows_before = _active_rows(db)
            with landing.batch_lock(planned.batch):
                landed = landing.apply_native(
                    staged, cfg=area.cfg, db=db, rows=scratch_rows, declared=declared
                )
            native.assert_rows_gridless(landed.collection)
            native.assert_rows_identified(landed.collection)
            rows_after = _active_rows(db)
    finally:
        rb_writer.close_db(db)
    if not rb_writer.integrity_ok(area.database):
        raise refuse(
            "snapshot-integrity-failed",
            f"the database copy {area.database} fails SQLite's integrity check after "
            f"the rehearsal's landing",
            origin=_ORIGIN,
            detail={"database": str(area.database)},
        )
    facts: dict[str, Any] = {
        "run": area.run_id,
        "landed": len(landed.moved),
        "refused": len(landed.refused),
        "added": len(landed.collection.added),
        "already present": len(landed.collection.present),
        "memberships": landed.collection.memberships_added,
        "active rows before": rows_before,
        "active rows after": rows_after,
        "landed rows gridless": True,
        "integrity": "ok",
    }
    return facts, payload, lines


def _mapped_back(
    area: rehearsal.Area,
    planned: landing.Plan,
    *,
    target: Path,
    scratch_target: Path,
    rows: native.NativePlan,
    scratch_rows: native.NativePlan,
) -> tuple[tuple[str, str], ...]:
    """Each scratch spelling in the area's plan and the live spelling it stands for.

    The area's staging and its batch folder in the MOUNTED spelling, the one
    every ``from`` and ``to`` is written in, and the batch folder again in the
    STORED spelling rekordbox keeps ``FolderPath`` under (U188). On a library
    whose base drive is not its mount, the live one, a row's path is stored
    under the base drive, so neither mounted pair occurs in it and every row
    differed by the area's prefix alone. The stored pair is spelled by the
    writer's own :func:`native.stored_folder_path`, with the drives each plan
    read off its database, so the comparison can never use a spelling rule
    the rows were not written by. A library whose drive never moved stores the
    mounted spelling, and the stored pair is the mounted one, dropped as a
    repeat.
    """
    stored = (
        native.stored_folder_path(
            scratch_target,
            base_drive=scratch_rows.base_drive,
            current_drive=scratch_rows.current_drive,
        ),
        native.stored_folder_path(
            target, base_drive=rows.base_drive, current_drive=rows.current_drive
        ),
    )
    return tuple(
        dict.fromkeys(
            (
                (str(area.staging), str(planned.folder)),
                (str(scratch_target), str(target)),
                stored,
            )
        )
    )


def _fields_of(differ: list[str]) -> list[str]:
    """The fields the differing lines are in, each once, ``rows.columns.FolderPath`` for a row's path.

    The line's path with every index taken out and its first part, ``gate``
    or ``plan``, left off, so a field is named as the identity spells it and
    a leaf that is one entry of a list is named by the list it is in.
    """
    names = []
    for line in differ:
        path = re.sub(r"\[\d+\]", "", line[2:].split(" = ", 1)[0])
        names.append(path.split(".", 1)[-1])
    return list(dict.fromkeys(names))


def _place_owned(
    ctx,
    cfg: config.Config,
    spec,
    *,
    declared,
    owned: tuple[account_playlists.HeartRow, ...],
    empty: dict,
) -> Envelope:
    """The pass's owned hearts All Favorites lacks, placed when no file was downloaded (U146).

    THE LANDING'S GATE AND THE BACKFILL'S WRITER. Asked first of a handle
    opened to read, so a pass whose owned hearts are all placed, which is
    nearly every pass, opens nothing to write and asks nothing, and ends
    NO_OP exactly as an empty landing did. When some heart is missing, the
    order is :func:`ask_then_write`'s: the database opened with write intent,
    the plan taken again on it, the acknowledgment, the gate, and the guarded
    session of :func:`backfill.apply`, which takes the plan once more and
    refuses a digest that moved, then reads every membership back.

    A LIBRARY WITH NO ALL FAVORITES, OR TWO, IS NOT A REFUSAL, as a landing
    with files skips its placement: there is nothing else to land, so the
    pass ends NO_OP and says why.
    """
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
                {
                    "code": FAVORITES_SKIPPED,
                    "message": (
                        f"nothing to land and no owned heart was placed: "
                        f"{exc.cause.message}; run crate favorites backfill once the "
                        f"playlist exists"
                    ),
                }
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
        ctx,
        cfg,
        spec,
        plan=lambda db: backfill.plan_owned(cfg, db, source=source, rows=owned),
        payload=lambda planned: backfill.payload(planned, cfg),
        shown=backfill.landing_facts,
        write=written,
    )
    if done is None:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    backfill.assert_read_back(done)
    placed = done.placed
    totals = {**payload["totals"], "hearts placed": placed.added}
    warnings = [
        {
            "code": FAVORITES_PLACED,
            "message": (
                f"{placed.said()}, for {len(payload['items'])} owned heart(s); no file "
                f"was landed; undo with a restore of session {done.session_id}"
            ),
        }
    ]
    # THE COLOUR'S NOTES (U153), the same two a landing with files carries.
    if placed.colour_skipped:
        warnings.append(
            {
                "code": colour_mod.PINK_COLOUR_MISSING,
                "message": (
                    f"no row is coloured: {placed.colour_skipped}; the hearts are placed "
                    f"all the same, and crate favorites backfill colours them once the "
                    f"library carries Pink again"
                ),
            }
        )
    if placed.held:
        warnings.append(
            {
                "code": FAVORITES_COLOUR_HELD,
                "message": (
                    f"{len(placed.held)} row(s) carry a colour a person chose and keep it: "
                    + "; ".join(one.said() for one in placed.held)
                ),
            }
        )
    return ctx.envelope(data={**payload, "totals": totals}, warnings=warnings)


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
    notes = [{"code": FAVORITES_PLACED, "message": placed.said()}]
    # THE COLOUR'S OWN NOTES (U153), from what the write knew, so the apply
    # reports the held rows and the missing Pink row the gate screen showed.
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


def _native_split(
    db,
    cfg: config.Config,
    claims: tuple[account_playlists.Claim, ...],
    *,
    tree_id: str,
    registry,
    batch: str,
    target: Path,
) -> tuple[tuple[native.PlaylistPlan, ...], tuple[tuple[str, account_playlists.Left], ...]]:
    """Each account playlist named against what the database's INBOX holds, on the write handle.

    AND EACH OWNED TRACK'S ROW FOUND BY PATH ON THE SAME HANDLE (U128), at plan
    time, so the screen and the digest name the rows the apply adds and the
    apply finds nothing again. Asked of the candidate rows whose stored path
    ends in the file's name, the native landing's own lookup, rather than of
    the whole collection. Answers the playlists and the left rows of the ones
    left holding nothing.
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
                name=claimed.name,
                account=claimed.playlist_id,
                members=tuple(
                    native.PlaylistMember(target=target / member.file.name, member=member)
                    if member.file is not None
                    else native.PlaylistMember(content_id=member.row, member=member)
                    for member in claimed.members
                ),
                account_name=claimed.account_name,
                left=claimed.left,
            )
            for claimed in resolved
        ),
        emptied,
    )




#: Why a set landing's account archive did not finish after the rows wrote (U129).
LAND_ARCHIVE_FAILED = "intake-land-archive-failed"


def _apply_landing_archive(cfg, archived) -> list[dict[str, str]]:
    """Apply the account archive after the landing wrote. Failures are warnings.

    The landing's rows are already in the library. An account call that raises,
    or an apply that leaves the playlist unrenamed, must not turn the landing
    into a failure: both ride the warnings channel on the landed envelope.
    """
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


def _plan_set_archive(cfg, *, set_job, words, pass_name: str):
    """The account archive for this set landing, or None when there is none to file (U129)."""
    if set_job is None:
        return None
    from cratekit.export import set_cli
    from cratekit.modules.outbound import ledger

    name = set_playlist.frozen_name(set_job)
    if not name and words is not None:
        name = set_cli.set_name(set_playlist.playlist_name(words))
    if not name or ledger.set_playlist(cfg, name) is None:
        return None
    try:
        return set_cli.plan_archive_named(cfg, name, pass_name=pass_name)
    except CratekitError:
        # Soft: the landing still lands; archive can run later via export archive.
        return None


def _with_archive(payload: dict, archived) -> dict:
    """Fold the archive plan into the landing's digest and items so one approval covers both."""
    if archived is None:
        return payload
    identity = {
        "land": payload["digest"],
        "archive": archived.payload["digest"],
    }
    items = list(payload.get("items") or [])
    for item in archived.payload.get("items") or []:
        items.append({**item, "area": "account-archive"})
    totals = dict(payload.get("totals") or {})
    totals["archive_writes"] = bool(archived.writes)
    return {
        **payload,
        "digest": digest_of(identity),
        "items": items,
        "totals": totals,
    }



#: What a native write plans: a landing's rows, or the owned hearts alone (U146).
_Planned = TypeVar("_Planned")


def ask_then_write(
    ctx,
    cfg: config.Config,
    spec,
    *,
    plan: Callable[[Any], _Planned],
    payload: Callable[[_Planned], dict],
    shown: Callable[[_Planned], dict[str, Any]],
    write: Callable[[Any, _Planned], Any],
) -> tuple[dict, Any | None]:
    """The order every native intake write keeps, held once. Answers (payload, written).

    SHARED BY THE LANDING AND ``intake file`` (R-770), and by the landing's
    owned hearts when no file came (U146), because the order is the contract
    and two hand kept copies of it would come to differ:

    * THE DATABASE IS OPENED WITH WRITE INTENT BEFORE THE PLAN, so a running
      rekordbox or its agent refuses before anything is shown, and the plan is
      made against the database the write will be made to;
    * THE ACKNOWLEDGMENT IS READ BEFORE THE GATE (R-733): an approval is the
      one way door on a live library, and a person who reads the whole plan
      and answers should not then be refused by something the verb could have
      read first;
    * the gate is asked over the digested plan, and only ``apply`` writes;
    * the handle is closed whatever happened.

    * THE ANSWER IS PINNED TO THE FILE THE HANDLE OPENED (U161). The digest
      names the library and not the file, so a copy rehearsal digests as the
      live plan; the file is pinned on the run beside it, and a continuation
      that opens another file is refused stale rather than writing there.

    ``written`` is None when the answer was not ``apply``, and the payload is
    then the plan as it was shown.
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
    return [
        {
            "code": AWAITING_ANALYSIS,
            "message": (
                f"{len(collection.added)} row(s) joined the collection with no "
                f"tempo, grid, key or waveform, and rekordbox analyses nothing on its "
                f"own with Auto Analysis off; open rekordbox, select the "
                f"{collection.analyze_name} playlist, which holds every row waiting "
                f"for analysis, and run Analyze Track; then crate inbox analyzed takes "
                f"out each row rekordbox analysed"
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
            }
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
        }
    ]


__all__ = [
    "AWAITING_ANALYSIS",
    "LAND_ARCHIVE_FAILED",
    "INTAKE_SUFFIX",
    "NATIVE_GATE",
    "RETIRED_SUFFIX",
    "VERIFY_VERB",
    "XML_GATE",
    "ask_then_write",
    "awaiting_analysis",
    "build_land",
    "collection_facts",
    "vox_fact",
    "vox_warnings",
    "VOX_NOT_WRITTEN",
    "VOX_UNSCORED",
    "BRIDGE_VOX_OWED",
    "default_name",
    "gate_named",
    "intake_file",
    "intake_land",
    "intake_stem",
    "playlist_item",
    "set_playlist_item",
    "unretired_name",
]
