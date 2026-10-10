"""Export a library playlist to a streaming service (AE14, R27).

Unmatched tracks are reported, never dropped silently. A re-export of the
same local playlist updates the recorded remote playlist rather than
creating a second one. Each added track is recorded before the next write
so an interrupted run resumes without duplicating remote state.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.modules.outbound import kinds, ledger
from cratekit.modules.outbound.service import RemoteAccount


@dataclass(frozen=True, slots=True)
class LocalTrack:
    """One library row offered for export. ``identity`` is stable; the name is not.

    ``title`` is the row AS THE LIBRARY SHOWS IT, naming head and all, and is
    what an unmatched row is reported under. ``release_title`` is the same title
    with the head off, which is the only spelling a provider's own title can be
    compared against (R-356). Two fields because they answer two questions, and
    a report that dropped the head would name a row the person cannot find by
    looking.
    """

    identity: str
    title: str = ""
    artist: str = ""
    isrc: str = ""
    release_title: str = ""
    #: The album tag of the row's own file, which chooses among releases
    #: spelled alike under one ISRC when none is hearted (R-572).
    album: str = ""


@dataclass(frozen=True, slots=True)
class Unmatched:
    """A library row the streaming service could not match."""

    identity: str
    title: str
    artist: str
    reason: str = "unmatched"


@dataclass(frozen=True, slots=True)
class ExportPlan:
    """What an export will write, including the tracks it will not.

    ``adopts`` is the recorded key this crate used to live under, when the verb
    recognised one and a person confirmed it (R-229). ``expected`` is the remote
    playlist the person was shown this write updating. Both empty means create
    or reuse by this key alone, which is every export before that finding.

    ``contents`` IS THE WHOLE CRATE, NOT THIS PLAN'S ROWS. The outbound verb
    plans one track per item, so the rows here are one row of the crate, and the
    ledger records what the crate holds so it can be recognised under another
    path. Matched or not: a row the provider does not carry is still a row of
    the crate.
    """

    playlist_key: str
    name: str
    matched: tuple[tuple[str, str], ...]
    unmatched: tuple[Unmatched, ...]
    adopts: str = ""
    expected: str = ""
    contents: tuple[str, ...] = ()
    #: The ISO date of the collection export the plan was read from, recorded
    #: so ``export prune`` can refuse an older one (R-836). Empty when unread.
    written: str = ""


@dataclass(frozen=True, slots=True)
class ExportReport:
    """What one apply did, including unmatched tracks the brief requires."""

    playlist_key: str
    remote_id: str
    created: bool
    added: tuple[str, ...]
    already: tuple[str, ...]
    unmatched: tuple[Unmatched, ...]
    #: The key the recorded remote playlist was moved from BY THIS CALL, or
    #: empty. Set once per job under the per item shape: the first item moves
    #: the record and the rest find it under their own key.
    adopted_from: str = ""
    #: Why a playlist this call created is not in the ``Exports`` folder, or
    #: empty (U131). ``crate organize`` files one left at the root.
    unfiled: str = ""


def plan(
    tracks: Sequence[LocalTrack],
    *,
    playlist_key: str,
    name: str,
    account: RemoteAccount,
    adopts: str = "",
    expected: str = "",
    contents: Sequence[str] | None = None,
    written: str = "",
) -> ExportPlan:
    """Match every track. Unmatched stay on the plan; they are not omitted.

    ``contents`` defaults to the rows handed in, which is right for a caller
    planning a whole playlist at once and wrong for one planning a single item,
    so the per item verb always passes the frozen track set.
    """
    matched: list[tuple[str, str]] = []
    unmatched: list[Unmatched] = []
    for track in tracks:
        remote = account.match_track(
            identity=track.identity,
            isrc=track.isrc,
            title=track.release_title,
            artist=track.artist,
            album=track.album,
        )
        if remote:
            matched.append((track.identity, remote))
        else:
            unmatched.append(
                Unmatched(
                    identity=track.identity,
                    title=track.title,
                    artist=track.artist,
                    reason=account.unmatched_reason(track.identity) or "unmatched",
                )
            )
    return ExportPlan(
        playlist_key=playlist_key,
        name=name,
        matched=tuple(matched),
        unmatched=tuple(unmatched),
        adopts=adopts,
        expected=expected,
        written=written,
        contents=tuple(
            str(item)
            for item in (
                contents if contents is not None else [t.identity for t in tracks]
            )
        ),
    )


def apply(
    cfg: config.Config,
    account: RemoteAccount,
    planned: ExportPlan,
) -> ExportReport:
    """Write the matched tracks. Reuses a recorded remote playlist if one exists.

    THE CREATE AND ITS RECORD HAPPEN UNDER ONE LEDGER LOCK. This used to read the
    recorded id, create when there was none, and record afterwards, so a ledger
    that could not be written left an orphaned remote playlist and the next call
    made another one. Under the per item shape the outbound verbs use, that is one
    orphan per track: driven as three remote playlists from one three track
    export. ``ledger.reserve_playlist`` carries the ordering and the argument.

    EVERYTHING AFTER THE RESERVE IS RECORDED UNDER ``reserved.key`` (R-229),
    which is this plan's key unless the record moved to the crate's new path
    after this job was confirmed. Recording under the plan's own key then would
    start a second record for a remote playlist that already has one.
    """
    reserved = ledger.reserve_playlist(
        cfg,
        planned.playlist_key,
        # RESOLVED LAZILY, so an unwritable ledger refuses before the account is
        # touched at all rather than after.
        lambda: account.create_playlist(planned.name),
        adopts=planned.adopts,
        expected=planned.expected,
        contents=planned.contents,
        written=planned.written,
    )
    remote_id = reserved.remote_id
    already_on = set(account.playlist_tracks(remote_id))
    already_recorded = reserved.added
    added: list[str] = []
    already: list[str] = []
    for local, remote in planned.matched:
        if remote in already_on or remote in already_recorded:
            already.append(remote)
            # WHICH ROW A WRITTEN TRACK CAME FROM (R-836), kept for a track this
            # product wrote, so a prune can tell a row that left from a match
            # that drifted. A track a person put there is never claimed.
            if remote in already_recorded and reserved.rows.get(local) != remote:
                ledger.record_playlist_row(cfg, reserved.key, local, remote)
            continue
        account.add_to_playlist(remote_id, remote)
        ledger.record_playlist_track(cfg, reserved.key, remote, identity=local)
        added.append(remote)
    unfiled = ""
    if reserved.created:
        # FILED AT CREATION (U131), after the tracks, so a refused move leaves a
        # whole playlist at the root rather than an empty one, recorded, which
        # ``crate organize`` files on its next pass.
        try:
            unfiled = kinds.file_new(cfg, account, remote_id, kinds.EXPORTS)
        except CratekitError as exc:
            unfiled = exc.cause.message
    return ExportReport(
        unfiled=unfiled,
        playlist_key=planned.playlist_key,
        remote_id=remote_id,
        created=reserved.created,
        added=tuple(added),
        already=tuple(already),
        unmatched=planned.unmatched,
        adopted_from=reserved.adopted_from,
    )
