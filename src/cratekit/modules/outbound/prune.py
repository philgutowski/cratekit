"""Taking tracks off a playlist this product made on the account (R-836).

The account protocol's one removal, ``remove_tracks``, planned and applied,
from two kinds of playlist only: a label year playlist ``label playlists``
CREATED, for a release the genre gate now holds, the catalogue no longer
confirms, or a track ``crate delete review`` removed (U243); and a playlist
``export playlist`` made, for a track no longer in its library playlist.

ITS OWN VERBS (R-836), since both builders promise on their gates never to take
anything away, and a removal folded into the export job would change its digest
and its resume.

ONLY WHAT THE LEDGER SAYS THE PRODUCT PUT THERE, from a playlist
``ledger.product_made`` vouches for, so a person's track or a playlist adopted
by its name is left and said. A track held more than once is left too, since
this product never adds a member twice.

ABSENCE IS NEVER THE EVIDENCE. A label year track leaves only when a release the
read REACHED says so (held, credited to another label, or under a tombstone,
U243), since an empty or short read looks exactly like a catalogue that moved.

THE PLAN READS AND WRITES NOTHING. The apply records each chunk as it lands, so
a refusal part way resumes without taking anything off twice. Nothing here
removes a playlist, a folder or a heart: one the plan empties is said and kept.

Layer: modules.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound.folders import LabelCatalogue
from cratekit.modules.outbound.service import RemoteAccount

_ORIGIN = ("outbound", "prune")

#: What a plan prunes: a label's year playlists, or one exported playlist.
LABEL = "label-prune"
EXPORTED = "export-prune"

#: How many tracks one removal carries, so each is recorded as it lands.
CHUNK = 50


@dataclass(frozen=True, slots=True)
class Taken:
    """One track the plan takes off, as a person reads it on the gate."""

    remote_id: str
    artist: str = ""
    title: str = ""

    def said(self) -> str:
        return f"{self.artist or 'unknown artist'} - {self.title or f'track {self.remote_id}'}"


@dataclass(frozen=True, slots=True)
class PlaylistPrune:
    """What the plan does to one playlist the ledger records."""

    #: The year, for a label year playlist, or the library playlist's key.
    key: str
    name: str
    remote_id: str
    take: tuple[Taken, ...] = ()
    #: Tracks that should leave and are already off it, recorded with no call
    #: to take them off: a removal before a failure, or a person's own.
    settle: tuple[str, ...] = ()
    #: Tracks that should leave and are on it more than once: a person's copy.
    twice: tuple[str, ...] = ()
    #: Why the playlist is left alone, when it is, taking nothing off.
    why: str = ""
    #: How many tracks would leave a playlist left alone, for the sentence.
    would: int = 0
    #: Every track on it is taken off: said, never acted on (U243).
    empties: bool = False

    @property
    def writes(self) -> bool:
        return bool(self.take or self.settle) and not self.why


@dataclass(frozen=True, slots=True)
class Plan:
    """Every playlist the gate is asked over, decided against the account as it is."""

    kind: str
    #: The label's registry identifier, or the exported playlist's key.
    subject: str
    playlists: tuple[PlaylistPrune, ...] = ()
    #: What the plan could not judge, said on the gate rather than hidden.
    notes: tuple[str, ...] = ()

    @property
    def writes(self) -> bool:
        return any(one.writes for one in self.playlists)

    def identity(self) -> dict[str, Any]:
        """What the digest is taken over: every track taken off, and from where."""
        return {
            "kind": self.kind,
            "subject": self.subject,
            "playlists": [
                [
                    one.key,
                    one.remote_id,
                    sorted(taken.remote_id for taken in one.take),
                    sorted(one.settle),
                ]
                for one in self.playlists
                if one.writes
            ],
        }


@dataclass
class Pruned:
    """What an apply took off, by remote playlist, for the report and a failure."""

    taken: dict[str, list[str]] = field(default_factory=dict)
    #: Tracks recorded as taken off that were already off the playlist.
    settled: dict[str, list[str]] = field(default_factory=dict)

    @property
    def count(self) -> int:
        return sum(len(ids) for ids in self.taken.values())


def _incomplete(subject: str, what: str) -> CratekitError:
    return refuse(
        "internal-error",
        f"the prune of {subject!r} was handed a catalogue that does not say which tracks each "
        f"release holds ({what}), so nothing was planned and nothing was taken off",
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={"subject": subject},
    )


def _step(
    account: RemoteAccount, key: str, name: str, remote_id: str, leaving: Iterable[str]
) -> PlaylistPrune | None:
    """One playlist's step from the tracks that should leave it, read against it.

    On it once is taken off, more than once left alone, no longer on it
    settled; None when there is nothing to say. One that could not be read is
    left alone, said.
    """
    wanted = sorted(set(leaving))
    if not wanted:
        return None
    try:
        names = account.track_names(remote_id)
        order = account.playlist_tracks(remote_id)
    except CratekitError as exc:
        if exc.cause.reason != "unavailable-transient":
            raise
        why = f"the playlist could not be read, so nothing is taken off it: {exc.cause.message}"
        return PlaylistPrune(key, name, remote_id, why=why, would=len(wanted))
    copies = Counter(order)
    asked = set(wanted)
    take = tuple(
        Taken(remote_id=one, artist=artist, title=title)
        for one, (artist, title) in names.items()
        if one in asked and copies[one] == 1
    )
    return PlaylistPrune(
        key,
        name,
        remote_id,
        take=take,
        settle=tuple(one for one in wanted if one not in names and copies[one] == 0),
        twice=tuple(one for one in wanted if copies[one] > 1),
        # EMPTIED is read off the playlist as it is, so one holding nothing to
        # begin with is not one the plan empties.
        empties=bool(take) and set(order) <= {one.remote_id for one in take},
    )


def plan_label(
    cfg: config.Config,
    catalogue: LabelCatalogue,
    held: Iterable[str],
    account: RemoteAccount,
    *,
    tracks_of: Callable[[str], tuple[str, ...]] | None = None,
) -> Plan:
    """What leaves each year playlist this product created for one label.

    ``held`` is the releases the genre gate holds for the label; ``tracks_of``
    reads a held or mismatched release's tracks the catalogue did not, asked
    only while a recorded track is still unexplained.

    A TRACK LEAVES A YEAR the ledger records it as added to when no kept
    release of that year or of no year carries it and a release the read
    reached says it should go: one the gate holds, or one the verifier credits
    to another label, judged only when every confirmed release was read. A
    tombstoned track (U243) leaves whatever keeps it, the person's removal
    asking louder than the kept release.
    """
    if len(catalogue.by_release) + catalogue.gone != catalogue.releases:
        raise _incomplete(
            catalogue.label_id,
            f"{catalogue.releases} release(s) confirmed, {len(catalogue.by_release)} "
            f"with their tracks and {catalogue.gone} gone",
        )
    holding = set(held)
    taken_away = set(catalogue.tombstoned)
    judged = catalogue.gone == 0
    kept: dict[str, set[str]] = {}
    undated: set[str] = set()
    on_held: set[str] = set()
    for release_id, (year, tracks) in catalogue.by_release.items():
        if release_id in holding:
            on_held.update(tracks)
        elif year:
            kept.setdefault(year, set()).update(tracks)
        else:
            undated.update(tracks)
    on_other: set[str] = set()
    shape = ledger.label_shape(cfg, catalogue.label_id)

    def staying(year: str) -> set[str]:
        return kept.get(year, set()) | undated

    # ON NO RELEASE THE READ REACHED is judged against every kept release of
    # any year, so a re-dated release is not read as unreached.
    anywhere = undated.union(*kept.values())
    unexplained = {
        one
        for recorded in shape.years.values()
        for one in recorded.added
        if one not in anywhere and one not in on_held
    }
    unread = sorted(holding - set(catalogue.by_release))
    if judged:
        unread += sorted(set(catalogue.mismatched) - set(catalogue.by_release))
    for release_id in unread:
        if tracks_of is None or not unexplained:
            break
        tracks = set(tracks_of(release_id))
        (on_held if release_id in holding else on_other).update(tracks)
        unexplained -= tracks
    notes: list[str] = []
    if not judged:
        notes.append(
            f"{catalogue.gone} confirmed release(s) the provider no longer has, so a "
            f"release credited to another label is not judged and only the tracks "
            f"of held releases, and tracks removed from the library, are taken off"
        )
    if unexplained:
        notes.append(
            f"{len(unexplained)} recorded track(s) are on no release this read reached, and a "
            f"release the read did not reach is not evidence, so they stay"
        )
    steps: list[PlaylistPrune] = []
    for year in sorted(shape.years):
        recorded = shape.years[year]
        # ``on_other`` holds only what was read while ``judged``.
        leaving = [
            one
            for one in sorted(recorded.added)
            if one in taken_away
            or (one not in staying(year) and (one in on_held or one in on_other))
        ]
        if not leaving:
            continue
        name = recorded.name or year
        if recorded.created is not True:
            why = (
                "this product adopted the playlist rather than creating it, so "
                "nothing is taken off it"
                if recorded.created is False
                else "the record of this playlist predates the one that says whether "
                "this product made it, so nothing is taken off it"
            )
            steps.append(PlaylistPrune(year, name, recorded.remote_id, why=why, would=len(leaving)))
            continue
        step = _step(account, year, name, recorded.remote_id, leaving)
        if step is not None and (step.take or step.settle or step.twice or step.why):
            steps.append(step)
    return Plan(kind=LABEL, subject=catalogue.label_id, playlists=tuple(steps), notes=tuple(notes))


def plan_export(
    cfg: config.Config,
    playlist_key: str,
    name: str,
    crate: Iterable[str],
    wanted: Iterable[str],
    unmatched: int,
    account: RemoteAccount | None,
    *,
    older: str = "",
) -> Plan:
    """What leaves the remote playlist one library playlist was exported to.

    ``crate`` is the library playlist's rows now, ``wanted`` the remote tracks
    they match now, ``unmatched`` how many matched none. A recorded track
    leaves BY ITS ROW when the row it was written from left and no row matches
    it, or, written before rows were kept, BY MATCH ALONE when no row matches
    it, which is weak evidence: then a row matching nothing, or matching a
    track never written, leaves the playlist alone. So does an export ``older``
    than the one it was last written from, since every row added since would
    read as gone.
    """
    record = ledger.exported_playlist(cfg, playlist_key)
    if record is None:
        return Plan(
            kind=EXPORTED,
            subject=playlist_key,
            notes=(
                f"{playlist_key!r} has no remote playlist recorded under this path, "
                f"so there is nothing to take off",
            ),
        )
    rows_now = set(crate)
    matched_now = set(wanted)
    staying = matched_now | {one for row, one in record.rows.items() if row in rows_now}
    by_row = set(record.rows.values())
    leaving = [one for one in sorted(record.added) if one not in staying]
    unrowed = [one for one in leaving if one not in by_row]
    if not leaving:
        return Plan(kind=EXPORTED, subject=playlist_key)
    fresh = matched_now - record.added - record.pruned
    why = ""
    if older:
        why = (
            f"this collection export is older than the one the playlist was last written from, on "
            f"{older}, so a track added since would read as gone; export the collection again"
        )
    elif unrowed and unmatched:
        why = (
            f"{unmatched} row(s) of the library playlist matched no track on the "
            f"account, so which recorded tracks left it cannot be told"
        )
    elif unrowed and fresh:
        why = (
            f"{len(fresh)} row(s) of the library playlist match a track this playlist was never "
            f"written with, so a match may have moved; export the playlist first, then prune"
        )
    if why or account is None:
        why = why or "no account was opened to read the playlist"
        step = PlaylistPrune(playlist_key, name, record.remote_id, why=why, would=len(leaving))
    else:
        step = _step(account, playlist_key, name, record.remote_id, leaving)
    return Plan(kind=EXPORTED, subject=playlist_key, playlists=(step,) if step is not None else ())


def _not_made(remote_id: str) -> CratekitError:
    return refuse(
        "outbound-remove-refused",
        f"the outbound ledger no longer records the playlist {remote_id} as one this "
        f"product created, so no track was taken off it",
        steps=("run the prune again, so its plan is built against the ledger as it is",),
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={"playlist_id": remote_id, "problem": "not-product-made"},
    )


def apply(cfg: config.Config, account: RemoteAccount, planned: Plan, done: Pruned) -> Pruned:
    """Take the planned tracks off, recording each chunk as it lands, into ``done``.

    ``done`` is the caller's, so a raise part way leaves in it what was taken
    off. The ledger is asked again before each playlist, since the plan was
    read in another invocation.
    """
    for step in planned.playlists:
        if not step.writes:
            continue
        if not ledger.product_made(cfg, step.remote_id):
            raise _not_made(step.remote_id)
        # A SETTLED TRACK GOES THROUGH THE REMOVAL TOO, so the adapter's full
        # read vouches that it is off: the listing leaves out a track the
        # account cannot play, which the plan's word alone would call gone.
        settling = set(step.settle)
        ids = [taken.remote_id for taken in step.take] + list(step.settle)
        for start in range(0, len(ids), CHUNK):
            chunk = tuple(ids[start : start + CHUNK])
            gone = set(account.remove_tracks(step.remote_id, chunk))
            unsaid = [one for one in chunk if one not in gone]
            if unsaid:
                raise refuse(
                    "internal-error",
                    f"the account answered a removal from {step.remote_id} without "
                    f"saying {len(unsaid)} asked track(s) are off it, so they are not "
                    f"recorded as taken off",
                    scope=Scope.RUN,
                    origin=_ORIGIN,
                    detail={"playlist_id": step.remote_id, "unsaid": unsaid},
                )
            if planned.kind == LABEL:
                ledger.record_label_pruned(cfg, planned.subject, step.key, chunk)
            else:
                ledger.record_playlist_pruned(cfg, step.key, chunk)
            for one in chunk:
                held = done.settled if one in settling else done.taken
                held.setdefault(step.remote_id, []).append(one)
    return done


def payload(
    planned: Plan | None, *, kind: str, subject: str, digest: Callable[[Any], str]
) -> dict[str, Any]:
    """The ``plan/1`` payload the gate is asked over: one item per track taken off.

    ``digest`` is the CLI layer's, handed in so this module imports nothing from it.
    """
    identity = planned.identity() if planned is not None else {"kind": kind, "subject": subject}
    steps = planned.playlists if planned is not None else ()
    items: list[dict[str, Any]] = []
    for step in steps:
        if step.why:
            items.append(
                {
                    "id": step.remote_id,
                    "kind": "playlist",
                    "key": step.key,
                    "name": step.name,
                    "action": "left-alone",
                    "why": step.why,
                    "would": step.would,
                }
            )
            continue
        at = {"kind": "track", "playlist": step.remote_id, "key": step.key, "name": step.name}
        items.extend(
            {
                "id": one.remote_id,
                **at,
                "action": "take-off",
                "artist": one.artist,
                "title": one.title,
            }
            for one in step.take
        )
        items.extend({"id": one, **at, "action": "already-off"} for one in step.settle)
        twice = "on the playlist more than once, and a second copy is a person's"
        items.extend({"id": one, **at, "action": "left-alone", "why": twice} for one in step.twice)
    return {
        "digest": digest(identity),
        "items": items,
        "totals": {
            "count": len(items),
            "take_off": sum(1 for item in items if item["action"] == "take-off"),
            "writes": bool(planned is not None and planned.writes),
            # SAID AND NOT A WRITE, so outside the digest.
            "emptied": [step.name for step in steps if step.empties and not step.why],
        },
        "chunk": None,
    }


def shown(planned: Plan) -> dict[str, Any]:
    """What the gate screen says: every track taken off, by artist and title, per playlist."""
    lists: dict[str, Any] = {}
    for step in planned.playlists:
        if step.why:
            lists[step.name] = f"left alone, {step.why} ({step.would} track(s) would leave)"
            continue
        lines: list[str] = [taken.said() for taken in step.take]
        if step.settle:
            lines.append(
                f"and {len(step.settle)} track(s) already off the playlist, recorded as taken off"
            )
        if step.twice:
            lines.append(
                f"and {len(step.twice)} track(s) on the playlist more than once, left alone"
            )
        if step.empties:
            lines.append(
                "and the playlist is left empty; it stays on the account, since a "
                "prune never removes a playlist"
            )
        lists[step.name] = lines
    said: dict[str, Any] = {
        "take off": lists or "nothing: every playlist already holds only what it should",
        "removes only": (
            "tracks this product added, from playlists this product created; never a "
            "playlist, a folder, a heart, or a track from any other playlist"
        ),
    }
    if planned.notes:
        said["not judged"] = list(planned.notes)
    return said


def report(done: Pruned, names: Mapping[str, str]) -> dict[str, Any]:
    """What an apply took off, by playlist name, for the totals."""
    return {names.get(remote, remote): list(ids) for remote, ids in done.taken.items()}


def failed_part_way(
    exc: Exception, done: Pruned, *, origin: tuple[str, ...], again: str
) -> CratekitError:
    """The failure, with what was already taken off named in it.

    A refusal the account raised keeps its reason and remedy, and anything
    else is this build's own defect and says so. What was taken off is
    recorded already, so a run started again plans the rest.
    """
    wrote = (
        f"before this failed {done.count} track(s) were taken off and recorded"
        if done.count
        else "no track was recorded as taken off before this failed"
    )
    detail = {"taken": {remote: list(ids) for remote, ids in done.taken.items()}}
    if isinstance(exc, CratekitError):
        cause = exc.cause
        # A READ BACK THAT DIFFERED says to look by hand first, which "run it
        # again" beside it would undo.
        differed = cause.detail.get("problem") == "read-back-differs"
        return refuse(
            cause.reason,
            f"{wrote}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=cause.remediation.steps if differed else (*cause.remediation.steps, again),
            scope=Scope.RUN,
            retryable=cause.retryable,
            origin=origin,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    return refuse(
        "internal-error",
        f"{wrote}. The prune failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.RUN,
        origin=origin,
        detail={**detail, "kind": type(exc).__name__},
    )


def finished(ctx, payload: dict[str, Any], planned: Plan, done: Pruned) -> Any:
    """The envelope of an apply, with what was taken off riding on the totals."""
    names = {step.remote_id: step.name for step in planned.playlists}
    applied = {
        "taken": report(done, names),
        "settled": {names.get(remote, remote): list(ids) for remote, ids in done.settled.items()},
    }
    totals = {**payload["totals"], "applied": applied}
    return ctx.envelope(data={**payload, "totals": totals}, outcome=Outcome.OK)


def settle(
    ctx,
    cfg: config.Config,
    account: RemoteAccount,
    payload: dict[str, Any],
    planned: Plan,
    *,
    option: str,
    origin: Sequence[str],
    again: str,
) -> Any:
    """Apply an approved prune and report it, or report the plan alone.

    The tail ``export prune`` and ``label prune`` share; ``again`` is the
    command a person runs after a failure part way.
    """
    if option != "apply" or not planned.writes:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    done = Pruned()
    try:
        apply(cfg, account, planned, done)
    except Exception as exc:
        raise failed_part_way(exc, done, origin=origin, again=again) from exc
    return finished(ctx, payload, planned, done)


__all__ = [
    "CHUNK", "EXPORTED", "LABEL", "Plan", "PlaylistPrune", "Pruned", "Taken", "apply",
    "failed_part_way", "finished", "settle", "payload", "plan_export", "plan_label", "report",
    "shown",
]
