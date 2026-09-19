"""Preview renames, then apply after the confirm gate.

The naming engine owns mechanism. This shell owns the plan, the gate, and
the filesystem rename. Absent key and BPM fields are omitted (R20). A
lossy file is marked on filename, title tag, and library name together
(R21), or the engine refuses.

A file the rekordbox collection references is never renamed or retagged here
(U67). rekordbox records a path once, at import, so a rename leaves the row
pointing at nothing. The verb reads the collection, holds those files back and
lists them in the plan, and refuses outright when the collection cannot be read.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, locations, naming, rb_writer, tags
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import AUDIO_EXTS, MarkerRule, NameBudget, NameSpec, NameTemplate

RENAME = "rename"
REFERENCED = "referenced"


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


def _recorded(cfg: config.Config) -> tuple[str, ...]:
    """Every path the collection records, tombstones included, or a refusal.

    A READ, and the open says so: ``require_closed`` is the write-intent flag and
    it stays False, the same open ``write/metadata_cli._open`` makes for its plan.
    ``adopt.collection.read_collection`` is the same read one layer up, and the
    layering test forbids this layer from importing it.

    A TOMBSTONED ROW STILL COUNTS. rekordbox keeps the row, and a restore or a
    re-import brings it back pointing at whatever path it recorded, so renaming
    the file strands it exactly as it would strand a live one.

    A DATABASE THAT WOULD NOT OPEN IS A REFUSAL, NEVER AN EMPTY COLLECTION. An
    empty tuple from here means the database opened and holds no row, and that is
    the only way to get one. Folding the two would rename every imported file in
    the library on the day the volume holding the database is not mounted.
    """
    try:
        target = rb_writer.live_db_path(cfg)
        handle = rb_writer.open_db(
            target,
            require_closed=False,
            cfg=cfg,
        )
        try:
            return tuple(str(row.FolderPath or "") for row in handle.get_content())
        finally:
            rb_writer.close_db(handle)
    except CratekitError as exc:
        inner = exc.cause
        steps = inner.remediation.steps
        raise refuse(
            "collection-unreadable",
            f"the rekordbox collection could not be read, so nothing is renamed: "
            f"{inner.message}",
            remedy=inner.remediation.remedy or (None if steps else Remedy.REPORT_DEFECT),
            steps=steps,
            origin=("write.naming_cli",),
            detail={"declared_reason": inner.reason},
            inner=inner,
        ) from exc
    except Exception as exc:  # noqa: BLE001 - every failed read is one refusal
        raise refuse(
            "collection-unreadable",
            f"the rekordbox collection could not be read, so nothing is renamed: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            origin=("write.naming_cli",),
            detail={"kind": type(exc).__name__},
        ) from exc


def _key(path: str) -> str:
    """One path as the referenced set compares it.

    NFC for the reason ``core.locations`` gives, and casefolded because the
    volume a library normally sits on ignores case. A recorded path that differs
    from the file on disk only in case still names that file there, and a
    rename would strand its row. On a volume that respects case the cost is a
    file left unrenamed, which is the direction to be wrong in.
    """
    return locations.norm_for_compare(path).casefold()


def _referenced(recorded: tuple[str, ...], *, cfg: config.Config) -> frozenset[str]:
    """The keys of every file the collection references.

    Each row contributes its path as recorded AND its path after the configured
    volume rewrites, because most rows in a real library still carry a volume
    name the drive stopped using long ago, and either spelling can be the one
    that is on disk today. A row naming another host has no local path and
    contributes nothing, since no local file can be the one it names.
    """
    rules = [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]
    keys: set[str] = set()
    for value in recorded:
        if not value:
            continue
        try:
            decoded = locations.location_to_path(value)
        except locations.LocationDecodeError:
            continue
        keys.add(_key(decoded))
        resolved = locations.resolve_recorded_path(
            decoded, root=cfg.library.root, prefix_map=rules
        )
        if resolved.path is not None:
            keys.add(_key(resolved.path))
    return frozenset(keys)


def _is_referenced(path: Path, referenced: frozenset[str]) -> bool:
    """True when the collection records ``path``, by either spelling of it.

    Both the absolute and the resolved spelling are asked, so a ``--root`` given
    through a link or as a relative path is still recognised.
    """
    return _key(str(path.absolute())) in referenced or _key(str(path.resolve())) in referenced


def _plan_for(root: Path, *, cfg: config.Config) -> dict:
    """The plan, with every file the collection references held back.

    THE CHECK IS HERE, ON THE CHECKING PATH, so the digest the gate is answered
    against covers it: a row that starts referencing a file changes the plan a
    person approved. It runs for every root, inside the library or not, because a
    collection can record paths anywhere on the machine.

    The collection is read only when something would be renamed. With no rename
    candidate its contents cannot change the outcome, and an empty folder is a
    plan a person can still abort on a machine with no database yet.

    ``totals.count`` stays the number of renames, and ``items`` carries the
    referenced files too, each marked, so the plan says which files were held
    back rather than leaving them out silently.
    """
    template = _template(cfg)
    budget = _budget(cfg)
    candidates: list[tuple[Path, str]] = []
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
                candidates.append((path, rendered.filename))
    referenced = _referenced(_recorded(cfg), cfg=cfg) if candidates else frozenset()
    items: list[dict[str, str]] = []
    held = 0
    for path, filename in candidates:
        if _is_referenced(path, referenced):
            held += 1
            items.append({"action": REFERENCED, "from": path.name, "path": str(path)})
        else:
            items.append(
                {"action": RENAME, "from": path.name, "to": filename, "path": str(path)}
            )
    return {
        "digest": digest_of({"kind": "rename", "items": items}),
        "items": items,
        "totals": {"count": len(items) - held, "referenced": held},
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
    renames = [item for item in plan["items"] if item["action"] == RENAME]
    # READ AGAIN AFTER THE GATE, because the gate can wait on a person for as
    # long as they like and rekordbox can import a file in that time. The plan's
    # check decides what a person was shown; this one decides what is touched.
    referenced = _referenced(_recorded(cfg), cfg=cfg) if renames else frozenset()
    for item in renames:
        path = Path(item["path"])
        if not path.is_file() or _is_referenced(path, referenced):
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
