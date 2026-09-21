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
from cratekit.modules.outbound import ledger
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
    recognised one and a person confirmed it (R-229). Empty means create or
    reuse by this key alone, which is every export before that finding.
    """

    playlist_key: str
    name: str
    matched: tuple[tuple[str, str], ...]
    unmatched: tuple[Unmatched, ...]
    adopts: str = ""


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


def plan(
    tracks: Sequence[LocalTrack],
    *,
    playlist_key: str,
    name: str,
    account: RemoteAccount,
    adopts: str = "",
) -> ExportPlan:
    """Match every track. Unmatched stay on the plan; they are not omitted."""
    matched: list[tuple[str, str]] = []
    unmatched: list[Unmatched] = []
    for track in tracks:
        remote = account.match_track(
            identity=track.identity,
            isrc=track.isrc,
            title=track.release_title,
            artist=track.artist,
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

    EVERY MATCHED ROW'S LIBRARY IDENTITY IS RECORDED, added or already there
    (R-229). Those identities are the only thing that can recognise this crate
    once rekordbox shows it under another path, and a row that was already on
    the remote playlist is as much a part of the crate as one written just now.
    """
    reserved = ledger.reserve_playlist(
        cfg,
        planned.playlist_key,
        # RESOLVED LAZILY, so an unwritable ledger refuses before the account is
        # touched at all rather than after.
        lambda: account.create_playlist(planned.name),
        adopts=planned.adopts,
    )
    remote_id = reserved.remote_id
    already_on = set(account.playlist_tracks(remote_id))
    already_recorded = set(ledger.playlist_added(cfg, planned.playlist_key))
    added: list[str] = []
    already: list[str] = []
    for local, remote in planned.matched:
        if remote in already_on or remote in already_recorded:
            ledger.record_playlist_row(cfg, planned.playlist_key, local)
            already.append(remote)
            continue
        account.add_to_playlist(remote_id, remote)
        ledger.record_playlist_track(cfg, planned.playlist_key, remote, local=local)
        added.append(remote)
    return ExportReport(
        playlist_key=planned.playlist_key,
        remote_id=remote_id,
        created=reserved.created,
        added=tuple(added),
        already=tuple(already),
        unmatched=planned.unmatched,
        adopted_from=reserved.adopted_from,
    )
