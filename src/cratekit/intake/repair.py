"""Path repair proposals. Offered here, and read back once a person decided.

A wrong answer here re-points a library row at somebody else's file. The
proposal is therefore a review item in ``Queue.PATH_REPAIR``. A decision
is never read back out of a file somebody edited. It is read back out of the
queue, by ``decided``, and only ``repair_cli`` acts on what that returns.

Idempotent: a name that already fits the budget and has no duplicate tail
proposes itself. Re-running the pass then offers nothing new, because
``review.offer`` is idempotent on the same identity.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cratekit.core import config, naming, review
from cratekit.core.naming import AUDIO_EXTS, MarkerRule, NameBudget, NameTemplate
from cratekit.core.review import Option, Queue, Verdict

#: The kind every item this module offers carries, and the only kind it reads.
KIND = "path-repair"
#: The option that means "rename the file to the proposed name".
ACCEPT = "accept"
#: The option that means "the name it has is the name it keeps".
KEEP = "keep"


def _template_for(cfg: config.Config) -> NameTemplate:
    marker = cfg.naming.lossy_marker
    return NameTemplate(markers=(MarkerRule(field="lossy", literal=marker),))


def _budget_for(cfg: config.Config) -> NameBudget:
    return NameBudget(
        path_budget_bytes=cfg.naming.path_budget_bytes,
        filename_max_bytes=cfg.naming.filename_max_bytes,
    )


def propose_name(path: Path, *, cfg: config.Config) -> tuple[str, str]:
    """(proposed filename, error). The existing head is kept verbatim.

    Padding belongs to a later stage. Measuring uses the widest head so a
    later pad cannot push a fitted name over the ceiling.
    """
    template = _template_for(cfg)
    budget = _budget_for(cfg)
    head, tail = naming.split_head(path.stem, template=template)
    parsed = naming.parse_head(path.stem, template=template) or {}
    bpm_raw = parsed.get("bpm")
    try:
        bpm = int(bpm_raw) if bpm_raw is not None else None
    except ValueError:
        bpm = None
    spec = naming.NameSpec(
        stem=tail,
        suffix=path.suffix,
        key=parsed.get("key"),
        bpm=bpm,
        lossy=cfg.naming.lossy_marker in head,
    )
    measured = naming.budget_head(spec, template=template) if head else head
    deduped = naming.dedupe_stem(tail, sep=template.segment_sep)
    try:
        fitted = naming.fit_stem_to_budget(
            str(path.parent),
            measured,
            deduped,
            path.suffix,
            budget=budget,
            hash_source=tail,
        )
    except ValueError as exc:
        return path.name, str(exc)
    return head + fitted + path.suffix, ""


def scan(root: Path, *, cfg: config.Config) -> list[tuple[Path, str, str]]:
    """Audio files under ``root`` whose proposed name differs, plus errors."""
    found: list[tuple[Path, str, str]] = []
    if not root.is_dir():
        return found
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in AUDIO_EXTS:
            continue
        proposed, error = propose_name(path, cfg=cfg)
        if error or proposed != path.name:
            found.append((path, proposed, error))
    return found


def offer_repairs(
    store: review.ReviewStore,
    findings: list[tuple[Path, str, str]],
    *,
    handler_key: str = "repair.paths",
) -> list[review.Item]:
    """Offer each proposal into the path-repair queue. Never apply one."""
    offered: list[review.Item] = []
    for path, proposed, error in findings:
        item = review.offer(
            store,
            queue=Queue.PATH_REPAIR,
            kind=KIND,
            identity={"path": str(path.resolve())},
            payload={
                "recorded": path.name,
                "proposed": proposed,
                "error": error,
            },
            options=(
                Option(option_id=ACCEPT, summary=proposed),
                Option(option_id=KEEP, summary=path.name),
            ),
            handler_key=handler_key,
        )
        offered.append(item)
    return offered


@dataclass(frozen=True, slots=True)
class Accepted:
    """One proposal a person accepted, as the queue holds it.

    ``path`` is the identity the item was offered under, which is the resolved
    path of the file at scan time, and it is None for an item that arrived by
    import, because an imported item carries no identity at all. ``proposed`` is
    the name the person was SHOWN, taken from the payload and never rendered
    again: a name computed at apply time is a name nobody approved.
    """

    item_id: str
    path: str | None
    recorded: str
    proposed: str
    error: str


@dataclass(frozen=True, slots=True)
class Decided:
    """The path-repair queue, sorted by what a person said about each item."""

    accepted: tuple[Accepted, ...]
    kept: int
    rejected: int
    still_open: int


def decided(store: review.ReviewStore) -> Decided:
    """Every path-repair item, sorted by its verdict. Reads, and changes nothing.

    ACCEPTED IS TWO FACTS TOGETHER: the verdict is accepted AND the option is
    the one that names the proposal. The item offers two options and ``keep`` is
    an accepted verdict too, settled in favour of the name the file already has,
    and a verdict recorded with no option names no candidate at all. Reading the
    verdict alone would rename a file whose owner said to leave it.

    A verdict this build cannot read arrives as None, which is how every reader
    of the queue treats one, so it is counted open and nothing is renamed on it.
    """
    # PAGED, through the walk the queue provides for exactly this. The queue
    # keeps every settled item, so a library sweep leaves thousands of rows here
    # and only the accepted ones are held past their page.
    selection = review.Predicate(queue=str(Queue.PATH_REPAIR), kind=KIND)
    accepted: list[Accepted] = []
    kept = rejected = still_open = 0
    for item in review.iter_items(store, predicate=selection, include_resolved=True):
        if item.verdict is Verdict.REJECTED:
            rejected += 1
        elif item.verdict is not Verdict.ACCEPTED:
            still_open += 1
        elif item.option != ACCEPT:
            kept += 1
        else:
            identity = review.identity_of(store, item.item_id) or {}
            held = identity.get("path")
            accepted.append(
                Accepted(
                    item_id=item.item_id,
                    path=held if isinstance(held, str) and held else None,
                    recorded=str(item.payload.get("recorded") or ""),
                    proposed=str(item.payload.get("proposed") or ""),
                    error=str(item.payload.get("error") or ""),
                )
            )
    return Decided(
        accepted=tuple(accepted), kept=kept, rejected=rejected, still_open=still_open
    )
