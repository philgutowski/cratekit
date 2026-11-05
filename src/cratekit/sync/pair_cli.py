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

**EVERY PLAYLIST THE AUTHOR MADE, PAIRED BY ITSELF (U198).** Decided by
Phillip on 2026-11-04: ``crate sync pair`` with no argument also finds every
plain rekordbox playlist he made outside Cratekit's trees, the Favorites folder
and the folders ``outbound.pair_skip_folders`` names (ARCHIVE by default), as
``sync/pair_discover.py`` reads them, and pairs each one that no pair holds
with an account playlist this sync makes: one private playlist per rekordbox
playlist, in one account root folder per rekordbox top folder, titled
``<Folder> <path below> <Playlist>``, and ``Playlists`` for the rekordbox
root. It is made on the account's gate only, reserved and marked in the pairs
document before it is created, and its first sync adds only, as any pair's
does. A root folder of the name is adopted when the pairs document records
none and no other list of Cratekit's keeps it, and a playlist of the title
already in that folder is left and named, never joined. A made pair that
loses either side is unpaired, its survivor left where it is and released,
so it is never made again. A rekordbox row the account had no track for is
remembered with the ISRC it was asked under (R-988), so the next plan asks
the provider nothing about it until that ISRC changes.

**A PLAYLIST MADE ON THE ACCOUNT IN A SYNCED FOLDER COMES TO REKORDBOX (U202).**
Decided by Phillip on 2026-11-04, the other half of U198: a playlist he makes
on the account inside one of the root folders the pairs document records is
made in rekordbox at the next sync of every pair, and paired as one the
product made. ``sync/pair_discover.home_of`` says where: the account title
less ``<Folder> `` is its name, in the live rekordbox top folder of the
folder's name, down any subfolder the title reads that is there, and
``Playlists`` is the rekordbox root. It is made on the rekordbox gate only,
by ``sync/pair_reverse.py`` under the pairs lock, and its first sync adds
only, so every track the library owns lands in the account's order and every
one it lacks is queued once. Listed and never made: a playlist a pair already
holds is not offered at all; a released one (its rekordbox side was deleted),
one that is not the author's own or that a pair may not hold, one whose place
``home_of`` refuses, and two that would take one rekordbox name in one folder,
which refuse that name only.

**THE LATER OF TWO OPPOSITE CHANGES WINS (U202).** Where one track was added
on one side and removed on the other since the last sync, the merge applies
the later change to both (``sync/pair_merge.py``). The moments are the
account's added date for each playlist track, rekordbox's membership row
``created_at`` for an addition, and the base membership row's ``updated_at``
for a removal while that row is still there marked removed. The account keeps
no record of a removal, so an account removal never beats an addition, and
every call made with a moment unknown keeps the track and is named on the
gate. The snapshot records each account track's added date, so a track taken
out and put back on the account reads as added there (R-990).

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

**THE SNAPSHOT MOVES ONLY WHEN THE WHOLE PAIR WAS WRITTEN.** Both gates
applied, every write landed, and the account listed the whole playlist: only
then are both sides' snapshots recorded, together. Anything less, a side
skipped, a write that failed part way or a short listing, records the links the
plan made and leaves the snapshot where it was, so the next sync merges against
the same last sync and finishes what this one did not. A side's removal that
the other side never took is still a removal then, because the base that saw
the track is still the base. A first sync that did not finish is still a first
sync, and adds only.

**A SHORT ACCOUNT LISTING REMOVES NOTHING.** The provider counts tracks it will
not serve. A track it withheld would read as one the author removed, so when the
listing is short no account track is read as removed, the account side takes no
removal and no reorder, and the answer says how many were withheld.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any

from cratekit.acquire import match
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import analysis_store, config, jobs, locations, rb_writer, session, tags
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.favorites import placeholders
from cratekit.intake import cli as intake_cli
from cratekit.intake import ingest
from cratekit.modules.outbound.pairs import ACCOUNT_SIDE, REKORDBOX_SIDE
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

#: What a row with no ISRC anywhere is said to be. The account is not asked:
#: the seam matches on a code or on an exact provider reference, and a row with
#: neither has nothing it could match on.
NO_ISRC = "the row carries no ISRC, in the database or in its file"

#: The warning codes the answer carries.
UNMATCHED = "sync-pair-unmatched"
AWAITING = "sync-pair-awaiting"
AMBIGUOUS = "sync-pair-ambiguous"
WITHHELD = "sync-pair-withheld"
SKIPPED = "sync-pair-skipped"
NOTHING = "sync-pair-nothing"
LEFT_OUT = "sync-pair-left-out"
WRITTEN = "sync-pair-written"
#: A custom playlist twin's pair forgotten because its account playlist is gone (U149).
UNPAIRED = "sync-pair-twin-unpaired"

#: The refusals that are about one pair's own playlists, which a sync of every
#: pair names and passes over rather than stopping at.
PER_PAIR_REASONS = frozenset({"sync-pair-unknown", "sync-pair-out-of-scope"})
#: U202. The refusals one account playlist brought from a synced folder may
#: raise about itself, which list it rather than refuse the sync.
BROUGHT_REASONS = PER_PAIR_REASONS | frozenset(
    {"label-playlist-unreadable", "intake-list-unusable"}
)

#: The item states an intake job's report gives a track the library holds.
OWNED_STATE = "owned"

#: U198. What a pair whose account side is still to be made is named by on
#: the gate, before the rekordbox playlist's identifier.
NEW = "new:"

#: U198. A discovered playlist left out and named, and a made pair unpaired.
NOT_DISCOVERED = "sync-pair-not-discovered"
RELEASED = "sync-pair-released"
#: U202. Account playlists in a synced folder not made in rekordbox, and the
#: calls between an addition and a removal, by time and with a time unknown.
NOT_BROUGHT = "sync-pair-not-brought"
LATER_CHANGE = "sync-pair-later-change"
TIME_UNKNOWN = "sync-pair-time-unknown"

#: U198. What becomes of the account root folder a discovered playlist goes in.
FOLDER_CREATE = "create"
FOLDER_REUSE = "reuse"
FOLDER_ADOPT = "adopt"


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
    #: U198. For a rekordbox playlist a sync of every pair found, whose
    #: account side is still to be made: its root folder and its title.
    #: ``account_id`` is empty until the account gate makes it.
    folder: str = ""
    title: str = ""

    @property
    def new(self) -> bool:
        """Whether the account side is still to be made."""
        return not self.account_id

    @property
    def rekordbox_new(self) -> bool:
        """Whether the rekordbox side is still to be made (U202)."""
        return not self.rekordbox_id

    @property
    def key(self) -> str:
        """What the gate names this pair by: its account playlist, or the rekordbox one."""
        return self.account_id or f"{NEW}{self.rekordbox_id}"


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
    #: ``ListingShortfall.block()`` when the account listing was short.
    withheld: dict[str, int] | None = None
    #: U198. Where the account side is made, for a pair whose account side is new.
    place: Place | None = None
    #: U202. Where the rekordbox side is made, for a pair whose rekordbox side
    #: is new, a ``pair_discover.Home``.
    home: Any = None
    #: U202. When the account says each listed track was added, ISO text by
    #: remote id, recorded with the snapshot.
    account_dates: dict[str, str] = field(default_factory=dict)

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
            # U198, ONLY FOR A NEW ONE, so a marked pair digests as it did.
            **({"place": self.place.identity()} if self.place is not None else {}),
            # U202, the same for a pair whose rekordbox side is new.
            **({"home": self.home.identity()} if self.home is not None else {}),
        }


@dataclass(frozen=True, slots=True)
class Place:
    """The account root folder a discovered playlist's account side is made in (U198)."""

    folder: str
    title: str
    action: str
    #: The root folder's identifier, empty when the write makes it.
    folder_id: str = ""
    #: A recorded folder read as gone, so a new one is made in its place.
    stale: str = ""

    def identity(self) -> dict[str, str]:
        return {
            "folder": self.folder,
            "title": self.title,
            "action": self.action,
            "folder_id": self.folder_id,
        }


def _scope_account(
    account_id: str,
    listed: Mapping[str, Any],
    label_owned: frozenset[str],
    set_built: frozenset[str],
    mirrored: frozenset[str] = frozenset(),
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
    if account_id in mirrored:
        # U147. ``crate organize`` keeps a mirrored playlist equal to its
        # rekordbox playlist, so a pair merging both ways would fight it.
        raise _out_of_scope(
            f"{name!r} ({account_id}) is a mirrored playlist, which organize keeps "
            f"equal to its rekordbox playlist, so it was not synced",
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
    #: Every playlist ``crate organize`` mirrors (U147).
    mirrored: frozenset[str] = frozenset()
    #: U198, R-988. Every row the account had no track for, as remembered,
    #: and what this plan asked fresh or matched since.
    misses: Mapping[str, Any] = field(default_factory=dict)
    fresh: dict[str, Any] = field(default_factory=dict)
    matched: set[str] = field(default_factory=set)
    #: U202. Each account root folder's playlists, listed once per plan.
    inside: dict[str, dict[str, str]] = field(default_factory=dict)

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

    @cached_property
    def by_isrc(self) -> dict[str, tuple[str, ...]]:
        return playlist_pair.rows_by_isrc(self.db, match.isrc_token)

    @cached_property
    def pair_jobs(self) -> tuple[jobs.Job, ...]:
        """Every intake job this verb queued on this library that did not fail, newest first."""
        return tuple(
            job
            for job in jobs.list_jobs(self.store)
            if job.handler_key == INTAKE_HANDLER
            and job.library_id == self.cfg.library.volume_id
            and (job.payload or {}).get("source_id") == PAIR_SOURCE
            and job.state not in (jobs.JobState.FAILED, jobs.JobState.CANCELLED)
        )

    @cached_property
    def mirrors(self) -> dict[str, frozenset[str]]:
        """Each account playlist's INBOX playlists, as the landing records name them (U128)."""
        return landed_inbox_playlists(self.cfg)

    def jobs_for(self, account_id: str) -> tuple[jobs.Job, ...]:
        return tuple(
            job
            for job in self.pair_jobs
            if str((job.payload or {}).get(intake_cli.SOURCE) or "") == account_id
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


def landed_inbox_playlists(cfg: config.Config) -> dict[str, frozenset[str]]:
    """Each account playlist's INBOX playlists, as the landing records name them (U128).

    PUBLIC because the custom playlist twins' backfill (U149) finds a landed
    track's row the same way a pair does.
    """
    standing = {
        session.SessionState.AWAITING_IMPORT,
        session.SessionState.COMMITTED_UNVERIFIED,
        session.SessionState.CLOSED,
    }
    records, _unreadable = session.scan_log(cfg)
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
    return {account_id: frozenset(ids) for account_id, ids in found.items()}


def landed_isrcs(
    cfg: config.Config, db: Any, playlist_ids: Iterable[str]
) -> dict[str, tuple[str, ...]]:
    """ISRC to content ids, read from the files of the INBOX playlists named.

    U128 records each INBOX playlist a landing made for an account playlist
    with the account playlist's identifier. A track a pair queued and a landing
    brought sits there, and its row may carry no ISRC of its own, since a
    landed row's code is in its file. Only those rows' files are read.
    """
    found: dict[str, list[str]] = {}
    for mirror in sorted(playlist_ids):
        for row in playlist_pair.members(db, mirror):
            code = match.isrc_token(row.isrc) or file_identity(cfg, row.path)[0]
            if code and row.content_id not in found.setdefault(code, []):
                found[code].append(row.content_id)
    return {code: tuple(ids) for code, ids in found.items()}


def _mirror_isrcs(reader: _Reader, account_id: str) -> dict[str, tuple[str, ...]]:
    """ISRC to content ids, from the INBOX playlists landed for this account playlist."""
    return landed_isrcs(reader.cfg, reader.db, reader.mirrors.get(account_id, ()))


def plan_pair(reader: _Reader, target: Target, held, *, home: Any = None) -> PairPlan:
    """Read both sides of one pair, match them, merge them, and say what to write.

    ``home`` is where the rekordbox side is made, for a pair whose rekordbox
    side is new (U202); that side then holds nothing yet.
    """
    cfg = reader.cfg
    if target.new:
        # U198. NOTHING TO LIST: the account side is made by this sync, so it
        # holds nothing yet, and the first sync adds only.
        name = target.title
    else:
        name = _scope_account(
            target.account_id, reader.listed, reader.label_owned, reader.set_built, reader.mirrored
        )
    if target.rekordbox_new:
        # U202. NOTHING TO READ: the rekordbox side is made by this sync, so
        # it holds nothing yet, and the first sync adds only.
        rekordbox = playlist_pair.Playlist(
            playlist_id="",
            name=home.name,
            attribute=playlist_pair.PLAIN_PLAYLIST,
            removed=False,
            ancestors=(),
        )
    else:
        rekordbox = _scope_rekordbox(
            target.rekordbox_id,
            playlist_pair.read_playlist(reader.db, target.rekordbox_id),
            reader.tops,
        )
    dates: dict[str, str] = {}
    if target.new:
        tracks: Mapping[str, Any] = {}
        short = None
    else:
        tracks, short, dates = intake_cli.list_playlist_dated(reader.found, target.account_id)
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
    # THE ACCOUNT PLAYLIST'S OWN TRACKS FIRST, by ISRC, when exactly one of
    # them carries the row's code: the account already holds that recording,
    # and asking the provider would choose among its releases and could name
    # another one, which the account would then gain beside the first.
    on_account: dict[str, list[str]] = {}
    for remote_id in account_now:
        code = match.isrc_token(tracks[remote_id].get("isrc"))
        if code:
            on_account.setdefault(code, []).append(remote_id)
    linked = set(links)
    # U207. EACH UNLINKED ROW'S CODE AND ALBUM, read once, a file's tag
    # included, so the codes the provider will be asked are known before the
    # first is asked and screened in batches: a code the catalogue files
    # nothing under is then answered with no request of its own.
    identities: dict[str, tuple[str, str]] = {}
    for row in rows.values():
        if by_row.get(row.content_id, ""):
            continue
        code = match.isrc_token(row.isrc)
        album = ""
        if not code:
            code, album = file_identity(cfg, row.path)
        identities[row.content_id] = (code, album)

    def held_on_account(code: str) -> list[str]:
        return [one for one in on_account.get(code, ()) if one not in linked]

    asked = [
        code
        for content_id, (code, _album) in identities.items()
        if code
        and len(held_on_account(code)) != 1
        and _remembered_miss(reader, content_id, code) is None
    ]
    if asked:
        reader.remote.screen_isrcs(asked)
    for row in rows.values():
        remote_id = by_row.get(row.content_id, "")
        reason = ""
        if not remote_id:
            from cratekit.core import naming
            from cratekit.modules.outbound import source

            if template is None:
                template = source.name_template(cfg)
            isrc, album = identities[row.content_id]
            held_there = held_on_account(isrc)
            if isrc and len(held_there) == 1:
                remote_id = held_there[0]
            elif not isrc:
                reason = NO_ISRC
            else:
                remote_id, reason = _ask(
                    reader,
                    row,
                    isrc=isrc,
                    title=naming.strip_heads(row.title, template=template),
                    album=album,
                )
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
    unseen: set[str] = set()
    # U202. THE MOMENTS EACH SIDE CAN GIVE, read only where a base exists,
    # since a first sync adds only and decides nothing by time.
    account_added = {
        remote_key(remote_id): moment
        for remote_id, said in dates.items()
        if (moment := placeholders.parse_hearted(said)) is not None
    }
    account_readded: set[str] = set()
    rekordbox_added: dict[str, Any] = {}
    rekordbox_removed: dict[str, Any] = {}
    row_to_remote = {**by_row, **{row: remote for remote, row in made.items()}}

    def as_key(content_id: str) -> str:
        remote_id = row_to_remote.get(content_id, "")
        return remote_key(remote_id) if remote_id else row_key(content_id)

    if held is not None and not held.first:
        base_account = tuple(remote_key(one) for one in held.account or ())
        if short is not None:
            # A WITHHELD TRACK IS NOT A REMOVED ONE. Which tracks the provider
            # left out is not known, so no track the base held is read as gone,
            # and none of them is offered to the account as an addition either:
            # it may be on the playlist, served to nobody.
            unseen = {key for key in base_account if key not in set(account_keys)}
            base_account = tuple(key for key in base_account if key not in unseen)
        # A RE-ADD IS A TRACK NONE OF WHOSE BASE MEMBERSHIPS SURVIVES. A track
        # the playlist holds twice that lost one copy still holds the other,
        # which the base saw, so it was not taken out and put back.
        base_rows: dict[str, set[str]] = {}
        for member in held.rekordbox or ():
            base_rows.setdefault(member.content_id, set()).add(member.row_id)
        current_rows: dict[str, set[str]] = {}
        for row in rekordbox.rows:
            current_rows.setdefault(row.content_id, set()).add(row.row_id)
        base_rekordbox = tuple(as_key(member.content_id) for member in held.rekordbox or ())
        readded = {
            as_key(content_id)
            for content_id, row_ids in current_rows.items()
            if content_id in base_rows and not (row_ids & base_rows[content_id])
        }
        synced = placeholders.parse_hearted(held.synced)
        # A TRACK TAKEN OUT AND PUT BACK ON THE ACCOUNT (R-990, closed by
        # U202): the base held it with one added date and the account dates it
        # later now, and later than the base's own sync, so the putting back
        # was done since. A track the base dated nowhere is never read so.
        if synced is not None:
            for remote_id in account_now:
                key = remote_key(remote_id)
                was = placeholders.parse_hearted(held.account_added.get(remote_id))
                now = account_added.get(key)
                if (
                    key in base_account
                    and was is not None
                    and now is not None
                    and now > was
                    and now > synced
                ):
                    account_readded.add(key)
        # REKORDBOX'S MOMENTS: a live row's ``created_at`` is when its track
        # was put there, and a base row still there marked removed carries
        # when it was taken out in ``updated_at``. A base row gone outright,
        # or still live under a track the collection lost, says no moment.
        stamped = playlist_pair.stamps(reader.db, rekordbox.playlist_id)
        for row in rekordbox.rows:
            stamp = stamped.get(row.row_id)
            if stamp is None or stamp.created is None:
                continue
            key = as_key(row.content_id)
            if key not in rekordbox_added or stamp.created > rekordbox_added[key]:
                rekordbox_added[key] = stamp.created
        for content_id, row_ids in base_rows.items():
            if content_id in current_rows:
                continue
            read = [stamped.get(row_id) for row_id in sorted(row_ids)]
            if read and all(
                one is not None
                and one.removed
                and one.content_id == content_id
                and one.updated is not None
                for one in read
            ):
                rekordbox_removed[as_key(content_id)] = max(
                    one.updated for one in read if one is not None and one.updated is not None
                )
        base = pair_merge.Base(account=base_account, rekordbox=base_rekordbox, synced=synced)

    merged = pair_merge.merge(
        base,
        pair_merge.Side(
            tuple(account_keys), frozenset(account_readded), added_at=account_added
        ),
        pair_merge.Side(
            tuple(rekordbox_keys),
            frozenset(readded),
            added_at=rekordbox_added,
            removed_at=rekordbox_removed,
        ),
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
    # Held live and staying: a track matched under another key already has its
    # membership, and a second would be the same track twice.
    live_here = {
        content_of[key] for key in rekordbox_keys if key in rekordbox_held and key in content_of
    }
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
            rekordbox_held.add(key)
            if content_id not in live_here:
                adds.append(content_id)
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
    account_adds = tuple(
        remote_of(key) for key in merged.add_account if remote_of(key) and key not in unseen
    )
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
        withheld=short.block() if short is not None else None,
        home=home,
        account_dates=dict(dates),
    )


def _remembered_miss(reader: _Reader, content_id: str, isrc: str) -> Any:
    """The miss remembered for this row under this ISRC that a plan reuses, or None.

    The one test :func:`_ask` reuses a miss by, and the one the screen before
    it leaves a row out by (U207), so the two cannot drift: a row whose miss
    is reused is never asked, and is never screened either. A TIE IS ASKED
    AGAIN (R-1032's rule, one file over): releases that agree today may be
    told apart tomorrow, so a tie is never remembered as an answer.
    """
    from cratekit.modules.outbound.service import AGREEING_RELEASES

    held = reader.misses.get(content_id)
    if held is not None and held.isrc == isrc and AGREEING_RELEASES not in held.reason:
        return held
    return None


def _ask(reader: _Reader, row: Any, *, isrc: str, title: str, album: str) -> tuple[str, str]:
    """The account track for one unlinked row, or why there is none: asked once per ISRC.

    R-988, closed by U198. A row the account had no track for is remembered
    with the ISRC it was asked under and its answer, and a plan meeting it
    again under the same ISRC reuses the answer without a request, so the
    three plans one sync makes ask once, and a sync of every pair does not ask
    again each time. A row whose ISRC changed is asked again. An answer that
    says a candidate could not be read is no answer about the row, and is
    never remembered.
    """
    from cratekit.modules.outbound.service import AGREEING_RELEASES, UNREADABLE_CANDIDATE

    held = reader.misses.get(row.content_id)
    reused = _remembered_miss(reader, row.content_id, isrc)
    if reused is not None:
        return "", reused.reason
    remote = reader.remote
    remote_id = str(
        remote.match_track(
            identity=row.content_id,
            isrc=isrc,
            title=title,
            artist=row.artist,
            album=album,
        )
        or ""
    )
    if remote_id:
        if held is not None:
            reader.matched.add(row.content_id)
        return remote_id, ""
    reason = remote.unmatched_reason(row.content_id) or NO_MATCH
    if UNREADABLE_CANDIDATE not in reason and AGREEING_RELEASES not in reason:
        from cratekit.modules.outbound import pairs

        reader.fresh[row.content_id] = pairs.Miss(isrc, reason)
    return "", reason


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
    by_isrc = reader.by_isrc
    for remote_id, code in codes.items():
        if code and by_isrc.get(code):
            found[remote_id] = by_isrc[code]
    rest = {remote_id for remote_id in lacking if remote_id not in found}
    if rest:
        for remote_id, content_id in _owned_by_jobs(
            reader, reader.jobs_for(account_id), rest
        ).items():
            found[remote_id] = (content_id,)
    rest = {remote_id for remote_id in lacking if remote_id not in found and codes.get(remote_id)}
    if rest:
        landed = _mirror_isrcs(reader, account_id)
        for remote_id in rest:
            if landed.get(codes[remote_id]):
                found[remote_id] = landed[codes[remote_id]]
    return found


def _queued(reader: _Reader, account_id: str) -> frozenset[str]:
    """Every track an intake job this verb queued for the pair still holds or resolved."""
    return frozenset(
        str(item)
        for job in reader.jobs_for(account_id)
        for item in (job.payload or {}).get(intake_cli.TRACKS) or {}
    )


@dataclass(frozen=True, slots=True)
class Unpaired:
    """A custom playlist twin's pair whose account playlist the account no longer lists (U149).

    Its pair is forgotten and its rekordbox playlist is left where it is,
    named, never removed: the account side is gone, and the twin is still the
    list it was.
    """

    account_id: str
    rekordbox_id: str
    name: str
    rekordbox_name: str
    #: U198. The side that is GONE, and whether the product made the account
    #: side for a discovered playlist, whose survivor is then released.
    gone: str = ACCOUNT_SIDE
    made: bool = False
    #: Why the rekordbox side is let go when it is still there: moved under a
    #: folder the configuration skips (U198, the review's finding).
    why: str = ""

    def identity(self) -> dict[str, str]:
        block = {"account_id": self.account_id, "rekordbox_id": self.rekordbox_id}
        if self.made:
            block["gone"] = self.gone
        return block


@dataclass
class Plan:
    """Every pair this invocation syncs, decided, and the marked pairs it could not."""

    pairs: tuple[PairPlan, ...] = ()
    #: A marked pair a sync of every pair could not plan, account id to why.
    left_out: dict[str, str] = field(default_factory=dict)
    #: Twin pairs whose account playlist is gone, forgotten when a gate is applied.
    unpaired: tuple[Unpaired, ...] = ()
    #: U198. Every rekordbox playlist a sync of every pair left out and named.
    listed: tuple[Any, ...] = ()
    #: U198, R-988. Rows the account had no track for, asked fresh by this
    #: plan, and rows remembered as misses that matched since.
    misses: dict[str, Any] = field(default_factory=dict)
    matched: frozenset[str] = frozenset()
    #: U202. Every account playlist in a synced folder left out and named.
    listed_back: tuple[Any, ...] = ()

    @property
    def digest(self) -> str:
        # THE UNPAIRED ONLY WHEN THERE ARE ANY, so a plan with none digests
        # as it did before U149.
        extra = (
            {"unpaired": [one.identity() for one in self.unpaired]} if self.unpaired else {}
        )
        return digest_of(
            {"kind": "sync.pair", "pairs": [one.identity() for one in self.pairs], **extra}
        )

    @property
    def writes(self) -> bool:
        return bool(self.unpaired) or any(
            one.rekordbox_writes or one.account_writes or one.acquire or not one.target.marked
            for one in self.pairs
        )


def plan(
    cfg: config.Config, wanted: Sequence[Target], *, store, every: bool = False
) -> Plan:
    """Read the account and the database once, and plan every pair.

    ``every`` says the pairs are every marked pair rather than one named, and
    then a pair whose own playlist is gone is left out and named rather than
    refusing the rest.
    """
    if not wanted and not every:
        return Plan()
    from cratekit.core import active_taxonomy, tree_registry
    from cratekit.label import catalogue
    from cratekit.modules.outbound import ledger, pairs

    store_of_pairs = pairs.PairStore(cfg)
    document = store_of_pairs._document()
    held = document.pairs
    # U198. THE ACCOUNT IS LISTED ONLY FOR A MARKED PAIR: a sync that only
    # discovers plans its new pairs over an empty account side, and asks the
    # account seam for its root folders only when it found something. U202:
    # or when a sync of every pair has root folders recorded to look in.
    reads_account = bool(wanted) or (every and bool(document.folders))
    found = catalogue.resolve(cfg) if reads_account else None
    listed = (
        {one.playlist_id: one for one in playlists._listed_or_refuse(found)}
        if reads_account
        else {}
    )
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
            mirrored=ledger.mirror_playlist_ids(cfg),
            misses=dict(document.misses),
        )
        planned: list[PairPlan] = []
        left_out: dict[str, str] = {}
        unpaired: list[Unpaired] = []
        for target in wanted:
            # A TWIN WHOSE ACCOUNT PLAYLIST IS GONE IS UNPAIRED (U149), never
            # refused and never removed: its rekordbox playlist is left and
            # named. A pair the person made is refused or left out as before.
            pair = held.get(target.account_id)
            if pair is not None and (pair.twin or pair.made) and target.account_id not in listed:
                twin = playlist_pair.read_playlist(db, pair.rekordbox_id)
                unpaired.append(
                    Unpaired(
                        account_id=target.account_id,
                        rekordbox_id=pair.rekordbox_id,
                        name=pair.name,
                        rekordbox_name=twin.name if twin is not None else "",
                        made=pair.made,
                    )
                )
                continue
            if pair is not None and pair.made:
                # U198. A MADE PAIR WHOSE REKORDBOX PLAYLIST IS GONE IS UNPAIRED,
                # and its account playlist left where it is, named.
                there = playlist_pair.read_playlist(db, pair.rekordbox_id)
                moved = ""
                if there is not None and not there.removed:
                    from cratekit.core import active_taxonomy as _taxonomy
                    from cratekit.favorites import placement
                    from cratekit.sync import pair_discover

                    moved = pair_discover.left_behind(
                        db,
                        there,
                        favorites=placement.source_name(_taxonomy.load(cfg)),
                        skip=cfg.outbound.pair_skip_folders,
                    )
                if moved:
                    # MOVED WHERE NO PAIR IS KEPT, under ARCHIVE, another app's
                    # folder or the Favorites folder, is let go as a rekordbox
                    # side gone, so nothing there is written and the account
                    # playlist stays.
                    unpaired.append(
                        Unpaired(
                            account_id=target.account_id,
                            rekordbox_id=pair.rekordbox_id,
                            name=pair.name,
                            rekordbox_name=there.name,
                            gone=REKORDBOX_SIDE,
                            made=True,
                            why=moved,
                        )
                    )
                    continue
                if there is None or there.removed:
                    unpaired.append(
                        Unpaired(
                            account_id=target.account_id,
                            rekordbox_id=pair.rekordbox_id,
                            name=pair.name,
                            rekordbox_name=there.name if there is not None else "",
                            gone=REKORDBOX_SIDE,
                            made=True,
                        )
                    )
                    continue
            try:
                planned.append(plan_pair(reader, target, held.get(target.account_id)))
            except CratekitError as exc:
                # ONE PAIR WHOSE PLAYLIST IS GONE DOES NOT HOLD EVERY OTHER. Only
                # when every marked pair was asked for, and only for the two
                # refusals that are about that pair's own playlists; a pair
                # named on the command line refuses as itself.
                if not every or exc.cause.reason not in PER_PAIR_REASONS:
                    raise
                left_out[target.account_id] = exc.cause.message
        listed_out: list[Any] = []
        listed_back: list[Any] = []
        if every:
            news, listed_out = _discovered(cfg, reader, db, document)
            for target, place in news:
                one = plan_pair(reader, target, None)
                one.place = place
                planned.append(one)
            backs, listed_back = _discovered_back(cfg, reader, db, document)
            for target, home in backs:
                try:
                    planned.append(plan_pair(reader, target, None, home=home))
                except CratekitError as exc:
                    # ONE ACCOUNT PLAYLIST THE PROVIDER CANNOT LIST DOES NOT HOLD
                    # EVERY PAIR (U202, from the review): it is listed, never made.
                    if exc.cause.reason not in BROUGHT_REASONS:
                        raise
                    from cratekit.sync import pair_discover

                    listed_back.append(
                        pair_discover.Listed(
                            "",
                            target.title,
                            (target.folder, target.title),
                            pair_discover.TAKEN,
                            exc.cause.message,
                            account_id=target.account_id,
                        )
                    )
        return Plan(
            tuple(planned),
            left_out,
            tuple(unpaired),
            listed=tuple(listed_out),
            misses=dict(reader.fresh),
            matched=frozenset(reader.matched),
            listed_back=tuple(listed_back),
        )
    finally:
        rb_writer.close_db(db)


def _discovered(cfg: config.Config, reader: _Reader, db: Any, document) -> tuple[list, list]:
    """Every discovered playlist to pair, each with its account place, and every one left out.

    U198. The rekordbox side is :mod:`pair_discover`'s. The account side is
    read only when something was found: the root folders once, and each
    folder's playlists once. A root folder is the one the pairs document
    records, else the one root folder of the name, else a new one. Two root
    folders of the name, or one another list of Cratekit's keeps, leave that
    folder's playlists out and named; a playlist of the title already in the
    folder is a person's or another pair's, and is left and named rather than
    joined or made twice.
    """
    from cratekit.core import active_taxonomy
    from cratekit.favorites import placement
    from cratekit.modules.outbound import ledger
    from cratekit.sync import pair_discover

    discovery = pair_discover.discover(
        db,
        tops=reader.tops,
        favorites=placement.source_name(active_taxonomy.load(cfg)),
        skip=cfg.outbound.pair_skip_folders,
        paired=(pair.rekordbox_id for pair in document.pairs.values()),
        released=document.released.rekordbox,
    )
    listed = list(discovery.listed)
    if not discovery.found:
        return [], listed

    def left(one, why: str) -> None:
        listed.append(
            pair_discover.Listed(one.rekordbox_id, one.name, one.path, pair_discover.TAKEN, why)
        )

    root = reader.root_folders
    others = ledger.recorded_folder_ids(cfg)
    by_folder: dict[str, list] = {}
    for one in discovery.found:
        by_folder.setdefault(one.folder, []).append(one)
    news: list[tuple[Target, Place]] = []
    for folder, found in sorted(by_folder.items()):
        recorded = document.folders.get(folder)
        stale = ""
        if recorded is not None and recorded.folder_id in root:
            action, folder_id = FOLDER_REUSE, recorded.folder_id
        else:
            stale = recorded.folder_id if recorded is not None else ""
            named = sorted(fid for fid, name in root.items() if name == folder)
            why = ""
            if len(named) > 1:
                why = (
                    f"the account holds {len(named)} root folders named {folder!r}, so which "
                    f"one it goes in is not something a name decides; rename or merge them"
                )
            elif named and named[0] in others:
                why = (
                    f"the account's root folder {folder!r} is one Cratekit fills with another "
                    f"list, so nothing of a pair is made in it; rename the rekordbox folder"
                )
            if why:
                for one in found:
                    left(one, why)
                continue
            action, folder_id = (FOLDER_ADOPT, named[0]) if named else (FOLDER_CREATE, "")
        inside = reader.folder_listing(folder_id) if folder_id else {}
        taken = set(inside.values())
        for one in found:
            if one.title in taken:
                left(
                    one,
                    f"the account's {folder!r} folder already holds a playlist titled "
                    f"{one.title!r} that no pair made for this one, so it is left as it is "
                    f"and nothing is made beside it; pair the two by hand with crate sync "
                    f"pair, or rename one",
                )
                continue
            news.append(
                (
                    Target("", one.rekordbox_id, False, folder=folder, title=one.title),
                    Place(folder, one.title, action, folder_id, stale),
                )
            )
    return news, listed


def _discovered_back(cfg: config.Config, reader: _Reader, db: Any, document) -> tuple[list, list]:
    """Every account playlist in a recorded root folder to bring to rekordbox, and every one left.

    U202. Only the root folders the pairs document records are read, each
    once, and a folder the account no longer lists is passed over, since
    U198's discovery makes it again when rekordbox still has playlists for it.
    A playlist a pair holds is not offered. Listed and never made: a released
    one, one the account does not list among the author's own or that a pair
    may not hold, one ``pair_discover.home_of`` places nowhere, and two that
    would take one rekordbox name in one folder, which refuse that name only.
    """
    from cratekit.core import active_taxonomy
    from cratekit.favorites import placement
    from cratekit.sync import pair_discover

    if not document.folders:
        return [], []
    listed: list[Any] = []

    def left(account_id: str, title: str, folder: str, kind: str, why: str) -> None:
        listed.append(
            pair_discover.Listed("", title, (folder, title), kind, why, account_id=account_id)
        )

    root = reader.root_folders
    held = set(document.pairs)
    released = document.released.account
    favorites = placement.source_name(active_taxonomy.load(cfg))
    wanted: list[tuple[str, str, str, Any]] = []
    for folder, recorded in sorted(document.folders.items()):
        if recorded.folder_id not in root:
            continue
        inside = reader.folder_listing(recorded.folder_id)
        for account_id, title in sorted(inside.items(), key=lambda one: (one[1], one[0])):
            if account_id in held:
                continue
            if account_id in released:
                left(
                    account_id,
                    title,
                    folder,
                    pair_discover.RELEASED,
                    "its rekordbox playlist was deleted, so it was unpaired and is not made "
                    "again; pair it by hand with crate sync pair to sync it once more",
                )
                continue
            try:
                _scope_account(
                    account_id, reader.listed, reader.label_owned, reader.set_built, reader.mirrored
                )
            except CratekitError as exc:
                left(account_id, title, folder, pair_discover.TAKEN, exc.cause.message)
                continue
            home = pair_discover.home_of(
                db,
                folder,
                title,
                tops=reader.tops,
                favorites=favorites,
                skip=cfg.outbound.pair_skip_folders,
            )
            if isinstance(home, str):
                left(account_id, title, folder, pair_discover.TAKEN, home)
                continue
            wanted.append((account_id, title, folder, home))
    # TWO ACCOUNT PLAYLISTS TAKING ONE REKORDBOX NAME IN ONE FOLDER REFUSE
    # THAT NAME, and only that one: which of them the rekordbox playlist
    # copies is not something a name decides.
    counted: dict[tuple[str, str], int] = {}
    for _account_id, _title, _folder, home in wanted:
        place = (home.parent_id, home.name)
        counted[place] = counted.get(place, 0) + 1
    news: list[tuple[Target, Any]] = []
    for account_id, title, folder, home in wanted:
        many = counted[(home.parent_id, home.name)]
        if many > 1:
            left(
                account_id,
                title,
                folder,
                pair_discover.TWICE,
                f"{many} account playlists would take the rekordbox name {home.where!r}, so "
                f"which one it copies is not something a name decides; rename one of them "
                f"on the account",
            )
            continue
        news.append((Target(account_id, "", False, folder=folder, title=title), home))
    return news, listed


# ---------------------------------------------------------------------------
# The screen
# ---------------------------------------------------------------------------


def _items(one: PairPlan) -> list[dict[str, Any]]:
    """Every change one pair's sync makes, by name, both sides, in the order it is written."""
    by_content = {content_id: one.names.get(key) for key, content_id in one.content_of.items()}
    by_remote = {named.remote_id: named for named in one.names.values() if named.remote_id}

    def row(side: str, action: str, named: Named | None, **extra: Any) -> dict[str, Any]:
        return {
            "pair": one.target.key,
            "side": side,
            "action": action,
            **(named.shown() if named is not None else {}),
            **extra,
        }

    items: list[dict[str, Any]] = []
    if one.place is not None:
        items.append(
            row(
                "account",
                "create",
                None,
                title=one.place.title,
                folder=one.place.folder,
                folder_action=one.place.action,
                rekordbox_id=one.target.rekordbox_id,
                rekordbox_name=one.rekordbox_name,
            )
        )
    if one.home is not None:
        items.append(
            row(
                "rekordbox",
                "create",
                None,
                name=one.home.name,
                where=one.home.where,
                account_id=one.target.account_id,
                account_name=one.name,
            )
        )
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
    # U202. EVERY CALL BETWEEN AN ADDITION AND A REMOVAL IS NAMED, with the
    # moments it was decided on, empty where unknown.
    for call in one.merged.calls:
        items.append(
            row(
                "merge",
                call.outcome,
                one.names.get(call.key),
                added_on=call.added_on,
                added_at=call.added_at.isoformat() if call.added_at else "",
                removed_at=call.removed_at.isoformat() if call.removed_at else "",
            )
        )
    return items


def _reordered(one: PairPlan) -> bool:
    before = [content_id for content_id, _row in one.change.before]
    expected = pair_merge.appended(before, one.change.removes, one.change.adds)
    return tuple(expected) != one.change.order


def payload(planned: Plan) -> dict[str, Any]:
    """The plan as both gates show it: one item per change, both sides named."""
    items = [item for one in planned.pairs for item in _items(one)]
    items.extend(
        {
            "pair": one.account_id,
            "side": "pairs",
            "action": "unpair",
            "name": one.name,
            "rekordbox_id": one.rekordbox_id,
            "rekordbox_name": one.rekordbox_name,
            **({"gone": one.gone} if one.made else {}),
        }
        for one in planned.unpaired
    )
    # U198. EVERY PLAYLIST LEFT OUT IS LISTED, never written.
    items.extend(
        {"pair": "", "side": "discovery", "action": one.kind, **one.shown()}
        for one in planned.listed
    )
    # U202. And every account playlist in a synced folder not brought over.
    items.extend(
        {"pair": one.account_id, "side": "account-discovery", "action": one.kind, **one.shown()}
        for one in planned.listed_back
    )

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
            "unpaired": count("pairs", "unpair"),
            "created": count("account", "create"),
            "not_discovered": sum(1 for item in items if item["side"] == "discovery"),
            "created_in_rekordbox": count("rekordbox", "create"),
            "not_brought": sum(1 for item in items if item["side"] == "account-discovery"),
            "later_change": sum(
                1
                for item in items
                if item["side"] == "merge" and item["action"] != pair_merge.TIME_UNKNOWN
            ),
            "time_unknown": count("merge", pair_merge.TIME_UNKNOWN),
        },
        "chunk": None,
    }


def facts(planned: Plan) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per pair."""
    shown: dict[str, Any] = {"pairs": len(planned.pairs)}
    for one in planned.pairs:
        lead = "the account's" if one.merged.leader == pair_merge.ACCOUNT else "rekordbox's"
        made = ""
        if one.place is not None:
            folder = {
                FOLDER_CREATE: "a new root folder",
                FOLDER_REUSE: "its root folder",
                FOLDER_ADOPT: "the root folder already of that name",
            }[one.place.action]
            made = f"made on the account in {folder} {one.place.folder!r}, "
        if one.home is not None:
            # U202, from the review: the rekordbox side has no identifier yet.
            head = (
                f"{one.name!r} on the account, made in rekordbox as {one.home.where!r}; "
            )
        else:
            head = (
                f"{one.name!r} {made}on the account with {one.rekordbox_name!r} "
                f"({one.target.rekordbox_id}) in rekordbox; "
            )
        shown[f"pair {one.target.key}"] = (
            head
            + (
                "first sync, additions only, and it completes only when both sides "
                "are applied; "
                if one.first
                else ""
            )
            + ("not yet marked, approving marks it; " if not one.target.marked else "")
            + f"order follows {lead}"
            + (
                f"; the account withheld {one.withheld.get('withheld', 0)} track(s), so "
                f"nothing is removed or reordered there"
                if one.withheld
                else ""
            )
        )
    for gone in planned.unpaired:
        if gone.gone == REKORDBOX_SIDE:
            shown[f"pair {gone.account_id}"] = (
                f"the rekordbox playlist {gone.rekordbox_name or gone.rekordbox_id!r} is "
                f"{gone.why or 'gone'}, so {gone.name!r} is unpaired and left on the account"
            )
            continue
        shown[f"pair {gone.account_id}"] = (
            f"{gone.name!r} is gone from the account, so its "
            f"{'playlist' if gone.made else 'twin'} "
            f"{gone.rekordbox_name or gone.rekordbox_id!r} is unpaired and left in rekordbox"
        )
    if planned.listed:
        from cratekit.sync import pair_discover

        shown["not paired"] = "; ".join(
            f"{len(rows)} {kind}" for kind, rows in pair_discover.by_kind(planned.listed).items()
        )
    if planned.listed_back:
        shown["not made in rekordbox"] = f"{len(planned.listed_back)} account playlist(s)"
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
    #: Whether both sides' snapshots moved, which only a whole pair does.
    snapshot: bool = False
    #: U198. The account playlist made for a discovered rekordbox playlist.
    created: str = ""
    #: U202. The rekordbox playlist made for an account playlist.
    created_in_rekordbox: str = ""

    @property
    def wrote(self) -> bool:
        written = self.rekordbox
        return bool(
            (written and (written.added or written.removed or written.renumbered))
            or self.account_added
            or self.account_removed
            or self.account_ordered
            or self.queued
            or self.marked
            or self.created
            or self.created_in_rekordbox
        )


def _record(
    cfg: config.Config,
    one: PairPlan,
    *,
    rekordbox_after: Sequence[playlist_pair.Row] | None,
    account_after: Sequence[str] | None,
) -> bool:
    """Record both sides' snapshots when the whole pair was written, else the links alone.

    Returns whether the snapshot moved. Every live rekordbox membership is
    recorded, a track held twice with both its rows, so a later sync can tell
    a copy that was removed from a track that was taken out and put back.
    """
    from cratekit.modules.outbound import pairs

    whole = rekordbox_after is not None and account_after is not None and not one.withheld
    held_after = pair_merge.distinct(account_after or ())
    pairs.PairStore(cfg).record(
        one.target.account_id,
        account=list(held_after) if whole else None,
        # U202. THE ADDED DATES THE PLAN LISTED, for the tracks the account
        # holds after the write; a track this sync added is dated by the next.
        account_added=(
            {one_id: one.account_dates[one_id] for one_id in held_after if one_id in one.account_dates}
            if whole
            else None
        ),
        rekordbox=(
            [pairs.Membership(row.content_id, row.row_id) for row in rekordbox_after]
            if whole
            else None
        ),
        links=one.links,
        name=one.name,
    )
    return whole


def _made(cfg: config.Config, one: PairPlan) -> PairPlan:
    """Make a discovered playlist's account side in its root folder, and pair it (U198).

    The folder and the playlist are each reserved in the pairs document under
    its lock before they are created, and the playlist is marked in the same
    write, so an unwritable document refuses before anything is made and a
    sync stopped part way leaves what it made recorded for the next one. The
    playlist is moved into its folder only when this sync made it.
    """
    from dataclasses import replace

    from cratekit.modules.outbound import account as outbound_account
    from cratekit.modules.outbound import pairs

    place = one.place
    assert place is not None
    remote = outbound_account.resolve(cfg)
    store = pairs.PairStore(cfg)
    folder_id, _created = store.reserve_folder(
        place.folder,
        lambda: remote.create_folder(place.folder),
        adopt=place.folder_id if place.action == FOLDER_ADOPT else "",
        stale=place.stale,
    )
    account_id, made = store.reserve_made(
        one.target.rekordbox_id,
        name=place.title,
        folder=place.folder,
        create=lambda: remote.create_playlist(place.title),
    )
    if made:
        remote.move_to_folder(account_id, folder_id)
    return replace(one, target=replace(one.target, account_id=account_id, marked=True))


def _made_in_rekordbox(
    cfg: config.Config, one: PairPlan
) -> tuple[PairPlan, playlist_pair.Written | None]:
    """Make an account playlist's rekordbox side at its home, and pair it (U202).

    The pairs lock is taken before the database is opened, so an unwritable
    document refuses before anything is made, and the pair is marked as the
    product's straight after the commit. An account playlist another sync
    paired first makes nothing and answers None. The playlist is read back
    after it is recorded, so a read back that refuses leaves it paired.
    """
    from dataclasses import replace

    from cratekit.modules.outbound import pairs
    from cratekit.sync import pair_reverse

    home = one.home
    assert home is not None
    holder: dict[str, Any] = {}

    def landed(playlist_id: str) -> None:
        holder["landed"] = playlist_id

    def create() -> str:
        db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
        try:
            holder["written"] = pair_reverse.create(
                cfg,
                db,
                home,
                one.change.order,
                source=f"{PAIR_SOURCE}:{one.target.account_id}",
                analysis_roots=analysis_store.watch_roots(cfg),
                on_commit=landed,
            )
        except BaseException as exc:
            # A FAILURE AFTER THE COMMIT LANDED still pairs what landed (U202,
            # from the review), so the playlist is never left in rekordbox
            # unpaired; the failure is raised once the pair is recorded.
            if not holder.get("landed"):
                raise
            holder["failed"] = exc
            return holder["landed"]
        finally:
            rb_writer.close_db(db)
        return holder["written"].playlist_id

    rekordbox_id, made = pairs.PairStore(cfg).reserve_made_rekordbox(
        one.target.account_id, name=one.name, folder=home.folder, create=create
    )
    if "failed" in holder:
        raise holder["failed"]
    if not made:
        return one, None
    change = replace(one.change, playlist_id=rekordbox_id)
    playlist_pair.assert_read_back(holder["written"], change)
    return (
        replace(
            one,
            target=replace(one.target, rekordbox_id=rekordbox_id, marked=True),
            change=change,
        ),
        holder["written"],
    )


def _queue(cfg: config.Config, one: PairPlan, store) -> str:
    """Queue the pair's missing tracks through the intake path, once. The job id, or ``""``."""
    if not one.acquire:
        return ""
    job = intake_cli.queue_playlist(
        store,
        cfg,
        handler_key=INTAKE_HANDLER,
        reference=one.target.account_id,
        tracks=one.acquire,
        source_id=PAIR_SOURCE,
        name=one.name,
    )
    return job.job_id


def apply_pair(
    cfg: config.Config, one: PairPlan, *, rekordbox: bool, account: bool, store
) -> Done:
    """Write one pair: mark it, rekordbox and the queue, then the account, then its snapshot."""
    from cratekit.modules.outbound import pairs

    done = Done(account_id=one.target.account_id)
    if not (rekordbox or account):
        return done
    rekordbox_after: tuple[playlist_pair.Row, ...] | None = None
    account_after: tuple[str, ...] | None = None
    if one.target.rekordbox_new:
        # U202. THE REKORDBOX SIDE IS MADE ONLY ON REKORDBOX'S GATE, and with
        # nothing made there is nothing to pair, so an account side approved
        # alone writes nothing; the next sync finds the playlist again.
        if not rekordbox:
            return done
        one, written = _made_in_rekordbox(cfg, one)
        if written is None:
            return done
        done.marked = True
        done.created_in_rekordbox = one.target.rekordbox_id
        done.rekordbox = written
        rekordbox_after = written.read_back
        done.queued = _queue(cfg, one, store)
        # Nothing further on rekordbox: the playlist was made holding the plan.
        rekordbox = False
    elif one.target.new:
        # U198. THE ACCOUNT SIDE IS MADE ONLY ON THE ACCOUNT'S GATE, and with
        # nothing made there is nothing to pair, so a rekordbox side approved
        # alone writes nothing; the next sync finds the playlist again.
        if not account:
            return done
        one = _made(cfg, one)
        done.account_id = one.target.account_id
        done.marked = True
        done.created = one.target.account_id
    else:
        pairs.PairStore(cfg).mark(one.target.account_id, one.target.rekordbox_id, name=one.name)
        done.marked = not one.target.marked

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
        done.queued = _queue(cfg, one, store)

    if account:
        from cratekit.modules.outbound import account as outbound_account

        remote = outbound_account.resolve(cfg)
        playlist_id = one.target.account_id
        if one.account_removes:
            done.account_removed = len(remote.remove_tracks(playlist_id, one.account_removes))
        if one.account_adds:
            done.account_added = len(set(remote.add_tracks(playlist_id, one.account_adds)))
        if one.account_order:
            account_after = tuple(remote.order_tracks(playlist_id, one.account_order))
            done.account_ordered = True
        else:
            account_after = tuple(remote.playlist_tracks(playlist_id))
    done.snapshot = _record(
        cfg, one, rekordbox_after=rekordbox_after, account_after=account_after
    )
    return done


def _warnings(planned: Plan) -> list[dict[str, str]]:
    """What the plan could not do, said by name, one warning per kind."""
    said: list[dict[str, str]] = []
    if planned.left_out:
        said.append(
            {
                "code": LEFT_OUT,
                "message": (
                    f"{len(planned.left_out)} marked pair(s) were not synced: "
                    + "; ".join(
                        f"{account_id}: {why}" for account_id, why in planned.left_out.items()
                    )
                ),
            }
        )

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
    if planned.listed:
        from cratekit.sync import pair_discover

        parts = []
        for kind, rows in pair_discover.by_kind(planned.listed).items():
            if kind == pair_discover.SKIPPED:
                reasons: dict[str, int] = {}
                for one in rows:
                    reasons[one.why] = reasons.get(one.why, 0) + 1
                parts.extend(
                    f"{count} playlist(s) skipped: {why}" for why, count in reasons.items()
                )
                continue
            parts.append(
                f"{len(rows)} {pair_discover.SAID[kind]}: "
                + "; ".join(f"{one.where} ({one.why})" for one in rows)
            )
        said.append(
            {
                "code": NOT_DISCOVERED,
                "message": "rekordbox playlists not paired with the account: " + "; ".join(parts),
            }
        )
    if planned.listed_back:
        said.append(
            {
                "code": NOT_BROUGHT,
                "message": (
                    f"{len(planned.listed_back)} account playlist(s) in a synced folder were "
                    f"not made in rekordbox: "
                    + "; ".join(f"{one.where} ({one.why})" for one in planned.listed_back)
                ),
            }
        )

    def called(one: PairPlan, call: pair_merge.Call) -> str:
        named = one.names.get(call.key)
        words = f"{named.artist} - {named.title}" if named is not None else call.key
        added = "the account" if call.added_on == pair_merge.ACCOUNT else "rekordbox"
        removed = "rekordbox" if call.added_on == pair_merge.ACCOUNT else "the account"
        return f"{words} in {one.name!r} (added on {added}, taken off {removed})"

    by_time = [
        (one, call)
        for one in planned.pairs
        for call in one.merged.calls
        if call.outcome != pair_merge.TIME_UNKNOWN
    ]
    if by_time:
        said.append(
            {
                "code": LATER_CHANGE,
                "message": (
                    f"{len(by_time)} track(s) were added on one side and taken off the other "
                    f"since the last sync, and the later change is applied to both: "
                    + "; ".join(
                        called(one, call)
                        + (
                            ", kept, the removal was not later"
                            if call.kept
                            else ", taken off both, the removal was later"
                        )
                        for one, call in by_time
                    )
                ),
            }
        )
    unknown = [
        (one, call)
        for one in planned.pairs
        for call in one.merged.calls
        if call.outcome == pair_merge.TIME_UNKNOWN
    ]
    if unknown:
        said.append(
            {
                "code": TIME_UNKNOWN,
                "message": (
                    f"{len(unknown)} track(s) were added on one side and taken off the other "
                    f"since the last sync, and when one of the two was done is not known, so "
                    f"each stays on both: "
                    + "; ".join(called(one, call) for one, call in unknown)
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
        every = not getattr(ctx.args, "account", None)
        planned = plan(cfg, wanted, store=store, every=every)
        # R-988. WHAT THE ACCOUNT SAID OF A ROW IS A FACT ABOUT THE ROW, recorded
        # before the gate, so the plans the gates make again ask it nothing.
        store_of_pairs.remember(planned.misses, forget=planned.matched)
        data = payload(planned)
        shown = facts(planned)
        warnings = _warnings(planned)
        gates = {spec.name: spec for spec in ctx.entry.gates}
        on_rekordbox = (
            ctx.gate.require(gates[REKORDBOX_GATE], plan=data, context=shown) == APPLY
        )
        on_account = ctx.gate.require(gates[ACCOUNT_GATE], plan=data, context=shown) == APPLY
        if not planned.pairs and not planned.unpaired:
            if planned.listed or planned.listed_back:
                return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
            return ctx.envelope(
                data=data,
                outcome=Outcome.NO_OP,
                warnings=[
                    *warnings,
                    {
                        "code": NOTHING,
                        "message": (
                            "no playlist is paired yet and none of your own was found "
                            "in rekordbox to pair; pair one with crate sync pair "
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
    forgotten = [
        one
        for one in planned.unpaired
        if not one.made
        and store_of_pairs.unmark(one.account_id, one.rekordbox_id) is not None
    ]
    # U198. A MADE PAIR THAT LOST A SIDE IS UNPAIRED AND ITS SURVIVOR RELEASED,
    # so a sync of every pair never makes the lost side again.
    released = [
        one
        for one in planned.unpaired
        if one.made
        and store_of_pairs.release(one.account_id, one.rekordbox_id, side=one.gone) is not None
    ]
    if released:
        warnings.append(
            {
                "code": RELEASED,
                "message": (
                    f"{len(released)} pair(s) lost a side and were unpaired; the other "
                    f"side is left as it was and is not made again: "
                    + "; ".join(
                        (
                            f"{one.name or one.account_id} stays on the account (its "
                            f"rekordbox playlist is {one.why or 'gone'})"
                            if one.gone == REKORDBOX_SIDE
                            else f"{one.rekordbox_name or one.rekordbox_id} stays in "
                            f"rekordbox (its account playlist is gone)"
                        )
                        for one in released
                    )
                ),
            }
        )
    if forgotten:
        warnings.append(
            {
                "code": UNPAIRED,
                "message": (
                    f"{len(forgotten)} custom playlist twin(s) lost their account "
                    f"playlist and were unpaired; each is left in rekordbox as it was: "
                    + "; ".join(
                        f"{one.rekordbox_name or one.rekordbox_id} (was paired with "
                        f"{one.name or one.account_id})"
                        for one in forgotten
                    )
                ),
            }
        )
    totals = {
        **data["totals"],
        "rekordbox_added": sum(d.rekordbox.added for d in done if d.rekordbox),
        "rekordbox_removed": sum(d.rekordbox.removed for d in done if d.rekordbox),
        "account_added": sum(d.account_added for d in done),
        "account_removed": sum(d.account_removed for d in done),
        "queued_jobs": [d.queued for d in done if d.queued],
        "marked": sum(1 for d in done if d.marked),
        "unpaired": len(forgotten) + len(released),
        "created_playlists": [d.created for d in done if d.created],
        "created_in_rekordbox": [d.created_in_rekordbox for d in done if d.created_in_rekordbox],
    }
    answered = {"rekordbox": on_rekordbox, "the account": on_account}
    sides = [side for side, on in answered.items() if on]
    skipped = [side for side, on in answered.items() if not on]
    message = (
        f"{len(done)} pair(s) synced on {' and '.join(sides)}"
        + (
            f", {len(totals['created_playlists'])} account playlist(s) made"
            if totals["created_playlists"]
            else ""
        )
        + (
            f", {len(totals['created_in_rekordbox'])} rekordbox playlist(s) made"
            if totals["created_in_rekordbox"]
            else ""
        )
        + ": "
        f"{totals['rekordbox_added']} added and {totals['rekordbox_removed']} taken off "
        f"in rekordbox, {totals['account_added']} added and "
        f"{totals['account_removed']} taken off on the account, "
        f"{len(totals['queued_jobs'])} acquisition job(s) queued; no track left the "
        f"collection or the account"
        + (f"; {' and '.join(skipped)} skipped, its snapshot unchanged" if skipped else "")
    )
    wrote = any(d.wrote for d in done) or bool(forgotten) or bool(released)
    return ctx.envelope(
        data={**data, "totals": totals},
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
        warnings=[*warnings, {"code": WRITTEN if wrote else NOTHING, "message": message}],
    )


__all__ = [
    "ACCOUNT_GATE",
    "BROUGHT_REASONS",
    "INTAKE_HANDLER",
    "PAIR_SOURCE",
    "REKORDBOX_GATE",
    "LATER_CHANGE",
    "NEW",
    "NOT_BROUGHT",
    "NOT_DISCOVERED",
    "RELEASED",
    "TIME_UNKNOWN",
    "Done",
    "PairPlan",
    "Place",
    "Plan",
    "Target",
    "Unpaired",
    "apply_pair",
    "build",
    "facts",
    "file_identity",
    "generated_tops",
    "landed_inbox_playlists",
    "landed_isrcs",
    "payload",
    "plan",
    "plan_pair",
    "sync_pair",
    "targets",
]
