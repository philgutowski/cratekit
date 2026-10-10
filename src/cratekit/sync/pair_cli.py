"""``crate sync pair``: keep the author's own account playlist and its rekordbox playlist one list.

U130, decided by Phillip on 2026-10-10: a playlist the author made, on the
account or in rekordbox, and marked for sync, stays the same list on both sides
after every sync, each side merged against the last sync. ``intake playlist``
pulls one way and ``export playlist`` pushes the other; this verb does both for
a pair, and removes as well as adds, because a removal on either side is applied
on both.

**WHAT A PAIR MAY HOLD.** One of the author's own account playlists, which is
one the account lists as the author's (the catalogue keeps only those), and one
plain rekordbox playlist, each named by its identifier and never by its name
(R-906). Refused before anything is listed track by track: the hearts, a
label's year or dated playlist, a set playlist, the label batch's debris, a
favourites placeholder, a rekordbox folder or smart playlist, and any rekordbox
playlist under one of Cratekit's own trees, which is a node under a tree root
the registry records or under a top level node carrying a name the taxonomy
declares for one of its trees. Those lists are Cratekit's to write, and a pair
writing them too would be two writers on one list.

**HOW A PAIR IS MARKED.** ``crate sync pair ACCOUNT_ID --rekordbox PLAYLIST_ID``
names a pair, and the pair is recorded when its first sync is approved on
either side. ``crate sync pair ACCOUNT_ID`` syncs a marked pair, and
``crate sync pair`` with no argument syncs every marked pair. The record and the
snapshot are ``modules/outbound/pairs.py``'s, and the merge is
``sync/pair_merge.py``'s.

**HOW A TRACK IS MATCHED ACROSS THE SIDES.** A match one sync made is recorded
on the pair as a link and reused. A rekordbox row with no link is matched on the
account ISRC first, through the account seam ``export playlist`` uses, with the
code read from the database and else from the row's audio file; a row it does
not match is NAMED on the gate and in the answer with the account's reason, and
stays in rekordbox. An account track with no link is looked for in the library:
a live row carrying its ISRC, a row an intake job this pair queued resolved it
to, or a row of the INBOX playlist a landing made for this account playlist
(U128) whose file carries its ISRC. A track found nowhere is QUEUED FOR
ACQUISITION through the intake path, ``intake.playlist`` exactly as
``intake playlist`` queues it, and never written to rekordbox as a row without a
file. A track an earlier sync queued is not queued again and is named as
awaiting.

**TWO GATES, BOTH ASKED BEFORE ANYTHING IS WRITTEN.** ``sync.pair.rekordbox``
and ``sync.pair.account`` each show the whole plan, every addition and every
removal on both sides by artist and title, and each answers for its own side.
Both are explicit (R34), digest bound to the plan, so a list that moved between
the plan and the write refuses as stale. Rekordbox is written first, through the
session spine and the native writer's guarded commit, behind the backup
acknowledgment read before the plan; then the account, through the account
seam, whose removals and orders a pair vouches for. A side whose gate is
answered ``skip`` is not written and its snapshot is not moved, so the next sync
finishes it.

**A REMOVAL OWED IS REMEMBERED.** When a removal one side made is not applied
on the other, because that side was skipped or the account could not take it,
the snapshot of the side that removed it keeps the track, so the next sync still
reads it as removed there rather than adding it back.

**A SHORT ACCOUNT LISTING REMOVES NOTHING.** The provider counts tracks it will
not serve. A track it withheld would read as one the author removed, so when the
listing is short no account track is read as removed, the account side takes no
removal and no reorder, and the answer says how many were withheld.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cratekit.acquire import match
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import analysis_store, config, jobs, locations, rb_writer, session, tags
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.favorites import placeholders
from cratekit.intake import cli as intake_cli
from cratekit.intake import ingest
from cratekit.sync import cli as sync_cli
from cratekit.sync import pair_merge, playlists
from cratekit.write import playlist_pair

_ORIGIN = ("sync.pair",)

REKORDBOX_GATE = "sync.pair.rekordbox"
ACCOUNT_GATE = "sync.pair.account"
APPLY = "apply"

#: The handler key an acquisition is queued under: the ``intake playlist`` job,
#: which resolves each track to owned, offered or missing for ``acquire`` to
#: download and ``intake land`` to land, exactly as a playlist run by hand.
INTAKE_HANDLER = "intake.playlist"

#: The ``source_id`` every job this verb queues carries, so a later sync finds
#: the tracks it already queued for a pair and does not queue them again.
PAIR_SOURCE = "playlist-pair"

#: The two halves of a key, so a track the account carries and a rekordbox row
#: it does not are never one key by accident.
REMOTE = "r:"
ROW = "c:"

#: What an unmatched row is said to be when the account gave no reason.
NO_MATCH = "the account has no track this row's ISRC names"

#: The warning codes the answer carries.
UNMATCHED = "sync-pair-unmatched"
AWAITING = "sync-pair-awaiting"
AMBIGUOUS = "sync-pair-ambiguous"
WITHHELD = "sync-pair-withheld"
SKIPPED = "sync-pair-skipped"
NOTHING = "sync-pair-nothing"
WRITTEN = "sync-pair-written"

#: The row a snapshot gives a membership it keeps only as an owed removal. No
#: membership row carries it, so a track put back in rekordbox reads as added.
OWED_ROW = "owed"

#: The item states an intake job's report gives a track the library holds.
OWNED_STATE = "owned"


def remote_key(remote_id: str) -> str:
    return REMOTE + str(remote_id)


def row_key(content_id: str) -> str:
    return ROW + str(content_id)


def remote_of(key: str) -> str:
    return key[len(REMOTE) :] if key.startswith(REMOTE) else ""


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument(
        "account",
        nargs="?",
        default=None,
        metavar="ACCOUNT_PLAYLIST",
        help=(
            "the account playlist's identifier; with no argument every marked "
            "pair is synced"
        ),
    )
    parser.add_argument(
        "--rekordbox",
        default=None,
        metavar="PLAYLIST_ID",
        help=(
            "the rekordbox playlist's identifier, to mark a new pair; a marked "
            "pair needs none"
        ),
    )
    parser.set_defaults(_handler=sync_pair)


# ---------------------------------------------------------------------------
# What is asked
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Target:
    """One pair a sync was asked for, and whether it is marked yet."""

    account_id: str
    rekordbox_id: str
    marked: bool


def _unknown(message: str, *, steps: Sequence[str], **detail: Any) -> CratekitError:
    return refuse(
        "sync-pair-unknown", message, steps=tuple(steps), origin=_ORIGIN, detail=dict(detail)
    )


def _out_of_scope(message: str, **detail: Any) -> CratekitError:
    return refuse(
        "sync-pair-out-of-scope",
        message,
        steps=("pair one of your own account playlists with a rekordbox playlist you made",),
        origin=_ORIGIN,
        detail=dict(detail),
    )


def targets(
    store, account_id: str | None, rekordbox_id: str | None
) -> tuple[Target, ...]:
    """The pairs this invocation syncs, refused when the arguments name none."""
    held = store.all()
    if not account_id:
        if rekordbox_id:
            raise _unknown(
                "a rekordbox playlist was named with no account playlist to pair it "
                "with, so nothing was synced",
                steps=("name the account playlist before --rekordbox",),
                rekordbox_id=str(rekordbox_id),
            )
        return tuple(
            Target(pair.account_id, pair.rekordbox_id, True)
            for _key, pair in sorted(held.items())
        )
    account_id = str(account_id).strip()
    if intake_cli.is_favorites(account_id):
        raise _out_of_scope(
            "the account's hearts are not a playlist a pair may hold, so nothing was "
            "synced",
            account_id=account_id,
        )
    pair = held.get(account_id)
    if pair is not None:
        if rekordbox_id and str(rekordbox_id) != pair.rekordbox_id:
            from cratekit.modules.outbound import pairs

            raise pairs.conflict(account_id, str(rekordbox_id), pair)
        return (Target(account_id, pair.rekordbox_id, True),)
    if not rekordbox_id:
        raise _unknown(
            f"the account playlist {account_id} is not paired with a rekordbox "
            f"playlist, so there is nothing to sync it with",
            steps=(
                f"pair it first with crate sync pair {account_id} --rekordbox "
                f"PLAYLIST_ID",
            ),
            account_id=account_id,
        )
    for other in held.values():
        if other.rekordbox_id == str(rekordbox_id):
            from cratekit.modules.outbound import pairs

            raise pairs.conflict(account_id, str(rekordbox_id), other)
    return (Target(account_id, str(rekordbox_id), False),)


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Named:
    """One track as a person reads it on the gate."""

    key: str
    artist: str
    title: str
    remote_id: str = ""
    content_id: str = ""
    reason: str = ""

    def shown(self) -> dict[str, str]:
        block = {"artist": self.artist, "title": self.title}
        if self.remote_id:
            block["remote_id"] = self.remote_id
        if self.content_id:
            block["content_id"] = self.content_id
        if self.reason:
            block["reason"] = self.reason
        return block


@dataclass
class PairPlan:
    """One pair's sync, decided: the merge, and what each side and the queue are asked."""

    target: Target
    name: str
    rekordbox_name: str
    first: bool
    merged: pair_merge.Merged
    account_now: tuple[str, ...]
    rekordbox_before: tuple[tuple[str, str], ...]
    change: playlist_pair.Change
    account_adds: tuple[str, ...] = ()
    account_removes: tuple[str, ...] = ()
    account_order: tuple[str, ...] | None = None
    #: Rekordbox rows the account has no track for, named with the reason.
    unmatched: tuple[Named, ...] = ()
    #: Account tracks the library lacks, by remote id, as the intake job freezes them.
    acquire: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: Account tracks an earlier sync of this pair already queued.
    awaiting: tuple[Named, ...] = ()
    #: Account tracks two live library rows carry, so no row is chosen.
    ambiguous: tuple[Named, ...] = ()
    #: Links this plan made, remote id to content id.
    links: dict[str, str] = field(default_factory=dict)
    #: Every key's words, for the screen.
    names: dict[str, Named] = field(default_factory=dict)
    #: Remote id to content id for every key the plan resolved.
    content_of: dict[str, str] = field(default_factory=dict)
    #: The memberships the rekordbox snapshot held, by key, for owed removals.
    base_members: dict[str, tuple[str, str]] = field(default_factory=dict)
    #: ``ListingShortfall.block()`` when the account listing was short.
    withheld: dict[str, int] | None = None

    @property
    def account_writes(self) -> bool:
        return bool(self.account_adds or self.account_removes or self.account_order)

    @property
    def rekordbox_writes(self) -> bool:
        return not self.change.empty

    def identity(self) -> dict[str, Any]:
        """What the gate's digest covers for this pair. Identifiers only, no path."""
        return {
            "account_id": self.target.account_id,
            "rekordbox_id": self.target.rekordbox_id,
            "marked": self.target.marked,
            "account_now": list(self.account_now),
            "rekordbox_before": [list(one) for one in self.rekordbox_before],
            "rekordbox_adds": list(self.change.adds),
            "rekordbox_removes": list(self.change.removes),
            "rekordbox_order": list(self.change.order),
            "account_adds": list(self.account_adds),
            "account_removes": list(self.account_removes),
            "account_order": list(self.account_order or ()),
            "acquire": sorted(self.acquire),
        }


def _scope_account(
    account_id: str,
    listed: Mapping[str, Any],
    label_owned: frozenset[str],
    set_built: frozenset[str],
) -> str:
    """The account playlist's name, or the refusal saying why a pair may not hold it."""
    playlist = listed.get(account_id)
    if playlist is None:
        raise _unknown(
            f"the account does not list {account_id} among the author's own "
            f"playlists, so it was not synced",
            steps=("name one of your own account playlists by its identifier",),
            account_id=account_id,
        )
    name = str(playlist.name or "")
    if account_id in label_owned:
        raise _out_of_scope(
            f"{name!r} ({account_id}) is a label's playlist, which label playlists "
            f"and label heard keep, so it was not synced",
            account_id=account_id,
        )
    if account_id in set_built:
        raise _out_of_scope(
            f"{name!r} ({account_id}) is a set's playlist, which export set keeps, "
            f"so it was not synced",
            account_id=account_id,
        )
    if playlists.is_library_debris(name) or placeholders.is_placeholder(name):
        raise _out_of_scope(
            f"{name!r} ({account_id}) is a playlist the source system makes for its "
            f"own runs, so it was not synced",
            account_id=account_id,
        )
    return name


def generated_tops(declared, registry) -> tuple[frozenset[str], frozenset[str]]:
    """The tree roots the registry records, and the top level names the taxonomy declares."""
    roots = frozenset(
        str(record.root_id) for record in registry.trees if record.root_id
    )
    names = frozenset(
        node.display
        for node in (
            declared.tree,
            declared.intake,
            declared.catalog,
            declared.long_tracks,
            declared.inspiration,
        )
        if node is not None and node.display
    )
    return roots, names


def _scope_rekordbox(
    rekordbox_id: str,
    found: playlist_pair.Playlist | None,
    tops: tuple[frozenset[str], frozenset[str]],
) -> playlist_pair.Playlist:
    if found is None or found.removed:
        raise _unknown(
            f"the rekordbox library holds no live playlist {rekordbox_id}, so the pair "
            f"was not synced",
            steps=("name a rekordbox playlist by the identifier rekordbox gives it",),
            rekordbox_id=rekordbox_id,
        )
    if not found.plain:
        raise _out_of_scope(
            f"the rekordbox node {found.name!r} ({rekordbox_id}) is a folder or a "
            f"smart playlist, which holds no list a pair could keep",
            rekordbox_id=rekordbox_id,
        )
    roots, names = tops
    chain = ((found.playlist_id, found.name), *found.ancestors)
    top_id, top_name = found.top
    if any(node_id in roots for node_id, _name in chain) or top_name in names:
        raise _out_of_scope(
            f"the rekordbox playlist {found.name!r} ({rekordbox_id}) sits under "
            f"{top_name!r}, one of Cratekit's own trees, which Cratekit writes",
            rekordbox_id=rekordbox_id,
            top=top_id,
        )
    return found


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
    _remote: list[Any] = field(default_factory=list)
    _by_isrc: list[dict[str, tuple[str, ...]]] = field(default_factory=list)

    def remote(self):
        """The account, resolved on first use, so a plan with nothing to match asks nothing."""
        if not self._remote:
            from cratekit.modules.outbound import account

            self._remote.append(account.resolve(self.cfg))
        return self._remote[0]

    def by_isrc(self) -> dict[str, tuple[str, ...]]:
        if not self._by_isrc:
            self._by_isrc.append(playlist_pair.rows_by_isrc(self.db, match.isrc_token))
        return self._by_isrc[0]


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


def _pair_jobs(store, cfg: config.Config, account_id: str) -> tuple[jobs.Job, ...]:
    """Every intake job this verb queued for this pair on this library, newest first."""
    return tuple(
        job
        for job in jobs.list_jobs(store)
        if job.handler_key == INTAKE_HANDLER
        and job.library_id == cfg.library.volume_id
        and (job.payload or {}).get("source_id") == PAIR_SOURCE
        and str((job.payload or {}).get(intake_cli.SOURCE) or "") == account_id
        and job.state not in (jobs.JobState.FAILED, jobs.JobState.CANCELLED)
    )


def _owned_by_jobs(
    reader: _Reader, found: Sequence[jobs.Job], wanted: set[str]
) -> dict[str, str]:
    """Remote id to content id, for each wanted track a pair's intake job found owned."""
    from cratekit.intake import missing_cli, native

    paths: dict[str, Path] = {}
    for job in found:
        if job.state != jobs.JobState.SUCCEEDED:
            continue
        try:
            reports = missing_cli.job_reports(reader.store, job)
        except CratekitError:
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


def _mirror_isrcs(reader: _Reader, account_id: str, skip: set[str]) -> dict[str, tuple[str, ...]]:
    """ISRC to content ids, read from the files of the INBOX playlists landed for this account.

    U128 records each INBOX playlist a landing made for an account playlist
    with the account playlist's identifier. A track this pair queued and
    a landing brought sits there, and its row may carry no ISRC of its own,
    since a landed row's code is in its file. Only those rows' files are read.
    """
    standing = {
        session.SessionState.AWAITING_IMPORT,
        session.SessionState.COMMITTED_UNVERIFIED,
        session.SessionState.CLOSED,
    }
    records, _unreadable = session.scan_log(reader.cfg)
    mirrors = {
        str(entry.get("id"))
        for record in records
        if record.workflow == ingest.INTAKE_WORKFLOW and record.state in standing
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ()
        if isinstance(entry, dict)
        and str(entry.get(ingest.INBOX_ACCOUNT_KEY) or "") == account_id
        and entry.get("id")
    }
    found: dict[str, list[str]] = {}
    for mirror in sorted(mirrors):
        for row in playlist_pair.members(reader.db, mirror):
            if row.content_id in skip:
                continue
            code = match.isrc_token(row.isrc) or file_identity(reader.cfg, row.path)[0]
            if code and row.content_id not in found.setdefault(code, []):
                found[code].append(row.content_id)
    return {code: tuple(ids) for code, ids in found.items()}


def plan_pair(reader: _Reader, target: Target, held) -> PairPlan:
    """Read both sides of one pair, match them, merge them, and say what to write."""
    cfg = reader.cfg
    name = _scope_account(target.account_id, reader.listed, reader.label_owned, reader.set_built)
    rekordbox = _scope_rekordbox(
        target.rekordbox_id,
        playlist_pair.read_playlist(reader.db, target.rekordbox_id),
        reader.tops,
    )
    tracks, short = intake_cli.list_playlist_declared(reader.found, target.account_id)
    account_now = pair_merge.distinct(tracks)

    # ── the links, kept only while their rows are live ──────────────────────
    recorded = dict(held.links) if held is not None else {}
    live = playlist_pair.content(reader.db, recorded.values())
    links = {remote: row for remote, row in recorded.items() if row in live}
    made: dict[str, str] = {}

    # ── rekordbox now, as keys ──────────────────────────────────────────────
    template = None
    by_row = {row: remote for remote, row in links.items()}
    seen_remote: dict[str, str] = {}
    rekordbox_keys: list[str] = []
    names: dict[str, Named] = {}
    content_of: dict[str, str] = {}
    unmatched: list[Named] = []
    rows = playlist_pair.by_content(rekordbox.rows)
    for row in rows.values():
        remote_id = by_row.get(row.content_id, "")
        reason = ""
        if not remote_id:
            from cratekit.core import naming
            from cratekit.modules.outbound import source

            if template is None:
                template = source.name_template(cfg)
            isrc = match.isrc_token(row.isrc)
            album = ""
            if not isrc:
                isrc, album = file_identity(cfg, row.path)
            remote = reader.remote()
            remote_id = str(
                remote.match_track(
                    identity=row.content_id,
                    isrc=isrc,
                    title=naming.strip_heads(row.title, template=template),
                    artist=row.artist,
                    album=album,
                )
                or ""
            )
            if not remote_id:
                reason = remote.unmatched_reason(row.content_id) or NO_MATCH
        if remote_id and remote_id in seen_remote:
            other = rows[seen_remote[remote_id]]
            remote_id = ""
            reason = (
                f"another row of this playlist, {other.artist} - {other.title}, is "
                f"already the account track it matches"
            )
        if remote_id:
            key = remote_key(remote_id)
            seen_remote[remote_id] = row.content_id
            if remote_id not in links:
                made[remote_id] = row.content_id
        else:
            key = row_key(row.content_id)
        content_of[key] = row.content_id
        rekordbox_keys.append(key)
        names[key] = Named(
            key=key,
            artist=row.artist,
            title=row.title,
            remote_id=remote_id,
            content_id=row.content_id,
            reason=reason,
        )
        if not remote_id:
            unmatched.append(names[key])
    known = {**links, **made}

    # ── the account now, as keys ────────────────────────────────────────────
    account_keys = [remote_key(remote_id) for remote_id in account_now]
    for remote_id in account_now:
        key = remote_key(remote_id)
        said = tracks[remote_id]
        if key not in names:
            names[key] = Named(
                key=key,
                artist=str(said.get("artist") or ""),
                title=str(said.get("title") or ""),
                remote_id=remote_id,
                content_id=known.get(remote_id, ""),
            )

    # ── the bases ───────────────────────────────────────────────────────────
    base: pair_merge.Base | None = None
    readded: set[str] = set()
    base_members: dict[str, tuple[str, str]] = {}
    row_to_remote = {**by_row, **{row: remote for remote, row in made.items()}}

    def as_key(content_id: str) -> str:
        remote_id = row_to_remote.get(content_id, "")
        return remote_key(remote_id) if remote_id else row_key(content_id)

    if held is not None and not held.first:
        base_account = tuple(remote_key(one) for one in held.account or ())
        if short is not None:
            # A WITHHELD TRACK IS NOT A REMOVED ONE. Which tracks the provider
            # left out is not known, so no track the base held is read as gone.
            base_account = tuple(key for key in base_account if key in set(account_keys))
        base_rows = {member.content_id: member.row_id for member in held.rekordbox or ()}
        base_members = {
            as_key(member.content_id): (member.content_id, member.row_id)
            for member in held.rekordbox or ()
        }
        base_rekordbox = tuple(as_key(member.content_id) for member in held.rekordbox or ())
        current_rows = {row.content_id: row.row_id for row in rows.values()}
        readded = {
            as_key(content_id)
            for content_id, row_id in current_rows.items()
            if content_id in base_rows and base_rows[content_id] != row_id
        }
        base = pair_merge.Base(account=base_account, rekordbox=base_rekordbox)

    merged = pair_merge.merge(
        base,
        pair_merge.Side(tuple(account_keys)),
        pair_merge.Side(tuple(rekordbox_keys), frozenset(readded)),
    )

    # ── what rekordbox is asked: adds need a live row, never a row without a file
    rekordbox_held = set(rekordbox_keys) - set(merged.remove_rekordbox)
    adds: list[str] = []
    acquire: dict[str, dict[str, Any]] = {}
    awaiting: list[Named] = []
    ambiguous: list[Named] = []
    lacking = [
        remote_of(key) for key in merged.add_rekordbox if remote_of(key) not in known
    ]
    found_rows = _owned(reader, target.account_id, tracks, lacking)
    queued_before = _queued(reader, target.account_id)
    for key in merged.add_rekordbox:
        remote_id = remote_of(key)
        content_id = known.get(remote_id, "")
        if not content_id:
            answer = found_rows.get(remote_id, ())
            if len(answer) == 1:
                content_id = answer[0]
                made[remote_id] = content_id
                known[remote_id] = content_id
            elif len(answer) > 1:
                ambiguous.append(
                    _with_reason(names[key], f"{len(answer)} library rows carry its ISRC")
                )
                continue
        if content_id:
            content_of[key] = content_id
            adds.append(content_id)
            rekordbox_held.add(key)
            continue
        if remote_id in queued_before:
            awaiting.append(names[key])
        else:
            acquire[remote_id] = dict(tracks[remote_id])
    order = tuple(
        content_of[key] for key in merged.order if key in rekordbox_held and key in content_of
    )
    change = playlist_pair.Change(
        playlist_id=rekordbox.playlist_id,
        before=rekordbox.memberships(),
        adds=tuple(dict.fromkeys(adds)),
        removes=tuple(
            content_of[key] for key in merged.remove_rekordbox if key in content_of
        ),
        order=tuple(dict.fromkeys(order)),
    )

    # ── what the account is asked ───────────────────────────────────────────
    account_adds = tuple(remote_of(key) for key in merged.add_account if remote_of(key))
    account_removes: tuple[str, ...] = ()
    account_order: tuple[str, ...] | None = None
    if short is None:
        account_removes = tuple(remote_of(key) for key in merged.remove_account)
        after = pair_merge.appended(account_now, account_removes, account_adds)
        wanted = tuple(
            remote_of(key)
            for key in pair_merge.as_held(merged.order, {remote_key(one) for one in after})
        )
        if wanted != after:
            account_order = wanted

    return PairPlan(
        target=target,
        name=name,
        rekordbox_name=rekordbox.name,
        first=merged.first,
        merged=merged,
        account_now=account_now,
        rekordbox_before=rekordbox.memberships(),
        change=change,
        account_adds=account_adds,
        account_removes=account_removes,
        account_order=account_order,
        unmatched=tuple(unmatched),
        acquire=acquire,
        awaiting=tuple(awaiting),
        ambiguous=tuple(ambiguous),
        links=made,
        names=names,
        content_of=content_of,
        base_members=base_members,
        withheld=short.block() if short is not None else None,
    )


def _with_reason(named: Named, reason: str) -> Named:
    return Named(
        key=named.key,
        artist=named.artist,
        title=named.title,
        remote_id=named.remote_id,
        content_id=named.content_id,
        reason=reason,
    )


def _owned(
    reader: _Reader,
    account_id: str,
    tracks: Mapping[str, Mapping[str, Any]],
    lacking: Sequence[str],
) -> dict[str, tuple[str, ...]]:
    """Each lacking account track's library rows: by ISRC, by an intake job, by its landing."""
    if not lacking:
        return {}
    found: dict[str, tuple[str, ...]] = {}
    codes = {
        remote_id: match.isrc_token((tracks.get(remote_id) or {}).get("isrc"))
        for remote_id in lacking
    }
    by_isrc = reader.by_isrc()
    for remote_id, code in codes.items():
        if code and by_isrc.get(code):
            found[remote_id] = by_isrc[code]
    rest = {remote_id for remote_id in lacking if remote_id not in found}
    if rest:
        for remote_id, content_id in _owned_by_jobs(
            reader, _pair_jobs(reader.store, reader.cfg, account_id), rest
        ).items():
            found[remote_id] = (content_id,)
    rest = {remote_id for remote_id in lacking if remote_id not in found and codes.get(remote_id)}
    if rest:
        landed = _mirror_isrcs(reader, account_id, skip=set())
        for remote_id in rest:
            if landed.get(codes[remote_id]):
                found[remote_id] = landed[codes[remote_id]]
    return found


def _queued(reader: _Reader, account_id: str) -> frozenset[str]:
    """Every track an intake job this verb queued for the pair still holds or resolved."""
    return frozenset(
        str(item)
        for job in _pair_jobs(reader.store, reader.cfg, account_id)
        for item in (job.payload or {}).get(intake_cli.TRACKS) or {}
    )


@dataclass
class Plan:
    """Every pair this invocation syncs, decided."""

    pairs: tuple[PairPlan, ...] = ()

    @property
    def digest(self) -> str:
        return digest_of({"kind": "sync.pair", "pairs": [one.identity() for one in self.pairs]})

    @property
    def writes(self) -> bool:
        return any(
            one.rekordbox_writes or one.account_writes or one.acquire or not one.target.marked
            for one in self.pairs
        )


def plan(cfg: config.Config, wanted: Sequence[Target], *, store) -> Plan:
    """Read the account and the database once, and plan every pair."""
    if not wanted:
        return Plan()
    from cratekit.core import active_taxonomy, tree_registry
    from cratekit.label import catalogue
    from cratekit.modules.outbound import ledger, pairs

    held = pairs.PairStore(cfg).all()
    found = catalogue.resolve(cfg)
    listed = {one.playlist_id: one for one in playlists._listed_or_refuse(found)}
    label_owned = ledger.label_playlist_ids(cfg) | ledger.label_dated_ids(cfg)
    set_built = ledger.set_playlist_ids(cfg)
    tops = generated_tops(active_taxonomy.load(cfg), tree_registry.read(cfg))
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        reader = _Reader(
            cfg=cfg,
            db=db,
            found=found,
            listed=listed,
            label_owned=label_owned,
            set_built=set_built,
            tops=tops,
            store=store,
        )
        return Plan(
            tuple(plan_pair(reader, target, held.get(target.account_id)) for target in wanted)
        )
    finally:
        rb_writer.close_db(db)


# ---------------------------------------------------------------------------
# The screen
# ---------------------------------------------------------------------------


def _items(one: PairPlan) -> list[dict[str, Any]]:
    """Every change one pair's sync makes, by name, both sides, in the order it is written."""
    by_content = {content_id: one.names.get(key) for key, content_id in one.content_of.items()}
    by_remote = {named.remote_id: named for named in one.names.values() if named.remote_id}

    def row(side: str, action: str, named: Named | None, **extra: Any) -> dict[str, Any]:
        return {
            "pair": one.target.account_id,
            "side": side,
            "action": action,
            **(named.shown() if named is not None else {}),
            **extra,
        }

    items: list[dict[str, Any]] = []
    for content_id in one.change.removes:
        items.append(row("rekordbox", "remove", by_content.get(content_id)))
    for content_id in one.change.adds:
        items.append(row("rekordbox", "add", by_content.get(content_id), content_id=content_id))
    if one.change.order and not one.change.empty and _reordered(one):
        items.append(row("rekordbox", "order", None, tracks=len(one.change.order)))
    for remote_id in one.account_removes:
        items.append(row("account", "remove", by_remote.get(remote_id)))
    for remote_id in one.account_adds:
        items.append(row("account", "add", by_remote.get(remote_id)))
    if one.account_order:
        items.append(row("account", "order", None, tracks=len(one.account_order)))
    for remote_id in one.acquire:
        items.append(row("library", "acquire", by_remote.get(remote_id)))
    for named in one.awaiting:
        items.append(row("library", "awaiting", named))
    for named in one.unmatched:
        items.append(row("account", "unmatched", named))
    for named in one.ambiguous:
        items.append(row("rekordbox", "ambiguous", named))
    return items


def _reordered(one: PairPlan) -> bool:
    before = [content_id for content_id, _row in one.change.before]
    expected = pair_merge.appended(before, one.change.removes, one.change.adds)
    return tuple(expected) != one.change.order


def payload(planned: Plan) -> dict[str, Any]:
    """The plan as both gates show it: one item per change, both sides named."""
    items = [item for one in planned.pairs for item in _items(one)]

    def count(side: str, action: str) -> int:
        return sum(1 for item in items if item["side"] == side and item["action"] == action)

    return {
        "digest": planned.digest,
        "items": items,
        "totals": {
            "count": len(items),
            "pairs": len(planned.pairs),
            "first": sum(1 for one in planned.pairs if one.first),
            "rekordbox_adds": count("rekordbox", "add"),
            "rekordbox_removes": count("rekordbox", "remove"),
            "account_adds": count("account", "add"),
            "account_removes": count("account", "remove"),
            "acquire": count("library", "acquire"),
            "awaiting": count("library", "awaiting"),
            "unmatched": count("account", "unmatched"),
            "ambiguous": count("rekordbox", "ambiguous"),
        },
        "chunk": None,
    }


def facts(planned: Plan) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per pair."""
    shown: dict[str, Any] = {"pairs": len(planned.pairs)}
    for one in planned.pairs:
        lead = "the account's" if one.merged.leader == pair_merge.ACCOUNT else "rekordbox's"
        shown[f"pair {one.target.account_id}"] = (
            f"{one.name!r} on the account with {one.rekordbox_name!r} "
            f"({one.target.rekordbox_id}) in rekordbox; "
            + ("first sync, additions only; " if one.first else "")
            + ("not yet marked, approving marks it; " if not one.target.marked else "")
            + f"order follows {lead}"
            + (
                f"; the account withheld {one.withheld.get('withheld', 0)} track(s), so "
                f"nothing is removed or reordered there"
                if one.withheld
                else ""
            )
        )
    return shown


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


@dataclass
class Done:
    """What one pair's sync did."""

    account_id: str
    rekordbox: playlist_pair.Written | None = None
    account_added: int = 0
    account_removed: int = 0
    account_ordered: bool = False
    queued: str = ""
    marked: bool = False


def _record(
    cfg: config.Config,
    one: PairPlan,
    *,
    rekordbox_after: Sequence[playlist_pair.Row] | None,
    account_after: Sequence[str] | None,
) -> None:
    """Record each written side's snapshot, keeping the removals the other side owes.

    A side passed None was not written and keeps the snapshot it had. A track
    the merge removed that this side no longer holds and the other side still
    does is kept in this side's snapshot, so the next sync reads it as removed
    here again and takes it off the other side then.
    """
    from cratekit.modules.outbound import pairs

    removed = sorted(set(one.merged.remove_account) | set(one.merged.remove_rekordbox))
    to_key = {content_id: key for key, content_id in one.content_of.items()}
    held_rekordbox = (
        {to_key.get(row.content_id, row_key(row.content_id)) for row in rekordbox_after}
        if rekordbox_after is not None
        else {
            to_key.get(content_id, row_key(content_id))
            for content_id, _row in one.rekordbox_before
        }
    )
    held_account = {
        remote_key(remote_id)
        for remote_id in (account_after if account_after is not None else one.account_now)
    }

    rekordbox_base: list[pairs.Membership] | None = None
    if rekordbox_after is not None:
        rekordbox_base = [
            pairs.Membership(row.content_id, row.row_id)
            for row in playlist_pair.by_content(rekordbox_after).values()
        ]
        for key in removed:
            if key in held_rekordbox or key not in held_account:
                continue
            content_id, row_id = one.base_members.get(key) or (one.content_of.get(key, ""), "")
            if content_id:
                rekordbox_base.append(pairs.Membership(content_id, row_id or OWED_ROW))
    account_base: list[str] | None = None
    if account_after is not None:
        account_base = list(pair_merge.distinct(account_after))
        for key in removed:
            if key in held_account or key not in held_rekordbox or not remote_of(key):
                continue
            account_base.append(remote_of(key))
    pairs.PairStore(cfg).record(
        one.target.account_id,
        account=account_base,
        rekordbox=rekordbox_base,
        links=one.links,
        name=one.name,
    )


def apply_pair(
    cfg: config.Config, one: PairPlan, *, rekordbox: bool, account: bool, store
) -> Done:
    """Write one pair: mark it, rekordbox and the queue, then the account, then its snapshot."""
    from cratekit.modules.outbound import pairs

    done = Done(account_id=one.target.account_id)
    if not (rekordbox or account):
        return done
    pairs.PairStore(cfg).mark(one.target.account_id, one.target.rekordbox_id, name=one.name)
    done.marked = not one.target.marked

    rekordbox_after: tuple[playlist_pair.Row, ...] | None = None
    if rekordbox:
        db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
        try:
            if one.rekordbox_writes:
                written = playlist_pair.apply(
                    cfg,
                    db,
                    one.change,
                    source=f"{PAIR_SOURCE}:{one.target.rekordbox_id}",
                    analysis_roots=analysis_store.watch_roots(cfg),
                )
                playlist_pair.assert_read_back(written, one.change)
                done.rekordbox = written
                rekordbox_after = written.read_back
            else:
                rekordbox_after = playlist_pair.members(db, one.target.rekordbox_id)
        finally:
            rb_writer.close_db(db)
        if one.acquire:
            job = intake_cli.queue_playlist(
                store,
                cfg,
                handler_key=INTAKE_HANDLER,
                reference=one.target.account_id,
                tracks=one.acquire,
                source_id=PAIR_SOURCE,
                name=one.name,
            )
            done.queued = job.job_id
        # THE REKORDBOX SNAPSHOT IS RECORDED NOW, before the account is asked,
        # so an account that fails leaves the rekordbox side recorded as written.
        _record(cfg, one, rekordbox_after=rekordbox_after, account_after=None)

    if account:
        from cratekit.modules.outbound import account as outbound_account

        remote = outbound_account.resolve(cfg)
        playlist_id = one.target.account_id
        if one.account_removes:
            done.account_removed = len(remote.remove_tracks(playlist_id, one.account_removes))
        if one.account_adds:
            done.account_added = len(set(remote.add_tracks(playlist_id, one.account_adds)))
        if one.account_order:
            after = tuple(remote.order_tracks(playlist_id, one.account_order))
            done.account_ordered = True
        else:
            after = tuple(remote.playlist_tracks(playlist_id))
        _record(cfg, one, rekordbox_after=rekordbox_after, account_after=after)
    return done


def _warnings(planned: Plan) -> list[dict[str, str]]:
    """What the plan could not do, said by name, one warning per kind."""
    said: list[dict[str, str]] = []

    def listed(rows: Sequence[Named]) -> str:
        return "; ".join(
            f"{row.artist} - {row.title}" + (f" ({row.reason})" if row.reason else "")
            for row in rows
        )

    unmatched = [row for one in planned.pairs for row in one.unmatched]
    if unmatched:
        said.append(
            {
                "code": UNMATCHED,
                "message": (
                    f"{len(unmatched)} rekordbox track(s) have no match on the account "
                    f"and stay in rekordbox only: {listed(unmatched)}"
                ),
            }
        )
    awaiting = [row for one in planned.pairs for row in one.awaiting]
    if awaiting:
        said.append(
            {
                "code": AWAITING,
                "message": (
                    f"{len(awaiting)} account track(s) were queued for acquisition by "
                    f"an earlier sync and are not in the library yet: {listed(awaiting)}"
                ),
            }
        )
    ambiguous = [row for one in planned.pairs for row in one.ambiguous]
    if ambiguous:
        said.append(
            {
                "code": AMBIGUOUS,
                "message": (
                    f"{len(ambiguous)} account track(s) are carried by more than one "
                    f"library row, so none was added to rekordbox: {listed(ambiguous)}"
                ),
            }
        )
    withheld = [one for one in planned.pairs if one.withheld]
    if withheld:
        said.append(
            {
                "code": WITHHELD,
                "message": (
                    "the account withheld tracks it counts on "
                    + ", ".join(
                        f"{one.name!r} ({one.withheld.get('withheld', 0)})" for one in withheld
                    )
                    + ", so nothing there was read as removed and nothing is removed "
                    "from or reordered on the account until it serves the whole list"
                ),
            }
        )
    return said


def sync_pair(ctx) -> Envelope:
    """Plan every asked pair, ask both gates, then write each side approved."""
    from cratekit.modules.outbound import pairs

    cfg = sync_cli._load()
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733), as every verb that
    # writes the database reads it.
    session.assert_backup_acknowledged(cfg)
    store_of_pairs = pairs.PairStore(cfg)
    wanted = targets(
        store_of_pairs, getattr(ctx.args, "account", None), getattr(ctx.args, "rekordbox", None)
    )
    with jobs.open_store() as store:
        planned = plan(cfg, wanted, store=store)
        data = payload(planned)
        shown = facts(planned)
        warnings = _warnings(planned)
        gates = {spec.name: spec for spec in ctx.entry.gates}
        on_rekordbox = (
            ctx.gate.require(gates[REKORDBOX_GATE], plan=data, context=shown) == APPLY
        )
        on_account = ctx.gate.require(gates[ACCOUNT_GATE], plan=data, context=shown) == APPLY
        if not planned.pairs:
            return ctx.envelope(
                data=data,
                outcome=Outcome.NO_OP,
                warnings=[
                    *warnings,
                    {
                        "code": NOTHING,
                        "message": (
                            "no playlist is paired yet; pair one with crate sync pair "
                            "ACCOUNT_PLAYLIST --rekordbox PLAYLIST_ID"
                        ),
                    },
                ],
            )
        if not (on_rekordbox or on_account):
            return ctx.envelope(
                data=data,
                outcome=Outcome.NO_OP,
                warnings=[
                    *warnings,
                    {"code": SKIPPED, "message": "both sides were skipped, nothing was written"},
                ],
            )
        done = [
            apply_pair(cfg, one, rekordbox=on_rekordbox, account=on_account, store=store)
            for one in planned.pairs
        ]
    totals = {
        **data["totals"],
        "rekordbox_added": sum(d.rekordbox.added for d in done if d.rekordbox),
        "rekordbox_removed": sum(d.rekordbox.removed for d in done if d.rekordbox),
        "account_added": sum(d.account_added for d in done),
        "account_removed": sum(d.account_removed for d in done),
        "queued_jobs": [d.queued for d in done if d.queued],
        "marked": sum(1 for d in done if d.marked),
    }
    answered = {"rekordbox": on_rekordbox, "the account": on_account}
    sides = [side for side, on in answered.items() if on]
    skipped = [side for side, on in answered.items() if not on]
    message = (
        f"{len(done)} pair(s) synced on {' and '.join(sides)}: "
        f"{totals['rekordbox_added']} added and {totals['rekordbox_removed']} taken off "
        f"in rekordbox, {totals['account_added']} added and "
        f"{totals['account_removed']} taken off on the account, "
        f"{len(totals['queued_jobs'])} acquisition job(s) queued; no track left the "
        f"collection or the account"
        + (f"; {' and '.join(skipped)} skipped, its snapshot unchanged" if skipped else "")
    )
    wrote = planned.writes or any(d.marked for d in done)
    return ctx.envelope(
        data={**data, "totals": totals},
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
        warnings=[*warnings, {"code": WRITTEN if wrote else NOTHING, "message": message}],
    )


__all__ = [
    "ACCOUNT_GATE",
    "INTAKE_HANDLER",
    "PAIR_SOURCE",
    "REKORDBOX_GATE",
    "Done",
    "PairPlan",
    "Plan",
    "Target",
    "apply_pair",
    "build",
    "facts",
    "file_identity",
    "generated_tops",
    "payload",
    "plan",
    "plan_pair",
    "sync_pair",
    "targets",
]
