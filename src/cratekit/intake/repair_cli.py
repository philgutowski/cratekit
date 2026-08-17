"""``crate repair paths``: propose, offer, never apply.

A wrong answer re-points a library row at somebody else's file. This verb
walks the library, proposes a name, and offers each proposal into the
path-repair queue. Applying is a later act after ``review resolve``.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, review
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.intake import repair


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
        help="folder to scan; the configured library root when omitted",
    )
    parser.set_defaults(_handler=repair_paths)


def repair_paths(ctx) -> Envelope:
    cfg = _load()
    root = Path(ctx.args.root) if ctx.args.root else Path(cfg.library.root)
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
