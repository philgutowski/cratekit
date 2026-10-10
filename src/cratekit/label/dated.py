"""New label releases kept apart from the ones already heard (U117).

A followed label's year playlist on the account, ``<Label> <year>``, holds
every track of that year's confirmed catalogue (R-835), so a release a go just
downloaded lands among the ones the author has already listened to. This
module plans, for each followed label, a dated playlist beside the year,
``<Label> <year> new <date>``, in the label's folder, holding the tracks of the
releases a go took that the author has not yet said he has heard.

WHAT A GO TOOK is read from the label review store, ``label_sync.json``: every
``all`` or ``pick`` answer for the label that a go has settled, and the
releases it took. The date is the local calendar day of the settling, which is
written when the go plans and queues, so the name in the plan is the name on
the account, and a second go the same day lands in the same playlist.

HEARD is the per label ``heard`` list of release identifiers in that record,
written only by ``crate label heard`` (U123, :mod:`cratekit.label.heard`); an
absent list is nothing heard. Nothing here writes the record.

THE YEAR PLAYLIST IS LEFT AS IT IS. The dated playlist is one more playlist in
the label's folder, reused by its exact name, and only ever added to. No merge
into the year and no removal happen here; ``label heard`` does both. A dated
playlist older than ``labels.new_playlist_age_days`` is reported and nothing
moves.

ONE THIS PLAN CREATES IS RECORDED IN THE OUTBOUND LEDGER (U123), the ledger's
lock taken before the create, because a removal is asked of a playlist the
ledger vouches for and of no other. One reused by its name is never recorded.

A WRITE THE ACCOUNT REFUSES PART WAY is raised naming what was written first,
and the next plan finds the dated playlist by its name and adds only the rest.

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.label import sync_cli
from cratekit.modules.outbound import folders, ledger

_ORIGIN = ("label.dated",)

#: The answers that take releases, the go's own.
TAKING = frozenset({sync_cli.ALL, sync_cli.PICK})

#: The per label key in ``label_sync.json`` read as the releases heard.
HEARD = "heard"

CREATE = folders.CREATE
REUSE = folders.REUSE
AMBIGUOUS = folders.AMBIGUOUS

#: How many tracks one add carries, the year build's own chunk.
CHUNK = folders.CHUNK


def dated_name(label: str, year: str, day: str) -> str:
    """The dated playlist's title, ``<Label> <year> new <YYYY-MM-DD>``."""
    return f"{folders.year_name(label, year)} new {day}"


def _pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"^{re.escape(label)} (\d{{4}}) new (\d{{4}}-\d{{2}}-\d{{2}})$")


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
    """Every release a go took for the label, mapped to the day the go took it.

    A release taken by two goes keeps the first day, so it is filed once.
    """
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
            held = days.get(identity)
            if held is None or day < held:
                days[identity] = day
    return days


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
        items: list[dict[str, Any]] = [
            {
                "id": step.remote_id,
                "kind": "playlist",
                "year": step.year,
                "date": step.day,
                "name": step.name,
                "action": step.action,
                "add": len(step.add),
                "tracks": step.tracks,
                **({"why": step.why} if step.why else {}),
            }
            for step in self.steps
        ]
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
    #: Each created dated playlist's identifier by its name, recorded the
    #: moment the create returns, before the move into the folder.
    ids: dict[str, str] = field(default_factory=dict)
    #: Created playlists not yet in the label's folder.
    unplaced: list[str] = field(default_factory=list)
    added: dict[str, int] = field(default_factory=dict)
    refused: dict[str, int] = field(default_factory=dict)


def _aged(
    label: str, inside: Mapping[str, str], today: date, limit: int
) -> tuple[Aged, ...]:
    pattern = _pattern(label)
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
    """Decide each dated playlist against the record and the account.

    ``folder_id`` is the label's folder as the year plan decided it, empty
    when that plan creates the folder, in which case every dated playlist is
    created once the folder exists.
    """
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
        # ONLY WHAT THE YEAR PATH WOULD ASK FOR. ``by_release`` carries every
        # track, playable or not, for the prune; ``years`` holds only the ones
        # the provider will play. A track it will not play would be refused
        # on every add, so the step would read planned on every run.
        playable = set(catalogue.years.get(year, ()))
        held = wanted.setdefault((year, day), [])
        held.extend(one for one in tracks if one in playable and one not in held)

    inside = account.folder_playlists(folder_id) if folder_id else {}
    steps: list[DatedStep] = []
    for (year, day), tracks in sorted(wanted.items()):
        name = dated_name(catalogue.name, year, day)
        matching = sorted(pid for pid, title in inside.items() if title == name)
        if len(matching) > 1:
            steps.append(
                DatedStep(
                    year=year,
                    day=day,
                    name=name,
                    action=AMBIGUOUS,
                    tracks=len(tracks),
                    why=(
                        f"the folder holds {len(matching)} playlists named {name!r}, "
                        f"so which one is the dated playlist is not something a name decides"
                    ),
                )
            )
            continue
        if matching:
            have = set(account.playlist_tracks(matching[0]))
            steps.append(
                DatedStep(
                    year=year,
                    day=day,
                    name=name,
                    action=REUSE,
                    remote_id=matching[0],
                    add=tuple(one for one in tracks if one not in have),
                    tracks=len(tracks),
                )
            )
            continue
        steps.append(
            DatedStep(year=year, day=day, name=name, action=CREATE, add=tuple(tracks), tracks=len(tracks))
        )
    return DatedPlan(
        label_id=catalogue.label_id,
        label=catalogue.name,
        folder_id=folder_id,
        steps=tuple(steps),
        aged=_aged(catalogue.name, inside, today, cfg.labels.new_playlist_age_days),
        left_out={key: value for key, value in left_out.items() if value},
    )


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


def _failed_part_way(exc: Exception, done: DatedApplied, planned: DatedPlan) -> CratekitError:
    """The failure, with what was already written named in it."""
    if done.created or done.added:
        wrote = (
            f"before this failed {len(done.created)} dated playlist(s) were created "
            f"and {sum(done.added.values())} track(s) added"
        )
    else:
        wrote = "nothing was written before this failed"
    detail = {
        "label_id": planned.label_id,
        "created": list(done.created),
        "ids": dict(done.ids),
        "unplaced": [[name, done.ids[name]] for name in done.unplaced],
        "added": dict(done.added),
    }
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
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{wrote}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.RUN,
            retryable=cause.retryable,
            origin=_ORIGIN,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    return refuse(
        "internal-error",
        f"{wrote}. The dated playlists failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        steps=(again,),
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={**detail, "kind": type(exc).__name__},
    )


def apply(cfg: config.Config, account, planned: DatedPlan) -> DatedApplied:
    """Make and fill what the plan names, or raise naming what was written first."""
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
                # VOUCHED FOR IN THE LEDGER AS IT IS MADE (U123), the lock
                # taken before the create, so ``label heard`` may remove it.
                remote_id = ledger.reserve_label_dated(
                    cfg,
                    planned.label_id,
                    step.name,
                    lambda name=step.name: account.create_playlist(name),
                )
                # RECORDED BEFORE THE MOVE, so a refusal between the two
                # names the playlist now at the account root and its id.
                done.created.append(step.name)
                done.ids[step.name] = remote_id
                done.unplaced.append(step.name)
                account.move_to_folder(remote_id, folder_id)
                done.unplaced = [one for one in done.unplaced if one != step.name]
            for start in range(0, len(step.add), CHUNK):
                chunk = step.add[start : start + CHUNK]
                held = set(account.add_tracks(remote_id, chunk))
                added = sum(1 for one in chunk if one in held)
                done.added[step.name] = done.added.get(step.name, 0) + added
                if added < len(chunk):
                    done.refused[step.name] = done.refused.get(step.name, 0) + len(chunk) - added
    except Exception as exc:
        raise _failed_part_way(exc, done, planned) from exc
    return done


def add_step(cfg, area, entry, year_plan: folders.Plan, remote_of) -> None:
    """Append the label's dated playlist step to ``crate organize``'s account area.

    The one call ``organize``'s label step makes (U117). A record or an
    account that cannot be read refuses this step alone.
    """
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
        said.append(
            f"create {totals['create']} dated playlist(s) and add {totals['add']} track(s)"
        )
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
                step.warnings.append(
                    {
                        "code": "label-new-playlists-tracks-refused",
                        "message": (
                            f"the provider would not add {sum(done.refused.values())} "
                            f"track(s) to {len(done.refused)} dated playlist(s)"
                        ),
                    }
                )
            return {
                "created": list(done.created),
                "ids": dict(done.ids),
                "added": dict(done.added),
                "refused": dict(done.refused),
            }

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
