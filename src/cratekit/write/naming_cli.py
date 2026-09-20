"""Preview renames, then apply after the confirm gate.

The naming engine owns mechanism. This shell owns the plan, the gate, and
the filesystem rename. Absent key and BPM fields are omitted (R20). A
lossy file is marked on filename, title tag, and library name together
(R21), or the engine refuses.

A file the rekordbox collection references is never renamed or retagged here
(U67). rekordbox records a path once, at import, so a rename leaves the row
pointing at nothing. The verb reads the collection, holds those files back and
lists them in the plan, and refuses outright when the collection cannot be read.

A row recorded under a volume no prefix rule names, whose recorded file is not
on this machine either, refuses the whole verb too (R-500). Nothing here carries
that spelling, so the row matches no candidate and the file it names would be
planned as an ordinary rename. The deletion pass refuses on an unmapped row for
the same reason: a row that did not answer is a hole in the proof, not a row
that references nothing.
"""

from __future__ import annotations

import os
from pathlib import Path

from cratekit.cli import output
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, locations, naming, rb_writer, tags
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import AUDIO_EXTS, MarkerRule, NameBudget, NameSpec, NameTemplate
from cratekit.write import trees

RENAME = "rename"
REFERENCED = "referenced"
COLLIDES = "collides"

#: How many incomplete items one cause's detail carries, the same bound the
#: unmapped refusal puts on its own list and for the same measured reason.
INCOMPLETE_SHOWN = 20


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
    """The keys of every file the collection references, or a refusal.

    Each row contributes its path as recorded AND its path after the configured
    volume rewrites, because most rows in a real library still carry a volume
    name the drive stopped using long ago, and either spelling can be the one
    that is on disk today. A row naming another host has no local path and
    contributes nothing, since no local file can be the one it names, and a
    streaming pseudo-location references no file at all.

    THE DECODE AND THE RESOLVE ARE ``trees.located``, the one locate the
    membership and routing writers use, so a row is unmapped here exactly when
    it is unmapped there. The KEYING stays this verb's own, because the two ask
    different questions: a writer needs the one row that IS a file and compares
    exactly, and this guard needs every row that COULD name a file and errs
    toward holding it back, which is what the casefold and the second spelling
    are for. Casefolding the writers' index would manufacture ambiguous rows.

    A DARK ROW REFUSES THE WHOLE VERB (R-500). Dark is two facts together: no
    rule resolves the row, and the file it records is not on this machine under
    that spelling. Its only key is then a spelling nothing here carries, so it
    would match no candidate and the file it names would be renamed out from
    under it. Holding nothing back for that row is absence read as evidence. A
    rule that differs from the recorded volume only in case is no rule, here as
    in every other consumer of the shared resolver.

    AN UNMAPPED ROW WHOSE RECORDED FILE EXISTS HAS ANSWERED. A track imported
    from a downloads folder, or the demo tracks rekordbox installs, sit outside
    the library under no rule, and the recorded spelling is the one on disk, so
    the recorded key already protects the file. Refusing on those would stop the
    verb on most real libraries over rows that are not in doubt. The existence
    test fails closed: a path that cannot be inspected reads as absent.

    WHERE THIS IS STRICTER THAN THE DELETION PASS, and it is deliberate. That
    pass skips a tombstoned row before it asks whether the row resolved. This
    verb counts one, by its own rule above that a restore brings a tombstone
    back pointing at whatever it recorded. And two shapes that pass refuses on,
    a drive letter and a location on another host, are still excused here.
    """
    rules = [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]
    keys: set[str] = set()
    dark: list[str] = []
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
            dark.append(decoded)
    if dark:
        raise _unmapped_refusal(dark)
    return frozenset(keys)


def _unmapped_refusal(dark: list[str]) -> CratekitError:
    """The refusal over rows nothing resolves, worded as the deletion pass's is.

    The count leads and the first location follows, because the count says how
    much of the collection is dark and the location is what a person compares
    against their rules. It is the DECODED location, since that is the text a
    rule is matched against, and a percent-encoded spelling copied into a rule
    would never match. The prefixes are grouped in the detail so ten thousand
    rows under one old volume name read as one correction.

    ``fix-config-values`` and not ``run-doctor``, which is what the deletion
    pass says: no doctor check reads the prefix map, so that token would send a
    caller to a report that comes back clean.
    """
    count = len(dark)
    rows = "collection row records" if count == 1 else "collection rows record"
    prefixes = sorted({prefix for prefix in map(locations.leading_prefix, dark) if prefix})
    return refuse(
        "collection-row-unmapped",
        f"{count} {rows} a location this machine cannot resolve, the first of "
        f"them {dark[0]}, so which file each of them names is not known and a "
        f"rename could strand any of them; nothing is renamed",
        steps=(
            "add a rule to library.location_prefix_map whose from side is the "
            "recorded volume spelled exactly as it is named here, capitals "
            "included, and whose to side is where that volume is mounted now, "
            "then run this again",
        ),
        remedy=Remedy.FIX_CONFIG_VALUES,
        scope=Scope.RUN,
        origin=("write.naming_cli",),
        detail={
            "unmapped": count,
            "unmapped_locations": dark[:20],
            "unmapped_prefixes": prefixes[:20],
        },
    )


def _is_referenced(path: Path, referenced: frozenset[str]) -> bool:
    """True when the collection records ``path``, by either spelling of it.

    Both the absolute and the resolved spelling are asked, so a ``--root`` given
    through a link or as a relative path is still recognised.
    """
    return _key(str(path.absolute())) in referenced or _key(str(path.resolve())) in referenced


def _collisions(movers: list[tuple[Path, str]]) -> dict[str, str]:
    """Each mover that must not be renamed, mapped to why, keyed by path.

    THE PLAN PASS OWNS A COLLISION (R-172). Two files rendering to one name left
    the plan promising two renames and the apply performing one, because the
    loser's ``claim_target`` failed and the loop moved on. Detecting it here is
    what the ledger asked for: it is knowable before the gate, so the plan a
    person approves says which files cannot be renamed instead of promising a
    rename the filesystem was never going to allow.

    TWO SHAPES ARE HELD, and one deliberately is not:

    * several movers rendering to ONE target. Nothing decides which of them
      earns the name, so none of them takes it. Letting the first in sort order
      win is what shipped, and an arbitrary winner is worse than no winner,
      since the report said both moved.
    * a target that is a file on disk NOTHING here is moving. The claim would
      fail against a file with its own content, which is the collision the U67
      table drove.

    A TARGET ANOTHER MOVER STILL HOLDS IS LEFT PROMISED. The chain resolves
    whenever sort order reaches the occupant first, which it usually does, so
    holding it back would lose a rename that works today. When order runs the
    other way the apply pass reports it, which is the one case where discovering
    a collision during the rename is still the right place.

    KEYED THROUGH ``_key``, for the reason that function gives: the volume a
    library normally sits on ignores case, so two targets differing only in case
    are one name there. On a volume that respects case the cost is a file left
    unrenamed, which is the direction to be wrong in.

    TO A FIXPOINT, because holding a file back makes it an occupant. The first
    cut asked whether a target belonged to a mover ONCE, over every mover,
    including the ones it was in the middle of holding back. A file whose target
    was occupied by a collider therefore read as a chain that sort order would
    resolve, so the plan promised its rename and no rename was possible: three
    files in one folder produced ``totals.count`` of one and zero renames, which
    is the finding this unit exists to close, one file over. Each round removes
    what it held and asks again, and it ends when a round holds nothing.
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
                found[str(path)] = (
                    f"{target.name} is already taken in the folder by a file nothing "
                    f"here is renaming"
                )
        if not found:
            return held
        held.update(found)


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
    back rather than leaving them out silently. A colliding file is a third
    marked class (R-172) and is held back the same way, so ``count`` is the
    number of renames that can actually be performed rather than the number the
    plan wished for.
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
    # ASKED ONCE PER CANDIDATE. ``_is_referenced`` resolves the path, which is a
    # syscall per candidate, and a sweep of a real library has thousands.
    decided = [
        (path, filename, _is_referenced(path, referenced)) for path, filename in candidates
    ]
    collides = _collisions([(path, filename) for path, filename, ref in decided if not ref])
    items: list[dict[str, str]] = []
    held = 0
    for path, filename, ref in decided:
        if ref:
            held += 1
            items.append({"action": REFERENCED, "from": path.name, "path": str(path)})
        elif str(path) in collides:
            items.append(
                {
                    "action": COLLIDES,
                    "from": path.name,
                    "to": filename,
                    "path": str(path),
                    "why": collides[str(path)],
                }
            )
        else:
            items.append(
                {"action": RENAME, "from": path.name, "to": filename, "path": str(path)}
            )
    return {
        "digest": digest_of({"kind": "rename", "items": items}),
        "items": items,
        "totals": {
            "count": len(items) - held - len(collides),
            "referenced": held,
            "collides": len(collides),
        },
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


def _incomplete_cause(
    incomplete: list[dict[str, str]], *, renamed: int, collides: int
) -> Cause:
    """What the run answers when part of the plan did not happen (R-172).

    THE COUNT LEADS AND THE FIRST FILE FOLLOWS, worded as the unmapped refusal
    beside it is: the count says how much of the approved plan is outstanding
    and the name is what a person goes and looks at. Every item is in the detail,
    capped, with the reason it carries, so a report names which file stayed put
    instead of leaving a person to diff the folder against the plan.

    WHAT LANDED IS SAID IN THE SAME SENTENCE. This is not a refusal: the renames
    that could happen did, and a message naming only the failures reads like a
    run that touched nothing and would send a person to repeat it.

    THE STEP SENDS A PERSON TO THE REPORT, and only a real collision adds the
    sentence about naming a file by hand. Five reasons reach here and one of them
    is a target that was free by the time the run ended, so a single collision
    worded step told a person to rename a file that needed nothing, over a run
    that a second attempt completes. The per item reason is the specific
    instruction and the step is what points at it.
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
    # EVERY RENAME THIS RUN OWES AND DID NOT PERFORM, collected by name as it
    # happens (R-172). Each of the branches below used to be a bare ``continue``,
    # so a plan promising two renames and performing one answered ok with nothing
    # naming the file that stayed put. A collision the plan already held back
    # counts here too: it is a rename the library still needs, and answering ok
    # over it means every later sweep answers ok over it as well.
    incomplete: list[dict[str, str]] = [
        {"from": item["from"], "path": item["path"], "why": item["why"]}
        for item in plan["items"]
        if item["action"] == COLLIDES
    ]
    renamed = 0
    # HOW MANY OF THE OUTSTANDING ITEMS ARE A NAME ALREADY IN USE, which decides
    # whether the remediation says to name a file by hand. The plan's own
    # collisions start the count and a claim that failed after the gate joins it.
    collided = plan["totals"]["collides"]

    def _owed(item: dict[str, str], why: str, *, at: Path | None = None) -> None:
        """One outstanding item, named where the file IS rather than where it was.

        ``at`` is the file's path now, and only the tag write needs it: that
        branch runs after a successful rename, so the plan's ``from`` and ``path``
        name a file nobody can go and look at.
        """
        where = item["path"] if at is None else str(at)
        incomplete.append({"from": Path(where).name, "path": where, "why": why})

    # READ AGAIN AFTER THE GATE, because the gate can wait on a person for as
    # long as they like and rekordbox can import a file in that time. The plan's
    # check decides what a person was shown; this one decides what is touched.
    referenced = _referenced(_recorded(cfg), cfg=cfg) if renames else frozenset()
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
        rendered = naming.build(
            _spec_for(path, template=template, cfg=cfg),
            template=template,
            budget=budget,
            parent_dir=str(path.parent),
        )
        target = path.with_name(rendered.filename)
        if target != path:
            if not naming.claim_target(target):
                collided += 1
                _owed(item, f"{rendered.filename} is already taken in the folder")
                continue
            try:
                path.rename(target)
            except OSError as exc:
                target.unlink(missing_ok=True)
                _owed(item, f"the filesystem refused the rename: {exc.strerror or exc}")
                continue
            path = target
        renamed += 1
        # READ, because ``write_tags`` reports a failure by returning False and
        # a renamed file whose title never took the head is a promised write
        # that did not happen. The rename itself stands and is counted.
        if not tags.write_tags(path, {"title": rendered.title_tag}):
            _owed(item, "it was renamed and its title tag could not be written", at=path)
    plan["totals"] = {
        **plan["totals"],
        "renamed": renamed,
        "incomplete": len(incomplete),
    }
    if not incomplete:
        return ctx.envelope(data=plan, outcome=Outcome.OK)
    # THROUGH ``from_cause``, the one boundary where a cause becomes a status, so
    # this verb does not restate the code lookup or the origin hop for itself.
    # THE PLAN SURFACE AND NOT THE DIAGNOSTIC ONE, which is the ``schema``
    # argument's whole purpose: that function's default assumes a verb that
    # refused before producing a plan, and this one produced a plan and carried
    # out part of it, so what it DID rename is exactly what a person needs next.
    # ``items`` is untouched after the gate, so the digest keeps describing what
    # was approved.
    return output.from_cause(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        started=ctx.started,
        cause=_incomplete_cause(incomplete, renamed=renamed, collides=collided),
        schema=ctx.entry.output_schema or output.current_schema("plan"),
        data=plan,
    )
