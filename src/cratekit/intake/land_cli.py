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
the landing's own commit (U156, :mod:`cratekit.intake.label_filing`), and so,
with ``--label-from-tags``, is each file under the label its own label tag
names, which is how a Bandcamp batch of several sellers lands (U177).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, approving_actor, digest_of
from cratekit.core import config, rehearsal
from cratekit.core.cause import CratekitError, Outcome, Remedy, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import (
    account_playlists,
    batch_name,
    filing,
    ingest,
    land_native,
    landing,
    native,
    set_playlist,
)
from cratekit.intake import cli as intake_cli
from cratekit.intake.land_native import (  # noqa: F401 - re-exported, callers name these on land_cli
    DATABASE_PIN,
    LAND_ARCHIVE_FAILED,
    _apply_landing_archive,
    _place_owned,
    _plan_set_archive,
    _with_archive,
    ask_then_write,
)
from cratekit.intake.land_rehearse import (  # noqa: F401 - re-exported, callers name these on land_cli
    REHEARSAL_ARCHIVE_SKIPPED,
    REHEARSAL_LINES_SHOWN,
    REHEARSAL_VERB,
    _fields_of,
    _rehearse_native,
    plan_identity,
    plan_lines,
    rehearsal_key,
)
from cratekit.intake.land_report import (  # noqa: F401 - re-exported, callers name these on land_cli
    AUTO_ANALYSIS_STEP,
    AWAITING_ANALYSIS,
    BRIDGE_VOX_NONE,
    BRIDGE_VOX_OWED,
    DYN_NOT_WRITTEN,
    FAVORITES,
    FAVORITES_COLOUR_HELD,
    FAVORITES_PLACED,
    FAVORITES_SKIPPED,
    FILED,
    LAND,
    LANDED,
    PLAYLIST,
    REFUSED,
    TWIN,
    TWINS_LEFT,
    UNFILED,
    VOX_MOSTLY_UNSCORED,
    VOX_NOT_WRITTEN,
    VOX_UNSCORED,
    _folder,
    _native_payload,
    _native_reported,
    _native_shown,
    _payload,
    _reported,
    _shown,
    _with_filing,
    awaiting_analysis,
    bridge_vox_fact,
    collection_facts,
    dyn_fact,
    dyn_warnings,
    favorites_facts,
    favorites_notes,
    playlist_item,
    set_playlist_item,
    split_facts,
    twin_facts,
    vox_fact,
    vox_plan_warnings,
    vox_warnings,
)

#: The two gates, one per medium. The xml one answers inline as it always has;
#: the native one is explicit, because a content row in the collection is a
#: new kind of write and R34 forbids a blanket answer for it.
XML_GATE = "intake.land.confirm"
NATIVE_GATE = "intake.land.native"

_ORIGIN = ("intake.land_cli",)

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


def pass_landed(cfg: config.Config, name: str) -> bool:
    """Whether a landing of the pass ``name`` is proven, on either medium (R-1467).

    THE TWO PROOFS ``label mark`` AND ``sync mark`` ALREADY TAKE. On the bridge
    a landing writes its intake file at the library root, named for its pass
    (:func:`intake_file`), and keeps it there, pending or retired once its
    import is proven (:func:`unretired_name`). On a database native intake tree
    a closed landing that committed records the pass
    (:func:`cratekit.intake.native.landings_of_pass`). Either is read whatever
    the intake tree's medium is now, so a pass landed before a cutover still
    reads as landed after it.

    A ROOT THAT CANNOT BE READ REFUSES, NEVER READS AS NOT LANDED OR LANDED.
    Both proofs live under the library root, so an unmounted volume would
    answer "no proof" for every pass, and a caller naming which batch is
    still waiting in staging must be told it could not read rather than
    guess. A session log that cannot be listed refuses through
    :func:`cratekit.core.session.records`, as every reader of it does.
    """
    root = Path(cfg.library.root)
    wanted = f"{name}{INTAKE_SUFFIX}"
    try:
        if not root.is_dir():
            raise OSError(f"{root} is not a directory")
        for entry in root.iterdir():
            if unretired_name(entry.name) == wanted and entry.is_file():
                return True
    except OSError as exc:
        raise refuse(
            "library-root-unreachable",
            f"the library root {root} could not be read ({exc}), so whether the pass "
            f"{name!r} landed cannot be told from its intake file or its native "
            f"landing's record; refusing rather than reading it either way",
            steps=("mount the library volume, then run the command again",),
            origin=_ORIGIN,
            detail={"root": str(root), "pass": name},
        ) from exc
    return bool(native.landings_of_pass(cfg, name))


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
        "--label-from-tags",
        dest="label_from_tags",
        action="store_true",
        help=(
            "file each landed file under the label its own label tag names, in the "
            "year its date tag names, as crate acquire bandcamp-fetch tags a "
            "registered label's purchases; a file with no label tag or no date tag "
            "is named and filed nowhere (database native intake trees only)"
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
    from_tags: bool = False,
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

    ``--label-from-tags`` (U177) is held to every one of those but the blank,
    and is refused beside ``--label`` too, since one label for every file and
    each file's own are two answers to one question. It returns None, and the
    caller reads the flag itself.
    """
    if from_tags and given is not None:
        raise refuse(
            "intake-list-unusable",
            "--label and --label-from-tags both say which label each file is filed "
            "under, one for every file and the other each file's own tag; pass one "
            "of them, nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"label": given},
        )
    if given is None and not from_tags:
        return None
    flag = "--label-from-tags" if from_tags else "--label"
    if given is not None and not given.strip():
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
    return given.strip() if given is not None else None


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
    manifest = landing.read_label_manifest(Path(ctx.args.manifest)) if ctx.args.manifest else None
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
    label_from_tags = bool(getattr(ctx.args, "label_from_tags", False))
    label = _label_flag(
        ctx.args.label, manifest=manifest, medium=medium, cfg=cfg, from_tags=label_from_tags
    )
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
            medium=medium,
            owned=owned,
            rehearse=rehearse,
            manifest=manifest,
            label=label,
            label_from_tags=label_from_tags,
            claims=claims,
            hearted=hearted,
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


def _land_native(
    ctx,
    cfg: config.Config,
    planned: landing.Plan,
    *,
    medium: ingest.IntakeMedium,
    owned: tuple[account_playlists.HeartRow, ...] = (),
    rehearse: bool = False,
    **asked,
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
    declared = medium.declared
    tree_id = declared.intake.id
    unfiled = land_native.unfiled_reason(ctx, medium)
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
    set_job, words, reports = land_native.read_set(ctx)
    set_planned: list[set_playlist.SetPlaylistPlan] = []
    # U129. The account playlist's archive rides on this landing's gate when the
    # set already has one recorded under the frozen INSPIRATION name.
    archive_planned = _plan_set_archive(
        cfg,
        set_job=set_job,
        words=words,
        pass_name=ctx.args.pass_name or planned.batch,
    )
    planner = land_native.native_planner(
        ctx,
        medium,
        owned=owned,
        unfiled=unfiled,
        set_job=set_job,
        words=words,
        reports=reports,
        set_planned=set_planned,
        **asked,
    )
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
    warnings = land_native.landed_warnings(
        cfg, payload, landed, applied=applied, archive_notes=archive_notes, set_planned=set_planned
    )
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
            actor=approving_actor(ctx, spec),
        )
        warnings.extend(filing.warnings(sorted_in))
        reported = _with_filing(reported, sorted_in)
    return ctx.envelope(data=reported, warnings=warnings)


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
