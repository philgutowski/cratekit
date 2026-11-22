"""Which playlist on the account each file of a landing came from (U113).

Each playlist a pass swept on the streaming account becomes an INBOX playlist
of its own (U175) holding every track of it the library holds (U128). What a
playlist asked for is read from its job, never from the account again, and a
job with no recorded name, or the hearts, claims nothing.

A FILE IS TIED TO A ROW BY THE PRODUCT'S OWN MATCH RULE over the files the
landing planned and nothing else, since ``acquire download`` stamps no id and
staging holds partial downloads; a row only something close answers claims
nothing. Owned tracks are mirrored too (U128, R-905), by their report's
library files; anything else is LEFT and named. A rerun of a pass mirrors
nothing twice. The hearts are tied the same way (U120), dated from the job's
frozen row, and an owned heart joins too (U146).

Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from cratekit.acquire import match, match_cli
from cratekit.core import config, jobs, session
from cratekit.intake import batch_name, ingest, native
from cratekit.intake import cli as intake_cli

#: One row of an account playlist its INBOX playlist does not hold, and why:
#: the row a set's playlist leaves out, which is the same five fields.
from cratekit.intake.set_playlist import Left, _never_suppressed, _no_suppression_id

#: The report states a landing's files were downloaded for. ``owned`` and
#: ``suppressed`` rows were never downloaded, so no file of the landing is theirs.
CARRIED_STATES = frozenset({"missing", "offered"})

#: The job key a playlist of the account is queued under.
PLAYLIST_KEY = "intake.playlist"

#: The report state of a row the library already held when the job ran.
OWNED = "owned"

#: The keys an ``inbox_playlists`` record entry carries since U128, beside its
#: name: the account's identifier for the playlist and the pass that landed it.
ACCOUNT_KEY = ingest.INBOX_ACCOUNT_KEY
PASS_KEY = ingest.INBOX_PASS_KEY

#: Why a row of an account playlist is not in its INBOX playlist, as a person reads it.
NOT_BROUGHT = "neither owned nor landed by this landing"
SUPPRESSED = "suppressed"
NO_PATH = "owned, with no library file recorded for it"
NO_ROW = "owned on disk, and the collection holds no row for its file"
AMBIGUOUS_ROWS = "owned on disk, and two collection rows claim its file"
NOT_LANDED = native.NOT_LANDED

#: The warning code a landing names its left rows under.
LEFT_OUT = "account-playlist-left-out"


@dataclass(frozen=True, slots=True)
class Row:
    """One report of a playlist's job, in the account playlist's order (U128)."""

    position: int
    state: str
    wanted: match.Wanted
    #: The library files an owned report resolved the row to, the report's own.
    paths: tuple[str, ...] = ()

    @property
    def carried(self) -> bool:
        return self.state in CARRIED_STATES


@dataclass(frozen=True, slots=True)
class Source:
    """One playlist on the account a pass swept, and every row its job reported."""

    playlist_id: str
    #: The account's name for it, exactly as the sweep listed it.
    name: str
    job_id: str
    rows: tuple[Row, ...]

    @property
    def wanted(self) -> tuple[match.Wanted, ...]:
        """The rows a download was made from, the ones a planned file can answer."""
        return tuple(row.wanted for row in self.rows if row.carried)


@dataclass(frozen=True, slots=True)
class Member:
    """One track an INBOX playlist holds, in the account playlist's order (U128).

    ``file`` is a planned file this landing brings, a NEW member; ``paths`` are
    the library files an owned row resolved to, an OWNED member, whose row
    each medium finds by path before the gate (:func:`resolve_owned`) and keeps
    in ``row``: the content row's id natively, the export's TrackID on the bridge.
    """

    position: int
    file: Path | None = None
    paths: tuple[str, ...] = ()
    row: str = ""
    #: The row's words and report state, for the warning when no row is found.
    artist: str = ""
    title: str = ""
    state: str = ""

    def left(self, why: str) -> Left:
        """This member as a row its playlist does not hold, because ``why``."""
        return Left(self.position, self.artist, self.title, self.state, why)


@dataclass(frozen=True, slots=True)
class Claim:
    """What one playlist on the account claims of a landing, before it is named."""

    source: Source
    members: tuple[Member, ...]
    left: tuple[Left, ...] = ()

    @property
    def files(self) -> tuple[Path, ...]:
        """The planned files among the members, in the account playlist's order."""
        return tuple(one.file for one in self.members if one.file is not None)


@dataclass(frozen=True, slots=True)
class Claimed:
    """One INBOX playlist a landing writes for one playlist on the account."""

    #: The name it lands as, the account's own or that with `` 2`` and on.
    name: str
    #: The account's name for it, which ``name`` differs from only by a count.
    account_name: str
    playlist_id: str
    #: Every member, new and owned, in the account playlist's order (U128).
    members: tuple[Member, ...] = ()
    #: The rows of the account playlist it does not hold, each with why.
    left: tuple[Left, ...] = ()

    @property
    def files(self) -> tuple[Path, ...]:
        """The planned files it holds, in the account playlist's order."""
        return tuple(one.file for one in self.members if one.file is not None)

    @property
    def owned(self) -> int:
        return sum(1 for one in self.members if one.file is None)

    def identity(self) -> dict[str, Any]:
        """What a gate's digest covers for it, so another split is another plan.

        The owned members and the left rows are keys only when there are any,
        so a claim of new files alone keeps the digest it had before U128.
        """
        identity: dict[str, Any] = {
            "name": self.name,
            "account": self.playlist_id,
            "files": [path.name for path in self.files],
        }
        if self.owned:
            identity["members"] = [
                one.file.name if one.file is not None else {"paths": list(one.paths), "row": one.row}
                for one in self.members
            ]
        if self.left:
            identity["left"] = [one.identity() for one in self.left]
        return identity


@dataclass(frozen=True, slots=True)
class HeartRow:
    """One heart a hearts job carried: the row, and when the account said it was made."""

    wanted: match.Wanted
    hearted: datetime | None
    #: The provider's identifier, the job's item key.
    ref: str
    job_id: str
    #: Whether the job said anything about the date: a row frozen before U120
    #: carries no key, and its month is nobody's to guess.
    known: bool = True
    #: The library files an owned report resolved the row to (U146).
    paths: tuple[str, ...] = ()

    @property
    def title(self) -> str:
        return f"{self.wanted.artist} - {self.wanted.spelled or self.wanted.title}"


@dataclass(frozen=True, slots=True)
class Hearted:
    """One planned file that is a heart, and the month playlist it goes to (U120, U145)."""

    path: Path
    hearted: datetime | None
    ref: str
    known: bool = True

    @property
    def month(self) -> str | None:
        """The month playlist, ``Undated`` for a heart the account dates nowhere,
        and None for one whose job never said, which the backfill dates later."""
        from cratekit.favorites import placeholders  # noqa: PLC0415 - favorites is toggleable

        return placeholders.month_label(self.hearted) if self.known else None


def is_hearts_job(job: jobs.Job) -> bool:
    """Whether ``job`` listed the account's hearts, whatever queued it."""
    return (
        job.handler_key in intake_cli.INTAKE_KEYS
        and str((job.payload or {}).get("source_id") or "") == intake_cli.FAVORITES_SOURCE_ID
    )


def carried_hearts(
    store, job: jobs.Job, *, states: frozenset[str] | None = CARRIED_STATES
) -> tuple[HeartRow, ...]:
    """The rows of a hearts job in ``states``, each with its frozen date.

    By default the rows a landing's files can answer. ``states=None`` reads
    every row, for ``crate favorites split`` (U145) and ``backfill`` (U146);
    ``{OWNED}`` is the landing's owned hearts. One reader of the frozen rows,
    so no two can disagree about a heart's date or identifier.
    """
    from cratekit.favorites import placeholders  # noqa: PLC0415 - favorites is toggleable
    from cratekit.intake import missing_cli

    found: list[HeartRow] = []
    for report in missing_cli.job_reports(store, job):
        if states is not None and report.get("state") not in states:
            continue
        said = report.get("track") or {}
        found.append(
            HeartRow(
                wanted=intake_cli.thawed(said),
                hearted=placeholders.parse_hearted(said.get(intake_cli.HEARTED)),
                ref=str(said.get("ref") or report.get("item_id") or ""),
                job_id=job.job_id,
                known=intake_cli.HEARTED in said,
                paths=tuple(str(path) for path in (report.get("paths") or ())),
            )
        )
    return tuple(found)


def prefer_dated(held: HeartRow | None, row: HeartRow) -> bool:
    """Whether ``row`` is the mention of a heart to keep over ``held``.

    One rule for the landing and the backfill, the first mention unless a
    later one knows the date, or two readers would put one heart in two months.
    """
    return held is None or (not held.known and row.known)


def hearts(
    cfg: config.Config, pass_name: str, *, states: frozenset[str] | None = CARRIED_STATES
) -> tuple[HeartRow, ...]:
    """Every heart the pass's hearts jobs reported in ``states``, in queue order, a row once."""
    found: dict[str, HeartRow] = {}
    with jobs.open_store() as store:
        queued = sorted(
            batch_name.pass_jobs(cfg, pass_name), key=lambda job: (job.created, job.job_id)
        )
        for job in queued:
            if not is_hearts_job(job):
                continue
            for row in carried_hearts(store, job, states=states):
                if prefer_dated(found.get(row.ref), row):
                    found[row.ref] = row
    return tuple(found.values())


def owned_hearts(cfg: config.Config, pass_name: str | None) -> tuple[HeartRow, ...]:
    """The hearts the pass's hearts jobs found the library already held (U146).

    The report's own answer with its files, as for an owned account playlist
    member. Only while the pass holds the newest hearts job on the library:
    a job is a snapshot of the account, so an older pass's owned hearts may
    have been dropped since and are left to the latest pass and the backfill.
    """
    if not pass_name:
        return ()
    with jobs.open_store() as store:
        mine = [job for job in batch_name.pass_jobs(cfg, pass_name) if is_hearts_job(job)]
        if not mine:
            return ()
        newest = max((job.created, job.job_id) for job in mine)
        superseded = any(
            (job.created, job.job_id) > newest
            for job in batch_name.succeeded_intake_jobs(store, cfg)
            if is_hearts_job(job)
        )
    if superseded:
        return ()
    return hearts(cfg, pass_name, states=frozenset({OWNED}))


def _tied(
    wanted: match.Wanted, index: Any, planned: dict[Path, Path], order: dict[Path, int]
) -> list[Path]:
    """The planned files the match rule ties ``wanted`` to, in plan order; none unless MATCHED."""
    resolved = match.resolve_one(
        wanted, index, suppresses=_never_suppressed, suppression_id=_no_suppression_id
    )
    if resolved.state is not match.MatchState.MATCHED:
        return []
    return sorted(
        {
            planned[Path(path).resolve()]
            for path in resolved.paths
            if Path(path).resolve() in planned
        },
        key=order.__getitem__,
    )


def _plan_index(files: Sequence[Path], template: Any):
    """The match index over the planned files, each resolved path's file, and its place."""
    index = match.index_paths(files, template=template)
    return index, {path.resolve(): path for path in files}, {p: i for i, p in enumerate(files)}


def hearted(
    cfg: config.Config, pass_name: str | None, files: Sequence[Path]
) -> tuple[Hearted, ...]:
    """Which of the planned ``files`` the pass's hearts asked for, with each one's month.

    The one match rule :func:`claims` uses, over the planned files only, and
    nothing for a landing of no pass (placed later by the backfill). A file
    two rows resolve to is one heart, the first row's.
    """
    if not pass_name or not files:
        return ()
    rows = hearts(cfg, pass_name)
    if not rows:
        return ()
    index, planned, order = _plan_index(files, match_cli.library_template(cfg))
    found: dict[Path, Hearted] = {}
    for row in rows:
        for held in _tied(row.wanted, index, planned, order):
            if held not in found:
                found[held] = Hearted(path=held, hearted=row.hearted, ref=row.ref, known=row.known)
    return tuple(sorted(found.values(), key=lambda one: order[one.path]))


def _named(job: jobs.Job) -> str | None:
    """The account's name the job recorded, or None for a job that is not one of his playlists."""
    payload = job.payload or {}
    if job.handler_key != PLAYLIST_KEY:
        return None
    if str(payload.get("source_id") or "") == intake_cli.FAVORITES_SOURCE_ID:
        return None
    name = payload.get(intake_cli.PLAYLIST_NAME)
    if not isinstance(name, str) or not name.strip():
        return None
    return name


def sources(cfg: config.Config, pass_name: str) -> tuple[Source, ...]:
    """Every playlist of the account the pass ``pass_name`` swept, in queue order.

    The pass's SUCCEEDED jobs, the set the batch is named for. A job whose
    reports cannot be read refuses before the gate, since the landing could
    not say which playlist its files belong to.
    """
    named = playlist_jobs(cfg, pass_name)
    with jobs.open_store() as store:
        return tuple(read_source(store, job, name) for job, name in named)


def playlist_jobs(cfg: config.Config, pass_name: str) -> tuple[tuple[jobs.Job, str], ...]:
    """Each account playlist job of the pass and the account's name for it, no report read.

    In the order the sweep queued them, so the refill (U134) can refuse a
    playlist before the account's tracks are read.
    """
    queued = sorted(
        batch_name.pass_jobs(cfg, pass_name), key=lambda job: (job.created, job.job_id)
    )
    return tuple((job, name) for job in queued if (name := _named(job)) is not None)


def account_of(job: jobs.Job) -> str:
    """The account's identifier for the playlist the job was queued for."""
    return str((job.payload or {}).get(intake_cli.SOURCE) or "")


def read_source(store, job: jobs.Job, name: str) -> Source:
    """One account playlist job as a :class:`Source`, every report in item order (U128)."""
    from cratekit.intake import missing_cli

    reports = missing_cli.job_reports(store, job)
    return Source(
        playlist_id=account_of(job),
        name=name,
        job_id=job.job_id,
        rows=tuple(
            Row(
                position=position,
                state=str(report.get("state") or ""),
                wanted=intake_cli.thawed(report["track"]),
                paths=tuple(str(path) for path in (report.get("paths") or ())),
            )
            for position, report in enumerate(reports, start=1)
        ),
    )


def mirrored(cfg: config.Config, pass_name: str) -> frozenset[str]:
    """The account playlists an earlier landing of ``pass_name`` already gave an INBOX playlist.

    Read from both media's landing records, which name each account playlist
    with the pass since U128. A record counts while its landing stands, not
    once abandoned, since the person discarded what it would have written.
    """
    standing = {
        session.SessionState.AWAITING_IMPORT,
        session.SessionState.COMMITTED_UNVERIFIED,
        session.SessionState.CLOSED,
    }
    records, _unreadable = session.scan_log(cfg)
    return frozenset(
        str(entry[ACCOUNT_KEY])
        for record in records
        if record.workflow == ingest.INTAKE_WORKFLOW and record.state in standing
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ()
        if isinstance(entry, dict)
        and entry.get(ACCOUNT_KEY)
        and entry.get(PASS_KEY) == pass_name
    )


def _member(row: Row, *, file: Path | None = None) -> Member:
    return Member(
        position=row.position,
        file=file,
        paths=() if file is not None else row.paths,
        artist=row.wanted.artist,
        title=row.wanted.listed,
        state=row.state,
    )


def _left(row: Row, why: str) -> Left:
    return _member(row).left(why)


def claims(
    found: Sequence[Source],
    files: Sequence[Path],
    *,
    template: Any = None,
    mirrored: Iterable[str] = (),
) -> tuple[Claim, ...]:
    """Each source's members in the account playlist's order, sources that hold none left out.

    A carried row is a NEW member for each planned file the match rule ties it
    to, an owned row an OWNED member carrying its report's library files, and
    any other row is LEFT with why (U128). A file two rows answer is one
    member, at the first row's place. A playlist in ``mirrored`` holds only
    the new files and lists nothing left, since the earlier landing named them.
    """
    if not found or not files:
        return ()
    index, planned, order = _plan_index(files, template)
    again = set(mirrored)
    claimed: list[Claim] = []
    for source in found:
        rerun = source.playlist_id in again
        members: list[Member] = []
        seen: set[Path | tuple[str, ...]] = set()
        left: list[Left] = []
        for row in source.rows:
            if row.carried:
                tied = _tied(row.wanted, index, planned, order)
                if not tied:
                    left.append(_left(row, NOT_BROUGHT))
                for path in tied:
                    if path not in seen:
                        seen.add(path)
                        members.append(_member(row, file=path))
                continue
            if rerun:
                continue
            if row.state != OWNED:
                left.append(_left(row, SUPPRESSED if row.state == SUPPRESSED else NOT_BROUGHT))
                continue
            if not row.paths:
                left.append(_left(row, NO_PATH))
                continue
            if row.paths not in seen:
                seen.add(row.paths)
                members.append(_member(row))
        if members:
            claimed.append(
                Claim(source=source, members=tuple(members), left=() if rerun else tuple(left))
            )
    return tuple(claimed)


def split(cfg: config.Config, pass_name: str | None, files: Sequence[Path]) -> tuple[Claim, ...]:
    """What each playlist of the account the pass swept holds of this landing.

    Nothing for a landing given no pass, whose files nobody can trace to a
    playlist, and nothing for a plan of no files.
    """
    if not pass_name or not files:
        return ()
    found = sources(cfg, pass_name)
    if not found:
        return ()
    return claims(
        found,
        files,
        template=match_cli.library_template(cfg),
        mirrored=mirrored(cfg, pass_name),
    )


def named(claimed: Sequence[Claim], held: Iterable[str], *, batch: str) -> tuple[Claimed, ...]:
    """Each claim with the INBOX name it lands as, given the names INBOX holds."""
    names = batch_name.inbox_names((one.source.name for one in claimed), held, batch=batch)
    return tuple(
        Claimed(
            name=name,
            account_name=one.source.name,
            playlist_id=one.source.playlist_id,
            members=one.members,
            left=one.left,
        )
        for name, one in zip(names, claimed, strict=True)
    )


def resolve_owned(
    cfg: config.Config, claimed: Sequence[Claimed], rows: Iterable[Any]
) -> tuple[tuple[Claimed, ...], tuple[tuple[str, Left], ...]]:
    """Each claim with its owned members' rows found by path, and the left rows of the emptied ones.

    One rule for both media, asked before the gate so the screen and digest
    name the rows joined. ``rows`` are :class:`cratekit.write.trees.ContentRow`
    entries. A member's files are tried in order and the first one active row
    holds answers; a file two active rows claim is no answer (U121). A claim
    left holding nothing is not written, its left rows answered by its name.
    """
    from cratekit.core import locations
    from cratekit.write import trees

    wanted = {one.paths for each in claimed for one in each.members if one.file is None}
    found: dict[tuple[str, ...], tuple[str, str]] = {}
    if wanted:
        prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
        index = trees.index_active_rows(rows, root=cfg.library.root, prefix_map=prefix_map)
        for paths in wanted:
            answer = ("", NO_ROW)
            for matched in trees.match_indexed_rows(
                paths, index, root=cfg.library.root, prefix_map=prefix_map
            ):
                if matched.outcome is trees.MatchOutcome.AMBIGUOUS:
                    answer = ("", AMBIGUOUS_ROWS)
                    continue
                if matched.outcome is trees.MatchOutcome.MATCHED and matched.content_id:
                    answer = (str(matched.content_id), "")
                    break
            found[paths] = answer
    kept: list[Claimed] = []
    emptied: list[tuple[str, Left]] = []
    for one in claimed:
        members: list[Member] = []
        left = list(one.left)
        for member in one.members:
            if member.file is not None:
                members.append(member)
                continue
            row, why = found[member.paths]
            if row:
                members.append(replace(member, row=row))
            else:
                left.append(member.left(why))
        if members:
            kept.append(replace(one, members=tuple(members), left=tuple(left)))
        else:
            emptied.extend((one.name, row) for row in left)
    return tuple(kept), tuple(emptied)


def left_warning(left: Sequence[tuple[str, Left]]) -> list[dict[str, str]]:
    """The one warning naming every account playlist track its INBOX playlist does not hold."""
    if not left:
        return []
    named_rows = "; ".join(
        f"{playlist} {one.position}. {one.artist} - {one.title} ({one.why})"
        for playlist, one in left
    )
    return [
        {
            "code": LEFT_OUT,
            "message": (
                f"{len(left)} track(s) of the account playlists are not in their INBOX "
                f"playlist, each named with why: {named_rows}"
            ),
        }
    ]


def pending_names(cfg: config.Config) -> tuple[str, ...]:
    """Every account playlist an intake file still waiting on its import names.

    No Fresh Export holds such a file's playlists yet, so a second landing
    named only against the export could give one of them the same name.
    """
    records, _unreadable = session.scan_log(cfg)
    return tuple(
        str(entry["name"])
        for record in records
        if record.workflow == ingest.INTAKE_WORKFLOW
        and record.state is session.SessionState.AWAITING_IMPORT
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ()
        if isinstance(entry, dict) and entry.get("name")
    )


def unclaimed(files: Sequence[Path], claimed: Iterable[Claimed]) -> tuple[Path, ...]:
    """The planned files no account playlist claimed, which stay in the batch's playlist."""
    taken = {path for one in claimed for path in one.files}
    return tuple(path for path in files if path not in taken)
