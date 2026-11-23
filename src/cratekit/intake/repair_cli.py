"""``crate repair paths``: propose and offer, and apply only what was accepted.

A wrong answer re-points a library row at somebody else's file, so a person
stands between proposing into the path-repair queue and ``--apply`` (U102),
which renames only what was ACCEPTED, under ``name apply``'s collection guard
(U67). EVERY RENAME OWED AND NOT PERFORMED IS NAMED, AND THE RUN IS NOT OK (R-172).
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from cratekit.cli import output
from cratekit.cli.output import Envelope, digest_of, load_config
from cratekit.core import config, locations, naming, review
from cratekit.core.cause import Cause, Outcome, Scope, refuse
from cratekit.intake import repair
from cratekit.write import naming_cli

RENAME = "rename"
REFERENCED = "referenced"
COLLIDES = "collides"
MISSING = "missing"
UNCHANGED = "unchanged"
UNUSABLE = "unusable"

#: The classes that are an accepted rename this run cannot perform; ``missing``
#: and ``unchanged`` leave nothing outstanding, or a run would fail for ever.
_HELD = (REFERENCED, COLLIDES, UNUSABLE)
#: The held classes only a person can clear, so a run holding only these is not retryable.
_NEEDS_A_PERSON = (REFERENCED, UNUSABLE)


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
    cfg = load_config(("intake.repair_cli",))
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

    THE PROPOSED NAME COMES OUT OF A STORE a person may have edited, so it is
    held to what ``propose_name`` produces: a bare filename with the file's own
    suffix, never a path out of the folder or out of every later scan.
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
        # THE QUEUE HOLDS THE RESOLVED PATH; differing from the name the scan
        # saw, it is a link's target, a file the person was never shown.
        return (
            f"it was offered for {accepted.recorded} and the queue addresses it as "
            f"{Path(accepted.path).name}, which is how a linked file reads, and the "
            f"file a link points at is not the one the proposal was shown for"
        )
    return ""


def _key(path: str) -> str:
    """One path as ``--root`` compares it: NFC and casefolded, as the library's volume ignores case."""
    return locations.norm_for_compare(path).casefold()


def _under(path: str, root: Path | None) -> bool:
    if root is None:
        return True
    held, wanted = _key(path), _key(str(root.resolve())).rstrip("/")
    return held == wanted or held.startswith(wanted + "/")


def _base(accepted: repair.Accepted, path: Path) -> dict[str, str]:
    return {
        "item_id": accepted.item_id,
        "from": path.name,
        "to": accepted.proposed,
        "path": str(path),
    }


def _plan_for(decided: repair.Decided, *, root: Path | None, cfg: config.Config) -> dict:
    """The apply plan over the accepted proposals, with every held file marked.

    The checks are on the checking path, so the gate's digest covers them. The
    collection is read only when something would be renamed, so an empty queue
    can be aborted with no database. ``totals.count`` is the renames it can
    perform; everything else accepted is an item with its class and reason.
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
            # An item with no path cannot be tested against the root, so it shows on every apply.
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
        base = _base(accepted, path)
        if path.name == accepted.proposed:
            # A proposal that failed to fit names the file's own name: no rename, but LISTED.
            why = accepted.error or "the proposal is the name the file has"
            items.append({"action": UNCHANGED, **base, "why": why})
            continue
        if not path.is_file():
            # ONE CLASS, CLAIMING ONLY WHAT WAS OBSERVED: a rename already done
            # and a deleted file beside one of that name read the same.
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
        base = _base(accepted, path)
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

    counted = Counter(item["action"] for item in items)
    return {
        "digest": digest_of({"kind": "path-repair", "apply": True, "items": items}),
        "items": items,
        "totals": {
            "count": counted[RENAME],
            **{
                name: counted[name] for name in (REFERENCED, COLLIDES, MISSING, UNCHANGED, UNUSABLE)
            },
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

    ``name apply``'s reason and wording; the steps are this verb's, since each
    outstanding rename is a decision in the review queue. ``retryable`` is the
    caller's, since a referenced file is held on every run.
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
    # READ AGAINST THE LIBRARY ROOT like every ``--root`` (U169), and not refused
    # when no folder is there: it filters proposals, counting the rest outside_root.
    root = (
        naming_cli.root_path(ctx.args.root, cfg, verb="repair paths --apply")
        if ctx.args.root is not None
        else None
    )
    with review.open_store(cfg) as store:
        decided = repair.decided(store)
    plan = _plan_for(decided, root=root, cfg=cfg)
    spec = next(gate for gate in ctx.entry.gates if gate.name == "repair.paths.confirm")
    # THE PLAN IS SHOWN THROUGH THE GATE LAYER (R-693). ``count`` is shown as
    # ``renames``, as ``name apply`` does, beside the screen's own count of items.
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

    # TRUE ONCE ANYTHING OUTSTANDING COULD CLEAR WITHOUT A PERSON: a collision or a later find.
    retryable = any(
        item["action"] in _HELD and item["action"] not in _NEEDS_A_PERSON
        for item in plan["items"]
    )

    def _owed(item: dict[str, str], why: str) -> None:
        nonlocal retryable
        retryable = True
        incomplete.append({"from": item["from"], "path": item["path"], "why": why})

    renamed = 0
    # READ AGAIN AFTER THE GATE: rekordbox can import a file between the two.
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
        # THE CLAIM IS A ZERO BYTE FILE, removed in a ``finally`` on any failure,
        # an interrupt included, or it holds the name against this rename for ever.
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
    # THE PLAN SURFACE, as ``name apply`` argues: part of the plan was carried
    # out, and ``items`` is untouched so the digest describes what was approved.
    return output.from_cause(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        started=ctx.started,
        cause=_incomplete_cause(incomplete, renamed=renamed, retryable=retryable),
        schema=ctx.entry.output_schema or output.current_schema("plan"),
        data=plan,
    )
