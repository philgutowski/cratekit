"""The account area of ``crate organize`` (U112): add only, every step its own verb's.

THE STEPS, each the owning verb's plan and apply:

* A FOLDER PER FOLLOWED LABEL, ``label playlists``'s plan for every label the
  registry follows. A label with no folder, or one missing a year, plans the
  missing part; that verb's plan also adds a year's new tracks, and it is
  composed whole rather than narrowed. A catalogue read in part refuses that
  label alone, and the other labels stay planned;
* EVERY LANDED SYNC PASS MARKED, ``sync mark``'s plan for every intake file at
  the library root, pending or retired, that a sync pass's playlist jobs
  belong to. An intake file of no pass is counted and is no step;
* EVERY DOWNLOADED SET ARCHIVED, ``export archive``'s plan for a recorded set
  whose download this area can PROVE. Nothing records which landing
  downloaded a set, so the only proof read is an intake file named for the
  set, ``<set>_inboxed.xml``, which is what ``intake land --pass <set>``
  writes. A set the mark record already names is archived. Any other set is
  listed as waiting, with the command that archives it, and nothing is
  planned for it;
* EVERY MARKED CUSTOM PLAYLIST FILED (U116), :mod:`cratekit.organize.filing`:
  each playlist at the account root that a sync marked is moved into the year
  folder of its mark, and every other playlist at the root is named with why
  it stays. A playlist marked by this same pass is filed by the next one,
  since the plan reads the mark record before the marks are applied.

A STEP THAT NEEDS THE ACCOUNT AND CANNOT HAVE IT is refused, with that
refusal's own reason, and every other step is still planned and shown.

WHAT THE AUTHOR MADE is every playlist the account created that the product did
not make, that is no source system debris, that sits in no folder and that the
filing step does not move. Each is
listed with a home where :mod:`cratekit.organize.own` finds an obvious one, and
the sync's word on it. Unread is not none: a listing that refuses is a refused
step, never an empty list.

Layer: modules.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.export import set_cli
from cratekit.intake import land_cli
from cratekit.label import dated, playlists_cli
from cratekit.organize import filing, own
from cratekit.organize.steps import LISTED, NOTHING, PLANNED, Area, Step, refused
from cratekit.sync import mark_cli, mark_record

AREA = "account"

LABELS = "labels"
SETS = "sets"
FILE = "file"
YOURS = "yours"

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

    ``X_inboxed.xml`` is the newest, a pending landing. Retired files are
    ``.imported``, then ``.imported-2`` and on, each later than the one before,
    so the number decides and never the spelling: ``-10`` is later than ``-9``.
    """
    tail = name[name.rfind(land_cli.INTAKE_SUFFIX) + len(land_cli.INTAKE_SUFFIX):]
    if not tail:
        return 1 << 30
    number = tail[len(land_cli.RETIRED_SUFFIX):].lstrip("-")
    return int(number) if number.isdigit() else 1


def intake_by_pass(cfg: config.Config) -> dict[str, Path]:
    """The latest intake file at the library root for each pass, pending or retired.

    ONE RULE for the mark and for the set's proof, so the two never read two
    different landings of one pass. Listed by reading the directory, never by a
    glob, since a pass or set name may hold ``[``, ``*`` or ``?``.
    """
    root = Path(cfg.library.root)
    if not root.is_dir():
        return {}
    by_pass: dict[str, Path] = {}
    for path in root.iterdir():
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
    if not followed:
        area.steps.append(
            Step(key=LABELS, title="label folders", state=NOTHING, detail="no label is followed")
        )
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
        step = Step(
            key=key,
            title=title,
            state=PLANNED if planned.writes else NOTHING,
            detail=(
                f"create {missing} folder or year playlist(s) and add {totals['add']} track(s)"
                if planned.writes
                else "the account already holds every year and track planned"
            ),
            digest=payload["digest"],
            counts={"create": totals["create"], "add": totals["add"]},
            items=list(payload["items"]),
        )
        if planned.writes:
            step.apply = _label_apply(cfg, step, planned, remote_of)
        area.steps.append(step)
        dated.add_step(cfg, area, entry, planned, remote_of)


def _label_apply(cfg, step: Step, planned, remote_of: _Lazy):
    def apply() -> dict[str, Any]:
        done = playlists_cli.apply_plan(cfg, remote_of.get(), planned)
        step.warnings.extend(playlists_cli.refused_warnings(done))
        return playlists_cli.applied_totals(done)

    return apply


def _mark_steps(cfg, area: Area) -> None:
    unpassed = 0
    # ONE LISTING OF THE ACCOUNT FOR EVERY PASS, asked only when a file a pass
    # owns needs it, and its refusal kept for each pass that asks.
    listing = _Lazy(lambda: mark_cli.listed(cfg))
    for xml in intake_files(cfg):
        name = mark_cli.pass_name_of(xml)
        key = f"mark:{name}"
        title = f"mark the playlists pass {name} finished"
        try:
            planned = mark_cli.plan_pass(cfg, xml, listing=listing.get)
        except CratekitError as exc:
            area.steps.append(refused(key, title, exc.cause))
            continue
        if not planned.of_a_pass:
            unpassed += 1
            continue
        totals = planned.payload["totals"]
        step = Step(
            key=key,
            title=title,
            state=PLANNED if planned.planned else NOTHING,
            detail=(
                f"prefix {totals['mark']} playlist(s) as downloaded"
                if planned.planned
                else f"nothing to mark: {totals['skip']} playlist(s) left alone, each with its reason"
            ),
            digest=planned.payload["digest"],
            counts={"mark": totals["mark"], "skip": totals["skip"]},
            items=list(planned.payload["items"]),
        )
        if planned.planned:
            step.apply = _mark_apply(cfg, step, planned)
        area.steps.append(step)
    area.facts["intake files of no sync pass"] = unpassed


def _mark_apply(cfg, step: Step, planned):
    def apply() -> dict[str, Any]:
        data, warnings, landed = mark_cli.apply_pass(cfg, planned)
        step.warnings.extend(warnings)
        return {"marked": len(landed), "totals": data["totals"]}

    return apply


def _proof(cfg: config.Config, name: str) -> Path | None:
    """The latest intake file named for a set, by :func:`intake_by_pass`'s rule."""
    return intake_by_pass(cfg).get(name)


def _set_steps(cfg, area: Area) -> None:
    from cratekit.modules.outbound import ledger

    try:
        names = ledger.set_playlist_names(cfg)
        # A MARK ``sync unmark`` PUT BACK IS NO MARK: the playlist carries its
        # old title again and is not archived as far as anyone can see.
        marked = {
            entry.playlist_id
            for entry in mark_record.MarkRecord(cfg).all()
            if not entry.unmarked
        }
    except CratekitError as exc:
        area.steps.append(refused(SETS, "archive downloaded sets", exc.cause))
        return
    if not names:
        area.steps.append(
            Step(key=SETS, title="archive downloaded sets", state=NOTHING, detail="no set playlist is recorded")
        )
        return
    for name in names:
        key = f"archive:{name}"
        title = f"archive the set {name}"
        xml = _proof(cfg, name)
        if xml is None:
            recorded = ledger.set_playlist(cfg, name)
            if recorded is not None and recorded.remote_id in marked:
                area.steps.append(
                    Step(key=key, title=title, state=NOTHING, detail="already archived and marked")
                )
                continue
            area.steps.append(
                Step(
                    key=key,
                    title=title,
                    state=LISTED,
                    detail=(
                        f"waiting: no intake file named for this set, so its download is "
                        f"not proven here and nothing is planned; archive it with crate "
                        f"export archive {name!r} --xml INTAKE once it has landed"
                    ),
                )
            )
            continue
        try:
            archived = set_cli.plan_archive(cfg, name, xml)
        except CratekitError as exc:
            area.steps.append(refused(key, title, exc.cause))
            continue
        step = Step(
            key=key,
            title=title,
            state=PLANNED if archived.writes else NOTHING,
            detail=(
                f"file it in its year folder and prefix it, proven by {xml.name}"
                if archived.writes
                else "already in its year folder and marked"
            ),
            digest=archived.payload["digest"],
            counts={"writes": int(archived.writes)},
            items=list(archived.payload["items"]),
        )
        if archived.writes:
            step.apply = _set_apply(cfg, step, archived)
        area.steps.append(step)


def _set_apply(cfg, step: Step, archived):
    def apply() -> dict[str, Any]:
        data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
        step.warnings.extend(warnings)
        return dict(data["totals"]["applied"])

    return apply


def _file_step(cfg, area: Area, labels: tuple[str, ...], catalogue_of: _Lazy, remote_of: _Lazy) -> frozenset[str]:
    """Plan the filing of every marked playlist at the root; answer what it moves."""
    from cratekit.favorites import placeholders
    from cratekit.sync import playlists

    title = "file marked playlists into their year folders"
    try:
        planned = filing.plan(
            cfg,
            listed=catalogue_of.get().account_playlists(),
            remote=remote_of.get(),
            labels=labels,
            marks=mark_record.MarkRecord(cfg).all(),
            working=lambda name: placeholders.is_placeholder(name) or playlists.is_library_debris(name),
        )
    except CratekitError as exc:
        area.steps.append(refused(FILE, title, exc.cause))
        return frozenset()
    moves = planned.moves
    created = planned.creates()
    step = Step(
        key=FILE,
        title=title,
        state=PLANNED if planned.writes else NOTHING,
        detail=(
            f"move {len(moves)} marked playlist(s) into their year folders, creating "
            f"{len(created)} folder(s), and leave {len(planned.rows) - len(moves)} at the root, each with its reason"
            if planned.writes
            else f"nothing to move: {len(planned.rows)} playlist(s) at the root, each left with its reason"
        ),
        digest=digest_of(planned.identity()),
        counts={"move": len(moves), "left": len(planned.rows) - len(moves), "create": len(created)},
        items=planned.items(),
    )
    if planned.writes:
        step.apply = _file_apply(cfg, planned, remote_of)
    area.steps.append(step)
    return frozenset(row.playlist_id for row in moves)


def _file_apply(cfg, planned, remote_of: _Lazy):
    def apply() -> dict[str, Any]:
        return filing.apply(cfg, remote_of.get(), planned).totals()

    return apply


def _yours(
    cfg,
    area: Area,
    labels: tuple[str, ...],
    catalogue_of: _Lazy,
    remote_of: _Lazy,
    moving: frozenset[str] = frozenset(),
) -> None:
    from cratekit.favorites import placeholders
    from cratekit.modules.outbound import ledger
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
        )
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
                "name": one.name,
                "playlist_id": one.playlist_id,
                "place": "account root",
                "kind": "playlist",
                "sync": (
                    "swept and marked by a sync"
                    if playlists.is_swept_name(one.name)
                    else "a sync sweeps it as intake"
                ),
                "suggested_home": own.account_home(one.name, labels),
            }
        )
    area.steps.append(
        Step(
            key=YOURS,
            title=title,
            state=LISTED,
            detail=f"{found} playlist(s) of your own at the account root, listed and never moved",
            counts={"account root": found, "in folders": len(in_folders)},
        )
    )


def plan_area(
    cfg: config.Config,
    *,
    available: frozenset[str],
    followed,
    unfollowed: CratekitError | None = None,
) -> Area:
    """Plan every account step; a step that refuses is shown and hides no other.

    ``unfollowed`` is the label registry's own refusal when it could not be
    read, shown as the label step's refusal, so the other steps still plan.
    """
    from cratekit.label import catalogue
    from cratekit.modules.outbound import account

    area = Area(name=AREA)
    catalogue_of = _Lazy(lambda: catalogue.resolve(cfg))
    remote_of = _Lazy(lambda: account.resolve(cfg))
    labels = tuple(entry.name for entry in followed)
    if LABELS_MODULE in available and unfollowed is not None:
        area.steps.append(refused(LABELS, "label folders", unfollowed.cause))
    elif LABELS_MODULE in available:
        _label_steps(cfg, area, followed, catalogue_of, remote_of)
    else:
        area.steps.append(
            Step(
                key=LABELS,
                title="label folders",
                state=LISTED,
                detail="the labels module is off in this profile, so no label folder is planned",
            )
        )
    if EXPORT_MODULE in available:
        _set_steps(cfg, area)
    else:
        area.steps.append(
            Step(
                key=SETS,
                title="archive downloaded sets",
                state=LISTED,
                detail="the export module is off in this profile, so no set is archived",
            )
        )
    _mark_steps(cfg, area)
    moving = _file_step(cfg, area, labels, catalogue_of, remote_of)
    _yours(cfg, area, labels, catalogue_of, remote_of, moving)
    area.facts["writes"] = "add only: folders are created and playlists filed and prefixed"
    return area


__all__ = ["AREA", "FILE", "LABELS", "SETS", "YOURS", "intake_files", "plan_area"]
