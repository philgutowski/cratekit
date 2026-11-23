"""The account area of ``crate organize`` (U112): add only, every step its own verb's.

The steps: a folder per followed label (``label playlists``), every landed sync
pass marked (``sync mark``), every downloaded set archived (``export
archive``), the root filed (U116, :mod:`cratekit.organize.filing`) and kept
(U143, :mod:`cratekit.organize.root`), and the routing tree, Favorites and
INBOX mirrored (U147, U150, :mod:`cratekit.organize.account_mirror`).

A SET IS ARCHIVED ONLY WHEN ITS DOWNLOAD IS PROVEN, by an intake file named for
it or (U142) an INSPIRATION playlist of its name; any other set is listed as
waiting, with the command that archives it.

A STEP THAT CANNOT HAVE WHAT IT NEEDS is refused with that refusal's reason and
hides no other; unread is not none. What the author made at the account root
is listed, with a home where :mod:`cratekit.organize.own` finds one.

Layer: modules.
"""

from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.intake import land_cli
from cratekit.organize import account_mirror, filing, own, root
from cratekit.organize.steps import LISTED, NOTHING, Area, Step, planned_step, refused, selection
from cratekit.sync import mark_cli, mark_record

AREA = "account"

LABELS = "labels"
SETS = "sets"
MARKS = "marks"
FILE = "file"
ROOT = "root"
MIRROR = account_mirror.MIRROR
YOURS = "yours"

#: Every step kind this area plans, in its order, each one ``--only`` may name.
#: ``root`` is one kind over debris, empties and a legacy year folder (U143),
#: which share one root read. The mirror (U147) is planned after the filing and
#: the root, whose plans read the account before anything here is created.
STEPS = (LABELS, SETS, MARKS, FILE, ROOT, MIRROR, YOURS)

#: The modules that switch a step on. Adoption, rotation and the mark are core.
LABELS_MODULE = "labels"
EXPORT_MODULE = "export"


class _Lazy:
    """One resolution of a provider seam per run, its refusal kept and handed on."""

    def __init__(self, resolve) -> None:
        self._resolve = resolve
        self._value: Any = None
        self._error: CratekitError | None = None
        self._done = False

    def get(self) -> Any:
        if not self._done:
            self._done = True
            try:
                self._value = self._resolve()
            except CratekitError as exc:
                self._error = exc
        if self._error is not None:
            raise self._error
        return self._value


def _rank(name: str) -> int:
    """How late a landing's file is: pending above every retired one, then by number.

    Retired files are ``.imported``, ``.imported-2`` and on, so the number
    decides and never the spelling: ``-10`` is later than ``-9``.
    """
    tail = name[name.rfind(land_cli.INTAKE_SUFFIX) + len(land_cli.INTAKE_SUFFIX):]
    if not tail:
        return 1 << 30
    number = tail[len(land_cli.RETIRED_SUFFIX):].lstrip("-")
    return int(number) if number.isdigit() else 1


def intake_by_pass(cfg: config.Config) -> dict[str, Path]:
    """The latest intake file at the library root for each pass, pending or retired.

    ONE RULE for the mark and for the set's proof, so the two never read two
    landings of one pass. The directory is read, never globbed, since a pass or
    set name may hold ``[``, ``*`` or ``?``.
    """
    library = Path(cfg.library.root)
    if not library.is_dir():
        return {}
    by_pass: dict[str, Path] = {}
    for path in library.iterdir():
        written = land_cli.unretired_name(path.name)
        if not written.endswith(land_cli.INTAKE_SUFFIX) or written == land_cli.INTAKE_SUFFIX:
            continue
        if not path.is_file():
            continue
        name = written[: -len(land_cli.INTAKE_SUFFIX)]
        held = by_pass.get(name)
        if held is None or _rank(path.name) > _rank(held.name):
            by_pass[name] = path
    return by_pass


def intake_files(cfg: config.Config) -> list[Path]:
    """Every pass's latest intake file, in pass name order."""
    by_pass = intake_by_pass(cfg)
    return [by_pass[name] for name in sorted(by_pass)]


def _label_steps(cfg, area: Area, followed, catalogue_of: _Lazy, remote_of: _Lazy) -> None:
    from cratekit.label import dated, playlists_cli

    if not followed:
        area.steps.append(Step(LABELS, "label folders", NOTHING, "no label is followed"))
        return
    for entry in followed:
        key = f"label:{entry.label_id}"
        title = f"label folder {entry.name}"
        try:
            planned = playlists_cli.plan_label(cfg, entry, catalogue_of.get(), remote_of.get())
        except CratekitError as exc:
            area.steps.append(refused(key, title, exc.cause))
            continue
        payload = playlists_cli.plan_payload(planned, name=entry.name)
        totals = payload["totals"]
        missing = sum(1 for item in payload["items"] if item["action"] == "create")
        area.steps.append(
            planned_step(
                key, title, planned.writes,
                f"create {missing} folder or year playlist(s) and add {totals['add']} track(s)"
                if planned.writes
                else "the account already holds every year and track planned",
                digest=payload["digest"], items=payload["items"],
                counts={"create": totals["create"], "add": totals["add"]},
                apply=partial(_label_apply, cfg, planned, remote_of),
            )
        )
        dated.add_step(cfg, area, entry, planned, remote_of)


def _label_apply(cfg, planned, remote_of: _Lazy, step: Step) -> dict[str, Any]:
    from cratekit.label import playlists_cli

    done = playlists_cli.apply_plan(cfg, remote_of.get(), planned)
    step.warnings.extend(playlists_cli.refused_warnings(done))
    return playlists_cli.applied_totals(done)


def _mark_steps(cfg, area: Area) -> None:
    """One step per landed pass, found by its intake file and by its native landing.

    A PASS LANDED ON A DATABASE NATIVE INTAKE TREE WRITES NO INTAKE FILE, so it
    is found by its landing's record (R-915, U174), every such pass and not only
    the latest, and a pass with an intake file is never planned twice. A native
    landing of no sync pass is counted and is no step.
    """
    unpassed = 0
    # ONE LISTING OF THE ACCOUNT FOR EVERY PASS, asked only when a pass needs it.
    listing = _Lazy(lambda: mark_cli.listed(cfg))
    seen: set[str] = set()
    for xml in intake_files(cfg):
        name = mark_cli.pass_name_of(xml)
        seen.add(name)
        if not _mark_step(cfg, area, name, partial(mark_cli.plan_pass, cfg, xml, listing=listing.get)):
            unpassed += 1
    area.facts["intake files of no sync pass"] = unpassed
    unlanded = 0
    try:
        native_names = mark_cli.native_passes(cfg)
    except CratekitError as exc:
        # REFUSED ALONE: the passes found by their intake files are still planned.
        area.steps.append(
            refused("mark:native", "mark the passes native landings committed", exc.cause)
        )
        native_names = ()
    for name in native_names:
        if name in seen:
            continue
        plan = partial(mark_cli.plan_pass, cfg, pass_name=name, listing=listing.get)
        if not _mark_step(cfg, area, name, plan):
            unlanded += 1
    if unlanded:
        area.facts["native landings of no sync pass"] = unlanded


def _mark_step(cfg, area: Area, name: str, plan) -> bool:
    """Plan one pass's marks as a step. False when the pass is no sync pass's."""
    key = f"mark:{name}"
    title = f"mark the playlists pass {name} finished"
    try:
        planned = plan()
    except CratekitError as exc:
        area.steps.append(refused(key, title, exc.cause))
        return True
    if not planned.of_a_pass:
        return False
    totals = planned.payload["totals"]
    area.steps.append(
        planned_step(
            key, title, planned.planned,
            f"record {totals['mark']} playlist(s) as taken"
            if planned.planned
            else f"nothing to mark: {totals['skip']} playlist(s) left alone, each with its reason",
            digest=planned.payload["digest"], items=planned.payload["items"],
            counts={"mark": totals["mark"], "skip": totals["skip"]},
            apply=partial(_mark_apply, cfg, planned),
        )
    )
    return True


def _mark_apply(cfg, planned, step: Step) -> dict[str, Any]:
    data, warnings, landed = mark_cli.apply_pass(cfg, planned)
    step.warnings.extend(warnings)
    return {"marked": len(landed), "totals": data["totals"]}


def _proof(cfg: config.Config, name: str) -> Path | None:
    """The latest intake file named for a set, by :func:`intake_by_pass`'s rule."""
    return intake_by_pass(cfg).get(name)


def _waiting(name: str, inspired: frozenset[str] | None) -> str:
    """Why a set with neither proof waits, naming the second proof's own state."""
    second = (
        "no INSPIRATION playlist of its name"
        if inspired is not None
        else "no INSPIRATION folder declared in the taxonomy to hold a playlist of its name"
    )
    return (
        f"waiting: no intake file named for this set and {second}, so its download "
        f"is not proven here and nothing is planned; archive it with crate export "
        f"archive {name!r} --xml INTAKE once it has landed"
    )


def _set_steps(cfg, area: Area, one_read: Any = None) -> None:
    from cratekit.export import set_cli
    from cratekit.modules.outbound import ledger, sets

    try:
        names = ledger.set_playlist_names(cfg)
        # A MARK ``sync unmark`` PUT BACK IS NO MARK. Since U242 the archive's
        # mark is a taken entry of its own kind, a legacy one a prefix mark; a
        # title ``sync strip`` wrote, or a prefix the migration found, is neither.
        record = mark_record.MarkRecord(cfg)
        marked = {
            entry.playlist_id for entry in mark_record.standing_prefix_marks(record.all())
        } | {
            identity
            for identity, entry in record.taken().items()
            if entry.held and entry.how == mark_record.BY_SET
        }
    except CratekitError as exc:
        area.steps.append(refused(SETS, "archive downloaded sets", exc.cause))
        return
    if not names:
        area.steps.append(
            Step(SETS, "archive downloaded sets", NOTHING, "no set playlist is recorded")
        )
        return
    # THE DATABASE IS READ ONCE, and only for a set with no intake file and no
    # standing mark.
    inspired = _Lazy(lambda: set_cli.inspiration_names(cfg, one_read=one_read))
    for name in names:
        key = f"archive:{name}"
        title = f"archive the set {name}"
        xml = _proof(cfg, name)
        proof = xml.name if xml is not None else ""
        if xml is None:
            recorded = ledger.set_playlist(cfg, name)
            if recorded is not None and recorded.remote_id in marked:
                area.steps.append(Step(key, title, NOTHING, "already archived and marked"))
                continue
            try:
                held = inspired.get()
            except CratekitError as exc:
                area.steps.append(refused(key, title, exc.cause))
                continue
            if held is None or name not in held:
                area.steps.append(Step(key, title, LISTED, _waiting(name, held)))
                continue
            proof = f"the INSPIRATION playlist {name}"
        try:
            archived = (
                set_cli.plan_archive(cfg, name, xml)
                if xml is not None
                # THE SET'S OWN NAME IS THE PASS, so ``sync unmark --pass <set>`` undoes it.
                else set_cli.plan_archive_named(cfg, name, pass_name=name)
            )
        except CratekitError as exc:
            area.steps.append(refused(key, title, exc.cause))
            continue
        planned = archived.planned
        folder = planned.folder_name if planned is not None else "its folder"
        if archived.writes and planned.move:
            detail = f"file it in {folder} and record it as taken, proven by {proof}"
        elif archived.writes:
            # IN THE FOLDER ALREADY: a mark and no move, so the line promises none.
            detail = f"record it as taken where it is, already in {folder}, proven by {proof}"
        elif planned is not None and planned.left == sets.RETITLED:
            detail = f"already in {folder}, its title left as a person set it"
        else:
            detail = f"already in {folder} and marked"
        area.steps.append(
            planned_step(
                key, title, archived.writes, detail,
                digest=archived.payload["digest"], items=archived.payload["items"],
                counts={"writes": int(archived.writes)}, apply=partial(_set_apply, cfg, archived),
            )
        )


def _set_apply(cfg, archived, step: Step) -> dict[str, Any]:
    from cratekit.export import set_cli

    data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    step.warnings.extend(warnings)
    return dict(data["totals"]["applied"])


def _filing_plan(
    cfg, labels: tuple[str, ...], catalogue_of: _Lazy, remote_of: _Lazy,
    unfollowed: CratekitError | None,
) -> filing.FilePlan:
    """The filing step's plan, which the root step reads its candidates from.

    AN UNREAD LABEL REGISTRY REFUSES THE FILING (U137): the followed labels are
    what leaves a label's playlist at the root for the label step, and planned
    over none the filing would move it into ``Mine``. Unread is not none.
    """
    from cratekit.favorites import placeholders

    if unfollowed is not None:
        raise unfollowed
    return filing.plan(
        cfg, listed=catalogue_of.get().account_playlists(), remote=remote_of.get(),
        labels=labels, marks=mark_record.MarkRecord(cfg).all(),
        working=placeholders.is_placeholder,
        taken=tuple(mark_record.MarkRecord(cfg).taken().values()),
    )


def _file_step(cfg, area: Area, filed_of: _Lazy, remote_of: _Lazy) -> frozenset[str]:
    """Plan the filing of every playlist at the root; answer what it moves."""
    title = "file playlists at the root into their folders"
    try:
        planned = filed_of.get()
    except CratekitError as exc:
        area.steps.append(refused(FILE, title, exc.cause))
        return frozenset()
    moves, created, rows = planned.moves, planned.creates(), len(planned.rows)
    area.steps.append(
        planned_step(
            FILE, title, planned.writes,
            f"move {len(moves)} playlist(s) into their year, Mine or Exports folders, creating "
            f"{len(created)} folder(s), and leave {rows - len(moves)} at the root, each with its reason"
            if planned.writes
            else f"nothing to move: {rows} playlist(s) at the root, each left with its reason",
            digest=digest_of(planned.identity()), items=planned.items(),
            counts={"move": len(moves), "left": rows - len(moves), "create": len(created)},
            apply=lambda _step: filing.apply(cfg, remote_of.get(), planned).totals(),
        )
    )
    return frozenset(row.playlist_id for row in moves)


def _root_step(cfg, area: Area, followed, catalogue_of: _Lazy, remote_of: _Lazy, filed_of: _Lazy) -> None:
    """Plan the root's removals and legacy moves (U143).

    A FILING THAT REFUSED REFUSES THIS STEP with the same reason, since the
    filing plan names the candidates.
    """
    title = "keep the account root to working custom playlists"
    try:
        planned = root.plan(
            cfg, listed=catalogue_of.get().account_playlists(), remote=remote_of.get(),
            filed=filed_of.get(),
            followed=tuple((entry.label_id, entry.name) for entry in followed),
        )
    except CratekitError as exc:
        area.steps.append(refused(ROOT, title, exc.cause))
        return
    removals, moves = planned.removals, planned.moves
    left = len(planned.rows) - len(removals) - len(moves)
    area.steps.append(
        planned_step(
            ROOT, title, planned.writes,
            f"remove {len(removals)} playlist(s) or folder(s), move {len(moves)} playlist(s) "
            f"out of a legacy year folder, and leave {left}, each with its reason"
            if planned.writes
            else f"nothing to remove or move: {left} left at the root, each with its reason",
            digest=digest_of(planned.identity()), items=planned.items(),
            counts={"remove": len(removals), "move": len(moves), "left": left},
            apply=partial(_root_apply, cfg, planned, remote_of),
        )
    )
    if planned.writes:
        area.deletes.extend(row.line() for row in removals)


def _root_apply(cfg, planned, remote_of: _Lazy, step: Step) -> dict[str, Any]:
    done = root.apply(cfg, remote_of.get(), planned)
    step.warnings.extend(
        {"code": "organize-root-kept", "message": f"the {kind} {name!r} was not removed: {why}"}
        for kind, _target, name, why in done.kept
    )
    return done.totals()


def _empties(filed_of: _Lazy) -> frozenset[str]:
    """Each root playlist the filing leaves for the root step as empty, or none unread."""
    try:
        planned = filed_of.get()
    except CratekitError:
        return frozenset()
    return frozenset(row.playlist_id for row in planned.rows if row.why == filing.EMPTY)


def _yours(
    cfg, area: Area, labels: tuple[str, ...], catalogue_of: _Lazy, remote_of: _Lazy,
    moving: frozenset[str] = frozenset(),
) -> None:
    from cratekit.favorites import placeholders
    from cratekit.modules.outbound import ledger, pairs
    from cratekit.sync import playlists

    title = "list your own playlists"
    try:
        listed = catalogue_of.get().account_playlists()
        remote = remote_of.get()
        in_folders = filing.playlists_in_folders(remote)
        label_built = ledger.label_playlist_ids(cfg)
        set_built = ledger.set_playlist_ids(cfg)
        made = (
            label_built
            | set_built
            | ledger.product_made_among(cfg, (one.playlist_id for one in listed))
            # U198. A PAIRED PLAYLIST IS SYNC PAIR'S, not one of yours to home.
            | pairs.paired_ids(cfg)
        )
        # U242. WHAT THE RECORD HOLDS AS TAKEN is still said to be marked by a sync.
        taken = playlists.taken_ids(cfg)
    except CratekitError as exc:
        area.steps.append(refused(YOURS, title, exc.cause))
        return
    found = 0
    for one in sorted(listed, key=lambda playlist: (playlist.name, playlist.playlist_id)):
        if (
            one.playlist_id in made
            or one.playlist_id in moving
            or one.playlist_id in in_folders
            or placeholders.is_placeholder(one.name)
            or playlists.is_library_debris(one.name)
        ):
            continue
        found += 1
        area.yours.append(
            {
                "name": one.name, "playlist_id": one.playlist_id,
                "place": "account root", "kind": "playlist",
                "sync": (
                    "swept and marked by a sync"
                    if playlists.is_taken(one.playlist_id, one.name, taken)
                    else "a sync sweeps it as intake"
                ),
                "suggested_home": own.account_home(one.name, labels),
            }
        )
    detail = f"{found} playlist(s) of your own at the account root, listed and never moved"
    counts = {"account root": found, "in folders": len(in_folders)}
    area.steps.append(Step(YOURS, title, LISTED, detail, counts=counts))


def plan_area(
    cfg: config.Config, *, available: frozenset[str], followed,
    unfollowed: CratekitError | None = None, only: frozenset[str] | None = None,
    run: account_mirror.Run | None = None, shared: account_mirror.Shared | None = None,
    one_read: Any = None,
) -> Area:
    """Plan every account step; a step that refuses is shown and hides no other.

    ``unfollowed`` is the label registry's own refusal, shown as the label
    step's and the filing's. ``only`` is ``--only``'s selection (U137): a step
    of no selected kind is not planned, so nothing it would read is read.
    ``run`` is the organize run the mirror records, freezes and rebuilds its
    plan on (R-1031). ``shared`` is the run's one account and mirror reading
    (U201), through which every step here resolves the account when given.
    ``one_read`` is ``--report``'s one read handle (U267), which the sets step
    reads INSPIRATION through.
    """
    from cratekit.label import catalogue
    from cratekit.modules.outbound import account

    area = Area(name=AREA, only=selection(STEPS, only))
    catalogue_of = _Lazy(lambda: catalogue.resolve(cfg))
    remote_of = _Lazy(shared.account if shared is not None else lambda: account.resolve(cfg))
    labels = tuple(entry.name for entry in followed)
    if area.wants(LABELS):
        if LABELS_MODULE not in available:
            said = "the labels module is off in this profile, so no label folder is planned"
            area.steps.append(Step(LABELS, "label folders", LISTED, said))
        elif unfollowed is not None:
            area.steps.append(refused(LABELS, "label folders", unfollowed.cause))
        else:
            _label_steps(cfg, area, followed, catalogue_of, remote_of)
    if area.wants(SETS):
        if EXPORT_MODULE in available:
            _set_steps(cfg, area, one_read)
        else:
            said = "the export module is off in this profile, so no set is archived"
            area.steps.append(Step(SETS, "archive downloaded sets", LISTED, said))
    if area.wants(MARKS):
        _mark_steps(cfg, area)
    # ONE FILING PLAN, read by the filing step and the root step (U143). A
    # REGISTRY THE PROFILE DOES NOT USE IS NO REASON TO REFUSE: with the labels
    # module off no label step exists to leave a playlist to.
    filed_of = _Lazy(
        lambda: _filing_plan(
            cfg, labels, catalogue_of, remote_of,
            unfollowed if LABELS_MODULE in available else None,
        )
    )
    moving: frozenset[str] = frozenset()
    if area.wants(FILE) or area.wants(YOURS):
        # THE FILING IS PLANNED FOR ``yours`` TOO, into an area nobody is shown
        # when the filing is not selected, so a playlist it moves is never listed.
        moving = _file_step(cfg, area if area.wants(FILE) else Area(name=AREA), filed_of, remote_of)
    if area.wants(ROOT):
        _root_step(cfg, area, followed, catalogue_of, remote_of, filed_of)
    if area.wants(YOURS):
        # AN EMPTY ROOT PLAYLIST IS THE ROOT STEP'S, read off the filing plan so
        # ``--only yours`` makes none of the root step's reads.
        _yours(cfg, area, labels, catalogue_of, remote_of, moving | _empties(filed_of))
    # THE MIRROR IS PLANNED LAST (U222): it freezes every step the gate shows, and
    # a step planned after it would be named on every stale answer.
    if area.wants(MIRROR):
        account_mirror.add_steps(cfg, area, remote_of.get, run, shared=shared)
    area.facts["writes"] = (
        "folders are created and playlists filed, and what is marked is recorded in "
        "Cratekit's own record with no title changed; at the root, only the "
        "source system's label debris whose tracks are in its label's folder, an empty "
        "playlist and an emptied legacy year folder are removed, each named; a mirrored "
        "playlist the product made loses the tracks its rekordbox playlist no longer holds"
    )
    return area


__all__ = [
    "AREA", "FILE", "LABELS", "MARKS", "MIRROR", "ROOT", "SETS", "STEPS", "YOURS",
    "intake_files", "plan_area",
]
