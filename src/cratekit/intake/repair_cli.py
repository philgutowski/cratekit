"""``crate repair paths``: propose and offer, and apply only what was accepted.

A wrong answer re-points a library row at somebody else's file. So the verb has
two acts and a person stands between them. Without ``--apply`` it walks the
library, proposes a name, and offers each proposal into the path-repair queue,
and touches nothing. With ``--apply`` (U102) it reads the queue back, renames the
files whose proposal a person ACCEPTED, and nothing else: an open item, a
rejected one and one answered ``keep`` are counted and left alone.

The rename runs under the collection guard ``name apply`` built (U67), asked of
that module rather than copied out of it. A file the rekordbox collection
references is held back, and a collection that cannot be read refuses the whole
verb, because rekordbox records a path once and a rename strands the row.

EVERY RENAME OWED AND NOT PERFORMED IS NAMED, AND THE RUN IS NOT OK (R-172). A
person accepted each of these by hand, so a file held back is a decision the
tool did not carry out, whether the plan held it or the filesystem refused it.

Rewriting the locations inside an export, the source system's third mode, is not
built here.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.cli import output
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, locations, naming, review
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import repair
from cratekit.write import naming_cli

RENAME = "rename"
REFERENCED = "referenced"
COLLIDES = "collides"
MISSING = "missing"
UNCHANGED = "unchanged"
UNUSABLE = "unusable"

#: The plan classes that are a rename a person accepted and this run cannot
#: perform. ``missing`` is absent because there is no file left to rename, and
#: ``unchanged`` because the proposal asked for none, so a run over either has
#: nothing outstanding and answering otherwise would fail for ever.
_HELD = (REFERENCED, COLLIDES, UNUSABLE)
#: The held classes a second run cannot clear by itself. A referenced file stays
#: referenced and an unusable item stays unusable until a person changes the
#: queue, so a run holding only these must not call itself retryable.
_NEEDS_A_PERSON = (REFERENCED, UNUSABLE)


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("intake.repair_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build_repair_paths(parser, entry) -> None:
    parser.add_argument(
        "--root",
        default=None,
        metavar="DIR",
        help="folder to scan, by its path from the library root or in full; the "
        "configured library root when omitted. With --apply, only accepted "
        "proposals under it, and every one when omitted",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="rename the files whose proposal was accepted in the review queue",
    )
    parser.set_defaults(_handler=repair_paths)


def repair_paths(ctx) -> Envelope:
    cfg = _load()
    if ctx.args.apply:
        return _apply(ctx, cfg)
    root = naming_cli.root_folder(ctx.args.root, cfg, verb="repair paths")
    findings = repair.scan(root, cfg=cfg)
    with review.open_store(cfg) as store:
        repair.offer_repairs(store, findings, handler_key=ctx.entry.handler_key)
    items = [
        {"path": str(path), "proposed": proposed, "error": error}
        for path, proposed, error in findings
    ]
    plan = {
        "digest": digest_of({"kind": "path-repair", "items": items}),
        "items": items,
        "totals": {"count": len(items)},
        "chunk": None,
    }
    return ctx.envelope(data=plan, outcome=Outcome.OK)


def _unusable_why(accepted: repair.Accepted) -> str:
    """Why this accepted proposal cannot be acted on at all, or the empty string.

    THE PROPOSED NAME COMES OUT OF A STORE, and a store can be imported from a
    document somebody edited. So it is held to the shape ``propose_name`` can
    produce: a bare filename, never a path, with the suffix the file already
    has. A proposal naming ``../elsewhere/x.flac`` would move the file out of
    its folder, and one naming ``x.txt`` would take an audio file out of every
    later scan, and neither is a rename anybody was shown as one.
    """
    if accepted.path is None:
        return (
            "the queue holds no path for it, which is how an item that arrived by "
            "import reads, so which file it names is not known"
        )
    proposed = accepted.proposed
    if not proposed or proposed in {".", ".."} or Path(proposed).name != proposed:
        return f"its proposed name {proposed!r} is not a bare filename"
    if Path(proposed).suffix.lower() != Path(accepted.path).suffix.lower():
        return f"its proposed name {proposed!r} would change the file's extension"
    if accepted.recorded and Path(accepted.path).name != accepted.recorded:
        # THE QUEUE ADDRESSES AN ITEM BY THE RESOLVED PATH, and the proposal was
        # made for the name the scan SAW. They differ exactly when the scanned
        # file was a link, and then the stored path is the link's target, a file
        # the person was never shown, possibly outside the library altogether.
        return (
            f"it was offered for {accepted.recorded} and the queue addresses it as "
            f"{Path(accepted.path).name}, which is how a linked file reads, and the "
            f"file a link points at is not the one the proposal was shown for"
        )
    return ""


def _key(path: str) -> str:
    """One path as ``--root`` compares it, which is how the guard beside it does.

    NFC and casefolded, for the reason ``naming_cli._key`` gives: the volume a
    library normally sits on ignores case, so a root typed in another case names
    the same folder. Compared exactly, every accepted item would read as outside
    it and the run would answer ok over a plan with nothing in it.
    """
    return locations.norm_for_compare(path).casefold()


def _under(path: str, root: Path | None) -> bool:
    if root is None:
        return True
    held, wanted = _key(path), _key(str(root.resolve())).rstrip("/")
    return held == wanted or held.startswith(wanted + "/")


def _plan_for(decided: repair.Decided, *, root: Path | None, cfg: config.Config) -> dict:
    """The apply plan over the accepted proposals, with every held file marked.

    THE CHECKS ARE HERE, ON THE CHECKING PATH, for the reason ``name apply``
    gives: the digest the gate is answered against then covers them, so a row
    that starts referencing a file changes the plan a person approved.

    The collection is read only when something would be renamed. With no
    candidate its contents cannot change the outcome, and an empty queue is a
    plan a person can still abort on a machine with no database yet.

    ``totals.count`` is the number of renames this plan can perform. Everything
    else a person accepted is in ``items`` under its own class with its reason,
    so nothing accepted is left out of the plan silently.
    """
    items: list[dict[str, str]] = []
    candidates: list[tuple[repair.Accepted, Path]] = []
    outside = 0
    for accepted in decided.accepted:
        if accepted.path is not None and not _under(accepted.path, root):
            outside += 1
            continue
        why = _unusable_why(accepted)
        if why:
            # An item with no path cannot be tested against the root, so it is
            # never filtered out and is shown on every apply.
            items.append(
                {
                    "action": UNUSABLE,
                    "item_id": accepted.item_id,
                    "from": accepted.recorded,
                    "to": accepted.proposed,
                    "path": accepted.path or "",
                    "why": why,
                }
            )
            continue
        path = Path(accepted.path)
        target = path.with_name(accepted.proposed)
        base = {
            "item_id": accepted.item_id,
            "from": path.name,
            "to": accepted.proposed,
            "path": str(path),
        }
        if path.name == accepted.proposed:
            # A proposal that failed to fit proposes the name the file has, and
            # carries why. It is accepted and asks for nothing, so it is not a
            # rename, and it is LISTED, with that reason, rather than dropped.
            items.append(
                {
                    "action": UNCHANGED,
                    **base,
                    "why": accepted.error or "the proposal is the name the file has",
                }
            )
            continue
        if not path.is_file():
            # ONE CLASS, AND IT CLAIMS ONLY WHAT WAS OBSERVED. Source gone with
            # the proposed name present is what every accepted item reads as on
            # the run after the one that applied it, since nothing retires an
            # item from the queue. It is also what a deleted file beside an
            # unrelated file of that name reads as, and nothing here can tell
            # the two apart, so the plan says which names exist and does not
            # call either one a rename that was carried out.
            if target.is_file():
                why = (
                    f"no file is at that path and {target.name} is in the folder, "
                    f"which is how a rename already carried out reads"
                )
            else:
                why = "no file is at that path, and none carries the proposed name"
            items.append({"action": MISSING, **base, "why": why})
            continue
        candidates.append((accepted, path))

    referenced = (
        naming_cli.referenced_keys(cfg, renaming=[path for _, path in candidates])
        if candidates
        else frozenset()
    )
    free = [
        (accepted, path)
        for accepted, path in candidates
        if not naming_cli.is_referenced(path, referenced)
    ]
    freed = {str(path) for _, path in free}
    collides = naming_cli.held_collisions([(path, acc.proposed) for acc, path in free])
    for accepted, path in candidates:
        base = {
            "item_id": accepted.item_id,
            "from": path.name,
            "to": accepted.proposed,
            "path": str(path),
        }
        if str(path) not in freed:
            items.append(
                {
                    "action": REFERENCED,
                    **base,
                    "why": "the rekordbox collection references it, and renaming it "
                    "would strand that row",
                }
            )
        elif str(path) in collides:
            items.append({"action": COLLIDES, **base, "why": collides[str(path)]})
        else:
            items.append({"action": RENAME, **base})

    def _count(action: str) -> int:
        return sum(1 for item in items if item["action"] == action)

    return {
        "digest": digest_of({"kind": "path-repair", "apply": True, "items": items}),
        "items": items,
        "totals": {
            "count": _count(RENAME),
            "referenced": _count(REFERENCED),
            "collides": _count(COLLIDES),
            "missing": _count(MISSING),
            "unchanged": _count(UNCHANGED),
            "unusable": _count(UNUSABLE),
            "outside_root": outside,
            "kept": decided.kept,
            "rejected": decided.rejected,
            "open": decided.still_open,
        },
        "chunk": None,
    }


def _incomplete_cause(
    incomplete: list[dict[str, str]], *, renamed: int, retryable: bool
) -> Cause:
    """What the run answers when an accepted rename did not happen (R-172).

    The same reason ``name apply`` answers with, worded the same way: the count
    leads, the first file follows with its reason, what DID land is said in the
    same sentence, and every item is in the detail, capped. The step is this
    verb's own, because here each outstanding rename is a decision sitting in the
    review queue, and the way to stop being told about one is to change it.

    ``retryable`` is the caller's to say, because it depends on WHICH renames
    are outstanding: a referenced file is held on every run, so a driver told to
    retry over one would retry for ever.
    """
    count = len(incomplete)
    return refuse(
        "rename-incomplete",
        f"{renamed} file(s) were renamed, and {count} accepted proposal(s) were "
        f"not carried out, the first of them {incomplete[0]['from']}, "
        f"{incomplete[0]['why']}",
        steps=(
            "read the file(s) this report names, each carries the reason its "
            "rename did not happen, and run this again once that is corrected",
            "a proposal that should never be applied is cleared and then "
            "rejected in the review queue, which takes it out of this plan",
        ),
        scope=Scope.RUN,
        retryable=retryable,
        origin=("intake.repair_cli",),
        detail={
            "renamed": renamed,
            "incomplete_count": count,
            "incomplete": incomplete[: naming_cli.INCOMPLETE_SHOWN],
        },
    ).cause


def _apply(ctx, cfg: config.Config) -> Envelope:
    # READ AGAINST THE LIBRARY ROOT like every ``--root`` (U169), and NOT
    # refused when no folder is there. Here the root filters accepted proposals
    # rather than naming a folder to walk, the comparison is deliberately case
    # blind for a case blind volume, and a proposal it leaves out is counted
    # under ``outside_root`` on the plan a person confirms.
    root = (
        naming_cli.root_path(ctx.args.root, cfg, verb="repair paths --apply")
        if ctx.args.root is not None
        else None
    )
    with review.open_store(cfg) as store:
        decided = repair.decided(store)
    plan = _plan_for(decided, root=root, cfg=cfg)
    spec = next(gate for gate in ctx.entry.gates if gate.name == "repair.paths.confirm")
    # THE PLAN IS SHOWN THROUGH THE GATE LAYER (R-693): every item with its
    # class and its reason, the digest they were taken over, and the root and
    # the totals in front of them, so a person confirms renames they have
    # read. ``totals.count`` is the renames this plan can perform and is
    # named ``renames`` here, the way ``name apply`` names it, because the
    # screen's own ``count`` is every item and two lines both called count
    # would read as a contradiction.
    totals = {"renames" if name == "count" else name: value for name, value in plan["totals"].items()}
    option = ctx.gate.require(
        spec, plan=plan, context={"root": str(root) if root is not None else None, **totals}
    )
    if option == "abort":
        return ctx.envelope(data=plan, outcome=Outcome.NO_OP)

    renames = [item for item in plan["items"] if item["action"] == RENAME]
    incomplete: list[dict[str, str]] = [
        {"from": item["from"], "path": item["path"], "why": item["why"]}
        for item in plan["items"]
        if item["action"] in _HELD
    ]

    # TRUE ONCE ANYTHING OUTSTANDING COULD CLEAR WITHOUT A PERSON: a collision,
    # since the file in the way can move, and everything found after the gate.
    retryable = any(
        item["action"] in _HELD and item["action"] not in _NEEDS_A_PERSON
        for item in plan["items"]
    )

    def _owed(item: dict[str, str], why: str) -> None:
        nonlocal retryable
        retryable = True
        incomplete.append({"from": item["from"], "path": item["path"], "why": why})

    renamed = 0
    # READ AGAIN AFTER THE GATE, as ``name apply`` does and for its reason: the
    # plan's check decides what a person was shown, this one decides what is
    # touched, and rekordbox can import a file between the two.
    referenced = (
        naming_cli.referenced_keys(cfg, renaming=[Path(item["path"]) for item in renames])
        if renames
        else frozenset()
    )
    for item in renames:
        path = Path(item["path"])
        if not path.is_file():
            _owed(item, "the file is no longer there")
            continue
        if naming_cli.is_referenced(path, referenced):
            _owed(
                item,
                "the rekordbox collection began referencing it after the plan was "
                "approved, and renaming it would strand that row",
            )
            continue
        target = path.with_name(item["to"])
        try:
            claimed = naming.claim_target(target)
        except OSError as exc:
            _owed(item, f"the filesystem refused the new name: {exc.strerror or exc}")
            continue
        if not claimed:
            _owed(item, f"{item['to']} is already taken in the folder")
            continue
        # THE CLAIM IS A ZERO BYTE FILE UNDER AN AUDIO NAME, and ``claim_target``
        # says the caller owns removing it on ANY failure after a True. An
        # interrupt between the claim and the rename is such a failure, so the
        # removal is in a ``finally`` and not only in the ``OSError`` branch:
        # a stub left behind holds the name against this same rename for ever.
        moved = False
        try:
            path.rename(target)
            moved = True
        except OSError as exc:
            _owed(item, f"the filesystem refused the rename: {exc.strerror or exc}")
        finally:
            if not moved:
                target.unlink(missing_ok=True)
        if moved:
            renamed += 1

    plan["totals"] = {**plan["totals"], "renamed": renamed, "incomplete": len(incomplete)}
    if not incomplete:
        return ctx.envelope(data=plan, outcome=Outcome.OK)
    # THE PLAN SURFACE AND NOT THE DIAGNOSTIC ONE, as ``name apply`` argues: this
    # run produced a plan and carried out part of it, so what it DID rename is
    # what a person needs next. ``items`` is untouched after the gate, so the
    # digest keeps describing what was approved.
    return output.from_cause(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        started=ctx.started,
        cause=_incomplete_cause(incomplete, renamed=renamed, retryable=retryable),
        schema=ctx.entry.output_schema or output.current_schema("plan"),
        data=plan,
    )
