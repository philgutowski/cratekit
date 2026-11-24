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
    #: U198, R-988. Rows the account had no track for, as remembered, and
    #: what this plan asked fresh or matched since.
    misses: Mapping[str, Any] = field(default_factory=dict)
    fresh: dict[str, Any] = field(default_factory=dict)
    matched: set[str] = field(default_factory=set)
    #: U202. Each account root folder's playlists, listed once per plan.
    inside: dict[str, dict[str, str]] = field(default_factory=dict)
    #: U216. Each playlist's made date, only for a folder adopted with no record
    #: of what it held.
    made_at: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: U229. Each landed INBOX playlist's codes and each intake job's reports,
    #: read once per plan.
    landed_codes: dict[str, tuple[tuple[str, str], ...]] = field(default_factory=dict)
    reports: dict[str, tuple[dict[str, Any], ...] | Exception] = field(default_factory=dict)
    #: R-1385. Each track a pair of this plan acquires, with the pair's key and
    #: name, so a later pair listing it awaits it.
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
        """The landing records' INBOX playlists and the log's entries unread, read once per plan.

        One scan, so an unreadable landing is never read as no landing (R-1383).
        """
        return landed_inbox_playlists(self.cfg)

    @property
    def mirrors(self) -> dict[str, frozenset[str]]:
        """Each account playlist's INBOX playlists, as the landing records name them (U128)."""
        return self.landings[0]

    @cached_property
    def stopped(self) -> tuple[dict[str, tuple[Any, Any]], tuple[str, ...]]:
        """Each pair's write stopped part way through its order, and the runs' steps unread (U225).

        Read from every run's kept steps and every pair's carried steps
        (R-1372), so a stop is never forgotten while its pair is unfinished. A
        carried record gives way to its own run's steps under the same plan,
        since they say whether the pair finished.
        """
        from cratekit.sync import held_plan

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

        A snapshot that cannot be read as a moment places no write after it,
        so nothing is finished. A write begun before the pair was marked is
        another pair's, since a carried record outlives a pair marked again
        (R-1372).
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

        Read whatever the mark, since the stop predates it, so a first sync
        never puts the stopped write's scramble into rekordbox; FOR ITS ORDER
        ALONE, since its bases are another pair's and a first sync folds none.
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

        A landed row is the library's copy whichever playlist brought it, so a
        pair adds it and never downloads the track again.
        """
        every: set[str] = set()
        for ids in self.mirrors.values():
            every.update(ids)
        return landed_isrcs(self.cfg, self.db, every, read=self.mirror_codes)

    def job_reports(
        self, job: jobs.Job, *, own: bool = True
    ) -> tuple[dict[str, Any], ...] | None:
        """One finished intake job's reports, None when they cannot be read, read once per plan.

        A job whose frozen configuration no longer reads refuses only the plan
        of the pair that queued it, and is passed over by every other pair's
        (``own`` false, U229).
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

        Remote id to each holding job's account playlist and name, newest first.
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

    Every failure to read answers empty, leaving the row unmatched and named,
    as ``outbound.source.file_identity`` does for a collection export's row.
    Callers in sync write ``pair_read.file_identity``, so a suite that replaces
    it here reaches them; organize reads it through ``pair_cli`` (U304).
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

    Public for the twins' backfill (U149). THE UNREAD HALF IS KEPT (R-1383),
    since an unreadable record cannot say whether its landing stands, so none
    is read as no landing.
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
    """ISRC to content ids, read from the files of the INBOX playlists named (U128).

    A landed row's code may be only in its file. ``read`` reads one playlist's
    codes, :func:`mirror_codes` unless a caller keeps its own copy (U229).
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
