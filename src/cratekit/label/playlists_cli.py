"""``label.playlists``: a followed label as a folder of year playlists (R-835).

The source system's label shape on the account, kept once it retires: one
``<Label>`` folder holding one private ``<Label> <year>`` playlist per release
year, each filled with that year's tracks from the label's catalogue. This verb
plans that shape, shows it at one explicit gate, and on ``apply`` builds what is
missing. It adds and never removes, and a second run over an unchanged
catalogue plans nothing to write.

THE CATALOGUE IS THE ONE THE PRODUCT ALREADY CRAWLS. The roster, the release
listing, the tombstone question and the verifier are the label sweep's own,
through :func:`cratekit.label.sweep.confirmed_releases`, and each release's
tracks are read through :class:`cratekit.label.catalogue.ReleaseTracks`. Every
call passes the provider gate's pacing, since both the catalogue and the
account are built over the gated session. Nothing here is a second crawler.

A CATALOGUE READ IN PART IS REFUSED BEFORE THE GATE, ``label-playlists-
incomplete``. A plan built from half a label would be shown as the label, and
the person approving it could not tell. A release the provider no longer has
is the provider answering, and is counted rather than refused.

A LABEL THAT IS NOT FOLLOWED IS A PLAN OF NOTHING, still gated, decided before
a credential is asked for, on ``sync unmark``'s precedent. It ends NO_OP under
a warning that says why.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.label import catalogue, sweep
from cratekit.label import cli as label_cli
from cratekit.label import registry as labels
from cratekit.modules.outbound import folders
from cratekit.sync import run

_ORIGIN = ("label.playlists",)

#: What the gate screen and the warning say about a label nobody follows.
NOT_FOLLOWED_SAID = (
    "no followed label goes by this name, so there is no catalogue to build a "
    "folder from"
)


def build_playlists(parser, entry) -> None:
    del entry
    parser.add_argument(
        "name",
        metavar="LABEL",
        help="a followed label, by its name or its registry identifier",
    )
    parser.set_defaults(_handler=label_playlists)


def incomplete(entry: labels.LabelEntry, what: str) -> CratekitError:
    return refuse(
        "label-playlists-incomplete",
        f"the catalogue of {entry.name!r} was not read in full ({what}), so no plan "
        f"was made from it and nothing was written to the account",
        steps=("run it again once the provider is answering",),
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={"label_id": entry.label_id},
    )


def _year(stated: Any, release: Any) -> str:
    """The release's year: the provider's own dating of it, else the listing's."""
    if isinstance(stated, int) and stated > 0:
        return f"{stated:04d}"
    listed = sweep.year_of(release)
    return listed if len(listed) == 4 and listed.isdigit() else ""


def _id(row: Any) -> str:
    return str(getattr(row, "id", "") or "")


def read_catalogue(
    cfg, entry: labels.LabelEntry, found: catalogue.Catalogue
) -> folders.LabelCatalogue:
    """The label's confirmed catalogue, grouped by year, or the refusal."""
    try:
        confirmed = sweep.confirmed_releases(cfg, entry, found)
    except run.LookupFailure as exc:
        raise incomplete(entry, str(exc)) from exc
    if confirmed.unread:
        raise incomplete(
            entry,
            "; ".join(f"{one.artist} ({one.listing}: {one.reason})" for one in confirmed.unread),
        )
    # A CATALOGUE THAT CONFIRMS NOTHING IS NOT A LABEL WITH NOTHING ON IT, the
    # sweep worker's own refusal (``label.cli._refuse_unfinished``): releases
    # were read and the verifier would vouch for none, which is what a degraded
    # credit endpoint answers. Shown, it would be an empty folder under the
    # label's name, approved as the label.
    if confirmed.dropped and not confirmed.releases:
        raise incomplete(
            entry,
            f"{len(confirmed.dropped)} release(s) were read and the catalogue "
            f"confirmed none of them as the label's",
        )
    tracks = catalogue.ReleaseTracks(found)
    years: dict[str, list[str]] = {}
    by_release: dict[str, tuple[str, tuple[str, ...]]] = {}
    undated = gone = 0
    for release in confirmed.releases:
        release_id = str(getattr(release, "id", "") or "")
        try:
            rows, stated = tracks.release_tracks(release_id)
        except catalogue.ReleaseUnresolvable:
            gone += 1
            continue
        except CratekitError:
            raise
        except Exception as exc:  # noqa: BLE001 - refused, never swallowed
            raise incomplete(
                entry,
                f"the tracks of the release {release_id} could not be read "
                f"({type(exc).__name__}: {exc})",
            ) from exc
        year = _year(stated, release)
        # EVERY TRACK the release carries, playable or not, is what the prune
        # reads as still the label's (R-836): a track that stopped playing is
        # still on a release the catalogue confirms.
        by_release[release_id] = (
            year,
            tuple(dict.fromkeys(_id(row) for row in rows if _id(row))),
        )
        if not year:
            undated += 1
            continue
        held = years.setdefault(year, [])
        for row in rows:
            identifier = _id(row)
            # A TRACK THE PROVIDER WILL NOT PLAY is never asked for, since the
            # client skips it on an add and it would be refused every run.
            if identifier and getattr(row, "available", True) is not False:
                if identifier not in held:
                    held.append(identifier)
    return folders.LabelCatalogue(
        label_id=entry.label_id,
        name=entry.name,
        years={year: tuple(ids) for year, ids in years.items()},
        releases=len(confirmed.releases),
        undated=undated,
        dropped=len(confirmed.dropped),
        gone=gone,
        suppressed=confirmed.suppressed,
        by_release=by_release,
        # A VERDICT OF MISMATCH IS THE CATALOGUE SAYING ANOTHER LABEL, which is
        # what "no longer confirms" means to the prune. "unconfirmed" is no
        # credit found, an absence, and is not evidence of anything (R-836).
        mismatched=tuple(one.identity for one in confirmed.dropped if one.reason == "mismatch"),
    )


def _items(planned: folders.Plan | None) -> list[dict[str, Any]]:
    if planned is None:
        return []
    items: list[dict[str, Any]] = [
        {
            "id": planned.folder_id,
            "kind": "folder",
            "name": planned.catalogue.name,
            "action": planned.folder_action,
        }
    ]
    for step in planned.years:
        items.append(
            {
                "id": step.remote_id,
                "kind": "playlist",
                "year": step.year,
                "name": step.name,
                "action": step.action,
                "move": step.move,
                "add": len(step.add),
                "tracks": step.tracks,
                **({"why": step.why} if step.why else {}),
            }
        )
    return items


def _payload(planned: folders.Plan | None, *, name: str) -> dict[str, Any]:
    identity = planned.identity() if planned is not None else {"kind": "label-playlists", "label": name}
    items = _items(planned)
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {
            "count": len(items),
            "create": sum(1 for item in items if item["action"] == folders.CREATE),
            "add": sum(int(item.get("add") or 0) for item in items),
            "writes": bool(planned is not None and planned.writes),
        },
        "chunk": None,
    }


def _line(step: folders.YearStep) -> str:
    if step.action in (folders.AMBIGUOUS, folders.UNREADABLE):
        return f"{step.name}: left alone, {step.why}"
    doing = {
        folders.CREATE: "create it private",
        folders.ADOPT: "use the one already in the folder",
        folders.REUSE: "use the one already built",
    }[step.action]
    parts = [doing]
    if step.move or step.action == folders.CREATE:
        parts.append("put it in the folder")
    parts.append(f"add {len(step.add)} of {step.tracks} track(s)")
    return f"{step.name}: " + ", ".join(parts)


def _shown(planned: folders.Plan | None, *, name: str) -> dict[str, Any]:
    if planned is None:
        return {"label": name, "nothing to build": NOT_FOLLOWED_SAID}
    read = planned.catalogue
    folder = {
        folders.CREATE: "create it",
        folders.ADOPT: "use the one already on the account under this name",
        folders.REUSE: "use the one already built",
    }[planned.folder_action]
    shown: dict[str, Any] = {
        "label": read.name,
        "folder": f"{read.name}: {folder}",
        "year playlists": [_line(step) for step in planned.years],
        "catalogue": (
            f"{read.releases} confirmed release(s) read; left out {read.undated} with "
            f"no year, {read.dropped} the catalogue did not confirm as the label's, "
            f"{read.gone} the provider no longer has, {read.suppressed} deleted on purpose"
        ),
        "removes": "nothing, ever: no track, playlist or folder is taken away",
    }
    if planned.stale_folder:
        shown["recorded folder"] = (
            f"the folder recorded for this label, {planned.stale_folder}, is no longer "
            f"on the account, so its record is replaced"
        )
    if not planned.writes:
        shown["nothing to write"] = "the account already holds every year and track planned"
    return shown


def _failed_part_way(
    exc: Exception, done: folders.Applied, planned: folders.Plan
) -> CratekitError:
    """The failure, with what was already written named in it.

    ``sync unmark``'s rule: a refusal the account raised keeps its reason and
    remedy, and anything else is this build's own defect and says so. What was
    written is recorded already, so a run started again plans only the rest.
    """
    wrote = (
        f"before this failed the folder was {'created' if done.folder_created else 'in hand'}"
        if done.folder_id
        else "nothing was written before this failed"
    )
    if done.created or done.added:
        wrote += (
            f", {len(done.created)} year playlist(s) were created and "
            f"{sum(done.added.values())} track(s) added"
        )
    detail = {
        "label_id": planned.catalogue.label_id,
        "folder_id": done.folder_id,
        "created": list(done.created),
        "moved": list(done.moved),
        "added": dict(done.added),
    }
    again = "run crate label playlists again; what was written is reused, never made twice"
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
        f"{wrote}. The build failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={**detail, "kind": type(exc).__name__},
    )


def plan_label(cfg, entry: labels.LabelEntry, found: catalogue.Catalogue, remote) -> folders.Plan:
    """One followed label's plan against the account as it is, or its refusal.

    PUBLIC FOR ``crate organize`` (U112), which plans every followed label
    through this one body, so a label is planned there exactly as here.
    """
    return folders.plan(cfg, read_catalogue(cfg, entry, found), remote)


def refused_warnings(done: folders.Applied) -> list[dict[str, str]]:
    """What an apply says about tracks the provider would not add."""
    if not done.refused:
        return []
    return [
        {
            "code": "label-playlists-tracks-refused",
            "message": (
                f"the provider would not add {sum(done.refused.values())} track(s) "
                f"to {len(done.refused)} year playlist(s); they are recorded and "
                f"not asked for again"
            ),
        }
    ]


def apply_plan(cfg, remote, planned: folders.Plan) -> folders.Applied:
    """Build what one label's plan names, or raise naming what was written first.

    Public for ``crate organize`` (U112), for :func:`plan_label`'s reason.
    """
    done = folders.Applied()
    try:
        folders.apply(cfg, remote, planned, done)
    except Exception as exc:
        raise _failed_part_way(exc, done, planned) from exc
    return done


def applied_totals(done: folders.Applied) -> dict[str, Any]:
    """What was written, as the totals carry it."""
    return {
        "folder_id": done.folder_id,
        "folder_created": done.folder_created,
        "created": list(done.created),
        "moved": list(done.moved),
        "added": dict(done.added),
        "refused": dict(done.refused),
    }


#: Public for ``crate organize`` (U112), whose label step shows these items.
plan_payload = _payload


def label_playlists(ctx) -> Envelope:
    cfg = label_cli._load()
    name = str(ctx.args.name)
    entry = labels.RegistryStore().load().resolve(name)
    planned: folders.Plan | None = None
    remote = None
    if entry is not None:
        from cratekit.modules.outbound import account

        found = catalogue.resolve(cfg)
        read = read_catalogue(cfg, entry, found)
        remote = account.resolve(cfg)
        planned = folders.plan(cfg, read, remote)
    payload = _payload(planned, name=name)
    # THE PLAN ITSELF, so the screen shows every item the digest covers
    # (R-693), with the year by year sentences as the facts in front of them.
    option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=_shown(planned, name=name))
    if planned is None:
        return ctx.envelope(
            data=payload,
            outcome=Outcome.NO_OP,
            warnings=[
                {"code": "label-playlists-not-followed", "message": f"{name}: {NOT_FOLLOWED_SAID}"}
            ],
        )
    if option != "apply" or not planned.writes:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)

    done = apply_plan(cfg, remote, planned)
    # WHAT WAS WRITTEN RIDES ON THE TOTALS, since ``plan/1`` admits no other
    # key at the top of the payload.
    totals = {**payload["totals"], "applied": applied_totals(done)}
    return ctx.envelope(
        data={**payload, "totals": totals}, outcome=Outcome.OK, warnings=refused_warnings(done)
    )


__all__ = [
    "applied_totals",
    "apply_plan",
    "build_playlists",
    "incomplete",
    "label_playlists",
    "plan_label",
    "plan_payload",
    "read_catalogue",
    "refused_warnings",
]
