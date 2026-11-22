"""What a pair plan reads beside the two playlists: the landings, the intake jobs and the codes the files carry (U130, U304)."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any

from cratekit.acquire import match
from cratekit.cli.output import timestamp
from cratekit.core import config, jobs, locations, session, tags
from cratekit.core.cause import CratekitError
from cratekit.intake import cli as intake_cli
from cratekit.intake import ingest
from cratekit.sync import pair_stopped
from cratekit.sync.pair_model import (
    INTAKE_HANDLER,
    NEW,
    OWNED_STATE,
    PAIR_SOURCE,
    STEP_ACCOUNT,
    STEP_DONE,
    STEP_MADE,
    STEP_MOVED,
    STEP_MOVING,
    STEP_ORDERING,
)
from cratekit.write import playlist_pair


@dataclass
class _Reader:
    """What one plan reads once and every pair shares."""

    cfg: config.Config
    db: Any
    found: Any
    listed: Mapping[str, Any]
    label_owned: frozenset[str]
    set_built: frozenset[str]
    tops: tuple[frozenset[str], frozenset[str]]
    store: Any
    #: Every playlist ``crate organize`` mirrors (U147).
    mirrored: frozenset[str] = frozenset()
    #: U198, R-988. Every row the account had no track for, as remembered,
    #: and what this plan asked fresh or matched since.
    misses: Mapping[str, Any] = field(default_factory=dict)
    fresh: dict[str, Any] = field(default_factory=dict)
    matched: set[str] = field(default_factory=set)
    #: U202. Each account root folder's playlists, listed once per plan.
    inside: dict[str, dict[str, str]] = field(default_factory=dict)
    #: U216. When the account says each playlist in a folder was made, listed
    #: once per plan, and only for a folder adopted with no record of what it held.
    made_at: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: U229. Each landed INBOX playlist's codes and rows, and each intake
    #: job's reports, read once per plan whichever pair asks for them.
    landed_codes: dict[str, tuple[tuple[str, str], ...]] = field(default_factory=dict)
    reports: dict[str, tuple[dict[str, Any], ...] | Exception] = field(default_factory=dict)
    #: R-1385. Each track a pair of this plan asks to acquire, by remote id,
    #: with the pair's key and name, so a later pair listing it awaits it.
    asked: dict[str, tuple[str, str]] = field(default_factory=dict)

    @cached_property
    def remote(self):
        """The account, resolved on first use, so a plan with nothing to match asks nothing."""
        from cratekit.modules.outbound import account

        return account.resolve(self.cfg)

    @cached_property
    def root_folders(self) -> dict[str, str]:
        """The account's root folders, folder id to name, listed once per plan."""
        return dict(self.remote.folders())

    def folder_listing(self, folder_id: str) -> dict[str, str]:
        """One root folder's playlists, id to title, listed once per plan (U202)."""
        if folder_id not in self.inside:
            self.inside[folder_id] = dict(self.remote.folder_playlists(folder_id))
        return self.inside[folder_id]

    def folder_dates(self, folder_id: str) -> dict[str, Any]:
        """When the account says each playlist in one root folder was made, None unknown (U216)."""
        if folder_id not in self.made_at:
            self.made_at[folder_id] = {
                playlist_id: made
                for playlist_id, (_title, made) in self.remote.folder_playlists_dated(
                    folder_id
                ).items()
            }
        return self.made_at[folder_id]

    @cached_property
    def by_isrc(self) -> dict[str, tuple[str, ...]]:
        return playlist_pair.rows_by_isrc(self.db, match.isrc_token)

    @cached_property
    def pair_jobs(self) -> tuple[jobs.Job, ...]:
        """Every intake job this verb queued on this library that did not fail, newest first."""
        return pair_jobs(self.cfg, self.store)

    @cached_property
    def landings(self) -> tuple[dict[str, frozenset[str]], tuple[Path, ...]]:
        """The landing records' INBOX playlists, and the log's entries unread, read once per plan.

        R-1383. Both halves of one scan, so a landing whose record does not
        read is never read as no landing.
        """
        return landed_inbox_playlists(self.cfg)

    @property
    def mirrors(self) -> dict[str, frozenset[str]]:
        """Each account playlist's INBOX playlists, as the landing records name them (U128)."""
        return self.landings[0]

    @cached_property
    def stopped(self) -> tuple[dict[str, tuple[Any, Any]], tuple[str, ...]]:
        """Each pair's write stopped part way through its order, and the runs' steps unread (U225).

        Read once per plan, from every run's steps still kept, so a fresh
        plan knows a write that stopped part way through a pair's order, and
        from every pair's steps carried past its run (R-1372), whatever their
        age, so a stop is never forgotten while its pair is unfinished. A
        carried record gives way to its own run's steps when those are still
        kept under the same plan, since they say whether the pair finished.
        """
        from cratekit.core import held_plan

        records, problems = held_plan.recorded_steps()
        kept, unread = held_plan.carried()
        current = {(one.run_id, one.digest) for one in records}
        records = [*records, *(one for one in kept if (one.run_id, one.digest) not in current)]
        problems = [*problems, *unread]
        return (
            pair_stopped.stopped_writes(
                records,
                new=NEW,
                account=STEP_ACCOUNT,
                ordering=STEP_ORDERING,
                made=STEP_MADE,
                done=STEP_DONE,
                moving=STEP_MOVING,
                moved=STEP_MOVED,
            ),
            tuple(problems),
        )

    def stopped_write(self, account_id: str, held: Any) -> Any:
        """The write on this pair that stopped part way through its order since its snapshot, or None (U225).

        The pair's latest write that began to order and never finished, when
        no later run finished the pair and it began after the pair's last
        snapshot.
        A snapshot that cannot be read as a moment says nothing was written
        since, so nothing is finished from a write it cannot place. And a
        write that began before the pair was marked is another pair's: a
        carried record outlives a pair forgotten and marked again (R-1372).
        """
        from cratekit.favorites import placeholders
        if not account_id or held is None:
            return None
        began, write = self.stopped[0].get(account_id, (None, None))
        if write is None or began is None:
            return None
        marked = placeholders.parse_hearted(held.marked) if held.marked else None
        if marked is not None and began < marked:
            return None
        if held.synced:
            synced = placeholders.parse_hearted(held.synced)
            if synced is None or not began > synced:
                return None
        return write

    def first_stop(self, account_id: str) -> Any:
        """The write that stopped part way through ordering this account playlist, for a first sync, or None (R-1376).

        A pair released after a stop and paired again, or marked and never
        written whole, syncs first with no snapshot, and the account it reads
        is the stopped write's scramble, which a first sync's order would put
        into rekordbox. Read whatever the mark, since the stop predates the
        new one, and FOR ITS ORDER ALONE: its bases are another pair's, and a
        first sync has none to fold. The latest write that began to order the
        playlist and that no later run finished, as :meth:`stopped` keeps it.
        """
        if not account_id:
            return None
        _began, write = self.stopped[0].get(account_id, (None, None))
        return write

    def see(self, account_id: str, order: Sequence[str]) -> None:
        """Keep this plan's reading of a pending order's playlist on its pair, for the next to agree with (U231)."""
        from cratekit.modules.outbound import pairs

        pairs.PairStore(self.cfg).see(account_id, order, at=timestamp())

    def see_stop(self, account_id: str, reading: Any) -> None:
        """Keep the readings of a playlist a stopped order left on its pair (U234)."""
        from cratekit.modules.outbound import pairs

        pairs.PairStore(self.cfg).see_stop(account_id, reading)

    def mirror_codes(self, mirror: str) -> tuple[tuple[str, str], ...]:
        """One landed INBOX playlist's ISRC and row pairs, read once per plan (U229)."""
        if mirror not in self.landed_codes:
            self.landed_codes[mirror] = mirror_codes(self.cfg, self.db, mirror)
        return self.landed_codes[mirror]

    @cached_property
    def landed_anywhere(self) -> dict[str, tuple[str, ...]]:
        """ISRC to content ids, from every INBOX playlist landed on this library (U229).

        Whichever account playlist a landing brought a track in through, the
        row it made is the library's copy of that track, so a pair asking for
        the track is asked to add that row and never to download it again.
        Read once per plan, and only when a pair reaches it.
        """
        every: set[str] = set()
        for ids in self.mirrors.values():
            every.update(ids)
        return landed_isrcs(self.cfg, self.db, every, read=self.mirror_codes)

    def job_reports(
        self, job: jobs.Job, *, own: bool = True
    ) -> tuple[dict[str, Any], ...] | None:
        """One finished intake job's reports, None when they cannot be read, read once per plan.

        A job whose frozen configuration no longer reads refuses the plan of
        the pair that queued it, as it always has, and is passed over by every
        other pair's (``own`` false, U229), since one pair's old job is no
        reason to stop every pair's plan.
        """
        from cratekit.intake import missing_cli

        if job.job_id not in self.reports:
            try:
                self.reports[job.job_id] = tuple(missing_cli.job_reports(self.store, job))
            except (CratekitError, config.ConfigError) as error:
                self.reports[job.job_id] = error
        held = self.reports[job.job_id]
        if isinstance(held, config.ConfigError) and own:
            raise held
        return None if isinstance(held, Exception) else held

    def jobs_for(self, account_id: str) -> tuple[jobs.Job, ...]:
        return tuple(
            job
            for job in self.pair_jobs
            if str((job.payload or {}).get(intake_cli.SOURCE) or "") == account_id
        )

    @cached_property
    def held_by_jobs(self) -> dict[str, tuple[tuple[str, str], ...]]:
        """Each track any pair's intake job on this library holds, read once per plan (R-1385).

        Remote id to the account playlist and its name of every job holding
        it, newest first, from the jobs :attr:`pair_jobs` lists: every one
        that did not fail or cancel, as a pair's own are read.
        """
        found: dict[str, list[tuple[str, str]]] = {}
        for job in self.pair_jobs:
            payload = job.payload or {}
            source = str(payload.get(intake_cli.SOURCE) or "")
            name = str(payload.get(intake_cli.PLAYLIST_NAME) or "") or source
            for item in payload.get(intake_cli.TRACKS) or {}:
                found.setdefault(str(item), []).append((source, name))
        return {remote_id: tuple(held) for remote_id, held in found.items()}



def pair_jobs(cfg: config.Config, store) -> tuple[jobs.Job, ...]:
    """Every intake job this verb queued on this library that did not fail, newest first."""
    return tuple(
        job
        for job in jobs.list_jobs(store)
        if job.handler_key == INTAKE_HANDLER
        and job.library_id == cfg.library.volume_id
        and (job.payload or {}).get("source_id") == PAIR_SOURCE
        and job.state not in (jobs.JobState.FAILED, jobs.JobState.CANCELLED)
    )



def file_identity(cfg: config.Config, recorded: str) -> tuple[str, str]:
    """The ISRC and album tag the row's audio file carries, or empty strings.

    Every way this cannot read, a path that is not local, a prefix no rule
    maps, a file that is gone, a tag that is not an ISRC, answers empty, which
    leaves the row to be matched on nothing and named as unmatched, the route
    ``outbound.source.file_identity`` gives a collection export's row.
    """
    from cratekit.modules.outbound import source

    if not recorded:
        return "", ""
    resolved = locations.resolve_recorded_path(
        recorded, root=cfg.library.root, prefix_map=source.prefix_rules(cfg)
    )
    if resolved.path is None:
        return "", ""
    path = Path(resolved.path)
    if not path.is_file():
        return "", ""
    read = tags.read_tags(path, ("isrc", "album"))
    return match.isrc_token(read["isrc"]), str(read["album"] or "").strip()



def _owned_by_jobs(
    reader: _Reader, found: Sequence[jobs.Job], wanted: set[str], *, own: bool = True
) -> dict[str, str]:
    """Remote id to content id, for each wanted track a pair's intake job found owned.

    The newest job's report of a track answers for it, as ``found`` is newest first.
    """
    from cratekit.intake import native

    paths: dict[str, Path] = {}
    for job in found:
        if job.state != jobs.JobState.SUCCEEDED:
            continue
        reports = reader.job_reports(job, own=own)
        if reports is None:
            continue
        for report in reports:
            remote_id = str(report.get("item_id") or "")
            if remote_id not in wanted or remote_id in paths:
                continue
            if str(report.get("state") or "") != OWNED_STATE:
                continue
            held = [Path(str(one)) for one in report.get("paths") or ()]
            if len(held) == 1:
                paths[remote_id] = held[0]
    if not paths:
        return {}
    rows = native.content_ids_for(reader.db, reader.cfg, list(paths.values()))
    return {
        remote_id: rows[str(path)] for remote_id, path in paths.items() if str(path) in rows
    }



def landed_inbox_playlists(
    cfg: config.Config,
) -> tuple[dict[str, frozenset[str]], tuple[Path, ...]]:
    """Each account playlist's INBOX playlists, as the landing records name them (U128), and the unread.

    PUBLIC because the custom playlist twins' backfill (U149) finds a landed
    track's row the same way a pair does.

    THE UNREAD HALF IS KEPT (R-1383). Every entry of the log this build
    cannot read is answered beside the playlists, the log itself when it is
    there and cannot be listed, as the session log's own gates count every
    one (``session.assert_no_unresolved_session``): a torn record cannot say
    its workflow, and a state a later build wrote cannot say whether its
    landing stands, so none of them is read as no landing.
    """
    standing = {
        session.SessionState.AWAITING_IMPORT,
        session.SessionState.COMMITTED_UNVERIFIED,
        session.SessionState.CLOSED,
    }
    records, unreadable = session.scan_log(cfg)
    found: dict[str, set[str]] = {}
    for record in records:
        if record.workflow != ingest.INTAKE_WORKFLOW or record.state not in standing:
            continue
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ():
            if not isinstance(entry, dict) or not entry.get("id"):
                continue
            account_id = str(entry.get(ingest.INBOX_ACCOUNT_KEY) or "")
            if account_id:
                found.setdefault(account_id, set()).add(str(entry["id"]))
    return {account_id: frozenset(ids) for account_id, ids in found.items()}, tuple(unreadable)



def mirror_codes(cfg: config.Config, db: Any, mirror: str) -> tuple[tuple[str, str], ...]:
    """Each row of one landed INBOX playlist with its ISRC, the database's or else the file's.

    A row carrying no code anywhere is left out, since nothing can name it by one.
    """
    found: list[tuple[str, str]] = []
    for row in playlist_pair.members(db, mirror):
        code = match.isrc_token(row.isrc) or file_identity(cfg, row.path)[0]
        if code:
            found.append((code, row.content_id))
    return tuple(found)



def landed_isrcs(
    cfg: config.Config,
    db: Any,
    playlist_ids: Iterable[str],
    *,
    read: Callable[[str], Iterable[tuple[str, str]]] | None = None,
) -> dict[str, tuple[str, ...]]:
    """ISRC to content ids, read from the files of the INBOX playlists named.

    U128 records each INBOX playlist a landing made for an account playlist
    with the account playlist's identifier. A track a pair queued and a landing
    brought sits there, and its row may carry no ISRC of its own, since a
    landed row's code is in its file. Only those rows' files are read.

    ``read`` is how one playlist's codes are read, :func:`mirror_codes` unless
    a caller keeps its own copy, as a plan does so each file is read once (U229).
    """
    found: dict[str, list[str]] = {}
    for mirror in sorted(set(playlist_ids)):
        pairs_read = read(mirror) if read is not None else mirror_codes(cfg, db, mirror)
        for code, content_id in pairs_read:
            if content_id not in found.setdefault(code, []):
                found[code].append(content_id)
    return {code: tuple(ids) for code, ids in found.items()}



def _mirror_isrcs(reader: _Reader, account_id: str) -> dict[str, tuple[str, ...]]:
    """ISRC to content ids, from the INBOX playlists landed for this account playlist."""
    return landed_isrcs(
        reader.cfg, reader.db, reader.mirrors.get(account_id, ()), read=reader.mirror_codes
    )
