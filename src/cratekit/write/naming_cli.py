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


def _spec_for(path: Path, *, template: NameTemplate, cfg: config.Config) -> NameSpec:
    """One spec for one file, shared by the plan and the apply pass.

    The two passes previously built their specs separately and disagreed on
    the lossy flag, so a marked file was promised a rename the apply pass was
    never going to perform. One builder makes agreement structural.

    The head is recovered from the FILENAME first and the title tag second,
    as text through the head parser, never from any analysis surface (U39).
    Without this, a spec built from tags alone has no tempo, the default head
    is all or nothing, and a rename strips the head the file already carries.
    The title fallback heals the tag then rename crash window, where the head
    survives in the title and not in the filename. The key prefers the tag,
    because renaming from metadata is the verb's job; the head fills silence
    and supplies the tempo, which has no tag field at all, structurally.

    THE HEAD IS DERIVED AND THE BODY IS CARRIED (U41). Each surface keeps its
    own body: the filename's body renders the filename, the title tag's body
    renders the tag. ``NameSpec`` always held ``stem`` and ``title`` separately
    for exactly this, and collapsing them onto one value is what made a rename
    destructive. Composing the filename from the tag dropped the artist off
    almost every file in the library, since the convention keeps the artist in
    the name and the title alone in the tag (R-168). Feeding the filename's
    body the other way would have been worse, stuffing the artist and the album
    into every title tag the apply pass rewrites.

    No recomposition rule is attempted and that is the decision, not an
    omission. Measured over the library on 2026-08-25, read only: 53 percent of
    names are ``Title - Artist - Album``, 25 percent are ``Artist - Title``,
    one percent have a body equal to the title tag, and the remainder differ
    from the tag only because the filesystem cannot hold a colon or a quote. No
    single rule fits that, so the verb pads the head it understands and leaves
    the text it does not. Normalizing the library to one grammar is a separate
    decision for a person to take deliberately.
    """
    title = tags.read_tag(path, "title") or path.stem
    head = (
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)
        or {}
    )
    tag_key = tags.read_tag(path, "initialkey")
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")
    marker = cfg.naming.lossy_marker
    return NameSpec(
        stem=naming.strip_head(path.stem, template=template),
        suffix=path.suffix,
        key=key,
        bpm=int(head["bpm"]) if "bpm" in head else None,
        title=naming.strip_head(title, template=template),
        lossy=marker in path.stem or marker in title,
    )


def _plan_for(root: Path, *, cfg: config.Config) -> dict:
    template = _template(cfg)
    budget = _budget(cfg)
    items: list[dict[str, str]] = []
    if root.is_dir():
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in AUDIO_EXTS:
                continue
            rendered = naming.build(
                _spec_for(path, template=template, cfg=cfg),
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
        rendered = naming.build(
            _spec_for(path, template=template, cfg=cfg),
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
