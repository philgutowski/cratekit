"""Export a library playlist to a streaming service (AE14, R27).

Unmatched tracks are reported, never dropped silently. A re-export of the
same local playlist updates the recorded remote playlist rather than
creating a second one. The tracks a plan lacks go to the account in one
batched add (U270), and each is recorded once the provider's answer names
it, so an interrupted run resumes without duplicating remote state.
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

    ``title`` is the row as the library shows it, naming head and all, which an
    unmatched row is reported under; ``release_title`` has the head off, the
    only spelling a provider's title compares with (R-356).
    """

    identity: str
    title: str = ""
    artist: str = ""
    isrc: str = ""
    release_title: str = ""
    #: The row's own file's album tag, choosing among releases under one ISRC (R-572).
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

    ``adopts`` is the recorded key this crate used to live under, when a
    person confirmed it (R-229), and ``expected`` the remote playlist they were
    shown; both empty create or reuse by this key alone. ``contents`` is the
    WHOLE CRATE, matched or not, which the ledger records so the crate can be
    recognised under another path.
    """

    playlist_key: str
    name: str
    matched: tuple[tuple[str, str], ...]
    unmatched: tuple[Unmatched, ...]
    adopts: str = ""
    expected: str = ""
    contents: tuple[str, ...] = ()
    #: The ISO date of the collection export read, so ``export prune`` can
    #: refuse an older one (R-836). Empty when unread.
    written: str = ""
    #: The Exports folder decision the gate showed, :func:`kinds.token`, or
    #: empty when the gate planned no filing (U131).
    filing: str = ""


#: What one matched row came to, in :attr:`ExportReport.outcomes` (U270).
ADDED = "added"
ALREADY = "already"
#: The provider would not add the track: its answer did not name it and the
#: read back does not hold it.
REFUSED = "refused"

#: How many items the driver hands the export worker at once (U270), the
#: provider's limit on one add request.
BATCH = 100


@dataclass(frozen=True, slots=True)
class ExportReport:
    """What one apply did, including unmatched tracks the brief requires."""

    playlist_key: str
    remote_id: str
    created: bool
    added: tuple[str, ...]
    already: tuple[str, ...]
    unmatched: tuple[Unmatched, ...]
    #: The key the record was moved from BY THIS CALL, or empty.
    adopted_from: str = ""
    #: Why a playlist this call created is not in the ``Exports`` folder, or
    #: empty (U131); ``crate organize`` files one left at the root.
    unfiled: str = ""
    #: Each matched row's ``(row, track, outcome)`` in plan order (U270).
    outcomes: tuple[tuple[str, str, str], ...] = ()
    #: Tracks the provider would not add, which ``added`` does not name (U270).
    refused: tuple[str, ...] = ()


#: The playlist export creates is filed in the account's Exports folder (U131).
KIND = kinds.EXPORTS


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
    filing: str = "",
) -> ExportPlan:
    """Match every track. Unmatched stay on the plan; they are not omitted.

    ``contents`` defaults to the rows handed in; a per item caller passes the
    frozen track set.
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
            reason = account.unmatched_reason(track.identity) or "unmatched"
            unmatched.append(Unmatched(track.identity, track.title, track.artist, reason))
    rows = contents if contents is not None else [t.identity for t in tracks]
    return ExportPlan(
        playlist_key=playlist_key,
        name=name,
        matched=tuple(matched),
        unmatched=tuple(unmatched),
        adopts=adopts,
        expected=expected,
        written=written,
        filing=filing,
        contents=tuple(str(item) for item in rows),
    )


def apply(cfg: config.Config, account: RemoteAccount, planned: ExportPlan) -> ExportReport:
    """Write the matched tracks. Reuses a recorded remote playlist if one exists.

    THE CREATE AND ITS RECORD HAPPEN UNDER ONE LEDGER LOCK
    (``ledger.reserve_playlist``), so an unwritable ledger never orphans a
    remote playlist per item. Everything after is recorded under
    ``reserved.key`` (R-229), which differs from the plan's when the record
    moved to the crate's new path after this job was confirmed.
    """
    reserved = ledger.reserve_playlist(
        cfg,
        planned.playlist_key,
        # RESOLVED LAZILY, so an unwritable ledger refuses before the account
        # is touched.
        lambda: account.create_playlist(planned.name),
        adopts=planned.adopts,
        expected=planned.expected,
        contents=planned.contents,
        written=planned.written,
    )
    remote_id = reserved.remote_id
    already_on = set(account.playlist_tracks(remote_id))
    already_recorded = reserved.added
    outcome: dict[int, str] = {}
    lacking: dict[str, str] = {}
    noted: dict[str, str] = {}
    for at, (local, remote) in enumerate(planned.matched):
        if remote in already_on or remote in already_recorded:
            outcome[at] = ALREADY
            # WHICH ROW A WRITTEN TRACK CAME FROM (R-836), for a track this
            # product wrote, so a prune tells a row that left from a match
            # that drifted.
            if remote in already_recorded and reserved.rows.get(local) != remote:
                noted[local] = remote
            continue
        lacking[local] = remote
    answered: set[str] = set()
    if lacking:
        # ONE REQUEST FOR THE BATCH, through the mirror's add, which opens the
        # playlist afresh; a track is ADDED only when the answer, or for a
        # partial answer the adapter's read back, holds it.
        wanted = tuple(dict.fromkeys(lacking.values()))
        answered = {str(one) for one in account.add_tracks(remote_id, wanted)}
    landed = {local: remote for local, remote in lacking.items() if remote in answered}
    # ONE LEDGER WRITE FOR THE BATCH, AFTER THE ANSWER (U270, R-230).
    if landed or noted:
        ledger.record_playlist_tracks(cfg, reserved.key, landed=landed, rows=noted)
    added: list[str] = []
    by_outcome: dict[str, list[str]] = {ADDED: added, ALREADY: [], REFUSED: []}
    outcomes: list[tuple[str, str, str]] = []
    for at, (local, remote) in enumerate(planned.matched):
        said = outcome.get(at) or (ADDED if remote in answered else REFUSED)
        # TWO ROWS MATCHED TO ONE TRACK are sent once; the second reads as
        # already there, as a per item run would read it.
        if said == ADDED and remote in added:
            said = ALREADY
        outcomes.append((local, remote, said))
        by_outcome[said].append(remote)
    unfiled = ""
    if reserved.created:
        # FILED AT CREATION (U131), after the tracks, so a refused move leaves
        # a whole playlist at the root for ``crate organize``. ANY FAILURE HERE
        # IS A WARNING, never the export's: the write is done and recorded.
        try:
            unfiled = kinds.file_new(cfg, account, remote_id, KIND, planned.filing)
        except CratekitError as exc:
            unfiled = exc.cause.message
        except Exception as exc:  # noqa: BLE001 - reported as the warning
            unfiled = f"{type(exc).__name__}: {exc}"
    return ExportReport(
        unfiled=unfiled,
        playlist_key=planned.playlist_key,
        remote_id=remote_id,
        created=reserved.created,
        added=tuple(added),
        already=tuple(by_outcome[ALREADY]),
        unmatched=planned.unmatched,
        adopted_from=reserved.adopted_from,
        outcomes=tuple(outcomes),
        refused=tuple(by_outcome[REFUSED]),
    )
