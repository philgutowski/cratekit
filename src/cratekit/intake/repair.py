"""Path repair proposals. Offered here, and read back once a person decided.

A wrong answer re-points a library row at somebody else's file, so a proposal
is a review item in ``Queue.PATH_REPAIR``, read back out of the queue by
``decided`` and acted on only by ``repair_cli``. A name that already fits
proposes itself, and ``review.offer`` is idempotent, so a rerun offers nothing new.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cratekit.core import config, naming, review
from cratekit.core.naming import AUDIO_EXTS, NameBudget, NameTemplate
from cratekit.core.review import Option, Queue, Verdict

#: The kind every item this module offers carries, and the only kind it reads.
KIND = "path-repair"
#: The option that means "rename the file to the proposed name".
ACCEPT = "accept"
#: The option that means "the name it has is the name it keeps".
KEEP = "keep"


def propose_name(path: Path, *, cfg: config.Config) -> tuple[str, str]:
    """(proposed filename, error). The existing head is kept verbatim.

    Measured with the widest head, so a later pad cannot push it over the ceiling.
    """
    template = NameTemplate.lossy(cfg.naming.lossy_marker)
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
            budget=NameBudget.of(cfg.naming),
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
    return [
        review.offer(
            store,
            queue=Queue.PATH_REPAIR,
            kind=KIND,
            identity={"path": str(path.resolve())},
            payload={"recorded": path.name, "proposed": proposed, "error": error},
            options=(
                Option(option_id=ACCEPT, summary=proposed),
                Option(option_id=KEEP, summary=path.name),
            ),
            handler_key=handler_key,
        )
        for path, proposed, error in findings
    ]


@dataclass(frozen=True, slots=True)
class Accepted:
    """One proposal a person accepted, as the queue holds it.

    ``path`` is the resolved path offered under, None for an imported item,
    which carries no identity. ``proposed`` is the name the person was SHOWN,
    never rendered again: a name computed at apply time nobody approved.
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

    ACCEPTED IS TWO FACTS TOGETHER, the verdict and the ``accept`` option:
    ``keep`` is an accepted verdict too, so the verdict alone would rename a
    file its owner said to leave. An unreadable verdict, None, counts as open.
    """
    # PAGED: a library sweep leaves thousands of settled items here.
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
