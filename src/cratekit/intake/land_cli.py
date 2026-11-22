"""``intake.land``: a staged batch moves into the library behind one gate.

The engine is :mod:`cratekit.intake.landing`; this shell owns the plan, the
gate and what a person is told afterwards. The native medium's steps are in
:mod:`land_native`, its gate screens and notes in :mod:`land_report`, and the
rehearsal in :mod:`land_rehearse`; every name a caller reads here is
re-exported here.

THE PLAN IS SHOWN BEFORE ANYTHING MOVES, and an answer recorded against it is
refused as stale if the folder, the batch, the intake file or the manifest's
bytes changed since, because the digest covers all of them.

THE IMPORT IS THE PERSON'S AND BLOCKS NOTHING. A landed batch is an intake
file rekordbox has not seen; :func:`ingest.place_files` persists its
``rekordbox_import`` pending action on the intake session record (not the
run, where nothing would clear it), and the envelope carries that same
action, so the screen and the session log cannot differ.

A label row no landed file matches is a warning naming the track, never a
failure. On a database native tree a manifest's rows, ``--label`` or
``--label-from-tags`` file the batch under the Record Labels tree in the
landing's own commit (U156, U177).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, approving_actor
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
    _plan,
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

#: The verb that proves an intake file imported, spelled once in ``ingest``.
VERIFY_VERB = ingest.VERIFY_VERB

INTAKE_SUFFIX = "_inboxed.xml"

#: What an intake file's name gains once its import is proven (R-501). It ends
#: the name so the cutover precheck's ``*.xml`` scan stops seeing the file; a
#: second file retired under a taken name gains ``-2``.
RETIRED_SUFFIX = ".imported"

_RETIRED_TAIL = re.compile(re.escape(RETIRED_SUFFIX) + r"(-[0-9]+)?$")


def unretired_name(name: str) -> str:
    """An intake file's name as it was written, retired or not, so a verb
    handed the retired name reads the same pass off it."""
    return _RETIRED_TAIL.sub("", name)


def default_name(run_id: str) -> str:
    """A run's identifier WITHOUT ITS COLONS, as a file name for an intake file
    or a pass. A colon cannot be in a file name on exFAT and reads as a slash
    in Finder. Not the batch's name, which :mod:`batch_name` makes (U110).
    """
    return run_id.replace(":", "")


def intake_stem(*, pass_name: str | None, name: str | None, run_id: str) -> str:
    """What a landing's intake file is named for, before ``_inboxed.xml``.

    THE PASS FIRST, because the marks find and key the pass by the file's
    name; then ``--name``, so a landing typed before ``--pass`` existed still
    writes the file a later mark reads; then the landing's own run.
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
    """Where a landing's intake file is written: beside the library, not in
    staging, which a person cleans before rekordbox may have imported it. The
    suffix is one the pending intake scan walks, so the cutover check sees it.
    """
    return Path(cfg.library.root) / f"{stem}{INTAKE_SUFFIX}"


def pass_landed(cfg: config.Config, name: str) -> bool:
    """Whether a landing of the pass ``name`` is proven, on either medium (R-1467).

    The intake file at the library root, pending or retired, or a committed
    native landing's record of the pass, read whatever the medium is now, so a
    pass landed before a cutover still reads as landed after it.

    A ROOT THAT CANNOT BE READ REFUSES, never reads either way: an unmounted
    volume would answer "no proof" for every pass.
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

    UNDER THE BATCH LOCK, since the name was chosen before the gate and two
    landings that found it free would share a folder. Only a name this run
    chose: one given with ``--name`` is the person's to land into again.
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
        metavar="FOLDER",
        help="the folder of acquired files to land (default: download staging)",
    )
    parser.add_argument(
        "--export",
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
        metavar="PASS",
        help=(
            "the pass these files were acquired under, as crate intake missing --run "
            "or crate label sync --go printed it; the intake file is named for it, so "
            "sync mark finds the pass, and the batch is named for the pass's sources"
        ),
    )
    parser.add_argument(
        "--manifest",
        metavar="JSON",
        help=(
            "the manifest written beside the list these files were acquired "
            "from; its label rows are filed under the record labels tree"
        ),
    )
    parser.add_argument(
        "--label",
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

    NATIVE ONLY, since the bridge would ignore the flag and file the batch under
    nothing. NOT BESIDE A MANIFEST or, for ``--label-from-tags`` (U177), beside
    ``--label``: two answers to one question. NOT BLANK, since a playlist named
    for nothing stays in the tree. NOT ON AN UNREACHABLE ROOT, said as that,
    since the medium was not read. ``--label-from-tags`` returns None and the
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

    AN EMPTY FOLDER IS A PLAN, NOT A REFUSAL: staging is empty after every
    landing, and a person is told there is nothing to move. The empty plan
    never reaches :func:`landing.apply`. A path that is not a folder still goes
    to the engine, which refuses it.
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
    """Each account playlist named against the export's INBOX and the pending intake files.

    An export that cannot be read names against the pending files only: the
    preflight refuses it before anything moves.
    """
    if not claims:
        return ()
    held: tuple[str, ...] | str = ()
    if declared is not None and registry is not None:
        held = landing.inbox_held(export, landing.Checked(registry=registry, declared=declared))
    taken = (*(held if isinstance(held, tuple) else ()), *account_playlists.pending_names(cfg))
    return account_playlists.named(claims, taken, batch=batch)


def gate_named(entry, name: str):
    """One of a verb's gates by name, never by position, since the order the
    gates are declared in is no promise (R-746, R-770)."""
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
    # READ BEFORE THE GATE, so a bad manifest refuses before anybody answers.
    manifest = (
        landing.read_label_manifest(Path(ctx.args.manifest)) if ctx.args.manifest else None
    )
    # TWO NAMES (U110): the batch a person reads in INBOX, by date and source
    # unless ``--name`` says otherwise, and the intake file the marks read.
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
    # WHICH ACCOUNT PLAYLIST ASKED FOR EACH FILE (U113), before the gate, so
    # the screen says where every file goes.
    claims = account_playlists.split(cfg, pass_name, planned.items)
    # THE MEDIUM IS THE INTAKE TREE'S MODE (R-746), read through
    # ``ingest.intake_medium`` and no copy of it, so ``intake file`` cannot
    # choose by another rule (R-770). An unreachable root takes the xml path,
    # whose preflight names the library before the gate.
    medium = ingest.intake_medium(cfg)
    declared, registry = medium.declared, medium.registry
    # THE SET PLAYLIST IS A DATABASE WRITE (U121), refused on the bridge before
    # the gate rather than quietly written nowhere, and so is a word without
    # the set, since nothing would read it.
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
        # WHICH FILES ARE HEARTS (U120), and which hearts the library already
        # held (U146), on the native medium alone, since the bridge places none.
        hearted = account_playlists.hearted(cfg, pass_name, planned.items)
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
    # With no export and no library, the preflight refuses on the library first.
    export = (
        Path(ctx.args.export)
        if ctx.args.export is not None
        else Path(cfg.library.root) / "collection.xml"
    )
    destination = intake_file(cfg, stem)
    split = _xml_split(cfg, claims, export, batch=batch, declared=declared, registry=registry)
    # EACH OWNED TRACK FOUND IN THE EXPORT BEFORE THE GATE (U128), so the digest
    # covers what the intake file will hold.
    split, emptied = landing.owned_in_export(cfg, split, export)
    # THE ENGINE'S PRE-MOVE CHECKS BEFORE THE GATE TOO (R-677): a plan that
    # could never run is said before anybody answers it. Only when something
    # would move, since a plan of nothing splices nothing.
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
    facts = {"target": target, "destination": destination, "manifest": manifest, "split": split}
    payload = _payload(planned, export=export, emptied=emptied, **facts)
    spec = gate_named(ctx.entry, XML_GATE)
    try:
        option = ctx.gate.require(
            spec,
            digest=payload["digest"],
            context=_shown(planned, cfg=cfg, emptied=len(emptied), **facts),
        )
    except CratekitError as exc:
        # THE REFUSAL TAKES THE PLACE OF AN UNANSWERED GATE ONLY: an answer
        # already given is honoured, an abort ends in nothing done and an apply
        # reaches the engine, which checks again. Read off the remedy because
        # this layer cannot import the gate's own class.
        if unusable is not None and exc.cause.remediation.remedy is Remedy.ANSWER_DECISION:
            raise unusable from None
        raise
    if option != "apply" or not planned.items:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    # The engine lists the folder again and refuses a fingerprint that moved.
    # ONE LANDING PER BATCH NAME AND PER INTAKE FILE, held across the apply
    # (R-432, U110): the engine checks a target free and then renames over it,
    # and the file is named for the pass while the batch is named for the date.
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

    THE ORDER IS :func:`ask_then_write`'s. THE GATE TAKES NO INLINE ANSWER:
    content rows in the collection are answered by a separate recorded act
    (R34), which is not spent on learning there is nothing to move, so a plan
    of nothing is not asked. An empty staging folder still places the pass's
    owned hearts (U146) under this gate, through :func:`_place_owned`.
    ``asked`` is what :func:`land_native.native_planner` plans from.
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
        empty = _plan(identity, [], 0)
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
    # is named as the volume; the engine asks again before its first move.
    landing.preflight_native(planned, cfg=cfg)
    set_job, words, reports = land_native.read_set(ctx)
    set_planned: list[set_playlist.SetPlaylistPlan] = []
    # The account playlist's archive rides on this gate when the set has one
    # recorded under the frozen INSPIRATION name (U129).
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
        # ONE LANDING PER BATCH NAME, HELD ACROSS THE WHOLE APPLY (R-432).
        with landing.batch_lock(planned.batch):
            if ctx.args.name is None:
                _still_free(cfg, planned.batch)
            landed_native = landing.apply_native(
                planned, cfg=cfg, db=db, rows=rows, declared=declared
            )
        # Archive after the batch is in the library; a failure is a warning,
        # never a failure of a landing that already wrote (U129).
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
        # THE REHEARSAL THIS PLAN IS COMPARED AGAINST (U162).
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

    The newest rehearsal of the same folder and batch, and whether its digest
    equals this plan's; when not, the lines that differ, so the session sees
    what moved. No line when no rehearsal was kept.
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
