"""What ``crate sync pair`` is asked and the words it plans in: the targets, the scopes, the step names and the clock (U130, U304)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from cratekit.core.cause import CratekitError, refuse
from cratekit.intake import cli as intake_cli
from cratekit.sync import pair_merge, pair_stopped, playlists
from cratekit.write import playlist_pair

_ORIGIN = ("sync.pair",)

REKORDBOX_GATE = "sync.pair.rekordbox"

ACCOUNT_GATE = "sync.pair.account"

APPLY = "apply"


#: The handler key an acquisition is queued under, the ``intake playlist`` job,
#: so it is acquired and landed exactly as a playlist run by hand.
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


#: What a row with no ISRC anywhere is said to be; the account is not asked,
#: since the row has nothing it could match on.
NO_ISRC = "the row carries no ISRC, in the database or in its file"


#: The warning codes the answer carries.
UNMATCHED = "sync-pair-unmatched"

AWAITING = "sync-pair-awaiting"


#: R-1385. How an awaited track an earlier pair of the same plan is to queue
#: is named: no job holds it until that pair's rekordbox side is applied.
QUEUED_HERE = "to be queued by this sync for"

AMBIGUOUS = "sync-pair-ambiguous"

WITHHELD = "sync-pair-withheld"

SKIPPED = "sync-pair-skipped"

NOTHING = "sync-pair-nothing"

LEFT_OUT = "sync-pair-left-out"


#: U226. The refusal of a pair whose account window read disagrees with its
#: partial unpaged read, so neither is the playlist as it stands.
LAGGING = "sync-pair-account-lagging"


#: U231. The refusal of a pair whose account order was sent and not yet read
#: back by two readings that agree, held whole for this run.
SETTLING = "sync-pair-account-settling"


#: U231. Pairs whose order this run sent and the provider does not yet serve.
PENDING = "sync-pair-order-pending"

WRITTEN = "sync-pair-written"


#: A custom playlist twin's pair forgotten because its account playlist is gone (U149).
UNPAIRED = "sync-pair-twin-unpaired"


#: R-1264. Account tracks listed with no title or no artist, kept by their id.
UNREAD = "sync-pair-unread"


#: U221. A twin's tracks held for the author's choice, counted per twin.
ON_HOLD = "sync-pair-on-hold"


#: U225. Pairs a fresh sync plans as finishing a write stopped part way
#: through its order, each named with the run that stopped.
FINISHING = "sync-pair-finishing"


#: U225. Runs' steps a plan could not read, so a stopped write in them was
#: not looked for.
STOPPED_UNREAD = "sync-pair-stopped-unread"


#: R-1383. Account tracks the library lacks that an unreadable landing record
#: may have brought in, held and never queued until it reads.
LANDING_UNREAD = "sync-pair-landing-unread"


#: U221. The gate's item for one of them.
ON_HOLD_ACTION = "on-hold"


#: R-1383. The gate's item for one of them.
LANDING_UNREAD_ACTION = "landing-unread"


#: The refusals about one pair's own playlists, which a sync of every pair
#: names and passes over. An unusable account listing is one (R-1264).
PER_PAIR_REASONS = frozenset(
    {
        "sync-pair-unknown",
        "sync-pair-out-of-scope",
        "intake-list-unusable",
        # U226. Its account playlist's window read lags its unpaged read.
        LAGGING,
        # U231. Its account order was sent and is not yet read as landed.
        SETTLING,
    }
)


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



# ---------------------------------------------------------------------------
# What is asked
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Target:
    """One pair a sync was asked for, and whether it is marked yet."""

    account_id: str
    rekordbox_id: str
    marked: bool
    #: U198. A discovered pair's account root folder and title, while
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



def _lagging(account_id: str, name: str) -> CratekitError:
    """The pair held whole for this run, its account side served out of step (U226).

    HELD WHOLE, NOT ITS ORDER ALONE, since a lagging window shows old
    membership too and a track just taken off would be put back.
    """
    return refuse(
        LAGGING,
        f"the account playlist {name or account_id} reads one way through its pages "
        f"and another through the provider's unpaged read, which is not the whole "
        f"playlist, so it may lag a recent change; the pair was not synced this run",
        steps=(
            "wait a few minutes for the provider to serve the playlist as it "
            "stands, then sync the pair again",
        ),
        origin=_ORIGIN,
        detail={"account_id": account_id, "problem": "window-lags"},
    )



def _settling(
    account_id: str,
    name: str,
    run_id: str,
    *,
    lag: bool,
    write: pair_stopped.StoppedWrite | None = None,
    at: int = 0,
) -> CratekitError:
    """The pair held whole for this run, its account order sent and not yet read as landed (U231).

    HELD WHOLE, as a lagging pair is, since a reading that lags the moves may
    lag membership too. ``lag`` says the readings agree on an order ``at``
    moves along ``write``'s way, short of where the moves leave it, and the
    message names why (R-1394).
    """
    after = (
        "a read that lags them serves that, and so would a reorder by hand back onto "
        "their way, which leaves the pair held until the playlist is moved off it in "
        "the provider's player or the pair is released"
    )
    total = len(pair_stopped.front_moves(write.start, write.target)) if write else 0
    if not lag:
        said = (
            f"run {run_id}'s write sent its order's moves and no two readings of the "
            f"playlist since agree on where they left it"
        )
    elif write is None or write.moved:
        said = (
            f"every move run {run_id}'s write sent was accepted, and the playlist still "
            f"reads as one of the orders on their way, short of the order they leave: "
            f"{after}"
        )
    elif at < write.landed:
        said = (
            f"the provider accepted {write.landed} of the {total} moves run {run_id}'s "
            f"write sent before it stopped, and the playlist still reads as an order "
            f"from before the last of them: {after}"
        )
    elif write.sent - write.landed == 1:
        said = (
            f"run {run_id}'s write stopped while move {write.sent} of its {total} was "
            f"being sent, so whether it landed is not known, and the playlist still reads "
            f"as the order before it: moved again from that, the rest would land on the "
            f"wrong tracks if it did, so the pair is held until the provider serves that "
            f"move landed, the playlist is moved off their way in the provider's player, "
            f"or the pair is released"
        )
    else:
        said = (
            f"run {run_id}'s write stopped part way through its {total} moves and "
            f"recorded no count of how many landed, so the playlist's reading on their "
            f"way may lag them: moved again from it, the rest would land on the wrong "
            f"tracks, so the pair is held until the provider serves the order they "
            f"leave, the playlist is moved off their way in the provider's player, or "
            f"the pair is released"
        )
    return refuse(
        SETTLING,
        f"the account playlist {name or account_id}'s order is pending: {said}; the "
        f"pair was not synced this run, and nothing is moved again until the provider "
        f"serves it",
        steps=(
            "sync the pair again in a few minutes, once the provider serves the "
            "playlist as it stands",
        ),
        origin=_ORIGIN,
        detail={
            "account_id": account_id,
            "run_id": run_id,
            "problem": "order-pending",
            **({"landed": write.landed, "sent": write.sent, "moves": total} if write else {}),
        },
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
    #: Account tracks already queued by this pair, another pair's job or an
    #: earlier pair of this plan (R-1385).
    awaiting: tuple[Named, ...] = ()
    #: U221. Missing tracks a twin holds for the author's choice, never queued
    #: until ``sync release``.
    on_hold: tuple[Named, ...] = ()
    #: R-1383. Missing tracks with an ISRC, held while an unreadable landing
    #: record may have brought them in.
    landing_unread: tuple[Named, ...] = ()
    #: Account tracks two live library rows carry, so no row is chosen.
    ambiguous: tuple[Named, ...] = ()
    #: U208. Rekordbox rows matched as one of several releases that all agree.
    tied: tuple[Named, ...] = ()
    #: U208. Account tracks read as another release's key, by remote id.
    siblings: dict[str, Named] = field(default_factory=dict)
    #: Links this plan made, remote id to content id.
    links: dict[str, str] = field(default_factory=dict)
    #: Every key's words, for the screen.
    names: dict[str, Named] = field(default_factory=dict)
    #: Remote id to content id for every key the plan resolved.
    content_of: dict[str, str] = field(default_factory=dict)
    #: ``ListingShortfall.block()`` when the account listing was short.
    withheld: dict[str, int] | None = None
    #: R-1264. Unread account tracks in listing order, named with what they lack.
    unread: tuple[Named, ...] = ()
    #: U198. Where the account side is made, for a pair whose account side is new.
    place: Place | None = None
    #: U202. Where a new rekordbox side is made, a ``pair_discover.Home``.
    home: Any = None
    #: U202. Each listed track's account added date, ISO text by remote id.
    account_dates: dict[str, str] = field(default_factory=dict)
    #: U225. Every id the account listed, in order, which the write starts from.
    account_before: tuple[str, ...] = ()
    #: U225. The run whose stopped order this plan finishes, or empty; and
    #: whether the account stood where its moves left it, so the order was finished.
    finishing: str = ""
    finishing_order: bool = False
    #: U234. Whether the account stood off that write's path, read as the
    #: provider's partial state; whether settled readings since show it
    #: reordered, so it leads; and whether the plan merged against what the
    #: write left.
    finishing_off_path: bool = False
    reordered_since_stop: bool = False
    finishing_folded: bool = False
    #: U234. Whether that write sent no move, so an order off its path is the person's.
    stop_moved_nothing: bool = False
    #: R-1446. Whether only unread tracks moved since the stop, so the order
    #: was finished with each moved one kept where the person put it.
    stop_unread_moved: bool = False
    #: R-1446. Whether an unread track nobody moved is placed by the write's target.
    stop_unread_others: bool = False
    #: R-1446. Whether that write sent no move, so the account was read against
    #: where it began.
    stop_unread_unsent: bool = False
    #: U231. Whether a new account order goes unkept, its rekordbox playlist
    #: being outside GIG READY.
    order_unkept: bool = False

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
            # R-1264, ONLY WHEN ANY, so a pair served whole digests as it did.
            **(
                {"unread": [named.remote_id for named in self.unread]} if self.unread else {}
            ),
            # U221, ONLY WHEN ANY, so a pair holding nothing digests as it did.
            **(
                {"on_hold": sorted(named.remote_id for named in self.on_hold)}
                if self.on_hold
                else {}
            ),
            # R-1383, ONLY WHEN ANY, so a plan reading every record digests as it did.
            **(
                {"landing_unread": sorted(named.remote_id for named in self.landing_unread)}
                if self.landing_unread
                else {}
            ),
            # U225, ONLY WHEN ONE, so a pair no stopped write left digests as it did.
            **({"finishing": self.finishing} if self.finishing else {}),
            # U231, ONLY WHEN SO, so a pair that keeps its order digests as it did.
            **({"order_unkept": True} if self.order_unkept else {}),
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
    #: U216. The playlists an adopted folder already held, recorded so none
    #: comes to rekordbox; None when the plan did not say.
    held: frozenset[str] | None = None

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
    from cratekit.favorites import placeholders
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



def _now() -> datetime:
    """Now, in UTC, which a pending order's readings are aged against (U231).

    Callers write ``pair_model._now()``, never a copy of the name, so a suite
    that replaces the clock here reaches every caller (U304).
    """
    return datetime.now(UTC)



#: U210. The steps one pair's write records in its run, in the order they land.
STEP_MAKING = "making"

STEP_MADE = "made"

STEP_REKORDBOX = "rekordbox"

STEP_QUEUED = "queued"

STEP_ACCOUNT = "account"

STEP_ORDERING = "ordering"


#: U220. The pair's account order was refused part way, its message the value.
STEP_ORDER_REFUSED = "order-refused"


#: U231. The order's moves are about to be sent, recorded with their reading
#: and target (``pair_stopped.moving_step``) before the first goes, so no
#: command sends them again; then every one was accepted.
STEP_MOVING = "moving"

STEP_MOVED = "moved"

STEP_DONE = "done"


#: U231. The rekordbox top folder whose pairs keep the account's order, unless
#: ``outbound.pair_order_every_pair`` keeps every pair's.
ORDER_FOLDER = "GIG READY"


#: U220. Account order refusals that stop that pair alone, an untrusted read
#: or a provider failure; anything else stops the whole write, since every
#: later pair would meet it too.
ORDER_REFUSALS = frozenset({"outbound-remove-refused", "unavailable-transient"})


#: U210. The refusal a write stops with when a step it took cannot be recorded.
STEPS_UNWRITTEN = "sync-pair-steps-unwritten"
