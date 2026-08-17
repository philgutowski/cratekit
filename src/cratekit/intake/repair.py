"""Path repair proposals. Offered, never applied.

A wrong answer here re-points a library row at somebody else's file. The
proposal is therefore a review item in ``Queue.PATH_REPAIR``. A decision
is never read back out of a file somebody edited.

Idempotent: a name that already fits the budget and has no duplicate tail
proposes itself. Re-running the pass then offers nothing new, because
``review.offer`` is idempotent on the same identity.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.core import config, naming, review
from cratekit.core.naming import AUDIO_EXTS, MarkerRule, NameBudget, NameTemplate
from cratekit.core.review import Option, Queue


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
            kind="path-repair",
            identity={"path": str(path.resolve())},
            payload={
                "recorded": path.name,
                "proposed": proposed,
                "error": error,
            },
            options=(
                Option(option_id="accept", summary=proposed),
                Option(option_id="keep", summary=path.name),
            ),
            handler_key=handler_key,
        )
        offered.append(item)
    return offered
