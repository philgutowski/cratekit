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
    """One library row offered for export. ``identity`` is stable; the name is not."""

    identity: str
    title: str = ""
    artist: str = ""
    isrc: str = ""


@dataclass(frozen=True, slots=True)
class Unmatched:
    """A library row the streaming service could not match."""

    identity: str
    title: str
    artist: str
    reason: str = "unmatched"


@dataclass(frozen=True, slots=True)
class ExportPlan:
    """What an export will write, including the tracks it will not."""

    playlist_key: str
    name: str
    matched: tuple[tuple[str, str], ...]
    unmatched: tuple[Unmatched, ...]


@dataclass(frozen=True, slots=True)
class ExportReport:
    """What one apply did, including unmatched tracks the brief requires."""

    playlist_key: str
    remote_id: str
    created: bool
    added: tuple[str, ...]
    already: tuple[str, ...]
    unmatched: tuple[Unmatched, ...]


def plan(
    tracks: Sequence[LocalTrack],
    *,
    playlist_key: str,
    name: str,
    account: RemoteAccount,
) -> ExportPlan:
    """Match every track. Unmatched stay on the plan; they are not omitted."""
    matched: list[tuple[str, str]] = []
    unmatched: list[Unmatched] = []
    for track in tracks:
        remote = account.match_track(identity=track.identity, isrc=track.isrc)
        if remote:
            matched.append((track.identity, remote))
        else:
            unmatched.append(
                Unmatched(
                    identity=track.identity,
                    title=track.title,
                    artist=track.artist,
                )
            )
    return ExportPlan(
        playlist_key=playlist_key,
        name=name,
        matched=tuple(matched),
        unmatched=tuple(unmatched),
    )


def apply(
    cfg: config.Config,
    account: RemoteAccount,
    planned: ExportPlan,
) -> ExportReport:
    """Write the matched tracks. Reuses a recorded remote playlist if one exists."""
    existing = ledger.playlist_remote_id(cfg, planned.playlist_key)
    created = existing is None
    remote_id = existing or account.create_playlist(planned.name)
    if created:
        ledger.record_playlist(cfg, planned.playlist_key, remote_id)
    already_on = set(account.playlist_tracks(remote_id))
    already_recorded = set(ledger.playlist_added(cfg, planned.playlist_key))
    added: list[str] = []
    already: list[str] = []
    for _local, remote in planned.matched:
        if remote in already_on or remote in already_recorded:
            already.append(remote)
            continue
        account.add_to_playlist(remote_id, remote)
        ledger.record_playlist_track(cfg, planned.playlist_key, remote)
        added.append(remote)
    return ExportReport(
        playlist_key=planned.playlist_key,
        remote_id=remote_id,
        created=created,
        added=tuple(added),
        already=tuple(already),
        unmatched=planned.unmatched,
    )
