"""Every pair planned together, and what the gate shows: the facts, the payload and the warnings (U130, U304)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config, rb_writer, session
from cratekit.core.cause import CratekitError
from cratekit.sync import pair_merge, playlists
from cratekit.sync.pair_model import (
    AMBIGUOUS,
    AWAITING,
    BROUGHT_REASONS,
    FINISHING,
    FOLDER_ADOPT,
    FOLDER_CREATE,
    FOLDER_REUSE,
    LANDING_UNREAD,
    LANDING_UNREAD_ACTION,
    LATER_CHANGE,
    LEFT_OUT,
    NOT_BROUGHT,
    NOT_DISCOVERED,
    ON_HOLD,
    ON_HOLD_ACTION,
    ORDER_FOLDER,
    PER_PAIR_REASONS,
    QUEUED_HERE,
    STOPPED_UNREAD,
    TIME_UNKNOWN,
    UNMATCHED,
    UNREAD,
    WITHHELD,
    Named,
    PairPlan,
    Place,
    Target,
    _scope_account,
    generated_tops,
)
from cratekit.sync.pair_plan import plan_pair
from cratekit.sync.pair_read import _Reader
from cratekit.write import playlist_pair


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
    #: side for a discovered playlist, whose survivor is then released. The
    #: default is ``pairs.ACCOUNT_SIDE``, written out so this package imports
    #: the outbound module only where a function needs it (U304).
    gone: str = "account"
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
    #: U225. Runs' steps the plan could not read, each said, so a write that
    #: stopped part way in one of them was not looked for.
    stopped_unread: tuple[str, ...] = ()
    #: R-1383. The session log's entries the plan could not read when it
    #: looked for a landing, each said, or the log itself when it cannot be listed.
    landings_unread: tuple[str, ...] = ()

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
    from cratekit.modules.outbound.pairs import REKORDBOX_SIDE
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
            stopped_unread=reader.stopped[1] if "stopped" in reader.__dict__ else (),
            landings_unread=(
                _landings_said(cfg, reader.landings[1]) if "landings" in reader.__dict__ else ()
            ),
        )
    finally:
        rb_writer.close_db(db)



def _landings_said(cfg: config.Config, unread: Sequence[Path]) -> tuple[str, ...]:
    """The log's unread entries as a warning names them: the log itself, or each record (R-1383)."""
    if session.log_unlisted(unread, cfg):
        return (
            f"the session log at {unread[0]}, which exists and cannot be listed "
            f"by this account, and reads once this account may list it",
        )
    return tuple(
        f"the record {Path(path).name} in {Path(path).parent}, which reads under the "
        f"later build that wrote it, or is torn and is a defect to report"
        for path in unread
    )



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
                    Place(
                        folder,
                        one.title,
                        action,
                        folder_id,
                        stale,
                        # U216. WHAT AN ADOPTED FOLDER HOLDS NOW is what it held
                        # before any sync, recorded when the folder is adopted.
                        held=frozenset(inside) if action == FOLDER_ADOPT else None,
                    ),
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
    U216: and one the folder held before a sync adopted it
    (``pair_discover.before_adoption``), or a ``DOWNLOADED `` copy of one a
    pair in the folder holds (``pair_discover.downloaded_copy``).
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
    paired_ids = set(document.pairs)
    # U242. WHAT THE RECORD HOLDS AS TAKEN, so a downloaded copy stripped of
    # its old prefix is still read as the copy it is.
    taken = playlists.taken_ids(cfg)
    released = document.released.account
    favorites = placement.source_name(active_taxonomy.load(cfg))
    wanted: list[tuple[str, str, str, Any]] = []
    for folder, recorded in sorted(document.folders.items()):
        if recorded.folder_id not in root:
            continue
        inside = reader.folder_listing(recorded.folder_id)
        # U216. A FOLDER ADOPTED BEFORE ITS RECORD SAID WHAT IT HELD is read by
        # time: the earliest mark of a playlist made in it dates the adoption.
        unrecorded = recorded.held is None and not recorded.created
        adopted = (
            pair_discover.adoption_moment(
                pair.marked
                for pair in document.pairs.values()
                if pair.made and pair.folder == folder
            )
            if unrecorded
            else None
        )
        paired_titles = [
            title for account_id, title in inside.items() if account_id in paired_ids
        ]
        fresh: list[tuple[str, str]] = []
        for account_id, title in sorted(inside.items(), key=lambda one: (one[1], one[0])):
            if account_id in paired_ids:
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
            # U216. ONLY A PLAYLIST MADE ON THE ACCOUNT AFTER THE SYNC COMES IN,
            # decided by Phillip on 2026-11-04: one the folder held before a
            # sync adopted it is the account's own, and is named, never made.
            before = pair_discover.before_adoption(
                account_id,
                held=recorded.held,
                created=recorded.created,
                folder=folder,
                made=(
                    reader.folder_dates(recorded.folder_id).get(account_id)
                    if unrecorded and adopted is not None
                    else None
                ),
                adopted=adopted,
            )
            if before:
                left(account_id, title, folder, pair_discover.BEFORE, before)
                continue
            fresh.append((account_id, title))
        for account_id, title in fresh:
            # AND A DOWNLOADED COPY of a playlist a pair in this folder holds, or
            # of one this sync brings in beside it (U216, from the review), is
            # that playlist again, so making it would put it in rekordbox twice.
            beside = pair_discover.copy_candidates(fresh, account_id, title, taken)
            copied = pair_discover.downloaded_copy(
                folder, title, [*paired_titles, *beside], taken=account_id in taken
            )
            if copied:
                whose = (
                    "a pair in the same folder already holds"
                    if copied in paired_titles
                    else "this sync brings in from the same folder"
                )
                left(
                    account_id,
                    title,
                    folder,
                    pair_discover.COPY,
                    f"it is a downloaded copy of {copied!r}, which {whose}, so it is not "
                    f"made in rekordbox; {pair_discover.BY_HAND}",
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
    by_remote.update(one.siblings)

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
    broken = {named.remote_id for named in one.tied}
    for remote_id in one.account_adds:
        items.append(
            row(
                "account",
                "add",
                by_remote.get(remote_id),
                **({"tied": True} if remote_id in broken else {}),
            )
        )
    if one.account_order:
        items.append(row("account", "order", None, tracks=len(one.account_order)))
    for remote_id in one.acquire:
        items.append(row("library", "acquire", by_remote.get(remote_id)))
    for named in one.awaiting:
        items.append(row("library", "awaiting", named))
    for named in one.on_hold:
        items.append(row("library", ON_HOLD_ACTION, named))
    for named in one.landing_unread:
        items.append(row("library", LANDING_UNREAD_ACTION, named))
    for named in one.unmatched:
        items.append(row("account", "unmatched", named))
    for named in one.ambiguous:
        items.append(row("rekordbox", "ambiguous", named))
    for named in one.unread:
        items.append(row("account", "unread", named))
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
            # U221. A twin's tracks held for the author's choice.
            "on_hold": count("library", ON_HOLD_ACTION),
            # R-1383. Tracks an unread landing record may have brought in.
            "landing_unread": count("library", LANDING_UNREAD_ACTION),
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
            # U208. Rows matched as one of several releases that all agree.
            "tied": sum(len(one.tied) for one in planned.pairs),
            # R-1264. Account tracks listed with no title or no artist.
            "unread": count("account", "unread"),
        },
        "chunk": None,
    }



def facts(planned: Plan) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per pair."""
    from cratekit.modules.outbound.pairs import REKORDBOX_SIDE
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
            + (
                f"finishes run {one.finishing}'s write, stopped part way through its "
                f"order, "
                + (
                    # R-1446. Only its unread tracks were moved since, by hand.
                    (
                        "and the account stands off its moves' path only by where tracks "
                        "the account lists with no title or no artist stand, "
                        if one.stop_unread_unsent
                        else "and only tracks the account lists with no title or no artist "
                        "were moved since the stop, "
                    )
                    + "which neither side's order reads, so each one moved stays where "
                    "it was put, "
                    + (
                        "any other goes where the stopped order was taking it or else "
                        "behind the track it follows, "
                        if one.stop_unread_others
                        else ""
                    )
                    + "and the rest of its order is finished; "
                    if one.stop_unread_moved
                    else "and the account stands where none of its moves leaves it, which "
                    "is the provider's partial state as often as an edit, so its order "
                    "is not read as anybody's; "
                    if one.finishing_off_path
                    else "so its moves are not read as anybody's; "
                    if one.finishing_order
                    else (
                        "whose additions and removals are read as that write's; "
                        if one.finishing_folded
                        else ""
                    )
                    + (
                        "none of its moves was sent, so the account's order is read "
                        "as yours; "
                        if one.stop_moved_nothing
                        else "the account was reordered since syncs after the stop read "
                        "it settled, so its order is read as yours; "
                    )
                )
                if one.finishing
                else ""
            )
            + f"order follows {lead}"
            + (
                f"; the account's order is kept only for pairs under {ORDER_FOLDER}, so "
                f"it is left as it is there"
                if one.order_unkept
                else ""
            )
            + (
                f"; the account withheld {one.withheld.get('withheld', 0)} track(s), so "
                f"nothing is removed or reordered there"
                if one.withheld
                else ""
            )
            + (
                f"; the account lists {len(one.unread)} track(s) with no title or no "
                f"artist, so each is left where it is on both sides"
                + (
                    # R-1432. A finish puts one back where the stopped order
                    # was taking it, not where an interrupted move left it.
                    ", and the account's order puts each where the stopped order was "
                    "taking it, or else behind the track it follows"
                    if one.finishing_order
                    and one.account_order
                    and (not one.stop_unread_moved or one.stop_unread_others)
                    else ""
                )
                if one.unread
                else ""
            )
            + (
                f"; {len(one.tied)} row(s) matched as one of several releases that all "
                f"agree with it, the hearted one or else the lowest numbered"
                if one.tied
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
        # R-1385, from the review. A TRACK ANOTHER PAIR OF THIS PLAN QUEUES is
        # said apart, since no job holds it unless that pair's rekordbox side
        # is applied, and a skip leaves it for the next sync to queue.
        here = [row for row in awaiting if row.reason.startswith(QUEUED_HERE)]
        before = [row for row in awaiting if not row.reason.startswith(QUEUED_HERE)]
        parts: list[str] = []
        if before:
            parts.append(
                f"{len(before)} account track(s) were queued for acquisition, by an "
                f"earlier sync or for another pair, and are not in the library yet: "
                f"{listed(before)}"
            )
        if here:
            parts.append(
                f"{len(here)} account track(s) another pair of this sync lists are "
                f"queued once, for that pair, when its rekordbox side is applied: "
                f"{listed(here)}"
            )
        said.append({"code": AWAITING, "message": "; ".join(parts)})
    holding = [one for one in planned.pairs if one.on_hold]
    if holding:
        said.append(
            {
                "code": ON_HOLD,
                "message": (
                    f"{sum(len(one.on_hold) for one in holding)} account track(s) the "
                    f"library lacks are held for your choice and were not queued, each "
                    f"named on the gate: "
                    + "; ".join(
                        f"{one.name}: {len(one.on_hold)} (crate sync release "
                        f"{one.target.account_id})"
                        for one in holding
                    )
                    + "; crate sync release --all lets every twin's go"
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
    unread = [(one, named) for one in planned.pairs for named in one.unread]
    if unread:
        # R-1432. A finish of a stopped order puts an unread track where that
        # order was taking it, which is not where an interrupted move left it.
        # R-1446. Not one whose unread tracks the person moved since the
        # stop, which keep the place they were given, unless another unread
        # track is still placed by the target.
        finished_unread = any(
            one.finishing_order
            and one.account_order
            and (not one.stop_unread_moved or one.stop_unread_others)
            for one, _named in unread
        )
        said.append(
            {
                "code": UNREAD,
                "message": (
                    f"the account lists {len(unread)} track(s) that cannot be read, so each "
                    f"stays where it is on both sides until it reads"
                    + (
                        ", except that a pair finishing a stopped order puts each where "
                        "that order was taking it, or else behind the track it follows"
                        if finished_unread
                        else ""
                    )
                    + ": "
                    + "; ".join(
                        f"{one.name!r}: {named.artist or '?'} - {named.title or '?'} "
                        f"({named.reason})"
                        for one, named in unread
                    )
                ),
            }
        )
    finishing = [one for one in planned.pairs if one.finishing]
    if finishing:
        said.append(
            {
                "code": FINISHING,
                "message": (
                    f"{len(finishing)} pair(s) finish a write stopped part way through its "
                    f"order, so that write's own moves, additions and removals are not "
                    f"read as anybody's edit: "
                    + "; ".join(
                        f"{one.name!r} (run {one.finishing}, "
                        + (
                            (
                                "the account stands off its path only by where tracks the "
                                "account cannot read stand, so it is not read as a reorder; "
                                if one.stop_unread_unsent
                                else "only tracks the account cannot read were moved since, "
                                "so it is not read as a reorder; "
                            )
                            if one.stop_unread_moved
                            else "the account stands where none of its moves leaves it, so "
                            "it is not read as a reorder; "
                            if one.finishing_off_path
                            else ""
                        )
                        + (
                            f"order follows {'the account' if one.merged.leader == pair_merge.ACCOUNT else 'rekordbox'})"
                            if one.finishing_order
                            else "none of its moves was sent, so the account's order "
                            "leads)"
                            if one.stop_moved_nothing
                            else "the account was reordered since syncs after the stop "
                            "read it settled, so its order leads)"
                        )
                        for one in finishing
                    )
                ),
            }
        )
    if planned.landings_unread:
        waiting = [(one, named) for one in planned.pairs for named in one.landing_unread]
        said.append(
            {
                "code": LANDING_UNREAD,
                "message": (
                    "the session log could not be read whole, so a landing it records may "
                    "have brought in a track the library lacks, and "
                    + (
                        f"{len(waiting)} account track(s) that carry an ISRC were held and "
                        f"not queued until it reads: "
                        + "; ".join(
                            f"{one.name!r}: {named.artist or '?'} - {named.title or '?'}"
                            for one, named in waiting
                        )
                        if waiting
                        # THE SCAN WAS READ AND NOTHING WAITED ON IT (round one's
                        # finding 7): said as that, never as zero tracks held.
                        else "no track this plan would queue waited on it"
                    )
                    + ". Unread: "
                    + "; ".join(planned.landings_unread)
                    + ". This verb never moves or repairs a record"
                ),
            }
        )
    if planned.stopped_unread:
        said.append(
            {
                "code": STOPPED_UNREAD,
                "message": (
                    f"{len(planned.stopped_unread)} run(s)' steps could not be read, so a "
                    f"write stopped part way in them was not looked for, and a pair it "
                    f"left part ordered is planned as if nothing stopped: "
                    + "; ".join(planned.stopped_unread)
                ),
            }
        )
    return said
