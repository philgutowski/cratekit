"""Preview renames, then apply after the confirm gate.

The naming engine owns mechanism. This shell owns the plan, the gate, and
the filesystem rename. Absent key and BPM fields are omitted (R20). A
lossy file is marked on filename, title tag, and library name together
(R21), or the engine refuses.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, naming, tags
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import AUDIO_EXTS, MarkerRule, NameBudget, NameSpec, NameTemplate


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("write.naming_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _template(cfg: config.Config) -> NameTemplate:
    return NameTemplate(
        markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),)
    )


def _budget(cfg: config.Config) -> NameBudget:
    return NameBudget(
        path_budget_bytes=cfg.naming.path_budget_bytes,
        filename_max_bytes=cfg.naming.filename_max_bytes,
    )


def _plan_for(root: Path, *, cfg: config.Config) -> dict:
    template = _template(cfg)
    budget = _budget(cfg)
    items: list[dict[str, str]] = []
    if root.is_dir():
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in AUDIO_EXTS:
                continue
            title = tags.read_tag(path, "title") or path.stem
            key = tags.read_tag(path, "initialkey")
            rendered = naming.build(
                NameSpec(
                    stem=naming.strip_head(title, template=template),
                    suffix=path.suffix,
                    key=key,
                    title=naming.strip_head(title, template=template),
                ),
                template=template,
                budget=budget,
                parent_dir=str(path.parent),
            )
            if rendered.filename != path.name:
                items.append(
                    {
                        "from": path.name,
                        "to": rendered.filename,
                        "path": str(path),
                    }
                )
    return {
        "digest": digest_of({"kind": "rename", "items": items}),
        "items": items,
        "totals": {"count": len(items)},
        "chunk": None,
    }


def build(parser, entry) -> None:
    parser.add_argument(
        "--root",
        default=None,
        metavar="DIR",
        help="folder to rename; the configured library root when omitted",
    )
    parser.set_defaults(_handler=name_apply)


def name_apply(ctx) -> Envelope:
    cfg = _load()
    root = Path(ctx.args.root) if ctx.args.root else Path(cfg.library.root)
    plan = _plan_for(root, cfg=cfg)
    spec = ctx.entry.gates[0]
    option = ctx.gate.require(spec, digest=plan["digest"])
    if option == "abort":
        return ctx.envelope(data=plan, outcome=Outcome.NO_OP)
    template = _template(cfg)
    budget = _budget(cfg)
    for item in plan["items"]:
        path = Path(item["path"])
        if not path.is_file():
            continue
        title = tags.read_tag(path, "title") or path.stem
        key = tags.read_tag(path, "initialkey")
        marker = cfg.naming.lossy_marker
        rendered = naming.build(
            NameSpec(
                stem=naming.strip_head(title, template=template),
                suffix=path.suffix,
                key=key,
                title=naming.strip_head(title, template=template),
                lossy=marker in path.stem or marker in title,
            ),
            template=template,
            budget=budget,
            parent_dir=str(path.parent),
        )
        target = path.with_name(rendered.filename)
        if target != path:
            if not naming.claim_target(target):
                continue
            try:
                path.rename(target)
            except OSError:
                target.unlink(missing_ok=True)
                continue
            path = target
        tags.write_tags(path, {"title": rendered.title_tag})
    return ctx.envelope(data=plan, outcome=Outcome.OK)
