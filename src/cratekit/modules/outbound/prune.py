"""Taking tracks off a playlist this product made on the account (R-836).

The account protocol's one removal, ``remove_tracks``, planned and applied. Two
kinds of playlist can lose a track here and no others:

* a label year playlist ``label playlists`` CREATED, for a release the genre
  gate now holds or the label's catalogue no longer confirms, or for a track
  the library removed through ``crate delete review`` (U243);
* a playlist ``export playlist`` made, for a track no longer in the library
  playlist it was exported from.

TWO VERBS AND NOT A STEP OF THE TWO BUILDERS, decided on R-836. ``label
playlists`` and ``export playlist`` both say on their gates that they never
take anything away, and ``export playlist`` is a queued job whose items are the
tracks it adds, so a removal folded into it would change its digest and its
resume. As its own verb a removal is a named act a person asks for, behind its
own explicit gate, and one label's prune can be run alone at a sitting.

ONLY WHAT THE LEDGER SAYS THE PRODUCT PUT THERE. A track is planned only when
the outbound ledger records it as added by this product, so a track a person
put on the playlist by hand is never taken off, and only from a playlist
``ledger.product_made`` vouches for. A year playlist adopted by its name under
the label's folder was made by the source system or a person, and is said and
left alone. A track the playlist holds more than once is left alone too: this
product never adds a member twice, so a second copy is a person's, and the
removal takes every copy.

ABSENCE IS NEVER THE EVIDENCE. A label year track leaves only when a release
the read REACHED says so: one the genre gate holds, or one the verifier
credits to another label, or a tombstone stands over a track of a release the
read reached (U243), which is a person's own recorded act and not an absence. A track no release in the read carries stays,
however the read came out, since an empty or short read looks exactly like a
label whose catalogue moved on.

THE PLAN READS AND WRITES NOTHING. The apply takes tracks off in chunks and
records each chunk as it lands, moving it from ``added`` to ``pruned``, so a
refusal part way resumes without taking anything off twice and a second run
plans nothing. Nothing here removes a playlist, a folder or a heart: a year
playlist the plan takes every track off is said on the gate and kept.

Layer: modules.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Iterable, Mapping
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
        artist = self.artist or "unknown artist"
        title = self.title or f"track {self.remote_id}"
        return f"{artist} - {title}"


@dataclass(frozen=True, slots=True)
class PlaylistPrune:
    """What the plan does to one playlist the ledger records."""

    #: The year, for a label year playlist, or the library playlist's key.
    key: str
    name: str
    remote_id: str
    take: tuple[Taken, ...] = ()
    #: Tracks that should leave and are already off the playlist, recorded
    #: as taken off with no call to the provider. A removal that landed
    #: before a failure part way, or a person's own, ends here.
    settle: tuple[str, ...] = ()
    #: Tracks that should leave and are on the playlist more than once, left
    #: alone since the second copy is a person's.
    twice: tuple[str, ...] = ()
    #: Why the playlist is left alone, when it is. A playlist left alone
    #: takes nothing off however many tracks it would otherwise lose.
    why: str = ""
    #: How many tracks would leave a playlist left alone, for the sentence.
    would: int = 0
    #: True when every track on the playlist is taken off, so the playlist is
    #: left empty. Said, never acted on: the playlist itself stays (U243).
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
        f"the prune of {subject!r} was handed a catalogue that does not say which "
        f"tracks each release holds ({what}), so nothing was planned and nothing "
        f"was taken off",
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={"subject": subject},
    )


def _step(
    account: RemoteAccount, key: str, name: str, remote_id: str, leaving: Iterable[str]
) -> PlaylistPrune | None:
    """One playlist's step from the tracks that should leave it, read against it.

    A track on the playlist once is taken off, one on it more than once is
    left alone, and one no longer on it is settled. None when there is
    nothing to say. A playlist that could not be read is left alone, said.
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
        return PlaylistPrune(
            key=key,
            name=name,
            remote_id=remote_id,
            why=f"the playlist could not be read, so nothing is taken off it: {exc.cause.message}",
            would=len(wanted),
        )
    copies = Counter(order)
    asked = set(wanted)
    take = tuple(
        Taken(remote_id=one, artist=artist, title=title)
        for one, (artist, title) in names.items()
        if one in asked and copies[one] == 1
    )
    return PlaylistPrune(
        key=key,
        name=name,
        remote_id=remote_id,
        take=take,
        settle=tuple(one for one in wanted if one not in names and copies[one] == 0),
        twice=tuple(one for one in wanted if copies[one] > 1),
        # EMPTIED is read off the playlist as it is: every member it holds is
        # one this plan takes off. A playlist holding nothing to begin with is
        # not one the plan empties.
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

    ``held`` is the release identifiers the genre gate holds in force for the
    label, read from the review database, which is local. ``tracks_of`` reads
    a release's tracks for a held or mismatched release the catalogue read
    did not, and is asked only while a recorded track is still unexplained.

    A TRACK LEAVES A YEAR WHEN THE LEDGER RECORDS IT AS ADDED there, no kept
    release of that year or of no year carries it, and a release the read
    reached says it should go:

    * a release the gate holds carries it;
    * a release the verifier credits to another label carries it. Judged
      only when every confirmed release's tracks were read, since a release
      the provider no longer has could be the one that keeps it.

    A track on a held release and a kept one stays, since the kept release
    asked for it. A track on no release the read reached stays, said.

    A TRACK THE LIBRARY REMOVED LEAVES WHATEVER RELEASE KEEPS IT (U243):
    ``catalogue.tombstoned``, a track of a release the read reached with a
    tombstone standing over its artist and title. The kept release asks for
    the track, and the person who removed it from the library asked louder.
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
    # any year, so a release the provider re-dated is not read as unreached.
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
            f"of held releases are taken off"
        )
    if unexplained:
        notes.append(
            f"{len(unexplained)} recorded track(s) are on no release this read "
            f"reached, and a release the read did not reach is not evidence, so "
            f"they stay"
        )
    steps: list[PlaylistPrune] = []
    for year in sorted(shape.years):
        recorded = shape.years[year]
        # ``on_other`` holds only what was read while ``judged``, so the one
        # guard on a release credited elsewhere is where it is read, above.
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
            steps.append(
                PlaylistPrune(
                    key=year, name=name, remote_id=recorded.remote_id, why=why,
                    would=len(leaving),
                )
            )
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

    ``crate`` is the library playlist's rows now, ``wanted`` the remote
    identifiers they match now, and ``unmatched`` how many matched none. A
    track the ledger records as added leaves on one of two readings:

    * BY ITS ROW, for a track this build wrote: the library row it was matched
      from is no longer in the playlist, and no row now matches it. A match
      that drifted to another remote track says nothing about it.
    * BY MATCH ALONE, for a track written before the row was kept: no row
      matches it now. Absence of a match is weak evidence, so this reading
      leaves the playlist alone when any row matched nothing, or when any row
      matches a track the playlist was never written with, which is what a
      drifted match or a row added since the last export looks like.

    A playlist whose export is older than the one it was last written from,
    ``older`` being that date, is left alone whatever the reading: every row
    added since would read as gone.
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
            f"this collection export is older than the one the playlist was last "
            f"written from, on {older}, so a track added since would read as gone; "
            f"export the collection again"
        )
    elif unrowed and unmatched:
        why = (
            f"{unmatched} row(s) of the library playlist matched no track on the "
            f"account, so which recorded tracks left it cannot be told"
        )
    elif unrowed and fresh:
        why = (
            f"{len(fresh)} row(s) of the library playlist match a track this playlist "
            f"was never written with, so a match may have moved; export the playlist "
            f"first, then prune"
        )
    if why or account is None:
        step: PlaylistPrune | None = PlaylistPrune(
            key=playlist_key,
            name=name,
            remote_id=record.remote_id,
            why=why or "no account was opened to read the playlist",
            would=len(leaving),
        )
    else:
        step = _step(account, playlist_key, name, record.remote_id, leaving)
    if step is None:
        return Plan(kind=EXPORTED, subject=playlist_key)
    return Plan(kind=EXPORTED, subject=playlist_key, playlists=(step,))


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


def _record(cfg: config.Config, planned: Plan, step: PlaylistPrune, taken: Iterable[str]) -> None:
    if planned.kind == LABEL:
        ledger.record_label_pruned(cfg, planned.subject, step.key, taken)
    else:
        ledger.record_playlist_pruned(cfg, step.key, taken)


def apply(cfg: config.Config, account: RemoteAccount, planned: Plan, done: Pruned) -> Pruned:
    """Take the planned tracks off, recording each chunk as it lands, into ``done``.

    ``done`` is the caller's, so a raise part way leaves in it what was taken
    off before the raise, for the refusal to name. The ledger is asked again
    before each playlist, since the plan was read in another invocation.
    """
    for step in planned.playlists:
        if not step.writes:
            continue
        if not ledger.product_made(cfg, step.remote_id):
            raise _not_made(step.remote_id)
        # A SETTLED TRACK GOES THROUGH THE REMOVAL TOO, with nothing at its
        # position to take, so the adapter's full read vouches that it is off.
        # The listing leaves out a track the account cannot play, and recorded
        # on the plan's word alone such a track would be called gone while it
        # is still on the playlist.
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
            _record(cfg, planned, step, chunk)
            for one in chunk:
                held = done.settled if one in settling else done.taken
                held.setdefault(step.remote_id, []).append(one)
    return done


def payload(
    planned: Plan | None, *, kind: str, subject: str, digest: Callable[[Any], str]
) -> dict[str, Any]:
    """The ``plan/1`` payload the gate is asked over: one item per track taken off.

    ``digest`` is the CLI layer's digest function, handed in so this module
    imports nothing from that layer.
    """
    identity = planned.identity() if planned is not None else {"kind": kind, "subject": subject}
    items: list[dict[str, Any]] = []
    for step in planned.playlists if planned is not None else ():
        where = {"playlist": step.remote_id, "key": step.key, "name": step.name}
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
        items.extend(
            {
                "id": taken.remote_id,
                "kind": "track",
                **where,
                "action": "take-off",
                "artist": taken.artist,
                "title": taken.title,
            }
            for taken in step.take
        )
        items.extend(
            {"id": one, "kind": "track", **where, "action": "already-off"} for one in step.settle
        )
        items.extend(
            {
                "id": one,
                "kind": "track",
                **where,
                "action": "left-alone",
                "why": "on the playlist more than once, and a second copy is a person's",
            }
            for one in step.twice
        )
    return {
        "digest": digest(identity),
        "items": items,
        "totals": {
            "count": len(items),
            "take_off": sum(1 for item in items if item["action"] == "take-off"),
            "writes": bool(planned is not None and planned.writes),
            # SAID AND NOT A WRITE, so outside the digest: the playlists the
            # plan leaves empty, which stay on the account.
            "emptied": [
                step.name
                for step in (planned.playlists if planned is not None else ())
                if step.empties and not step.why
            ],
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

    ``label playlists``' rule: a refusal the account raised keeps its reason
    and remedy, and anything else is this build's own defect and says so. What
    was taken off is recorded already, so a run started again plans the rest.
    """
    wrote = (
        f"before this failed {done.count} track(s) were taken off and recorded"
        if done.count
        else "no track was recorded as taken off before this failed"
    )
    detail = {"taken": {remote: list(ids) for remote, ids in done.taken.items()}}
    if isinstance(exc, CratekitError):
        cause = exc.cause
        # A READ BACK THAT DIFFERED says to look by hand before anything runs
        # again, and "run it again" beside that would undo the advice.
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


__all__ = [
    "CHUNK",
    "EXPORTED",
    "LABEL",
    "Plan",
    "PlaylistPrune",
    "Pruned",
    "Taken",
    "apply",
    "failed_part_way",
    "finished",
    "payload",
    "plan_export",
    "plan_label",
    "report",
    "shown",
]
