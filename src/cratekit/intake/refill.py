"""Refill an INBOX account playlist from the pass that mirrored it (U134).

A pass sweeps the playlists the author made on the streaming account, and the
landing gives each one an INBOX playlist holding every track of it the library
owns, in the account's order (U113, U128). Nothing rebuilt one afterwards. At
sitting 34 every native row of four such playlists was removed and the files
dropped back into rekordbox from Finder, which left the playlists empty and
the tracks under new rows. ``intake land --pass`` again is a ``no_op`` with
nothing staged, and a later landing of a mirrored pass holds only its new
files; ``sync pair`` refuses a playlist under INBOX by design. This module is
the rebuild: the pass's recorded reports, read again, against the library as
it is now.

WHAT THE PLAYLIST SHOULD HOLD IS READ FROM THE PASS, never from the account.
Each ``intake.playlist`` job the pass ran recorded its account playlist's
tracks in item order, which is the account's order, and each committed report
says what the track resolved to. No provider is asked anything.

EVERY ROW IS RESOLVED BY THE SET BACKFILL'S RULE (U121), which is the same
question asked of a different job: a row the report called owned is found by
the report's library paths, and asked of the library again only when those
paths hold no row any more; a row that was downloaded is asked of the library
as it stands, with a person's review answers read back. Each answer is found
in the collection by path. A row the library does not own, a row two
collection rows claim, and a suppressed row are LEFT, each named with why,
never filed by a guess.

THE PLAYLIST IS FOUND BEFORE ONE REPORT IS READ, in this order:

* a landing record of the pass that names the account playlist by the
  account's identifier and the pass (U128), whose ``id`` is the playlist;
* a landing record from before U128, which names neither, whose ``pass`` is
  this pass and whose entry carries the account's name EXACTLY, so a second
  landing's ``Name 2`` is never taken for the first;
* a live playlist anywhere under the intake root with the account's name.

A RECORDED PLAYLIST THAT IS LIVE OUTSIDE INBOX IS REFUSED BY NAME. A person
moved it out of the listening queue, and filling it is not this verb's. An
account playlist nothing answers, or two playlists answer, is listed and
written nothing.

ONLY WHAT THE PLAYLIST LACKS IS PLANNED, in the account's order, through the
guarded writer's one membership rule, so a second run plans nothing. A
membership is the only thing written: no content row, no playlist row, no
file, and never a beat grid.

Layer: modules. It reads configuration through the objects it is handed and
opens no database of its own.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    jobs,
    rb_writer,
    session,
    snapshot,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import Remedy, refuse
from cratekit.intake import account_playlists, ingest, native, set_playlist
from cratekit.write import trees

#: The session workflow a refill's write is recorded under.
WORKFLOW = "inbox-refill"

#: The session record field naming what a refill wrote, by playlist.
RECORD_KEY = "inbox_refill"

#: The refusal this module owns, reserved in the cause vocabulary.
OUTSIDE_INBOX = "refill-playlist-outside-inbox"

#: How the INBOX playlist was found, as the screen says it.
BY_RECORD = "the landing record names it"
BY_NAME = "found by the account's name under INBOX"

#: Why an account playlist of the pass gets no refill, as the screen says it.
NOT_FOUND = "no live INBOX playlist answers it, by record or by name"
TWO_FOUND = "two live INBOX playlists answer it, so neither is the one"

#: What each row of a planned playlist does.
ADD = "add"
HELD = "held"

#: The landing records that still stand, the U128 rule (:func:`account_playlists.mirrored`).
_STANDING = frozenset(
    {
        session.SessionState.AWAITING_IMPORT,
        session.SessionState.COMMITTED_UNVERIFIED,
        session.SessionState.CLOSED,
    }
)

_ORIGIN = ("intake.refill",)


@dataclass(frozen=True, slots=True)
class Target:
    """One INBOX playlist the pass mirrored, and what a refill puts in it."""

    #: The account's identifier and name for the playlist, and its job.
    account: str
    account_name: str
    job_id: str
    #: The INBOX playlist's row and the name rekordbox shows.
    playlist_id: str
    name: str
    found_by: str
    #: Every row of the account playlist the library owns, in the account's order.
    members: tuple[set_playlist.Member, ...] = ()
    #: The content rows the playlist lacks, in the account's order.
    adds: tuple[str, ...] = ()
    #: Every row of the account playlist it will not hold, each with why.
    left: tuple[set_playlist.Left, ...] = ()

    def rows(self) -> list[dict[str, Any]]:
        """Each member with what the refill does to it, then each left row."""
        pending = set(self.adds)
        shown: list[dict[str, Any]] = []
        for one in self.members:
            action = ADD if one.content_id in pending else HELD
            pending.discard(one.content_id)
            shown.append({"action": action, **one.identity()})
        shown.extend({"action": "leave", **one.identity()} for one in self.left)
        return shown

    def identity(self) -> dict[str, Any]:
        return {
            "account": self.account,
            "account_name": self.account_name,
            "job": self.job_id,
            "playlist": self.playlist_id,
            "name": self.name,
            "found_by": self.found_by,
            "rows": self.rows(),
        }


@dataclass(frozen=True, slots=True)
class Unfound:
    """One account playlist of the pass that no single INBOX playlist answers."""

    account: str
    account_name: str
    job_id: str
    why: str
    #: The playlists that answered, when more than one did.
    candidates: tuple[str, ...] = ()

    def identity(self) -> dict[str, Any]:
        return {
            "account": self.account,
            "account_name": self.account_name,
            "job": self.job_id,
            "why": self.why,
            "candidates": list(self.candidates),
        }


@dataclass(frozen=True, slots=True)
class RefillPlan:
    """What a refill of one pass writes, every row named, digested."""

    pass_name: str
    tree_id: str
    root_id: str
    root_name: str
    targets: tuple[Target, ...]
    unfound: tuple[Unfound, ...] = ()
    digest: str = ""

    @property
    def writes(self) -> bool:
        return any(one.adds for one in self.targets)

    @property
    def adds(self) -> int:
        return sum(len(one.adds) for one in self.targets)


@dataclass(frozen=True, slots=True)
class Filled:
    """One playlist a refill wrote into, read back from SQL after the commit."""

    playlist_id: str
    name: str
    #: The distinct rows the playlist should hold, in the account's order.
    wanted: tuple[str, ...]
    #: The memberships this commit added.
    added: tuple[str, ...]
    #: Every content row read back under the playlist after the commit, in order.
    read_back: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Refilled:
    """What a refill's one commit wrote."""

    session_id: str
    filled: tuple[Filled, ...]

    @property
    def added(self) -> int:
        return sum(len(one.added) for one in self.filled)


def identity(plan: RefillPlan) -> dict[str, Any]:
    """What the digest covers: the pass, the root, every playlist and every row of it."""
    return {
        "kind": "inbox-refill",
        "pass": plan.pass_name,
        "tree": plan.tree_id,
        "root": plan.root_id,
        "targets": [one.identity() for one in plan.targets],
        "unfound": [one.identity() for one in plan.unfound],
    }


def anchored_root(db: Any, tree_id: str, registry: tree_registry.Registry) -> str:
    """The intake tree's adopted root, or the refusal that names ``tree cutover``."""
    try:
        return tree_registry.anchored_root(
            tree_id, registry, root_exists=lambda root_id: db.get_playlist(ID=root_id) is not None
        )
    except tree_registry.TreeModeRefused as exc:
        if exc.cause.reason != "tree-unconverged" or exc.mode != tree_registry.Mode.XML:
            raise
        raise refuse(
            "tree-unconverged",
            f"the intake tree {tree_id!r} is still on the xml bridge, so its playlists "
            f"are not this product's to fill in the database; cut the intake tree over "
            f"first, nothing was read or written",
            remedy=Remedy.COMPLETE_PENDING_ACTION,
            steps=(
                f"run crate tree cutover {tree_id} --export with a Fresh Export to "
                f"move the intake tree to the database",
            ),
            origin=_ORIGIN,
            detail={"tree_id": tree_id, "mode": str(exc.mode)},
            inner=exc.cause,
        ) from exc


def under_root(db: Any, root_id: str) -> dict[str, Any]:
    """Every live node anywhere under the intake root, by id, folders included.

    Every descendant and not only the root's children, :func:`native.inbox_held`'s
    rule, so a playlist the rotation moved into ``Old`` is still under INBOX.
    """
    children: dict[str, list[Any]] = {}
    for row in list(db.get_playlist()):
        if not rb_writer.node_removed(row):
            children.setdefault(str(getattr(row, "ParentID", "") or ""), []).append(row)
    found: dict[str, Any] = {}
    pending = [str(root_id)]
    while pending:
        for row in children.get(pending.pop(), ()):
            found[str(row.ID)] = row
            pending.append(str(row.ID))
    return found


def recorded_ids(
    records: Iterable[session.SessionRecord], *, pass_name: str, account: str, name: str
) -> tuple[str, ...]:
    """The playlist ids the standing landing records of ``pass_name`` give the account playlist.

    AN ENTRY SINCE U128 is matched by the account's identifier and the pass it
    carries. AN ENTRY FROM BEFORE carries neither, so it is matched by its
    record's pass and by the account's name exactly: a second landing of the
    same pass named its playlist ``Name 2``, and that is not the one the
    account's whole playlist was mirrored into. Oldest record first.
    """
    ids: list[str] = []
    for record in sorted(records, key=lambda one: one.session_id):
        if record.workflow != ingest.INTAKE_WORKFLOW or record.state not in _STANDING:
            continue
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ():
            if not isinstance(entry, Mapping) or not entry.get("id"):
                continue
            if entry.get(ingest.INBOX_ACCOUNT_KEY):
                ours = (
                    str(entry[ingest.INBOX_ACCOUNT_KEY]) == account
                    and entry.get(ingest.INBOX_PASS_KEY) == pass_name
                )
            else:
                ours = (
                    record.detail.get(native.PASS_KEY) == pass_name
                    and entry.get("name") == name
                )
            if ours:
                ids.append(str(entry["id"]))
    return tuple(dict.fromkeys(ids))


def _live_playlist(db: Any, playlist_id: str) -> Any | None:
    row = db.get_playlist(ID=playlist_id)
    if row is None or rb_writer.is_folder(row) or rb_writer.node_removed(row):
        return None
    return row


def locate(
    db: Any,
    under: Mapping[str, Any],
    recorded: Sequence[str],
    *,
    account: str,
    name: str,
    job_id: str,
) -> Target | Unfound:
    """The one INBOX playlist the account playlist was mirrored into, or why there is none.

    REFUSED BY NAME when a recorded playlist is live outside INBOX, before any
    report is read. A recorded playlist that is gone or removed is not an
    answer, and the account's name is asked next.
    """
    live = [row for row in (_live_playlist(db, one) for one in recorded) if row is not None]
    outside = [row for row in live if str(row.ID) not in under]
    if outside:
        named = ", ".join(f"{getattr(row, 'Name', '')!r} (row {row.ID})" for row in outside)
        raise refuse(
            OUTSIDE_INBOX,
            f"the landing record of this pass names {named} as the INBOX playlist of the "
            f"account's {name!r}, and it is no longer under INBOX, so it is not this "
            f"verb's to fill; nothing was read from the pass or written",
            remedy=Remedy.COMPLETE_PENDING_ACTION,
            steps=(
                "move the playlist back under INBOX in rekordbox and run it again",
                "or leave it where it is: a playlist kept outside INBOX is the person's",
            ),
            origin=_ORIGIN,
            detail={
                "account": account,
                "account_name": name,
                "playlists": [str(row.ID) for row in outside],
            },
        )
    if live:
        found_by, rows = BY_RECORD, live
    else:
        found_by = BY_NAME
        rows = [
            row
            for row in under.values()
            if not rb_writer.is_folder(row) and str(getattr(row, "Name", "") or "") == name
        ]
    if len(rows) != 1:
        return Unfound(
            account=account,
            account_name=name,
            job_id=job_id,
            why=TWO_FOUND if rows else NOT_FOUND,
            candidates=tuple(str(row.ID) for row in rows),
        )
    (row,) = rows
    return Target(
        account=account,
        account_name=name,
        job_id=job_id,
        playlist_id=str(row.ID),
        name=str(getattr(row, "Name", "") or ""),
        found_by=found_by,
    )


def _pass_unknown(cfg: config.Config, pass_name: str) -> Exception:
    return refuse(
        "job-unknown",
        f"no finished account playlist job of this library carries the pass "
        f"{pass_name!r}, so there is no recorded playlist to refill from",
        steps=(
            "name the pass as crate intake missing --run printed it, ending in _synced",
            "a pass that queued no playlist of the account has nothing to refill",
        ),
        origin=_ORIGIN,
        detail={"pass": pass_name, "library_id": cfg.library.volume_id},
    )


def plan_refill(
    cfg: config.Config,
    db: Any,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
    pass_name: str,
) -> RefillPlan:
    """Plan the refill of every INBOX playlist the pass mirrored. Reads, writes nothing."""
    tree_id = declared.intake.id
    root_id = anchored_root(db, tree_id, registry)
    root = db.get_playlist(ID=root_id)
    named = account_playlists.playlist_jobs(cfg, pass_name)
    if not named:
        raise _pass_unknown(cfg, pass_name)
    under = under_root(db, str(root_id))
    records, _unreadable = session.scan_log(cfg)

    # EVERY PLAYLIST FOUND, OR THE REFUSAL MADE, BEFORE ONE REPORT IS READ.
    located: list[tuple[jobs.Job, Target | Unfound]] = []
    for job, name in named:
        account = account_playlists.account_of(job)
        located.append(
            (
                job,
                locate(
                    db,
                    under,
                    recorded_ids(records, pass_name=pass_name, account=account, name=name),
                    account=account,
                    name=name,
                    job_id=job.job_id,
                ),
            )
        )

    targets: list[Target] = []
    unfound = [one for _job, one in located if isinstance(one, Unfound)]
    wanted = [(job, one) for job, one in located if isinstance(one, Target)]
    if wanted:
        collection = set_playlist._Collection(cfg, db)
        library = set_playlist._LibraryView(cfg)
        with jobs.open_store() as store:
            for job, target in wanted:
                members, left = set_playlist._members(
                    set_playlist.reports_of(store, job),
                    collection=collection,
                    downloaded=lambda one: (library.paths(one), set_playlist.OWNED),
                    owned_again=library.paths,
                )
                present = set(set_playlist.read_back(db, target.playlist_id))
                adds = tuple(
                    content_id
                    for content_id in dict.fromkeys(one.content_id for one in members)
                    if content_id not in present
                )
                targets.append(replace(target, members=members, adds=adds, left=left))
    plan = RefillPlan(
        pass_name=pass_name,
        tree_id=tree_id,
        root_id=str(root_id),
        root_name=str(getattr(root, "Name", "") or ""),
        targets=tuple(targets),
        unfound=tuple(unfound),
    )
    return replace(plan, digest=digest_of(identity(plan)))


def apply_refill(
    cfg: config.Config,
    db: Any,
    plan: RefillPlan,
    *,
    declared: taxonomy.Taxonomy,
    analysis_roots: Iterable[Path | str],
) -> Refilled:
    """Write the approved plan's memberships in one guarded commit and read them back.

    THE PLAN IS TAKEN AGAIN ON THIS HANDLE FIRST, the rotation's rule, and a
    digest that moved refuses with nothing written: the plan the person
    approved was read on a handle that has since closed.

    THE SESSION SPINE IS CALLED, NOT REBUILT, as every database tree writer
    calls it: the gates with a record kept, a capture verified before anything
    is written, the analysis watch over the roots named, the commit witness,
    and the guarded commit, whose whitelist admits the memberships and nothing
    a membership writer does not add.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    registry = tree_registry.read(cfg)
    again = plan_refill(cfg, db, declared=declared, registry=registry, pass_name=plan.pass_name)
    if again.digest != plan.digest:
        raise refuse(
            "decision-stale",
            "INBOX, the collection or the pass is not as the approved plan read it, so "
            "nothing was written; run it again and approve what it shows now",
            origin=_ORIGIN,
            detail={"approved": plan.digest, "now": again.digest},
        )
    convergence.assert_tree_writable(cfg, db, plan.tree_id, registry)

    added: dict[str, tuple[str, ...]] = {}
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record = gates.record
        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)
        try:
            for target in plan.targets:
                if not target.adds:
                    continue
                playlist = db.get_playlist(ID=target.playlist_id)
                added[target.playlist_id] = tuple(
                    rb_writer.add_memberships(db, playlist, target.adds)
                )
            rb_writer.commit_guarded(db)
        except BaseException:
            trees._rollback_quietly(db)
            if witness.landed:
                _record_refill_commit(record, plan, added, cfg)
            raise
        _record_refill_commit(record, plan, added, cfg)
        convergence.record_fingerprint(cfg, db)
        filled = tuple(
            Filled(
                playlist_id=target.playlist_id,
                name=target.name,
                wanted=tuple(dict.fromkeys(one.content_id for one in target.members)),
                added=added.get(target.playlist_id, ()),
                read_back=set_playlist.read_back(db, target.playlist_id),
            )
            for target in plan.targets
            if target.adds
        )
        session_id = record.session_id
    return Refilled(session_id=session_id, filled=filled)


def _record_refill_commit(
    record: session.SessionRecord,
    plan: RefillPlan,
    added: Mapping[str, Sequence[str]],
    cfg: config.Config,
) -> None:
    """Record the commit on the session, under the intake tree, with each playlist named.

    ONLY WHEN A MEMBERSHIP WAS ADDED, the landing's rule for its tree: a record
    saying the tree committed with no change would tell a restore otherwise.
    Named the way the write session guard reads a commit helper.
    """
    count = sum(len(ids) for ids in added.values())
    if not count:
        return
    names = {one.playlist_id: one.name for one in plan.targets}
    record.detail[RECORD_KEY] = {
        "pass": plan.pass_name,
        "playlists": [
            {"id": playlist_id, "name": names.get(playlist_id, ""), "added": len(ids)}
            for playlist_id, ids in added.items()
            if ids
        ],
    }
    changes = (session.TreeChange(tree=plan.tree_id, created=count),)
    session.record_commit(record, plan.tree_id, session.ChangeSummary(changes), cfg)


def assert_read_back(refilled: Refilled) -> None:
    """Refuse an answer the database does not hold: every wanted row live, in order when filled.

    EVERY ROW THE PLAYLIST SHOULD HOLD IS READ BACK LIVE, whatever it held
    before. THE ACCOUNT'S ORDER IS HELD ONLY FOR A PLAYLIST THIS COMMIT FILLED,
    one that held none of its rows before, for the set playlist's reason: a
    playlist that held some appends what it lacked after them, which is
    rekordbox's own order for an added track.
    """
    for one in refilled.filled:
        live = set(one.read_back)
        missing = [content_id for content_id in one.wanted if content_id not in live]
        filled = len(one.added) == len(one.wanted)
        wanted = set(one.wanted)
        in_order = [content_id for content_id in one.read_back if content_id in wanted] == list(
            one.wanted
        )
        if missing or (filled and not in_order):
            raise refuse(
                "session-committed-unverified",
                f"the INBOX playlist {one.name!r} ({one.playlist_id}) read back from the "
                f"database holds {len(one.read_back)} live track(s), {len(missing)} of "
                f"the {len(one.wanted)} the plan named not among them"
                + ("" if missing else " and not in the account's order")
                + "; the commit landed and this answer cannot be vouched for",
                origin=_ORIGIN,
                detail={
                    "playlist_id": one.playlist_id,
                    "planned": list(one.wanted),
                    "read": list(one.read_back),
                    "missing": missing,
                },
            )


__all__ = [
    "ADD",
    "BY_NAME",
    "BY_RECORD",
    "HELD",
    "NOT_FOUND",
    "OUTSIDE_INBOX",
    "RECORD_KEY",
    "TWO_FOUND",
    "WORKFLOW",
    "Filled",
    "RefillPlan",
    "Refilled",
    "Target",
    "Unfound",
    "anchored_root",
    "apply_refill",
    "assert_read_back",
    "identity",
    "locate",
    "plan_refill",
    "recorded_ids",
    "under_root",
]
