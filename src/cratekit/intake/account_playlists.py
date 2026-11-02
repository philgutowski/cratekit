"""Which playlist on the account each file of a landing came from (U113).

A pass sweeps the playlists the author made on the streaming account, and each
one becomes an INBOX playlist of its own, named as the account names it with
the landing's date at the end (U175), holding every track of it the library
holds (U128). This module answers the
one question that needs: which of the files about to land did which playlist
ask for, and which tracks it already owned. The name itself is chosen by :func:`cratekit.intake.batch_name.inbox_names`
and written by whichever medium lands the batch.

WHAT A PLAYLIST ASKED FOR IS READ FROM ITS JOB, never from the account again.
``crate sync all`` queues one ``intake.playlist`` job per playlist and records
the account's name for it on the job (``intake_cli.PLAYLIST_NAME``). Each item's
committed report says what the track resolved to, and the rows a landing can
carry are the ones the download was made from, ``missing`` and ``offered``. A
job with no recorded name, queued by a build before this unit or by ``crate
intake playlist`` alone, claims nothing, so its files stay in the batch's own
playlist exactly as they did. The hearts are a job of the same key and are not
a playlist the author made, so they claim nothing either.

A FILE IS TIED TO A ROW BY THE PRODUCT'S OWN MATCH RULE, for the reason the
label filing gives: ``acquire download`` stamps no provider id on a file. The
index is of THE FILES THE LANDING PLANNED and nothing else, since download
staging also holds partial downloads of attempts that never finished. A row
that resolves only to something close, a different version, claims nothing,
and the file stays in the batch's playlist rather than being filed by a guess.

A TRACK TWO PLAYLISTS BOTH ASKED FOR IS A MEMBER OF BOTH. The download fetched
it once, and each playlist's rows resolve to that one file.

THE INBOX PLAYLIST MIRRORS THE WHOLE ACCOUNT PLAYLIST, OWNED TRACKS INCLUDED
(U128), the author's decision of R-905 on 2026-10-10, reversing the 2026-10-03
choice of new tracks only, which left a playlist the library mostly owned thin
or empty in INBOX. Every report of the playlist's job is read in item order,
which is the account playlist's order. A carried row tied to a planned file is
a NEW member; a row the report called owned is an OWNED member, carrying the
library files the report resolved it to, and each medium finds that file's row
by path, the database's on the native medium and the export's entry on the
bridge. A row that is neither is LEFT, and the landing names it in a warning
rather than leaving it silently absent: a download refused as lossy, a row only
something close answered, a suppressed track.

A RERUN OF THE SAME PASS ADDS NOTHING TWICE. Each landing records, beside every
account playlist it wrote, the account's identifier and the pass. A later
landing of the same pass finds that record and holds, for that playlist, only
the new files it brings, U113's rule, so an owned track already mirrored is not
mirrored a second time under the next free name.

THE HEARTS ARE TIED TO THEIR FILES THE SAME WAY, SINCE U120, and for another
purpose: a file the pass's hearts job asked for is a heart, and the landing
puts it into All Favorites and its month beside its INBOX playlist (by
quarter until U145). The hearts claim no INBOX playlist of their own, as
before. The month is read
from the date the job froze on the row (``intake_cli.HEARTED``), never from
the account again, and a row frozen with no date is an undated heart.

AND AN OWNED HEART JOINS TOO, SINCE U146, the author's answer of 2026-10-14
to U120's open question: a heart on a track the library already held when
the job ran is a favourite all the same. Its row is found by the paths the
report resolved it to (:func:`owned_hearts`), the way an owned member of an
account playlist is, and the landing places it whether or not it brought a
file.

Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from cratekit.acquire import match, match_cli
from cratekit.core import config, jobs, session
from cratekit.favorites import placeholders
from cratekit.intake import batch_name, ingest, native
from cratekit.intake import cli as intake_cli

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
    the library files an owned row resolved to, an OWNED member, whose row each
    medium finds by path before the gate (:func:`resolve_owned`) and keeps in
    ``row``: the content row's id on the native medium, the export's TrackID
    on the bridge.
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
class Left:
    """One row of an account playlist its INBOX playlist does not hold, and why."""

    position: int
    artist: str
    title: str
    state: str
    why: str

    def identity(self) -> dict[str, Any]:
        return {
            "position": self.position,
            "artist": self.artist,
            "title": self.title,
            "state": self.state,
            "why": self.why,
        }


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

        THE OWNED MEMBERS, BY THE ROW EACH WAS FOUND AS, AND THE LEFT ROWS are
        keys added only when there are any, so a claim of new files alone keeps
        the keys it had before U128; its files are listed in the account
        playlist's order since then.
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
    #: Whether the job SAID anything about the date: a row frozen by a build
    #: before U120 carries no key at all, and its month is nobody's to guess.
    known: bool = True
    #: The library files an owned report resolved the row to, the report's
    #: own (U146), and nothing for a row the job downloaded.
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
    """The rows a hearts job's download was made from, each with its frozen date.

    THE SAME STATES A PLAYLIST'S CLAIM READS BY DEFAULT, ``missing`` and
    ``offered``, the rows a landing's files can answer. The date is the row's
    own frozen key, read as the job froze it.

    ``states=None`` reads EVERY row whatever its state, for a reader that wants
    the job's hearts rather than its downloads: ``crate favorites split``
    (U145) dates the hearts the quarters hold, and ``crate favorites
    backfill`` (U146) places every heart the library owns. ``{OWNED}`` is the
    landing's owned hearts (U146), each carrying the files its report named.
    One reader of the frozen rows, so the three cannot disagree about a
    heart's date or its identifier.
    """
    from cratekit.intake import missing_cli

    found: list[HeartRow] = []
    for report in missing_cli.job_reports(store, job):
        if states is not None and report.get("state") not in states:
            continue
        said = report.get("track") or {}
        wanted = intake_cli.thawed(said)
        found.append(
            HeartRow(
                wanted=wanted,
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

    ONE RULE FOR THE LANDING AND THE BACKFILL: the first mention, unless a
    later one knows the date where the first did not, since a job frozen by
    this build knows and an older one does not, and two readers that chose
    differently would put one heart in two months.
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

    THE REPORT'S OWN ANSWER, read with the files it resolved each row to, as
    an owned member of an account playlist is: the job ran the match rule
    when it listed the hearts, and the landing finds the row for each file by
    path on its own handle. A landing of no pass has no job to read, so it
    has no owned hearts, as it has no hearts.

    ONLY WHILE THE PASS HOLDS THE NEWEST HEARTS JOB ON THE LIBRARY. The job is
    a snapshot of the account, and a heart the author dropped since, un-hearted
    and taken out of All Favorites, is still owned in it; a later pass's job is
    the account's later word, so landing an older pass places no owned heart
    and leaves them to the latest pass and the backfill, which lists the
    account.
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


def hearted(
    cfg: config.Config, pass_name: str | None, files: Sequence[Path]
) -> tuple[Hearted, ...]:
    """Which of the planned ``files`` the pass's hearts asked for, with each one's month.

    THE ONE MATCH RULE :func:`claims` USES, over the planned files only, and
    the same answer for a landing of no pass: nothing, since no job ties a
    file to a heart then (a residual of U120, placed later by the backfill).
    A heart two rows resolve to one file for is one heart, the first row's.
    """
    if not pass_name or not files:
        return ()
    rows = hearts(cfg, pass_name)
    if not rows:
        return ()
    index = match.index_paths(files, template=match_cli.library_template(cfg))
    planned = {path.resolve(): path for path in files}
    order = {path: position for position, path in enumerate(files)}
    found: dict[Path, Hearted] = {}
    for row in rows:
        resolved = match.resolve_one(
            row.wanted,
            index,
            suppresses=_never_suppressed,
            suppression_id=_no_suppression_id,
        )
        if resolved.state is not match.MatchState.MATCHED:
            continue
        for path in resolved.paths:
            held = planned.get(Path(path).resolve())
            if held is not None and held not in found:
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

    The jobs are :func:`batch_name.pass_jobs`'s, the ones that SUCCEEDED, which
    is the comparison ``sync mark`` makes and the set the batch is named for. A
    job whose reports cannot be read refuses, through the reader ``intake
    missing`` and ``sync mark`` share, and the refusal comes before the gate,
    since the landing could not say which playlist its files belong to.
    """
    named = playlist_jobs(cfg, pass_name)
    with jobs.open_store() as store:
        return tuple(read_source(store, job, name) for job, name in named)


def playlist_jobs(cfg: config.Config, pass_name: str) -> tuple[tuple[jobs.Job, str], ...]:
    """Each account playlist job of the pass and the account's name for it, no report read.

    IN THE ORDER THE SWEEP QUEUED THEM, which the store lists newest first. The
    refill (U134) finds every INBOX playlist from these before it reads one
    report, so a playlist it must refuse is refused before the account's
    tracks are read.
    """
    queued = sorted(
        batch_name.pass_jobs(cfg, pass_name), key=lambda job: (job.created, job.job_id)
    )
    return tuple((job, name) for job in queued if (name := _named(job)) is not None)


def account_of(job: jobs.Job) -> str:
    """The account's identifier for the playlist the job was queued for."""
    return str((job.payload or {}).get(intake_cli.SOURCE) or "")


def read_source(store, job: jobs.Job, name: str) -> Source:
    """One account playlist job as a :class:`Source`, every report in item order."""
    from cratekit.intake import missing_cli

    reports = missing_cli.job_reports(store, job)
    return Source(
        playlist_id=account_of(job),
        name=name,
        job_id=job.job_id,
        # EVERY REPORT, IN ITEM ORDER, which is the order the sweep froze the
        # account playlist's tracks in (U128).
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

    READ FROM THE LANDING RECORDS, both media's, which name each account
    playlist they wrote with the account's identifier and the pass since U128.
    A record counts while its landing stands: an intake file waiting on its
    import, a commit not yet vouched for, or a closed record. An abandoned one
    does not, since the person discarded what it would have written. An entry
    written before U128 names no account and counts for nothing, which is
    right, since it never held an owned track.
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


def _never_suppressed(_recording: str, _address: object) -> bool:
    """No tombstone is consulted: a row is tied to a file this landing holds or to none."""
    return False


def _no_suppression_id(_recording: str, _address: object) -> str:
    return ""


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

    ``files`` are the landing's planned files. A carried row is a NEW member
    for each planned file the match rule ties it to, an owned row an OWNED
    member carrying its report's library files, and every other row is LEFT
    with why (U128). A file two rows answer, or a library file two owned rows
    name, is one member, at the first row's place.

    ``mirrored`` names the account playlists an earlier landing of the same
    pass already mirrored (:func:`mirrored`): each holds only the new files
    here, U113's rule, and lists nothing as left, since that landing named
    them. ``template`` is the library's naming template, which is
    ``match_cli.library_view``'s builder rule.
    """
    if not found or not files:
        return ()
    index = match.index_paths(files, template=template)
    planned = {path.resolve(): path for path in files}
    order = {path: position for position, path in enumerate(files)}
    again = set(mirrored)
    claimed: list[Claim] = []
    for source in found:
        rerun = source.playlist_id in again
        members: list[Member] = []
        seen: set[Path | tuple[str, ...]] = set()
        left: list[Left] = []
        for row in source.rows:
            if row.carried:
                resolved = match.resolve_one(
                    row.wanted,
                    index,
                    suppresses=_never_suppressed,
                    suppression_id=_no_suppression_id,
                )
                tied = (
                    sorted(
                        {
                            planned[Path(path).resolve()]
                            for path in resolved.paths
                            if Path(path).resolve() in planned
                        },
                        key=order.__getitem__,
                    )
                    if resolved.state is match.MatchState.MATCHED
                    else []
                )
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

    Nothing for a landing given no pass, which is a landing of files nobody
    can trace to a playlist, and nothing for a plan of no files.
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

    ONE RULE FOR BOTH MEDIA, asked BEFORE THE GATE so the screen and the
    digest name the rows the write joins to each playlist. ``rows`` are the
    database's content rows on the native medium and the export's collection
    entries on the bridge, each a :class:`cratekit.write.trees.ContentRow`.
    A member's files are tried in the report's order and the first one active
    row holds is the answer. A file two active rows claim is not an answer,
    the set playlist's rule (U121), since the playlist would hold whichever
    the index yielded first. A member no row answers is left, with why.

    A claim left holding nothing is not a playlist to write, and its left rows
    are answered beside the claims by its name, so the landing still names
    them.
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

    Rekordbox has not seen such a file, so no Fresh Export holds its playlists,
    and a second landing named only against the export would give one of them
    the same name. Read from the intake records, which list each by name.
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


__all__ = [
    "ACCOUNT_KEY",
    "CARRIED_STATES",
    "LEFT_OUT",
    "NOT_LANDED",
    "NO_ROW",
    "AMBIGUOUS_ROWS",
    "PASS_KEY",
    "Claim",
    "Claimed",
    "HeartRow",
    "Hearted",
    "Left",
    "Member",
    "Row",
    "Source",
    "account_of",
    "carried_hearts",
    "claims",
    "hearted",
    "hearts",
    "is_hearts_job",
    "left_warning",
    "mirrored",
    "named",
    "owned_hearts",
    "pending_names",
    "playlist_jobs",
    "prefer_dated",
    "read_source",
    "resolve_owned",
    "sources",
    "split",
    "unclaimed",
]
