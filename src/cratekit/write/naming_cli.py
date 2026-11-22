"""Preview renames, then apply after the confirm gate.

The naming engine owns mechanism; this shell owns the plan, the gate and the
rename. Absent key and BPM fields are omitted (R20). A lossy file is marked on
filename, title tag and library name together (R21), or the engine refuses.

A file the rekordbox collection references is never renamed or retagged (U67):
rekordbox records a path once, so a rename strands the row. Those files are
held back and listed, and an unreadable collection refuses the verb. So does a
dark row that could name a candidate (R-500), since it matches no candidate
and the file it names would be planned as an ordinary rename.

A provider identifier stem is given a body from its artist and title tags
(R-669); any other stem is carried as it is (R-168). An identifier whose tags
cannot compose a body is held back as ``unnamed``. A file held back because a
file with the SAME ISRC holds its name is a second copy of one recording
(U212), and its item carries the ISRC.
"""

from __future__ import annotations

import os
from collections.abc import Iterable
from pathlib import Path

from cratekit.cli import output
from cratekit.cli.output import Envelope, digest_of, load_config
from cratekit.core import config, locations, naming, rb_writer, tags
from cratekit.core.cause import Cause, CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import AUDIO_EXTS, NameBudget, NameSpec, NameTemplate
from cratekit.write import trees

RENAME = "rename"
REFERENCED = "referenced"
COLLIDES = "collides"
#: An identifier stem whose tags cannot compose a body (R-669), held back and
#: owed on apply like a collision.
UNNAMED = "unnamed"

#: How many incomplete items one cause's detail carries, the unmapped refusal's bound.
INCOMPLETE_SHOWN = 20
#: How many planned and held items the gate screen lists (R-670); a sweep of the
#: library root can be thousands, so past this the totals carry the rest.
PLAN_SHOWN = 200
#: Why a referenced item is held, carried on the item as the other classes carry theirs.
REFERENCED_WHY = "the rekordbox collection references it"


def _template(cfg: config.Config) -> NameTemplate:
    return NameTemplate.lossy(cfg.naming.lossy_marker)


def _is_identifier(stem: str) -> bool:
    """A stem of digits and nothing else, the form the downloader writes.

    Digits only, not "no letters": a chosen name can carry no letters
    (``2 + 2 = 5``), and R-168 stands over it.
    """
    return stem.strip().isdigit()


def _artist(path: Path) -> str | None:
    """The artist tag as one credit line, every credited artist kept.

    Read as values, because a Vorbis comment can hold several ``ARTIST`` fields,
    joined with a comma as the convention writes them. Not sanitized here:
    ``naming.compose_body`` sanitizes each part, one layer only.
    """
    values = tags.read_tag_values(path, "artist")
    if not values:
        return None
    return ", ".join(value.strip() for value in values if value and value.strip()) or None


def _composed_body(
    path: Path, tagged_title: str | None, *, template: NameTemplate
) -> tuple[str | None, str | None]:
    """The body for an identifier stem, or why none can be composed.

    ``Artist - Title``, the title stripped of any head (R-664). Both tags or
    nothing: a title alone loses the artist for life once imported (R-407).
    """
    artist = _artist(path)
    title = naming.strip_head(tagged_title, template=template).strip() if tagged_title else ""
    if not artist and not tagged_title:
        return None, (
            "its name is an identifier and it carries neither an artist tag nor a "
            "title tag, so no name can be composed for it"
        )
    if not artist:
        return None, (
            "its name is an identifier and it carries no artist tag, so it is not "
            "renamed to its title alone"
        )
    if not tagged_title:
        return None, (
            "its name is an identifier and it carries no title tag, so it is not "
            "renamed to its artist alone"
        )
    if not title:
        return None, (
            "its name is an identifier and its title tag is only a head, empty once "
            "the head is removed, so no name can be composed for it"
        )
    return naming.compose_body(artist, title, sep=template.segment_sep), None


def _spec_for(
    path: Path, *, template: NameTemplate, cfg: config.Config
) -> tuple[NameSpec, str | None]:
    """One spec for one file, shared by the plan and the apply so the two agree.

    Returns the spec and, for an identifier stem with no composable body, the
    reason. The head comes from the filename first and the title tag second, as
    text, never from analysis (U39); the key prefers the tag. The head is derived
    and each surface carries its own body (U41): the convention keeps the artist
    in the name and the title alone in the tag (R-168), and no single grammar fits
    the library's names, so none is recomposed. The one exception is a stem of
    digits only once the head is off, a provider identifier, which is composed
    from the tags (R-669).
    """
    tagged_title = tags.read_tag(path, "title")
    title = tagged_title or path.stem
    head = (
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)
        or {}
    )
    tag_key = tags.read_tag(path, "initialkey")
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")
    marker = cfg.naming.lossy_marker
    stem = naming.strip_head(path.stem, template=template)
    unnamed = None
    if _is_identifier(stem):
        composed, unnamed = _composed_body(path, tagged_title, template=template)
        stem = composed if composed is not None else stem
    return NameSpec(
        stem=stem,
        suffix=path.suffix,
        key=key,
        bpm=int(head["bpm"]) if "bpm" in head else None,
        title=naming.strip_head(title, template=template),
        lossy=marker in path.stem or marker in title,
    ), unnamed


def _recorded(cfg: config.Config) -> tuple[str, ...]:
    """Every path the collection records, tombstones included, or a refusal.

    A read: ``require_closed`` stays False. A tombstoned row counts, since a
    restore brings it back pointing at its path. A database that would not open
    is a refusal, never an empty collection, or every imported file would be
    renamed the day the volume holding it is not mounted.
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
    """One path as the referenced set compares it: NFC and casefolded.

    The library volume normally ignores case; on one that respects it the cost is
    a file left unrenamed, the safe direction.
    """
    return locations.norm_for_compare(path).casefold()


def _referenced(
    recorded: tuple[str, ...], *, cfg: config.Config, renaming: Iterable[Path]
) -> frozenset[str]:
    """The keys of every file the collection references, or a refusal.

    Each row adds its recorded path and its path after the volume rewrites, since
    either can be the one on disk; a row naming another host or a streaming
    pseudo-location adds nothing. Decode and resolve are ``trees.located``, shared
    with the writers; the keying is this verb's own and errs toward holding back.

    A dark row refuses the whole verb when it could name a candidate (R-500,
    narrowed by R-675). Dark is no rule resolving it and its recorded file absent
    here. Could name is its leaf matching a file this pass would rename that no
    resolved row already holds (R-407), since a moved volume changes a prefix and
    never a leaf. Tombstones count (R-524), unlike in the deletion pass. An
    unmapped row whose recorded file exists has answered; that test fails closed.
    """
    rules = [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]
    keys: set[str] = set()
    unplaced: list[str] = []
    for value in recorded:
        if not value:
            continue
        try:
            decoded, resolved = trees.located(value, root=cfg.library.root, prefix_map=rules)
        except locations.LocationDecodeError:
            continue
        keys.add(_key(decoded))
        if resolved.path is not None:
            keys.add(_key(resolved.path))
        elif resolved.resolution is locations.Resolution.UNMAPPED and not os.path.exists(decoded):
            unplaced.append(decoded)
    referenced = frozenset(keys)
    # The leaves this pass would rename, keyed as the rows are, less those a
    # resolved row holds, since those are never renamed.
    leaves: dict[str, list[str]] = {}
    for path in renaming:
        if not _is_referenced(path, referenced):
            leaves.setdefault(_key(path.name), []).append(str(path))
    dark = [
        (decoded, named)
        for decoded in unplaced
        if (named := leaves.get(_key(Path(decoded).name)))
    ]
    if dark:
        raise _unmapped_refusal(dark)
    return referenced


def _unmapped_refusal(dark: list[tuple[str, list[str]]]) -> CratekitError:
    """The refusal over dark rows, worded as the deletion pass's is.

    The count leads and the first decoded location follows, the text a rule is
    matched against. The detail groups the prefixes and pairs each row with the
    files it could name (R-675). One step per kind of row: an old drive name takes
    a prefix rule, a gone file a hand rename or a removal (R-523). The remedy is
    ``fix-config-values`` because no doctor check reads the prefix map.
    """
    count = len(dark)
    rows = "collection row records" if count == 1 else "collection rows record"
    locations_listed = [decoded for decoded, _ in dark]
    prefixes = sorted(
        {prefix for prefix in map(locations.leading_prefix, locations_listed) if prefix}
    )
    return refuse(
        "collection-row-unmapped",
        f"{count} {rows} a location this machine cannot resolve under the name "
        f"of a file this plan would rename, the first of them {dark[0][0]}, so "
        f"whether that row names the file is not known and the rename could "
        f"strand it; nothing is renamed",
        steps=(
            "when the recorded volume is this library's drive under an old name, "
            "add a rule to library.location_prefix_map whose from side is that "
            "volume spelled exactly as recorded, capitals included, and whose to "
            "side is where it is mounted now, then run this again",
            "when no volume is missing, the row names a file that is gone and no "
            "rule can place it: rename the file it could be naming by hand, or "
            "remove that track in rekordbox, then run this again",
        ),
        remedy=Remedy.FIX_CONFIG_VALUES,
        scope=Scope.RUN,
        origin=("write.naming_cli",),
        detail={
            "unmapped": count,
            "unmapped_locations": locations_listed[:20],
            "unmapped_prefixes": prefixes[:20],
            "could_name": [{"row": decoded, "files": named} for decoded, named in dark[:20]],
        },
    )


def _is_referenced(path: Path, referenced: frozenset[str]) -> bool:
    """True when the collection records ``path`` by its absolute or resolved spelling."""
    return _key(str(path.absolute())) in referenced or _key(str(path.resolve())) in referenced


def referenced_keys(cfg: config.Config, *, renaming: Iterable[Path]) -> frozenset[str]:
    """The referenced set, read fresh, for ``repair paths --apply`` (U102).

    One guard for both verbs, so every refusal here reaches that verb in the same
    words. ``_recorded`` is looked up through the module so one test stub covers
    both. ``renaming`` is the files that verb would rename.
    """
    return _referenced(_recorded(cfg), cfg=cfg, renaming=renaming)


def is_referenced(path: Path, referenced: frozenset[str]) -> bool:
    """``_is_referenced``, for the verb ``referenced_keys`` names."""
    return _is_referenced(path, referenced)


def held_collisions(movers: list[tuple[Path, str]]) -> dict[str, str]:
    """``_collisions``, for the verb ``referenced_keys`` names."""
    return _collisions(movers)


def second_copy(path: Path, target: Path) -> str:
    """The ISRC ``path`` and ``target`` both carry when they are one recording, else ``""``.

    Read from both files (U212). A missing or unreadable ISRC matches nothing.
    """
    mine = tags.isrc_token(tags.read_tag(path, "isrc"))
    if not mine:
        return ""
    return mine if tags.isrc_token(tags.read_tag(target, "isrc")) == mine else ""


def _taken(path: Path, target: Path, *, fallback: str) -> tuple[str, str]:
    """Why ``path`` cannot take ``target``'s name, and the ISRC when it is a second copy."""
    same = second_copy(path, target)
    if same:
        return (
            f"{target.name} is already taken in the folder by a file carrying the "
            f"same ISRC {same}, a second copy of one recording, so this one is not "
            f"renamed",
            same,
        )
    return fallback, ""


def _collisions(
    movers: list[tuple[Path, str]], seconds: dict[str, str] | None = None
) -> dict[str, str]:
    """Each mover that must not be renamed, mapped to why, keyed by path (R-172).

    Found at plan time, so an approved plan never promises a rename the filesystem
    refuses. Held: several movers rendering to one target, since no winner is
    decided, and a target that is a file on disk nothing here moves. A target
    another mover holds is left promised, since sort order usually resolves the
    chain and the apply reports it when not. Keyed through ``_key``, and run to a
    fixpoint because a held file becomes an occupant. ``seconds`` collects the
    ISRC of a second copy (U212).
    """
    targets = [(path, path.with_name(filename)) for path, filename in movers]
    held: dict[str, str] = {}
    while True:
        moving = [(path, target) for path, target in targets if str(path) not in held]
        holders: dict[str, list[Path]] = {}
        for path, target in moving:
            holders.setdefault(_key(str(target)), []).append(path)
        sources = {_key(str(path)) for path, _ in moving}
        found: dict[str, str] = {}
        for path, target in moving:
            sharing = sorted(
                other.name for other in holders[_key(str(target))] if other != path
            )
            if len(sharing) == 1:
                found[str(path)] = (
                    f"{sharing[0]} renders to the same name, and neither is renamed"
                )
            elif sharing:
                found[str(path)] = (
                    f"{', '.join(sharing)} render to the same name, and none of them "
                    f"is renamed"
                )
            elif _key(str(target)) not in sources and target.exists():
                found[str(path)], same = _taken(
                    path,
                    target,
                    fallback=(
                        f"{target.name} is already taken in the folder by a file "
                        f"nothing here is renaming"
                    ),
                )
                # The ISRC only for the collision naming the file on disk, so an
                # item's ISRC and reason describe one collision.
                if same and seconds is not None:
                    seconds[str(path)] = same
        if not found:
            return held
        held.update(found)


def _referenced_item(path: Path) -> dict[str, str]:
    return {"action": REFERENCED, "from": path.name, "path": str(path), "why": REFERENCED_WHY}


def _plan_for(root: Path, *, cfg: config.Config) -> dict:
    """The plan, with every file the collection references held back.

    Checked on the planning path so the gate's digest covers it; the collection
    is read only when something would be renamed. ``totals.count`` is the renames
    that can be performed, and ``items`` also lists each held class, marked:
    referenced, colliding (R-172) and unnamed (R-669). The collection wins over
    the unnamed hold, since an imported file can never be renamed (R-407).
    """
    template = _template(cfg)
    budget = NameBudget.of(cfg.naming)
    candidates: list[tuple[Path, str]] = []
    uncomposed: list[tuple[Path, str]] = []
    if root.is_dir():
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in AUDIO_EXTS:
                continue
            spec, why = _spec_for(path, template=template, cfg=cfg)
            if why is not None:
                uncomposed.append((path, why))
                continue
            rendered = naming.build(
                spec, template=template, budget=budget, parent_dir=str(path.parent)
            )
            if rendered.filename != path.name:
                candidates.append((path, rendered.filename))
    referenced = (
        _referenced(_recorded(cfg), cfg=cfg, renaming=[path for path, _ in candidates])
        if candidates or uncomposed
        else frozenset()
    )
    # Asked once per candidate: ``_is_referenced`` resolves the path, a syscall.
    decided = [(path, filename, _is_referenced(path, referenced)) for path, filename in candidates]
    seconds: dict[str, str] = {}
    collides = _collisions([(path, filename) for path, filename, ref in decided if not ref], seconds)
    items: list[dict[str, str]] = []
    held = 0
    unnamed: list[dict[str, str]] = []
    for path, why in uncomposed:
        if _is_referenced(path, referenced):
            held += 1
            items.append(_referenced_item(path))
        else:
            unnamed.append({"action": UNNAMED, "from": path.name, "path": str(path), "why": why})
    for path, filename, ref in decided:
        if ref:
            held += 1
            items.append(_referenced_item(path))
        elif str(path) in collides:
            item = {
                "action": COLLIDES,
                "from": path.name,
                "to": filename,
                "path": str(path),
                "why": collides[str(path)],
            }
            # The ISRC on the item (U212), as the fixpoint read it.
            if str(path) in seconds:
                item["isrc"] = seconds[str(path)]
            items.append(item)
        else:
            items.append({"action": RENAME, "from": path.name, "to": filename, "path": str(path)})
    items.extend(unnamed)
    return {
        "digest": digest_of({"kind": "rename", "items": items}),
        "items": items,
        "totals": {
            "count": len(items) - held - len(collides) - len(unnamed),
            "referenced": held,
            "collides": len(collides),
            "unnamed": len(unnamed),
        },
        "chunk": None,
    }


def _shown(plan: dict, *, root: Path) -> dict[str, object]:
    """What the gate screen shows (R-670): the totals and the items, each held item
    with its reason, each list capped at ``PLAN_SHOWN`` with a count of the rest.
    """
    items = plan["items"]
    planned = [
        {"from": item["from"], "to": item["to"]} for item in items if item["action"] == RENAME
    ]
    held = [
        {"from": item["from"], "as": item["action"], "why": item["why"]}
        for item in items
        if item["action"] != RENAME
    ]
    shown: dict[str, object] = {
        "root": str(root),
        "renames": plan["totals"]["count"],
        "referenced": plan["totals"]["referenced"],
        "collides": plan["totals"]["collides"],
        "unnamed": plan["totals"]["unnamed"],
        "planned": planned[:PLAN_SHOWN],
    }
    if len(planned) > PLAN_SHOWN:
        shown["planned not listed"] = len(planned) - PLAN_SHOWN
    shown["held"] = held[:PLAN_SHOWN]
    if len(held) > PLAN_SHOWN:
        shown["held not listed"] = len(held) - PLAN_SHOWN
    return shown


#: The refusal for a ``--root`` that names no folder (U169).
ROOT_MISSING = "root-folder-missing"


def root_path(given: str | None, cfg: config.Config, *, verb: str) -> Path:
    """The folder a ``--root`` names, relative to the library root (U169).

    Never relative to the shell's directory. ``~`` is expanded, an absolute path
    is taken as is, an omitted root is the library root, and an empty one is
    refused because ``Path("")`` is the working directory.
    """
    library = Path(cfg.library.root)
    if given is None:
        return library
    if not given.strip():
        raise _root_refused(
            f"--root was given an empty path, so {verb} has no folder to work on",
            tried=None,
            given=given,
        )
    named = Path(given).expanduser()
    return named if named.is_absolute() else library / named


def root_folder(given: str | None, cfg: config.Config, *, verb: str) -> Path:
    """:func:`root_path`, refused naming the path it tried unless a folder is there.

    A walk over a missing folder finds nothing, as a tidy folder does.
    """
    tried = root_path(given, cfg, verb=verb)
    if tried.is_dir():
        return tried
    if given is None:
        said = f"the library root {tried} is not a folder on this machine"
    elif Path(given).expanduser().is_absolute():
        said = f"--root {tried} is not a folder on this machine"
    else:
        said = (
            f"--root {given} was read against the library root as {tried}, and "
            f"no folder is there"
        )
    raise _root_refused(f"{said}, so {verb} has nothing to work on", tried=tried, given=given)


def _root_refused(message: str, *, tried: Path | None, given: str | None) -> CratekitError:
    return refuse(
        ROOT_MISSING,
        message,
        steps=(
            "name a folder inside the library by its path from the library root, "
            "or give its full path",
            "if the folder is on the library volume, check the volume is mounted",
        ),
        origin=("write.naming_cli",),
        detail={"tried": str(tried) if tried is not None else None, "given": given},
    )


def build(parser, entry) -> None:
    parser.add_argument(
        "--root",
        default=None,
        metavar="DIR",
        help="folder to rename, by its path from the library root or in full; "
        "the configured library root when omitted",
    )
    parser.set_defaults(_handler=name_apply)


def _incomplete_cause(
    incomplete: list[dict[str, str]], *, renamed: int, collides: int, unnamed: int
) -> Cause:
    """What the run answers when part of the plan did not happen (R-172).

    The renamed count, the outstanding count and the first file lead, with every
    item capped in the detail; what landed is said too, since this is no refusal.
    The first step points at the report; a collision, an unnamed file and a
    second copy each add their own.
    """
    count = len(incomplete)
    steps = [
        "read the file(s) this report names, each carries the reason its rename "
        "did not happen, and run this again",
    ]
    if collides:
        steps.append(
            "a file that renders to a name another file is using needs a name of "
            "its own, or one of the two moved out of the folder"
        )
    if unnamed:
        steps.append(
            "a file marked unnamed is named for its provider identifier and needs "
            "an artist tag and a title tag written before this can name it"
        )
    if any(item.get("isrc") for item in incomplete):
        steps.append(
            "a file held back as a second copy carries the same ISRC as the file "
            "whose name it would take, so it is one recording downloaded twice: "
            "compare the two and move the newer copy out of the folder"
        )
    return refuse(
        "rename-incomplete",
        f"{renamed} file(s) were renamed, and {count} file(s) this plan named were "
        f"not, the first of them {incomplete[0]['from']}, {incomplete[0]['why']}",
        steps=tuple(steps),
        scope=Scope.RUN,
        retryable=True,
        origin=("write.naming_cli",),
        detail={
            "renamed": renamed,
            "incomplete_count": count,
            "incomplete": incomplete[:INCOMPLETE_SHOWN],
        },
    ).cause


def name_apply(ctx) -> Envelope:
    cfg = load_config(("write.naming_cli",))
    root = root_folder(ctx.args.root, cfg, verb="name apply")
    plan = _plan_for(root, cfg=cfg)
    spec = ctx.entry.gates[0]
    option = ctx.gate.require(spec, digest=plan["digest"], context=_shown(plan, root=root))
    if option == "abort":
        return ctx.envelope(data=plan, outcome=Outcome.NO_OP)
    template = _template(cfg)
    budget = NameBudget.of(cfg.naming)
    renames = [item for item in plan["items"] if item["action"] == RENAME]
    # Every rename this run owes and did not perform, by name (R-172). A held
    # collision and an unnamed file (R-669) count, since the library still owes
    # them and answering ok would hide them from every later sweep.
    incomplete: list[dict[str, str]] = [
        {
            "from": item["from"],
            "path": item["path"],
            "why": item["why"],
            **({"isrc": item["isrc"]} if item.get("isrc") else {}),
        }
        for item in plan["items"]
        if item["action"] in (COLLIDES, UNNAMED)
    ]
    renamed = 0
    # Outstanding items that are a name in use, which decides the hand rename step.
    collided = plan["totals"]["collides"]

    def _owed(item: dict[str, str], why: str, *, at: Path | None = None, isrc: str = "") -> None:
        """One outstanding item, named where the file is now (``at``, after a rename)."""
        where = item["path"] if at is None else str(at)
        isrcs = {"isrc": isrc} if isrc else {}
        incomplete.append({"from": Path(where).name, "path": where, "why": why, **isrcs})

    # Read again after the gate, which can wait while rekordbox imports a file.
    referenced = (
        _referenced(
            _recorded(cfg), cfg=cfg, renaming=[Path(item["path"]) for item in renames]
        )
        if renames
        else frozenset()
    )
    for item in renames:
        path = Path(item["path"])
        if not path.is_file():
            _owed(item, "the file is no longer there")
            continue
        if _is_referenced(path, referenced):
            _owed(
                item,
                "the rekordbox collection began referencing it after the plan was "
                "approved, and renaming it would strand that row",
            )
            continue
        # The tags are read again too: a name the person did not see is not approved.
        built, why = _spec_for(path, template=template, cfg=cfg)
        if why is not None:
            _owed(item, why)
            continue
        rendered = naming.build(
            built, template=template, budget=budget, parent_dir=str(path.parent)
        )
        if rendered.filename != item["to"]:
            _owed(
                item,
                f"it now renders as {rendered.filename}, not the {item['to']} the plan "
                "was approved with, because a tag changed after the plan was built",
            )
            continue
        target = path.with_name(rendered.filename)
        if target != path:
            if not naming.claim_target(target):
                collided += 1
                # Read as the plan reads it (U212), a late taker may be a second copy.
                why, same = _taken(
                    path, target, fallback=f"{rendered.filename} is already taken in the folder"
                )
                _owed(item, why, isrc=same)
                continue
            try:
                path.rename(target)
            except OSError as exc:
                target.unlink(missing_ok=True)
                _owed(item, f"the filesystem refused the rename: {exc.strerror or exc}")
                continue
            path = target
        renamed += 1
        # ``write_tags`` reports failure by returning False; the rename stands.
        if not tags.write_tags(path, {"title": rendered.title_tag}):
            _owed(item, "it was renamed and its title tag could not be written", at=path)
    plan["totals"] = {
        **plan["totals"],
        "renamed": renamed,
        "incomplete": len(incomplete),
    }
    if not incomplete:
        return ctx.envelope(data=plan, outcome=Outcome.OK)
    # Through ``from_cause`` on the plan surface, not the diagnostic one, since
    # this verb carried out part of a plan; ``items`` is untouched after the
    # gate, so the digest still describes what was approved.
    return output.from_cause(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        started=ctx.started,
        cause=_incomplete_cause(
            incomplete,
            renamed=renamed,
            collides=collided,
            unnamed=plan["totals"]["unnamed"],
        ),
        schema=ctx.entry.output_schema or output.current_schema("plan"),
        data=plan,
    )
