"""``export.set`` and ``export.archive``: a set as a playlist on the account (R-837).

The source system turns an identified set, or a tracklist somebody typed, into
a private playlist on the streaming account, and once the set has been
downloaded it prefixes that playlist ``DOWNLOADED `` and files it in a root
folder named for the year the set was processed. These two verbs are those two
steps, each behind one explicit gate.

``export set TRACKLIST`` READS THE LIST THE INTAKE VERBS READ, the text file
``intake identify`` writes or one somebody typed, or a list document, through
``match_cli.read_list``. Neither text form carries an ISRC or a provider
identifier, and the account's own match never searches by title (R-356), so a
row is decided by the first of four that applies, and the plan writes nothing
on the way:

1. the provider identifier the row carries, which only a list document has;
2. its ISRC, through the account's own match, which chooses among releases;
   a row carrying none is asked of the library, and the ISRC and album the
   file it holds for the row carries go down the same match (R-879, R-572);
3. a provider candidate a person already accepted in review for the row,
   ``intake missing``'s own question, read and never offered here;
4. the catalogue's text search, read page by page within a bound and listed
   only on ``candidates.sole_exact``'s one distinct exact candidate, never on a
   score.

Anything else is LEFT OUT AND NAMED, with its reason, on the gate screen, in the
items and in a warning, as ``export playlist`` names its own (R-850). A second
run onto the same set reuses the playlist recorded under its name and plans
nothing when every matched track is on it.

``export archive NAME --xml INTAKE`` IS THE STEP AFTER THE DOWNLOAD. The intake
file ``intake land`` wrote is the proof it landed and names the pass, on
``sync/marks.py``'s rule that a title is changed only once the importable file
is on disk. The rename is recorded in ``sync mark``'s record under that pass,
so ``sync unmark --pass`` takes it off. A landing of a set (U129) runs the same
archive body behind its own gate once the batch is in the library, and a
backfill over INSPIRATION playlists that have no account playlist yet plans
both steps behind one gate each.

``export set --rename JOB`` FOLLOWS A RENAME IN THE LIBRARY (U140). A person
who renamed a set's INSPIRATION playlist left its account playlist, the
ledger's key and the job's frozen name on the old one, and a backfill then
read the set as having no account playlist and made a twin. The rename reads
the INSPIRATION playlist's live name and, behind its own gate, retitles the
account playlist by identifier, moves the ledger key and refreezes the job.

Layer: modules. The builders' parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

import shlex
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, review, secrets, tags
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.export.cli import UNMATCHED_WARNING
from cratekit.intake import candidates
from cratekit.intake.cli import PLAYLIST_NAME, TRACKLIST_SUFFIX
from cratekit.label import catalogue
from cratekit.modules.outbound import ledger, sets, shell
from cratekit.sync import mark_record, marks
from cratekit.sync.mark_cli import pass_name_of

_SET = ("export.set",)
_ARCHIVE = ("export.archive",)

#: What a row is in the plan, one word each.
ADD = "add"
ALREADY = "already"
UNMATCHED = "unmatched"
#: Matched, and the provider would not add it when it was asked before.
REFUSED = "refused"
#: Matched, recorded as written, and no longer on the playlist: a person took
#: it off, and it is not put back.
TAKEN_OFF = "taken-off"
#: The same track as an earlier row of the set, asked for once.
REPEAT = "repeat"

#: How a row was matched when the ISRC came off the library's own file.
LIBRARY_ISRC = "library-isrc"

_ROW_WHY = {
    REFUSED: "the provider would not add it when it was asked before, so it is not asked again",
    TAKEN_OFF: "it was written before and is no longer on the playlist, so it is not put back",
    REPEAT: "an earlier row of the set is the same track",
}

#: What the gate screen and the warning say when no set playlist is recorded.
NOTHING_BUILT_SAID = (
    "no set playlist was made under this name on this library, so there is "
    "nothing to archive"
)

#: The file name endings a tracklist is known by, taken off for its name.
#: ``intake identify``'s own first, so its ``.txt`` is not the one taken.
_ENDINGS = (TRACKLIST_SUFFIX, ".list.json", ".txt", ".json")


def build_set(parser, entry) -> None:
    del entry
    parser.add_argument(
        "tracklist",
        nargs="?",
        default=None,
        metavar="TRACKLIST",
        help=(
            "the tracklist intake identify wrote, a typed one, or a list document; "
            "omit it to backfill over INSPIRATION playlists that have no account playlist"
        ),
    )
    parser.add_argument(
        "--name",
        default=None,
        help="the playlist's name on the account; defaults to the tracklist's own",
    )
    parser.add_argument(
        "--rename",
        default=None,
        metavar="JOB",
        help=(
            "rename the set job's account playlist to the name its INSPIRATION "
            "playlist carries now, and record the new name"
        ),
    )
    parser.set_defaults(_handler=export_set)


def build_archive(parser, entry) -> None:
    del entry
    parser.add_argument(
        "name",
        nargs="?",
        default=None,
        metavar="NAME",
        help=(
            "the set playlist's name, as crate export set made it; omit it to "
            "archive every recorded set whose download is proven"
        ),
    )
    parser.add_argument(
        "--xml",
        default=None,
        metavar="XML",
        help="the intake file crate intake land wrote for the set's download",
    )
    parser.set_defaults(_handler=export_archive)


def set_name(given: str) -> str:
    """A set playlist's name as it is made and recorded, and as it is looked up.

    A slash becomes a dash, the source system's rule, since a downloader reads
    one in a playlist name as a folder. ONE SPELLING FOR BOTH VERBS, so a name
    the archive is handed finds the record the build wrote under it.
    """
    return str(given).replace("/", "-").strip()


def name_of(path: Path) -> str:
    """The playlist name a tracklist file gives, when none is asked for.

    The file's own name with its ending off. ``intake identify``'s piece of
    the recording's digest STAYS ON: it is what tells two recordings that share
    a recorder's stem apart (``intake.cli.tracklist_name``), and the name is the
    key the set's playlist is recorded under, so taking it off would add a
    second night's set to the first night's playlist. ``--name`` chooses another.
    """
    stem = path.name
    for ending in _ENDINGS:
        if stem.lower().endswith(ending):
            stem = stem[: -len(ending)]
            break
    return set_name(stem)


def _unnamed(given: str) -> CratekitError:
    return refuse(
        "intake-list-unusable",
        f"the set playlist would be named {given!r}, which is no name, so nothing "
        f"was planned",
        steps=("pass --name with the name the playlist should carry",),
        scope=Scope.RUN,
        origin=_SET,
        detail={"name": given},
    )


class _Deferred:
    """The account, resolved the first time one of its members is asked for.

    A set whose rows need no account before its gate, a list document of
    provider identifiers or of nothing, spends no login and refuses over no
    missing credential until the write it was approved for.
    """

    def __init__(self, cfg: config.Config) -> None:
        self._cfg = cfg
        self._held = None

    def __getattr__(self, name: str) -> Any:
        if self._held is None:
            from cratekit.modules.outbound import account

            self._held = account.resolve(self._cfg)
        return getattr(self._held, name)


# ── matching ────────────────────────────────────────────────────────────────


class _Library:
    """The library as ``intake missing`` sees it, built the first time a row asks.

    A set whose every row carries an identifier or an ISRC walks no music
    volume. A music folder that is not there is SAID, never read as a library
    that holds nothing, on ``intake missing``'s own rule: a row of a set the
    library holds would otherwise be told it is not held.
    """

    def __init__(self, cfg: config.Config) -> None:
        self._cfg = cfg
        self._view: tuple[Any, ...] | None = None
        self.music = Path(cfg.library.root) / cfg.library.music_dir

    def file_isrc(self, one: match.Wanted) -> tuple[str, str, str]:
        """The ISRC and album the library's own file of this row carries, or empties and why.

        ONLY A ROW THE LIBRARY HOLDS, matched at its version by the engine every
        intake verb asks. ONE ISRC OR NONE: held as several files carrying
        different codes, the files do not say which recording the row is, so
        none of them is asked about. The why is empty for a row the library
        does not hold, which is the ordinary case and not a reason.

        THE ALBUM IS READ OFF THE SAME FILE(S) the ISRC came from, the way
        ``source.file_identity`` reads both in one open (R-572). The library
        index does not carry the album tag, so the container is opened here for
        that field alone. Files that agree on one album name hand it on; files
        that disagree, or carry none, hand an empty album and the account's
        album rule then chooses nothing.
        """
        if not self.music.is_dir():
            return "", "", (
                f"the library's music folder {str(self.music)!r} is not there, so "
                f"no file's ISRC could be read for it"
            )
        if self._view is None:
            self._view = match_cli.library_view(self._cfg)
        index, suppresses, identify = self._view
        found = match.resolve_one(one, index, suppresses=suppresses, suppression_id=identify)
        if found.state is not match.MatchState.MATCHED:
            return "", "", ""
        paths = set(found.paths)
        carrying = [
            held
            for held in index.held(one.artist, one.title)
            if str(held.path) in paths and held.isrc
        ]
        codes = {held.isrc for held in carrying}
        if len(codes) == 1:
            return next(iter(codes)), _album_of(carrying), ""
        if codes:
            return "", "", (
                f"the library holds it in {len(paths)} file(s) carrying {len(codes)} "
                f"different ISRCs, so none was asked about"
            )
        return "", "", "the library holds it and its file carries no ISRC"


def _album_of(carrying: Sequence[Any]) -> str:
    """The one album tag the matched files agree on, stripped, or ``""``.

    READ THE WAY ``source.file_identity`` READS IT, from the container, not from
    the library index, which does not carry the album. Several files under one
    ISRC that name different albums leave the tag empty, so the account cannot
    guess which release the row was cut from.
    """
    albums = {
        str(tags.read_tags(held.path, ("album",))["album"] or "").strip()
        for held in carrying
    }
    if len(albums) == 1:
        return next(iter(albums))
    return ""


def _searched(found: catalogue.Catalogue, one: match.Wanted) -> candidates.Answer:
    """One search answer, page by page, or the refusal ``intake missing`` gives when none came."""
    title = candidates.query_title(one)
    try:
        return candidates.search_pages(
            lambda offset: found.search_tracks(one.artist, title, offset=offset), one
        )
    except CratekitError:
        raise
    except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
        raise refuse(
            "unavailable-transient",
            f"the streaming provider could not answer a search for {one.artist} - "
            f"{one.listed} ({exc}), so the set could not be matched; nothing was "
            f"written",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.RUN,
            origin=_SET,
            detail={"artist": one.artist, "title": one.listed},
        ) from exc


#: Where a person can answer a row the search did not settle.
_REVIEW_ROUTE = (
    "; crate intake missing --list over this tracklist offers its candidates for "
    "review when the library lacks the track, and one accepted there is used on "
    "the next run"
)


def _not_chosen(answer: candidates.Answer) -> str:
    """Why a search answer named no track, in words for a person.

    WHICH IT WAS, since each sends a person somewhere different (R-879): none
    found, several found, or the page bound reached with the listing still
    going. The rest are the refusals :func:`candidates.sole_exact` always had.
    """
    if not answer.hits:
        return "the provider's search returned nothing for it"
    read = f"the provider's search returned {answer.hits} hit(s) over {answer.pages} page(s)"
    exact = len(answer.exact_refs)
    if answer.ambiguous and (exact or answer.full):
        said = (
            f"{read} and its title reads two ways, as a version or as the end of "
            f"the title, so no candidate can be called the exact one"
        )
    elif exact > 1:
        said = f"{read} and several match it exactly, {exact} distinct tracks, so none was chosen"
    elif answer.unreadable:
        said = (
            f"{read} and {answer.unreadable} of them could not be read, so an exact "
            f"match among them cannot be ruled out"
        )
    elif any(one.exact and not one.track.ref for one in answer.candidates):
        said = f"{read} and an exact match among them carries no identifier, so none was chosen"
    elif answer.full:
        said = (
            f"{read}, the most read for one row, and the listing goes on past them, "
            f"so the page bound was reached with "
            + (
                "one exact match that may not be the only one"
                if exact
                else "no exact match found"
            )
        )
    else:
        said = f"{read} and none matches it exactly"
    if not candidates.shown(answer):
        if any(one.exact for one in answer.candidates):
            return said
        return f"{said}, and none resembles it"
    return said + _REVIEW_ROUTE


def _isrc_match(
    account,
    identity: str,
    one: match.Wanted,
    code: str,
    *,
    agree: bool,
    album: str = "",
) -> tuple[str, str]:
    """The provider track the account's own ISRC match names, or ``""`` and why not.

    ``agree`` for a code read off the library's file rather than the row: the
    file's tag is this library's statement, not the provider's, so even one
    track under it must agree with the row before it is listed.

    ``album`` is the album tag of that same file, for the account's release
    tie break when several tracks share the ISRC and none is hearted (R-572).
    """
    remote = account.match_track(
        identity=identity,
        isrc=code,
        title=one.listed,
        artist=one.artist,
        agree=agree,
        album=album,
    )
    if remote:
        return str(remote), ""
    whose = "its library file's ISRC" if agree else "its ISRC"
    return "", account.unmatched_reason(identity) or (
        f"the provider names no single track under {whose} {code}"
    )


def match_rows(
    cfg: config.Config, wanted: Sequence[match.Wanted], account
) -> tuple[sets.SetRow, ...]:
    """Each row of the set, matched to one provider track or left out with why.

    THE CATALOGUE IS RESOLVED ONLY WHEN A ROW HAS TO BE SEARCHED FOR, so a list
    document whose every row carries its identifier spends no login on it.

    A ROW CARRYING NO ISRC IS ASKED OF THE LIBRARY BEFORE ANY SEARCH (R-879). A
    typed line carries none, and the file the library holds for it usually
    does, so that file's code goes down the same account match a row's own ISRC
    does, after a person's answer in review and before any search is spent.
    """
    held: list[catalogue.Catalogue] = []
    library = _Library(cfg)
    decided: list[sets.SetRow] = []
    with review.open_store(cfg) as items:
        for position, one in enumerate(wanted, start=1):
            row = {"position": position, "artist": one.artist, "title": one.listed}
            # ONLY THE PROVIDER'S OWN IDENTIFIER, on ``listdoc``'s rule: a list
            # of another origin carries that source's identifier as provenance,
            # and handed to the account it names nothing or the wrong track.
            if one.ref and one.origin == match.TIDAL:
                decided.append(sets.SetRow(**row, remote_id=str(one.ref), how="ref"))
                continue
            said = ""
            identity = f"set-row-{position}"
            if one.isrc:
                remote, said = _isrc_match(account, identity, one, one.isrc, agree=False)
                if remote:
                    decided.append(sets.SetRow(**row, remote_id=remote, how="isrc"))
                    continue
            # A PERSON'S ANSWER BEFORE THE LIBRARY'S FILE, so an acceptance of
            # one release, or a rejection of every candidate, is never
            # overridden by a tag.
            answered = candidates.settled(items, one)
            if answered is not None:
                if answered.state == candidates.ACCEPTED and answered.track is not None:
                    decided.append(
                        sets.SetRow(**row, remote_id=answered.track.ref, how="accepted")
                    )
                else:
                    decided.append(sets.SetRow(**row, reason=answered.reason))
                continue
            if not one.isrc:
                code, album, said = library.file_isrc(one)
                if code:
                    remote, said = _isrc_match(
                        account, identity, one, code, agree=True, album=album
                    )
                    if remote:
                        decided.append(sets.SetRow(**row, remote_id=remote, how=LIBRARY_ISRC))
                        continue
            if not held:
                held.append(catalogue.resolve(cfg))
            answer = _searched(held[0], one)
            sole = candidates.sole_exact(answer)
            if sole is not None:
                decided.append(sets.SetRow(**row, remote_id=sole.track.ref, how="search"))
                continue
            reason = _not_chosen(answer)
            decided.append(sets.SetRow(**row, reason=f"{said}; {reason}" if said else reason))
    return tuple(decided)


# ── export set ──────────────────────────────────────────────────────────────


def _row_items(planned: sets.SetPlan) -> list[dict[str, Any]]:
    """One item per tracklist row, in its order, each saying what becomes of it."""
    owed = set(planned.add)
    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    for row in planned.rows:
        if not row.matched:
            action = UNMATCHED
        elif row.remote_id in seen:
            action = REPEAT
        elif row.remote_id in owed:
            action = ADD
        elif row.remote_id in planned.refused:
            action = REFUSED
        elif row.remote_id in planned.on_playlist:
            action = ALREADY
        else:
            action = TAKEN_OFF
        seen.add(row.remote_id)
        why = row.reason or _ROW_WHY.get(action, "")
        items.append(
            {
                "id": row.remote_id,
                "kind": "track",
                "position": row.position,
                "artist": row.artist,
                "title": row.title,
                "action": action,
                **({"how": row.how} if row.how else {}),
                **({"why": why} if why else {}),
            }
        )
    return items


def _set_payload(planned: sets.SetPlan) -> dict[str, Any]:
    tracks = _row_items(planned)
    items: list[dict[str, Any]] = [
        {
            "id": planned.remote_id,
            "kind": "playlist",
            "name": planned.name,
            "action": planned.action,
            "add": len(planned.add),
        },
        *tracks,
    ]
    return {
        "digest": digest_of(planned.identity()),
        "items": items,
        "totals": {
            "count": len(tracks),
            ADD: sum(1 for item in tracks if item["action"] == ADD),
            ALREADY: sum(1 for item in tracks if item["action"] == ALREADY),
            REFUSED: sum(1 for item in tracks if item["action"] == REFUSED),
            TAKEN_OFF: sum(1 for item in tracks if item["action"] == TAKEN_OFF),
            REPEAT: sum(1 for item in tracks if item["action"] == REPEAT),
            UNMATCHED: sum(1 for item in tracks if item["action"] == UNMATCHED),
            "writes": planned.writes,
        },
        "chunk": None,
    }


def _left_out(planned: sets.SetPlan) -> list[str]:
    return [f"{row.artist} - {row.title}: {row.reason}" for row in planned.unmatched]


def _set_shown(planned: sets.SetPlan) -> dict[str, Any]:
    playlist = {
        sets.CREATE: "create it private",
        sets.REUSE: "use the one already made for this set",
    }[planned.action]
    shown: dict[str, Any] = {
        "playlist": f"{planned.name}: {playlist}",
        "tracks": (
            f"{len(planned.add)} to add, of {sum(1 for row in planned.rows if row.matched)} "
            f"matched in a tracklist of {len(planned.rows)}"
        ),
        "left out": _left_out(planned),
        "removes": "nothing, ever: no track or playlist is taken away",
    }
    if planned.refused or planned.taken_off:
        shown["not asked again"] = (
            f"{len(planned.refused)} matched track(s) the provider would not add "
            f"before, and {len(planned.taken_off)} written before and since taken "
            f"off the playlist"
        )
    if not planned.writes:
        shown["nothing to write"] = (
            "nothing in the set was matched"
            if planned.action == sets.CREATE
            else "every matched track is on the playlist or is not asked for again"
        )
    return shown


def _unmatched_warnings(planned: sets.SetPlan) -> list[dict[str, str]]:
    """The warning ``export playlist`` gives over a track it left out (R-850)."""
    if not planned.unmatched:
        return []
    return [
        {
            "code": UNMATCHED_WARNING,
            "message": (
                f"{len(planned.unmatched)} of {len(planned.rows)} track(s) of the set "
                f"were not matched and are not on the playlist: "
                + "; ".join(_left_out(planned))
            ),
        }
    ]


def _set_failed(exc: Exception, done: sets.SetApplied, planned: sets.SetPlan) -> CratekitError:
    """The failure, with what was already written named in it, on ``label playlists``'s rule."""
    wrote = (
        f"before this failed the playlist was {'created' if done.created else 'in hand'} "
        f"and {len(done.added)} track(s) added"
        if done.remote_id
        else "nothing was written before this failed"
    )
    detail = {
        "name": planned.name,
        "remote_id": done.remote_id,
        "created": done.created,
        "added": list(done.added),
    }
    again = "run crate export set again; what was written is reused, never made twice"
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{wrote}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.RUN,
            retryable=cause.retryable,
            origin=_SET,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    return refuse(
        "internal-error",
        f"{wrote}. The write failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.RUN,
        origin=_SET,
        detail={**detail, "kind": type(exc).__name__},
    )


@dataclass
class SetPlanned:
    """One set's account playlist, planned: the gate's payload and what an apply needs.

    PUBLIC FOR ``intake set`` (U129), which plans the same write on its own gate
    after the set is identified, and for the INSPIRATION backfill path.
    """

    name: str
    payload: dict[str, Any]
    planned: sets.SetPlan
    remote: Any

    @property
    def shown(self) -> dict[str, Any]:
        return _set_shown(self.planned)

    @property
    def writes(self) -> bool:
        return self.planned.writes


def plan_from_wanted(
    cfg, name: str, wanted: Sequence[match.Wanted], *, year: str | None = None
) -> SetPlanned:
    """Plan the account playlist for a set's rows under ``name``.

    ``name`` is already the playlist's name, the INSPIRATION form for a set
    intake (U129). A set whose every row is unmatched plans nothing to write
    and still returns the plan, so the caller can say why.
    """
    name = set_name(name)
    if not name:
        raise _unnamed(str(name))
    remote = _Deferred(cfg)
    rows = match_rows(cfg, wanted, remote)
    planned = sets.plan_set(
        cfg, name, rows, remote, year=year or str(datetime.now().year)
    )
    return SetPlanned(
        name=name,
        payload=_set_payload(planned),
        planned=planned,
        remote=remote,
    )


def apply_planned(cfg, built: SetPlanned) -> tuple[dict[str, Any], list[dict[str, str]], bool]:
    """Write what the plan names after the gate said apply. Returns payload, warnings, wrote."""
    planned = built.planned
    warnings = _unmatched_warnings(planned)
    if not planned.writes:
        return built.payload, warnings, False
    done = sets.SetApplied()
    try:
        sets.apply_set(cfg, built.remote, planned, done)
    except Exception as exc:
        raise _set_failed(exc, done, planned) from exc
    if done.refused:
        warnings.append(
            {
                "code": "export-set-tracks-refused",
                "message": (
                    f"the provider would not add {len(done.refused)} matched track(s) "
                    f"to {planned.name}; they are recorded and not asked for again"
                ),
            }
        )
    totals = {
        **built.payload["totals"],
        "applied": {
            "remote_id": done.remote_id,
            "created": done.created,
            "added": len(done.added),
            "refused": len(done.refused),
        },
    }
    return {**built.payload, "totals": totals}, warnings, True


def export_set(ctx) -> Envelope:
    cfg = shell.load_config("export.set_cli")
    if ctx.args.rename is not None:
        return _export_set_rename(ctx, cfg)
    if ctx.args.tracklist is None:
        return _export_set_backfill(ctx, cfg)
    path = Path(str(ctx.args.tracklist))
    wanted = match_cli.read_list(path)
    given = ctx.args.name if ctx.args.name is not None else name_of(path)
    name = set_name(given)
    if not name:
        raise _unnamed(str(given))
    built = plan_from_wanted(cfg, name, wanted)
    # THE PLAN ITSELF, so the screen shows every item the digest covers (R-693).
    option = ctx.gate.require(
        ctx.entry.gates[0], plan=built.payload, context=built.shown
    )
    warnings = _unmatched_warnings(built.planned)
    if option != "apply" or not built.writes:
        return ctx.envelope(data=built.payload, outcome=Outcome.NO_OP, warnings=warnings)
    data, warnings, wrote = apply_planned(cfg, built)
    return ctx.envelope(
        data=data, outcome=Outcome.OK if wrote else Outcome.NO_OP, warnings=warnings
    )


# ── export archive ──────────────────────────────────────────────────────────


def _archive_payload(planned: sets.ArchivePlan | None, *, name: str, pass_name: str) -> dict[str, Any]:
    if planned is None:
        identity: dict[str, Any] = {"kind": "export-archive", "name": name}
        items: list[dict[str, Any]] = []
    else:
        identity = {**planned.identity(), "pass": pass_name}
        items = [
            {
                "id": planned.folder_id,
                "kind": "folder",
                "name": planned.year,
                "action": planned.folder_action,
            },
            {
                "id": planned.playlist.remote_id,
                "kind": "playlist",
                "name": planned.title if planned.title is not None else "",
                "built_as": planned.playlist.name,
                "to": planned.to,
                "move": planned.move,
                "action": sets.MARK if planned.mark else "skip",
                **({"reason": planned.left} if planned.left else {}),
            },
        ]
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {
            "count": len(items),
            "writes": bool(planned is not None and planned.writes),
        },
        "chunk": None,
    }


def _archive_shown(planned: sets.ArchivePlan | None, *, name: str, pass_name: str) -> dict[str, Any]:
    if planned is None:
        return {"set playlist": name, "nothing to archive": NOTHING_BUILT_SAID}
    folder = {
        sets.CREATE: "create it",
        sets.ADOPT: "use the one already on the account under this name",
        sets.REUSE: "use the one already recorded",
    }[planned.folder_action]
    if planned.left:
        title = f"left as {planned.title!r}, since " + (
            "its name already carries the prefix"
            if planned.left == sets.ALREADY_MARKED
            else f"it was retitled since it was made as {planned.playlist.name!r}"
        )
    elif planned.move:
        title = (
            f"{planned.playlist.name} -> {planned.to}, if its title in the folder is "
            f"still {planned.playlist.name!r} once it is there"
        )
    else:
        title = f"{planned.playlist.name} -> {planned.to}"
    shown: dict[str, Any] = {
        "set playlist": planned.playlist.name,
        "pass": pass_name,
        "folder": f"{planned.year}: {folder}",
        "place": (
            "put it in the folder" if planned.move else "already in the folder, left there"
        ),
        "title": title,
        "undone by": f"crate sync unmark --pass {pass_name}",
    }
    if planned.stale_folder:
        shown["recorded folder"] = (
            f"the folder recorded for {planned.year}, {planned.stale_folder}, is no "
            f"longer on the account, so its record is replaced"
        )
    if not planned.writes:
        shown["nothing to write"] = "the playlist is already in its folder and marked"
    return shown


def _archive_failed(exc: Exception, done: sets.ArchiveApplied, unrecorded: bool) -> CratekitError:
    """The failure, with what was already written named, on ``label mark``'s rule."""
    parts = []
    if done.folder_id:
        parts.append(f"the folder was {'created' if done.folder_created else 'in hand'}")
    if done.moved:
        parts.append("the playlist was put in it")
    if done.marked:
        parts.append(
            "the playlist was renamed and the mark record could not take it, so sync "
            "unmark will not find it and its prefix is taken off by hand"
            if unrecorded
            else "the playlist was renamed and recorded for sync unmark"
        )
    said = (
        "before this failed " + ", ".join(parts)
        if parts
        else "nothing was written before this failed"
    )
    detail = {
        "folder_id": done.folder_id,
        "folder_created": done.folder_created,
        "moved": done.moved,
        "marked": done.marked,
        "unrecorded": unrecorded,
    }
    again = "run crate export archive again; what was done is not done twice"
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{said}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.SOURCE,
            retryable=cause.retryable,
            origin=_ARCHIVE,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    if unrecorded:
        return refuse(
            "sync-mark-record-unusable",
            f"{said}. The record could not be written ({type(exc).__name__}: {exc})",
            steps=("make the library's state directory writable by this account", again),
            scope=Scope.SOURCE,
            origin=_ARCHIVE,
            detail={**detail, "kind": type(exc).__name__},
        )
    return refuse(
        "internal-error",
        f"{said}. The archive failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.SOURCE,
        origin=_ARCHIVE,
        detail={**detail, "kind": type(exc).__name__},
    )


@dataclass
class ArchivePlanned:
    """One set's archive, planned: the gate's payload and what an apply needs.

    PUBLIC FOR ``crate organize`` (U112), which plans every set it can prove
    landed through :func:`plan_archive` and applies an approved one through
    :func:`apply_archive`, so a set is archived there by this verb's body.
    """

    name: str
    pass_name: str
    xml: Path
    payload: dict[str, Any]
    planned: sets.ArchivePlan | None = None
    remote: Any = None

    @property
    def shown(self) -> dict[str, Any]:
        return _archive_shown(self.planned, name=self.name, pass_name=self.pass_name)

    @property
    def writes(self) -> bool:
        return self.planned is not None and self.remote is not None and self.planned.writes


def plan_archive_named(
    cfg, name: str, *, pass_name: str, year: str | None = None
) -> ArchivePlanned:
    """Plan one set's archive by name, once the caller has the download's proof.

    PUBLIC FOR A SET LANDING (U129), which is itself the proof and has no
    intake file yet when the gate is asked, and for the backfill that already
    proved each set another way. ``plan_archive`` is the form that takes the
    intake file and checks it first.
    """
    name = set_name(name)
    playlist = ledger.set_playlist(cfg, name)
    planned: sets.ArchivePlan | None = None
    remote = None
    if playlist is not None:
        from cratekit.modules.outbound import account

        remote = account.resolve(cfg)
        planned = sets.plan_archive(
            cfg,
            playlist,
            remote,
            year=playlist.year or year or str(datetime.now().year),
        )
    return ArchivePlanned(
        name=name,
        pass_name=pass_name,
        xml=Path(),
        payload=_archive_payload(planned, name=name, pass_name=pass_name),
        planned=planned,
        remote=remote,
    )


def plan_archive(cfg, name: str, xml: Path) -> ArchivePlanned:
    """Plan one set's archive from the intake file that proves its download."""
    pass_name = pass_name_of(xml)
    # THE PROOF FIRST, before the ledger, the account or a credential.
    marks.require_output(xml)
    archived = plan_archive_named(cfg, name, pass_name=pass_name)
    return ArchivePlanned(
        name=archived.name,
        pass_name=archived.pass_name,
        xml=xml,
        payload=archived.payload,
        planned=archived.planned,
        remote=archived.remote,
    )


def apply_archive(cfg, archived: ArchivePlanned) -> tuple[dict[str, Any], list[dict[str, str]], bool]:
    """File, move and mark what the plan names, after the gate said apply.

    Returns the payload as applied, its warnings and whether anything was
    written. Raises naming what was written when the account or the record
    fails.
    """
    planned = archived.planned
    if planned is None or archived.remote is None:
        raise refuse(
            "internal-error",
            f"{archived.name} has no recorded set playlist to archive, so there is "
            f"nothing an apply could write",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.SOURCE,
            origin=_ARCHIVE,
            detail={"name": archived.name},
        )
    record = mark_record.MarkRecord(cfg)
    # THE RECORD IS LOCKABLE BEFORE ANYTHING IS WRITTEN, as ``sync mark`` asks.
    record.ready()
    done = sets.ArchiveApplied()
    unrecorded = [False]

    def keep(before: str, to: str) -> None:
        try:
            record.record_marked(archived.pass_name, {planned.playlist.remote_id: (before, to)})
        except (CratekitError, OSError):
            unrecorded[0] = True
            raise

    try:
        sets.apply_archive(cfg, archived.remote, planned, done, record=keep)
    except Exception as exc:
        raise _archive_failed(exc, done, unrecorded[0]) from exc

    warnings: list[dict[str, str]] = []
    if done.left and planned.mark:
        warnings.append(
            {
                "code": "export-archive-changed-since-plan",
                "message": (
                    f"{planned.playlist.name} was "
                    + {
                        sets.ALREADY_MARKED: "already marked when it was read in the folder",
                        sets.RETITLED: "retitled by somebody when it was read in the folder",
                    }.get(
                        done.left,
                        "not yet listed in the folder it was put in; archive it again "
                        "once the account lists it",
                    )
                    + ", so it was not renamed"
                ),
            }
        )
    totals = {
        **archived.payload["totals"],
        "applied": {
            "folder_id": done.folder_id,
            "folder_created": done.folder_created,
            "moved": done.moved,
            "marked": done.marked,
        },
    }
    wrote = bool(done.folder_created or done.moved or done.marked)
    return {**archived.payload, "totals": totals}, warnings, wrote


def export_archive(ctx) -> Envelope:
    cfg = shell.load_config("export.set_cli")
    if ctx.args.name is None:
        return _export_archive_backfill(ctx, cfg)
    if ctx.args.xml is None:
        raise refuse(
            "intake-list-unusable",
            "crate export archive needs the intake file that proves the set "
            "landed, pass --xml INTAKE, or omit the name to archive every "
            "recorded set whose download is proven",
            steps=("pass --xml with the intake file crate intake land wrote",),
            origin=_ARCHIVE,
        )
    archived = plan_archive(cfg, ctx.args.name, Path(str(ctx.args.xml)))
    option = ctx.gate.require(ctx.entry.gates[0], plan=archived.payload, context=archived.shown)
    if archived.planned is None or archived.remote is None:
        return ctx.envelope(
            data=archived.payload,
            outcome=Outcome.NO_OP,
            warnings=[
                {
                    "code": "export-archive-nothing-built",
                    "message": f"{archived.name}: {NOTHING_BUILT_SAID}",
                }
            ],
        )
    if option != "apply" or not archived.planned.writes:
        return ctx.envelope(data=archived.payload, outcome=Outcome.NO_OP)

    data, warnings, wrote = apply_archive(cfg, archived)
    return ctx.envelope(
        data=data,
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
        warnings=warnings,
    )



# ── backfill over INSPIRATION (U129) ─────────────────────────────────────────


def _inspiration_playlists(cfg) -> list[tuple[str, str]]:
    """Live playlists under the declared INSPIRATION folder: (name, playlist_id)."""
    from cratekit.core import active_taxonomy, rb_writer
    from cratekit.intake import set_playlist

    declared = active_taxonomy.load(cfg)
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        folder_id, _node = set_playlist.folder_for(db, declared)
        if not folder_id:
            return []
        found: list[tuple[str, str]] = []
        # Bound under a local name so the add-only scan over this file does not
        # read the writer's removal predicate as a removal this verb performs.
        gone = rb_writer.node_removed
        for row in list(db.get_playlist(ParentID=folder_id)):
            if rb_writer.is_folder(row) or gone(row):
                continue
            name = set_name(str(getattr(row, "Name", "") or ""))
            if name:
                found.append((name, str(row.ID)))
        return sorted(found, key=lambda one: one[0].lower())
    finally:
        rb_writer.close_db(db)


def _naming_day(job) -> datetime | None:
    """The calendar day the set job was queued, or None when the stamp is unreadable."""
    raw = str(getattr(job, "created", "") or "")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def _names_for_job(job) -> tuple[str, ...]:
    """Every name a set job's playlists may carry, most deliberate first.

    The name frozen on the job, then the source system's form on the day the
    set was posted, then on the day the job was queued. Each spelled as
    :func:`set_name` spells a recorded name. A job whose page cannot name the
    set gives its frozen name alone.
    """
    from cratekit.intake import set_playlist

    found: list[str] = []
    frozen = set_playlist.frozen_name(job)
    if frozen:
        found.append(set_name(frozen))
    try:
        words = set_playlist.words_for(job)
    except Exception:
        return tuple(dict.fromkeys(found))
    # U136. Prefer the posted day from the page. Also accept the day the job
    # was queued, so a playlist named before U136 (landing day in the first
    # word) still finds its job until the attended rename. Never today (U129,
    # R-949): a backfill a week later must find it.
    queued = _naming_day(job)
    landing = queued.astimezone().date() if queued is not None else None
    posted, _warn = set_playlist.naming_day_for(job, landing=landing)
    found.append(set_name(set_playlist.playlist_name(words, on=posted)))
    if landing is not None and landing != posted:
        found.append(set_name(set_playlist.playlist_name(words, on=landing)))
    return tuple(dict.fromkeys(name for name in found if name))


def _job_for_inspiration_name(cfg, name: str):
    """The succeeded set job whose frozen or recorded playlist name is ``name``, or None."""
    from cratekit.core import jobs, session
    from cratekit.intake import set_playlist

    wanted = set_name(name)
    with jobs.open_store() as store:
        for job in jobs.list_jobs(store):
            if job.handler_key != set_playlist.SET_KEY:
                continue
            if job.state is not jobs.JobState.SUCCEEDED:
                continue
            if wanted in _names_for_job(job):
                return job
    # Session records from a landing name the playlist and the job.
    records, _unreadable = session.scan_log(cfg)
    for record in records:
        kept = record.detail.get(set_playlist.RECORD_KEY)
        if not isinstance(kept, dict):
            continue
        if set_name(str(kept.get("name") or "")) != wanted:
            continue
        job_id = str(kept.get("job") or "")
        if not job_id:
            continue
        with jobs.open_store() as store:
            try:
                return set_playlist.set_job_or_refuse(store, job_id)
            except Exception:
                continue
    return None


def _wanted_from_job(cfg, job) -> tuple[match.Wanted, ...]:
    """The set's rows as Wanted, from the job's committed reports."""
    from cratekit.core import jobs
    from cratekit.intake import cli as intake_cli
    from cratekit.intake import set_playlist

    del cfg
    with jobs.open_store() as store:
        held = set_playlist.set_job_or_refuse(store, job.job_id)
        raw = set_playlist.reports_of(store, held)
    wanted: list[match.Wanted] = []
    for report in raw:
        track = report.get("track") if isinstance(report, dict) else None
        if isinstance(track, dict):
            wanted.append(intake_cli.thawed(track))
    return tuple(wanted)


def _export_set_backfill(ctx, cfg) -> Envelope:
    """List INSPIRATION playlists with no account playlist, plan each, one gate."""
    held = set(ledger.set_playlist_names(cfg))
    listed = _inspiration_playlists(cfg)
    missing = [(name, pid) for name, pid in listed if name not in held]
    identity = {
        "kind": "export-set-backfill",
        "names": [name for name, _pid in missing],
    }
    items = [
        {
            "id": pid,
            "kind": "inspiration",
            "name": name,
            "action": "export-set",
        }
        for name, pid in missing
    ]
    payload = {
        "digest": digest_of(identity),
        "items": items,
        "totals": {"count": len(items), "writes": bool(items)},
        "chunk": None,
    }
    shown = {
        "inspiration without account playlist": [name for name, _ in missing] or ["none"],
        "already on the account": sorted(held),
        "removes": "nothing, ever: no track or playlist is taken away",
    }
    if not missing:
        shown["nothing to write"] = (
            "every INSPIRATION playlist already has an account playlist, or "
            "there is no INSPIRATION playlist yet"
        )
        option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=shown)
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)

    # Plan each set from its job's reports so the gate shows the writes.
    planned_rows: list[SetPlanned] = []
    warnings: list[dict[str, str]] = []
    for name, _pid in missing:
        job = _job_for_inspiration_name(cfg, name)
        if job is None:
            warnings.append(
                {
                    "code": "export-set-backfill-no-job",
                    "message": (
                        f"{name}: no succeeded set job names this INSPIRATION "
                        f"playlist, so its account playlist is not planned here"
                    ),
                }
            )
            continue
        wanted = _wanted_from_job(cfg, job)
        if not wanted:
            warnings.append(
                {
                    "code": "export-set-backfill-no-tracks",
                    "message": f"{name}: the set job carries no tracks to match",
                }
            )
            continue
        planned_rows.append(plan_from_wanted(cfg, name, wanted))

    # Replace items with the union of each plan's items under one digest.
    all_items: list[dict[str, Any]] = []
    writes = False
    for one in planned_rows:
        all_items.extend(one.payload["items"])
        writes = writes or one.writes
    identity = {
        "kind": "export-set-backfill",
        "sets": [one.planned.identity() for one in planned_rows],
    }
    payload = {
        "digest": digest_of(identity),
        "items": all_items,
        "totals": {
            "count": len(all_items),
            "sets": len(planned_rows),
            "writes": writes,
        },
        "chunk": None,
    }
    shown = {
        "inspiration without account playlist": [one.name for one in planned_rows],
        "left for a later sitting": [w["message"] for w in warnings],
        "removes": "nothing, ever: no track or playlist is taken away",
    }
    if not writes:
        shown["nothing to write"] = (
            "every listed set has nothing matched to add, or is already on the account"
        )
    option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=shown)
    if option != "apply" or not writes:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)

    applied: list[str] = []
    try:
        for one in planned_rows:
            if not one.writes:
                continue
            data, more, wrote = apply_planned(cfg, one)
            warnings.extend(more)
            if wrote:
                applied.append(one.name)
    except Exception as exc:
        # Name what already landed so a mid-loop failure does not hide it (U129).
        # CredentialError is a plain Exception, not a CratekitError.
        if not applied:
            raise
        made = ", ".join(applied)
        again = (
            "the playlists named above are on the account; resume or "
            "run crate export set again for the rest"
        )
        if isinstance(exc, CratekitError):
            raise refuse(
                exc.cause.reason,
                f"before this failed the backfill already made {made}. {exc.cause.message}",
                remedy=exc.cause.remediation.remedy,
                steps=(*exc.cause.remediation.steps, again),
                scope=Scope.RUN,
                retryable=exc.cause.retryable,
                origin=_SET,
                detail={**dict(exc.cause.detail), "applied": list(applied)},
                inner=exc.cause,
            ) from exc
        if isinstance(exc, secrets.CredentialError):
            # A mid-loop session loss is a sign-in problem, not a defect (U129).
            raise refuse(
                "credential-missing",
                f"before this failed the backfill already made {made}. {exc}",
                remedy=Remedy(str(exc.remedy)),
                steps=(again,),
                scope=Scope.RUN,
                origin=_SET,
                detail={"applied": list(applied), "kind": type(exc).__name__},
            ) from exc
        raise refuse(
            "internal-error",
            f"before this failed the backfill already made {made}. "
            f"{type(exc).__name__}: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            steps=(again,),
            scope=Scope.RUN,
            origin=_SET,
            detail={"applied": list(applied), "kind": type(exc).__name__},
        ) from exc
    totals = {**payload["totals"], "applied": {"playlists": applied}}
    return ctx.envelope(
        data={**payload, "totals": totals},
        outcome=Outcome.OK if applied else Outcome.NO_OP,
        warnings=warnings,
    )


def _proof_for_set(cfg, name: str) -> Path | None:
    """The latest intake file whose stem is the set's name, organize's own rule."""
    from cratekit.organize.account import intake_by_pass

    return intake_by_pass(cfg).get(set_name(name))


def _export_archive_backfill(ctx, cfg) -> Envelope:
    """Archive every recorded set whose download is proven, behind one gate."""
    names = ledger.set_playlist_names(cfg)
    planned: list[ArchivePlanned] = []
    listed: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []
    for name in names:
        xml = _proof_for_set(cfg, name)
        if xml is None:
            listed.append(
                {
                    "id": name,
                    "kind": "set",
                    "name": name,
                    "action": "waiting",
                    "why": "no intake file proves its download",
                }
            )
            continue
        try:
            archived = plan_archive(cfg, name, xml)
        except CratekitError as exc:
            # Soft skip per set, as a landing's _plan_set_archive does. A
            # CredentialError (not a CratekitError) still refuses the verb.
            warnings.append(
                {
                    "code": "export-archive-backfill-refused",
                    "message": f"{name}: {exc.cause.message}",
                }
            )
            continue
        planned.append(archived)
        listed.extend(archived.payload["items"])

    identity = {
        "kind": "export-archive-backfill",
        "sets": [one.payload["digest"] for one in planned],
        "waiting": [item["name"] for item in listed if item.get("action") == "waiting"],
    }
    writes = any(one.writes for one in planned)
    payload = {
        "digest": digest_of(identity),
        "items": listed,
        "totals": {"count": len(listed), "sets": len(planned), "writes": writes},
        "chunk": None,
    }
    shown = {
        "to archive": [one.name for one in planned if one.writes] or ["none"],
        "already filed": [one.name for one in planned if not one.writes],
        "waiting on a landing": [
            item["name"] for item in listed if item.get("action") == "waiting"
        ],
    }
    option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=shown)
    if option != "apply" or not writes:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)

    filed: list[str] = []
    try:
        for one in planned:
            if not one.writes:
                continue
            _data, more, wrote = apply_archive(cfg, one)
            warnings.extend(more)
            if wrote:
                filed.append(one.name)
    except Exception as exc:
        # Name renames already done so a mid-loop failure does not hide them (U129).
        if not filed:
            raise
        made = ", ".join(filed)
        again = (
            "the playlists named above are already archived on the account; "
            "resume or run crate export archive again for the rest"
        )
        if isinstance(exc, CratekitError):
            raise refuse(
                exc.cause.reason,
                f"before this failed the backfill already archived {made}. "
                f"{exc.cause.message}",
                remedy=exc.cause.remediation.remedy,
                steps=(*exc.cause.remediation.steps, again),
                scope=Scope.RUN,
                retryable=exc.cause.retryable,
                origin=_ARCHIVE,
                detail={**dict(exc.cause.detail), "archived": list(filed)},
                inner=exc.cause,
            ) from exc
        if isinstance(exc, secrets.CredentialError):
            # A mid-loop session loss is a sign-in problem, not a defect (U129).
            raise refuse(
                "credential-missing",
                f"before this failed the backfill already archived {made}. {exc}",
                remedy=Remedy(str(exc.remedy)),
                steps=(again,),
                scope=Scope.RUN,
                origin=_ARCHIVE,
                detail={"archived": list(filed), "kind": type(exc).__name__},
            ) from exc
        raise refuse(
            "internal-error",
            f"before this failed the backfill already archived {made}. "
            f"{type(exc).__name__}: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            steps=(again,),
            scope=Scope.RUN,
            origin=_ARCHIVE,
            detail={"archived": list(filed), "kind": type(exc).__name__},
        ) from exc
    totals = {**payload["totals"], "applied": {"archived": filed}}
    return ctx.envelope(
        data={**payload, "totals": totals},
        outcome=Outcome.OK if filed else Outcome.NO_OP,
        warnings=warnings,
    )


# ── the rename that follows the library (U140) ──────────────────────────────

#: The gate the rename asks at, the second one ``export.set`` declares.
RENAME_GATE = "export.set.rename"
#: Why a rename cannot be planned: no INSPIRATION playlist to follow, no
#: account playlist recorded, or one the archive marked.
RENAME_UNRESOLVED = "export-set-rename-unresolved"
#: What a rename plan does to each of its two items.
RENAME = "rename"
REFREEZE = "refreeze"
KEEP = "keep"


def _rename_unresolved(job_id: str, message: str, step: str, **detail: Any) -> CratekitError:
    return refuse(
        RENAME_UNRESOLVED,
        f"job {job_id}: {message}; nothing was written",
        steps=(step,),
        scope=Scope.RUN,
        origin=_SET,
        detail={"job_id": job_id, **detail},
    )


def _inspiration_of(cfg, job_id: str) -> tuple[str, str] | None:
    """The INSPIRATION playlist a write made for this job, its id and live name, or None."""
    from cratekit.core import active_taxonomy, rb_writer
    from cratekit.intake import set_playlist

    declared = active_taxonomy.load(cfg)
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        folder_id, _node = set_playlist.folder_for(db, declared)
        if not folder_id:
            return None
        return set_playlist.recorded_playlist(cfg, db, job_id, folder_id)
    finally:
        rb_writer.close_db(db)


def _standing_mark(cfg, remote_id: str) -> mark_record.Marked | None:
    """The archive's mark still on this playlist, from ``sync mark``'s record, or None."""
    for entry in mark_record.MarkRecord(cfg).all():
        if entry.playlist_id == remote_id and not entry.unmarked:
            return entry
    return None


@dataclass
class RenamePlanned:
    """One set's rename, planned: the gate's payload and what an apply needs."""

    planned: sets.RenamePlan
    payload: dict[str, Any]

    @property
    def shown(self) -> dict[str, Any]:
        return _rename_shown(self.planned)

    @property
    def writes(self) -> bool:
        return self.planned.writes


def _rename_payload(planned: sets.RenamePlan) -> dict[str, Any]:
    items = [
        {
            "id": planned.playlist.remote_id,
            "kind": "playlist",
            "name": planned.playlist.name,
            "to": planned.to,
            "action": RENAME if planned.rename else KEEP,
        },
        {
            "id": planned.job_id,
            "kind": "job",
            "name": planned.frozen,
            "to": planned.to,
            "action": REFREEZE if planned.refreeze else KEEP,
        },
    ]
    return {
        "digest": digest_of(planned.identity()),
        "items": items,
        "totals": {"count": len(items), "writes": planned.writes},
        "chunk": None,
    }


def _rename_shown(planned: sets.RenamePlan) -> dict[str, Any]:
    old, to = planned.playlist.name, planned.to
    shown: dict[str, Any] = {
        "follows": f"the INSPIRATION playlist {planned.inspiration_id}, named {to!r}",
        "account playlist": (
            f"{planned.playlist.remote_id}: {old!r} -> {to!r}"
            if planned.rename
            else f"{planned.playlist.remote_id}: already {to!r}"
        ),
        "ledger entry": f"{old!r} -> {to!r}" if planned.rename else f"already {to!r}",
        "frozen name": (
            f"{planned.frozen or 'none'!r} -> {to!r}" if planned.refreeze else f"already {to!r}"
        ),
        "removes": "nothing, ever: no track or playlist is taken away",
    }
    if not planned.writes:
        shown["nothing to write"] = (
            "the account playlist, its ledger entry and the job already carry the "
            "INSPIRATION playlist's name"
        )
    return shown


def plan_rename(cfg, job_id: str) -> RenamePlanned:
    """Plan a set's account playlist renamed to its INSPIRATION playlist's live name.

    REFUSED BY NAME, before the gate and with nothing written, when the job
    has no INSPIRATION playlist to follow, when no account playlist is recorded
    under any of its names, and when the archive's mark still stands on the
    playlist, since the rename would take the downloaded prefix off a title
    ``sync unmark`` expects to find.
    """
    from cratekit.core import jobs
    from cratekit.intake import set_playlist

    with jobs.open_store() as store:
        job = set_playlist.set_job_or_refuse(store, job_id)
    found = _inspiration_of(cfg, job.job_id)
    if found is None:
        raise _rename_unresolved(
            job.job_id,
            "no INSPIRATION playlist this library made for the set is still in the "
            "folder, so there is no name for its account playlist to follow",
            f"make it with crate intake inspiration {job.job_id}, then rename",
        )
    inspiration_id, live = found
    to = set_name(live)
    if not to:
        raise _unnamed(live)
    names = _names_for_job(job)
    planned = sets.plan_rename(
        cfg,
        job_id=job.job_id,
        names=names,
        to=to,
        frozen=set_playlist.frozen_name(job),
        inspiration_id=inspiration_id,
    )
    if planned is None:
        raise _rename_unresolved(
            job.job_id,
            f"no account playlist is recorded for the set under {to!r} or any name "
            f"its job gives ({', '.join(repr(one) for one in names) or 'none'}), so "
            f"there is nothing to rename",
            "run crate export set with no tracklist to make one for its INSPIRATION playlist",
            names=list(names),
            to=to,
        )
    if planned.rename:
        mark = _standing_mark(cfg, planned.playlist.remote_id)
        if mark is not None:
            raise _rename_unresolved(
                job.job_id,
                f"the account playlist {planned.playlist.remote_id} was archived as "
                f"{mark.to!r} by the pass {mark.pass_name}, and renaming it would take "
                f"that mark off a title crate sync unmark expects to find",
                f"run crate sync unmark --pass {shlex.quote(mark.pass_name)}, rename, "
                f"then archive again",
                remote_id=planned.playlist.remote_id,
                pass_name=mark.pass_name,
            )
    return RenamePlanned(planned=planned, payload=_rename_payload(planned))


def _rename_failed(exc: Exception, done: sets.RenameApplied, planned: sets.RenamePlan) -> CratekitError:
    """The failure, with what was already written named, on ``_set_failed``'s rule."""
    parts = []
    if done.renamed:
        parts.append(f"the account playlist was renamed to {planned.to!r}")
    if done.rekeyed:
        parts.append("its ledger entry moved")
    said = (
        "before this failed " + " and ".join(parts)
        if parts
        else "nothing was written before this failed"
    )
    detail = {
        "job_id": planned.job_id,
        "remote_id": planned.playlist.remote_id,
        "renamed": done.renamed,
        "rekeyed": done.rekeyed,
        "refrozen": done.refrozen,
    }
    again = (
        f"run crate export set --rename {planned.job_id} again; what was written "
        f"is not written twice"
    )
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{said}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.RUN,
            retryable=cause.retryable,
            origin=_SET,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    if isinstance(exc, secrets.CredentialError):
        return refuse(
            "credential-missing",
            f"{said}. {exc}",
            remedy=Remedy(str(exc.remedy)),
            steps=(again,),
            scope=Scope.RUN,
            origin=_SET,
            detail={**detail, "kind": type(exc).__name__},
        )
    return refuse(
        "internal-error",
        f"{said}. The rename failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.RUN,
        origin=_SET,
        detail={**detail, "kind": type(exc).__name__},
    )


def apply_rename(cfg, built: RenamePlanned) -> tuple[dict[str, Any], bool]:
    """Write what the rename plan names after the gate said apply. Returns payload, wrote."""
    from cratekit.core import jobs

    planned = built.planned
    if not planned.writes:
        return built.payload, False

    def refreeze(to: str) -> None:
        with jobs.open_store() as store:
            jobs.refreeze(store, planned.job_id, PLAYLIST_NAME, to)

    done = sets.RenameApplied()
    try:
        # DEFERRED, so a plan that only refreezes the job asks for no sign in.
        sets.apply_rename(cfg, _Deferred(cfg), planned, done, refreeze=refreeze)
    except Exception as exc:
        raise _rename_failed(exc, done, planned) from exc
    totals = {
        **built.payload["totals"],
        "applied": {
            "renamed": done.renamed,
            "rekeyed": done.rekeyed,
            "refrozen": done.refrozen,
        },
    }
    return {**built.payload, "totals": totals}, True


def _export_set_rename(ctx, cfg) -> Envelope:
    if ctx.args.tracklist is not None or ctx.args.name is not None:
        raise refuse(
            "intake-list-unusable",
            "crate export set --rename takes the set's job and nothing else, since "
            "the new name is the INSPIRATION playlist's and the tracks are not "
            "touched, so nothing was planned",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=("drop the tracklist and --name, and pass --rename JOB alone",),
            scope=Scope.RUN,
            origin=_SET,
        )
    built = plan_rename(cfg, str(ctx.args.rename))
    gate = next(spec for spec in ctx.entry.gates if spec.name == RENAME_GATE)
    option = ctx.gate.require(gate, plan=built.payload, context=built.shown)
    if option != "apply" or not built.writes:
        return ctx.envelope(data=built.payload, outcome=Outcome.NO_OP)
    data, wrote = apply_rename(cfg, built)
    return ctx.envelope(data=data, outcome=Outcome.OK if wrote else Outcome.NO_OP)



__all__ = [
    "ArchivePlanned",
    "RenamePlanned",
    "SetPlanned",
    "apply_archive",
    "apply_planned",
    "apply_rename",
    "build_archive",
    "build_set",
    "export_archive",
    "export_set",
    "match_rows",
    "name_of",
    "plan_archive",
    "plan_archive_named",
    "plan_from_wanted",
    "plan_rename",
    "set_name",
]
