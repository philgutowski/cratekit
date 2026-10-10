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
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Callable

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs, rb_writer, session
from cratekit.core.cause import CratekitError, Outcome, Remedy, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import placement
from cratekit.intake import account_playlists, batch_name, ingest, landing, native, set_playlist
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

#: The two gates, one per medium. The xml one answers inline as it always has;
#: the native one is explicit, because a content row in the collection is a
#: new kind of write and R34 forbids a blanket answer for it.
XML_GATE = "intake.land.confirm"
NATIVE_GATE = "intake.land.native"

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
    set_playlist.add_word_arguments(parser)
    parser.set_defaults(_handler=intake_land)


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
    if medium.native:
        # AND WHICH FILES ARE HEARTS (U120), read from the same jobs the same
        # way, each with the quarter the account dated it into. The native
        # medium alone, since the bridge writes an export and places none, so
        # the match over the planned files is not made for nothing there.
        hearted = account_playlists.hearted(cfg, pass_name, planned.items)
        return _land_native(
            ctx,
            cfg,
            planned,
            target=target,
            declared=declared,
            registry=registry,
            manifest=manifest,
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


def _native_payload(planned: landing.Plan, rows: native.NativePlan, *, target: Path) -> dict:
    """The plan as the approval gate shows it: one item per file, with its row.

    EVERY COLUMN THE ROW WOULD CARRY IS ON THE ITEM, and the digest is taken
    over the files, the folder, the batch and the collection plan together, so
    an answer given for one folder, one batch name, one database or one set of
    rows is stale for another. The engine's own digest already covers the rows
    and the root; the files' fingerprint covers what is on disk.
    """
    by_target = {str(row.target): row for row in rows.rows}
    hearts = (
        {str(one.target): one.quarter for one in rows.favorites.items}
        if rows.favorites is not None
        else {}
    )
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
            entry["heart"] = hearts[str(row.target)] or "quarter left to the backfill"
        if row.action == native.ADD and rows.vox_cut is not None and not rows.vox_blocked:
            # U127: the score each added row was read at and whether it is tagged.
            entry["voxlevel"] = row.voxlevel
            entry["vox"] = row.vox
        items.append(entry)
    identity = {
        "kind": "land-native",
        "folder": str(planned.folder),
        "batch": planned.batch,
        "target": str(target),
        "files": planned.digest,
        "collection": rows.digest,
    }
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
    facts: dict[str, Any] = {
        "hearts": f"{len(plan.items)} file(s) the account hearts, into {where} and their quarter",
        "quarter playlists": [
            f"{quarter} ({sum(1 for item in plan.items if item.quarter == quarter)} file(s))"
            + (", made" if quarter in plan.creates else "")
            for quarter in plan.quarters
        ],
    }
    if plan.unknown:
        facts["quarter left to the backfill"] = (
            f"{plan.unknown} file(s) whose job froze no date, which join "
            f"{plan.source_name!r} here and take their quarter from crate favorites backfill"
        )
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
    return {
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
    }


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
    return shown


def _native_reported(payload: dict, landed: landing.LandedNative) -> dict:
    """The plan, each item marked with what the apply actually did to it."""
    refused = {str(entry.path): entry for entry in landed.refused}
    added = {str(row.target): row for row in landed.collection.added}
    present = {str(row.target): row for row in landed.collection.present}
    items: list[dict[str, Any]] = []
    for item in payload["items"]:
        if item.get("action") == FAVORITES:
            # The skipped placement, carried through as the plan said it (U120).
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
            for name, row, count in placed.quarters
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
    target: Path,
    declared,
    registry,
    manifest: landing.LabelManifest | None,
    claims: tuple[account_playlists.Claim, ...] = (),
    hearted: tuple[account_playlists.Hearted, ...] = (),
) -> Envelope:
    """Plan the rows against the database, ask, then move and write.

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
    """
    tree_id = declared.intake.id
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
    if manifest is not None:
        raise refuse(
            "intake-list-unusable",
            f"the intake tree {tree_id!r} is database native and label filing from a "
            f"manifest is written into an intake file, which this medium does not "
            f"make; land without --manifest, nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"tree_id": tree_id, "manifest": str(manifest.path)},
        )
    spec = gate_named(ctx.entry, NATIVE_GATE)
    if not planned.items:
        identity = {"kind": "land-native", "folder": str(planned.folder), "batch": planned.batch}
        empty = {"digest": digest_of(identity), "items": [], "totals": {"count": 0}, "chunk": None}
        return ctx.envelope(data=empty, outcome=Outcome.NO_OP)

    # THE LIBRARY CHECKS BEFORE THE DATABASE IS OPENED, so an unmounted volume
    # is named as the volume and a staging folder on another device refuses
    # without a snapshot copy of anything. Once here, and again by the engine
    # before its first move, as the xml landing's preflight is.
    landing.preflight_native(planned, cfg=cfg)
    files = [(item, target / item.name) for item in planned.items]
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

    def set_plan(db) -> set_playlist.SetPlaylistPlan | None:
        if set_job is None or words is None:
            return None
        made = set_playlist.plan_for_landing(
            cfg, db, declared, set_job, words, reports, files=files
        )
        set_planned.append(made)
        return made

    def write(db, rows: native.NativePlan) -> landing.LandedNative:
        # ONE LANDING PER BATCH NAME, HELD ACROSS THE WHOLE APPLY (R-432), as on
        # the bridge: the engine checks a target free and then renames over it.
        with landing.batch_lock(planned.batch):
            if ctx.args.name is None:
                _still_free(cfg, planned.batch)
            return landing.apply_native(planned, cfg=cfg, db=db, rows=rows, declared=declared)

    def plan(db) -> native.NativePlan:
        split, emptied = _native_split(
            db,
            cfg,
            claims,
            tree_id=tree_id,
            registry=registry,
            batch=planned.batch,
            target=target,
        )
        return native.plan_rows(
            cfg,
            db,
            tree_id=tree_id,
            registry=registry,
            batch=planned.batch,
            files=files,
            split=split,
            unplanned_left=emptied,
            pass_name=ctx.args.pass_name,
            hearts=tuple(
                native.HeartItem(target=target / one.path.name, quarter=one.quarter, ref=one.ref)
                for one in hearted
            ),
            favorites_source=placement.source_name(declared),
            set_plan=set_plan(db),
        )

    payload, landed = ask_then_write(
        ctx,
        cfg,
        spec,
        plan=plan,
        payload=lambda rows: _native_payload(planned, rows, target=target),
        shown=lambda rows: _native_shown(rows, folder=planned.folder, target=target),
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
    return ctx.envelope(data=_native_reported(payload, landed), warnings=warnings)


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
    quarters = ", ".join(
        f"{name}{' (made)' if name in placed.created else ''}" for name, _row, _n in placed.quarters
    )
    return [
        {
            "code": FAVORITES_PLACED,
            "message": (
                f"{placed.added} membership(s) placed: {placed.added_source} into "
                f"{placed.source_name!r} and the rest into {quarters}"
            ),
        }
    ]


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


def ask_then_write(
    ctx,
    cfg: config.Config,
    spec,
    *,
    plan: Callable[[Any], native.NativePlan],
    payload: Callable[[native.NativePlan], dict],
    shown: Callable[[native.NativePlan], dict[str, Any]],
    write: Callable[[Any, native.NativePlan], Any],
) -> tuple[dict, Any | None]:
    """The order every native intake write keeps, held once. Answers (payload, written).

    SHARED BY THE LANDING AND ``intake file`` (R-770), because the order is the
    contract and two hand kept copies of it would come to differ:

    * THE DATABASE IS OPENED WITH WRITE INTENT BEFORE THE PLAN, so a running
      rekordbox or its agent refuses before anything is shown, and the plan is
      made against the database the write will be made to;
    * THE ACKNOWLEDGMENT IS READ BEFORE THE GATE (R-733): an approval is the
      one way door on a live library, and a person who reads the whole plan
      and answers should not then be refused by something the verb could have
      read first;
    * the gate is asked over the digested plan, and only ``apply`` writes;
    * the handle is closed whatever happened.

    ``written`` is None when the answer was not ``apply``, and the payload is
    then the plan as it was shown.
    """
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        rows = plan(db)
        data = payload(rows)
        session.assert_backup_acknowledged(cfg)
        option = ctx.gate.require(spec, plan=data, context=shown(rows))
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
    names = collection.names() or (collection.playlist,)
    said = f"the {ingest.spoken(names)} playlist" + ("s" if len(names) > 1 else "")
    return [
        {
            "code": AWAITING_ANALYSIS,
            "message": (
                f"{len(collection.added)} row(s) joined the collection with no "
                f"tempo, grid, key or waveform, and rekordbox analyses nothing on its "
                f"own with Auto Analysis off; open rekordbox, select "
                f"{said} under the intake folder and "
                f"run Analyze Track"
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
