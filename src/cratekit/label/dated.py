"""New label releases kept apart from the ones already heard (U117).

For each followed label, a dated playlist ``<Label> <year> new <date>`` in the
label's folder holds the tracks of the releases a go took (``all`` or ``pick``
answers it settled, dated by the local day of the settling) that the record's
``heard`` list does not name. It is reused by its exact name and only added to;
``label heard`` merges and removes it (U123), and one past
``labels.new_playlist_age_days`` is reported. One this plan creates is recorded
in the outbound ledger, which vouches for it before any removal. A write
refused part way names what was written first.

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from functools import partial
from typing import TYPE_CHECKING, Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.label import sync_cli

if TYPE_CHECKING:
    from cratekit.modules.outbound import folders

_ORIGIN = ("label.dated",)

#: The answers that take releases, the go's own.
TAKING = frozenset({sync_cli.ALL, sync_cli.PICK})

#: The per label key in ``label_sync.json`` read as the releases heard.
HEARD = "heard"

#: The year plan's actions by value, so the outbound package loads only to write.
CREATE = "create"
REUSE = "reuse"
AMBIGUOUS = "ambiguous"


def dated_name(label: str, year: str, day: str) -> str:
    """The dated playlist's title, ``<Label> <year> new <YYYY-MM-DD>``."""
    from cratekit.modules.outbound import folders

    return f"{folders.year_name(label, year)} new {day}"


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _local_day(instant: str) -> str:
    """The local calendar day of a recorded instant, or empty when unreadable."""
    try:
        moment = datetime.fromisoformat(instant)
    except ValueError:
        return ""
    if moment.tzinfo is not None:
        moment = moment.astimezone()
    return moment.date().isoformat()


def heard(document: Mapping[str, Any], label_id: str) -> frozenset[str]:
    """The releases the record says were heard, nothing when it says nothing."""
    held = (document.get("labels") or {}).get(label_id)
    listed = held.get(HEARD) if isinstance(held, Mapping) else None
    if not isinstance(listed, list):
        return frozenset()
    return frozenset(one for one in listed if isinstance(one, str) and one)


def taken_by_goes(document: Mapping[str, Any], label_id: str) -> dict[str, str]:
    """Every release a go took for the label, mapped to the first day one took it."""
    days: dict[str, str] = {}
    for entry in document.get("answers") or ():
        if not isinstance(entry, Mapping) or _text(entry.get("label_id")) != label_id:
            continue
        if entry.get("answer") not in TAKING:
            continue
        settled = entry.get(sync_cli.SETTLED)
        if not isinstance(settled, Mapping):
            continue
        day = _local_day(_text(settled.get("at")))
        if not day:
            continue
        named = entry.get("taken")
        if isinstance(named, list):
            identities = [one for one in named if isinstance(one, str) and one]
        else:
            releases = entry.get("releases")
            identities = [
                _text(one.get("identity"))
                for one in (releases if isinstance(releases, list) else ())
                if isinstance(one, Mapping) and _text(one.get("identity"))
            ]
        for identity in identities:
            days[identity] = min(day, days.get(identity, day))
    return days


def playlist_item(step, *, early: Mapping[str, Any] = {}, late: Mapping[str, Any] = {}):
    """One planned playlist step as a gate shows it, ``early`` keys before its
    name and ``late`` ones after its action."""
    return {
        "id": step.remote_id,
        "kind": "playlist",
        "year": step.year,
        **early,
        "name": step.name,
        "action": step.action,
        **late,
        "add": len(step.add),
        "tracks": step.tracks,
        **({"why": step.why} if step.why else {}),
    }


@dataclass(frozen=True, slots=True)
class DatedStep:
    """What the plan does for one dated playlist."""

    year: str
    day: str
    name: str
    action: str
    remote_id: str = ""
    add: tuple[str, ...] = ()
    tracks: int = 0
    why: str = ""

    @property
    def writes(self) -> bool:
        return self.action == CREATE or (self.action == REUSE and bool(self.add))


@dataclass(frozen=True, slots=True)
class Aged:
    """A dated playlist past the configured age, reported and never merged."""

    name: str
    remote_id: str
    day: str
    days: int
    limit: int


@dataclass(frozen=True, slots=True)
class DatedPlan:
    """One label's dated playlists, against the account as it is."""

    label_id: str
    label: str
    folder_id: str
    steps: tuple[DatedStep, ...] = ()
    aged: tuple[Aged, ...] = ()
    #: Releases a go took that this plan leaves out, by reason.
    left_out: Mapping[str, int] = field(default_factory=dict)

    @property
    def writes(self) -> bool:
        return any(step.writes for step in self.steps)

    def identity(self) -> dict[str, Any]:
        """What the digest is taken over: every write and its title."""
        return {
            "kind": "label-new-playlists",
            "label": self.label_id,
            "folder": self.folder_id,
            "steps": [
                [step.year, step.day, step.name, step.action, step.remote_id, list(step.add)]
                for step in self.steps
            ],
        }

    def items(self) -> list[dict[str, Any]]:
        items = [playlist_item(step, early={"date": step.day}) for step in self.steps]
        items.extend(
            {
                "id": one.remote_id,
                "kind": "playlist",
                "date": one.day,
                "name": one.name,
                "action": "report",
                "age_days": one.days,
                "why": (
                    f"{one.days} day(s) old, past the {one.limit} day(s) "
                    f"labels.new_playlist_age_days allows; reported and never merged on its "
                    f"own, crate label heard merges it once its releases are heard"
                ),
            }
            for one in self.aged
        )
        return items

    def payload(self) -> dict[str, Any]:
        items = self.items()
        return {
            "digest": digest_of(self.identity()),
            "items": items,
            "totals": {
                "count": len(items),
                "create": sum(1 for step in self.steps if step.action == CREATE),
                "add": sum(len(step.add) for step in self.steps),
                "aged": len(self.aged),
                "writes": self.writes,
            },
        }


@dataclass
class DatedApplied:
    """What an apply wrote, for the report and for a failure part way."""

    created: list[str] = field(default_factory=list)
    #: Each created playlist's identifier by name, recorded before its move.
    ids: dict[str, str] = field(default_factory=dict)
    #: Created playlists not yet in the label's folder.
    unplaced: list[str] = field(default_factory=list)
    added: dict[str, int] = field(default_factory=dict)
    refused: dict[str, int] = field(default_factory=dict)


def _aged(label: str, inside: Mapping[str, str], today: date, limit: int) -> tuple[Aged, ...]:
    pattern = re.compile(rf"^{re.escape(label)} (\d{{4}}) new (\d{{4}}-\d{{2}}-\d{{2}})$")
    found: list[Aged] = []
    for remote_id, title in sorted(inside.items(), key=lambda kv: kv[1]):
        matched = pattern.match(title or "")
        if matched is None:
            continue
        try:
            day = date.fromisoformat(matched.group(2))
        except ValueError:
            continue
        days = (today - day).days
        if days > limit:
            found.append(
                Aged(name=title, remote_id=remote_id, day=day.isoformat(), days=days, limit=limit)
            )
    return tuple(found)


def plan(
    cfg: config.Config,
    catalogue: folders.LabelCatalogue,
    folder_id: str,
    account,
    document: Mapping[str, Any],
    *,
    today: date | None = None,
) -> DatedPlan:
    """Decide each dated playlist against the record and the account; an empty
    ``folder_id`` is a folder the year plan creates, so each is created."""
    today = today or date.today()
    gone = heard(document, catalogue.label_id)
    took = taken_by_goes(document, catalogue.label_id)
    left_out = {"heard": 0, "not in the catalogue": 0, "undated": 0}
    wanted: dict[tuple[str, str], list[str]] = {}
    for identity, day in sorted(took.items(), key=lambda kv: (kv[1], kv[0])):
        if identity in gone:
            left_out["heard"] += 1
            continue
        found = catalogue.by_release.get(identity)
        if found is None:
            left_out["not in the catalogue"] += 1
            continue
        year, tracks = found
        if not year:
            left_out["undated"] += 1
            continue
        # ONLY TRACKS THE PROVIDER WILL PLAY, or a step is planned every run.
        playable = set(catalogue.years.get(year, ()))
        held = wanted.setdefault((year, day), [])
        held.extend(one for one in tracks if one in playable and one not in held)

    inside = account.folder_playlists(folder_id) if folder_id else {}
    steps: list[DatedStep] = []
    for (year, day), tracks in sorted(wanted.items()):
        name = dated_name(catalogue.name, year, day)
        matching = sorted(pid for pid, title in inside.items() if title == name)
        step_of = partial(DatedStep, year=year, day=day, name=name, tracks=len(tracks))
        if len(matching) > 1:
            why = (
                f"the folder holds {len(matching)} playlists named {name!r}, "
                f"so which one is the dated playlist is not something a name decides"
            )
            steps.append(step_of(action=AMBIGUOUS, why=why))
        elif matching:
            have = set(account.playlist_tracks(matching[0]))
            add = tuple(one for one in tracks if one not in have)
            steps.append(step_of(action=REUSE, remote_id=matching[0], add=add))
        else:
            steps.append(step_of(action=CREATE, add=tuple(tracks)))
    return DatedPlan(
        label_id=catalogue.label_id,
        label=catalogue.name,
        folder_id=folder_id,
        steps=tuple(steps),
        aged=_aged(catalogue.name, inside, today, cfg.labels.new_playlist_age_days),
        left_out={key: value for key, value in left_out.items() if value},
    )


def gate_plan(
    digest: str, items: list[dict[str, Any]], totals: Mapping[str, Any]
) -> dict[str, Any]:
    """A plan as the label verbs' gates show it, its totals counted first."""
    return {
        "digest": digest,
        "items": items,
        "totals": {"count": len(items), **totals},
        "chunk": None,
    }


def _no_folder(planned: DatedPlan) -> CratekitError:
    return refuse(
        "label-new-playlists-no-folder",
        f"the folder of {planned.label!r} is not recorded on the account, so no "
        f"dated playlist was made and nothing was written",
        steps=("run crate label playlists for the label, then organize again",),
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={"label_id": planned.label_id},
    )


def refused_part_way(
    exc: Exception,
    wrote: str,
    again: str,
    detail: Mapping[str, Any],
    *,
    failed: str,
    origin: Sequence[str],
    scope: Scope = Scope.RUN,
    steps: bool = True,
) -> CratekitError:
    """A label write failed part way, with what was written first named in it: a
    refusal keeps its reason and remedy, ``again`` added to its steps, and
    anything else is this build's own defect, ``failed`` naming what failed."""
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{wrote}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=scope,
            retryable=cause.retryable,
            origin=origin,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    return refuse(
        "internal-error",
        f"{wrote}. {failed} failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        steps=(again,) if steps else (),
        scope=scope,
        origin=origin,
        detail={**detail, "kind": type(exc).__name__},
    )


def _failed_part_way(exc: Exception, done: DatedApplied, planned: DatedPlan) -> CratekitError:
    """The failure, with what was already written named in it."""
    wrote = (
        f"before this failed {len(done.created)} dated playlist(s) were created "
        f"and {sum(done.added.values())} track(s) added"
        if done.created or done.added
        else "nothing was written before this failed"
    )
    detail = {"label_id": planned.label_id, **asdict(done)}
    detail["unplaced"] = [[name, done.ids[name]] for name in done.unplaced]
    del detail["refused"]
    again = "run crate organize again; a dated playlist is found by its name and only the rest is added"
    if done.unplaced:
        wrote += ", and " + ", ".join(
            f"{name!r} ({done.ids[name]}) was created and is not in the label's folder"
            for name in done.unplaced
        )
        again = (
            "move each playlist named above into the label's folder on the account "
            "before running crate organize again, or the next run makes a second one"
        )
    return refused_part_way(exc, wrote, again, detail, failed="The dated playlists", origin=_ORIGIN)


def apply(cfg: config.Config, account, planned: DatedPlan) -> DatedApplied:
    """Make and fill what the plan names, or raise naming what was written first."""
    from cratekit.modules.outbound import folders, ledger

    done = DatedApplied()
    folder_id = planned.folder_id or ledger.label_shape(cfg, planned.label_id).folder_id
    if not folder_id:
        raise _no_folder(planned)
    try:
        for step in planned.steps:
            if not step.writes:
                continue
            remote_id = step.remote_id
            if step.action == CREATE:
                # VOUCHED FOR IN THE LEDGER AS IT IS MADE (U123).
                remote_id = ledger.reserve_label_dated(
                    cfg,
                    planned.label_id,
                    step.name,
                    lambda name=step.name: account.create_playlist(name),
                )
                # RECORDED BEFORE THE MOVE, so a refusal names it at the root.
                done.created.append(step.name)
                done.ids[step.name] = remote_id
                done.unplaced.append(step.name)
                account.move_to_folder(remote_id, folder_id)
                done.unplaced = [one for one in done.unplaced if one != step.name]
            for start in range(0, len(step.add), folders.CHUNK):
                chunk = step.add[start : start + folders.CHUNK]
                held = set(account.add_tracks(remote_id, chunk))
                added = sum(1 for one in chunk if one in held)
                done.added[step.name] = done.added.get(step.name, 0) + added
                if added < len(chunk):
                    done.refused[step.name] = done.refused.get(step.name, 0) + len(chunk) - added
    except Exception as exc:
        raise _failed_part_way(exc, done, planned) from exc
    return done


def add_step(cfg, area, entry, year_plan: folders.Plan, remote_of) -> None:
    """Append the label's dated playlist step to ``crate organize``'s account area;
    a record or an account that cannot be read refuses this step alone."""
    from cratekit.organize.steps import NOTHING, PLANNED, Step, refused

    key = f"label-new:{entry.label_id}"
    title = f"new releases of {entry.name}"
    try:
        document = sync_cli.load_record(cfg)
        planned = plan(cfg, year_plan.catalogue, year_plan.folder_id, remote_of.get(), document)
    except CratekitError as exc:
        area.steps.append(refused(key, title, exc.cause))
        return
    payload = planned.payload()
    totals = payload["totals"]
    said = []
    if planned.writes:
        said.append(f"create {totals['create']} dated playlist(s) and add {totals['add']} track(s)")
    if planned.aged:
        said.append(
            f"{len(planned.aged)} dated playlist(s) older than "
            f"{cfg.labels.new_playlist_age_days} day(s), reported and left as they are"
        )
    step = Step(
        key=key,
        title=title,
        state=PLANNED if planned.writes else NOTHING,
        detail="; ".join(said) or "every release a go took is heard or already filed",
        digest=payload["digest"],
        counts={"create": totals["create"], "add": totals["add"], "aged": totals["aged"]},
        items=list(payload["items"]),
    )
    if planned.writes:
        def run() -> dict[str, Any]:
            done = apply(cfg, remote_of.get(), planned)
            if done.refused:
                message = (
                    f"the provider would not add {sum(done.refused.values())} "
                    f"track(s) to {len(done.refused)} dated playlist(s)"
                )
                warning = {"code": "label-new-playlists-tracks-refused", "message": message}
                step.warnings.append(warning)
            # EVERY FIELD WRITTEN, copied, but the moves still owed.
            written = asdict(done)
            del written["unplaced"]
            return written

        step.apply = run
    area.steps.append(step)


__all__ = [
    "HEARD",
    "Aged",
    "DatedApplied",
    "DatedPlan",
    "DatedStep",
    "add_step",
    "apply",
    "dated_name",
    "heard",
    "plan",
    "taken_by_goes",
]
