"""The plan held across the two gates, and the check before the write that refuses a moved list (U209, U304)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from cratekit.acquire import listing as provider_listing
from cratekit.core import config, rb_writer
from cratekit.core.cause import CratekitError, refuse
from cratekit.intake import cli as intake_cli
from cratekit.sync import pair_merge
from cratekit.sync.pair_model import (
    _ORIGIN,
    ACCOUNT_GATE,
    BROUGHT_REASONS,
    FOLDER_CREATE,
    REKORDBOX_GATE,
    STEP_ACCOUNT,
    STEP_DONE,
    STEP_MADE,
    STEP_MAKING,
    STEP_MOVING,
    STEP_ORDERING,
    STEP_QUEUED,
    STEP_REKORDBOX,
    Named,
    PairPlan,
    Place,
    Target,
    generated_tops,
)
from cratekit.sync.pair_read import pair_jobs
from cratekit.sync.pair_screen import Plan, Unpaired
from cratekit.sync.pair_write import PairSteps, _made_here
from cratekit.write import playlist_pair

# ---------------------------------------------------------------------------
# The plan held across the gates (U209)
# ---------------------------------------------------------------------------

#: The kind a held plan is filed under.
HELD_KIND = "sync.pair"


#: The warning a command carries when it planned again instead of using its run's held plan.
REPLANNED = "sync-pair-replanned"


#: The two gates whose offers a held plan must match.
GATES = (REKORDBOX_GATE, ACCOUNT_GATE)



def _held_classes() -> dict[str, type]:
    """Every class a plan holds, by name: the closed registry the held plan reads back through."""
    from cratekit.modules.outbound import pairs
    from cratekit.sync import pair_discover

    classes = (
        Plan,
        PairPlan,
        Target,
        Named,
        Place,
        Unpaired,
        pair_merge.Merged,
        pair_merge.Call,
        playlist_pair.Change,
        pair_discover.Home,
        pair_discover.Listed,
        pairs.Miss,
    )
    return {kind.__name__: kind for kind in classes}



def _spent() -> int:
    """The provider calls this process has made, read around each phase."""
    from cratekit.core import provider_gate

    return provider_gate.process_spend().calls



def _asked(wanted: Sequence[Target], every: bool) -> dict[str, Any]:
    """What a plan was made for: the pairs asked and whether every pair was, as plain JSON."""
    return {
        "every": every,
        "targets": [[one.account_id, one.rekordbox_id, one.marked] for one in wanted],
    }



def _held_plan(
    run_id: str, offered: Mapping[str, str], asked: Mapping[str, Any]
) -> tuple[Plan | None, int, str]:
    """The plan held for this run, the calls its plan took, and why not when there is none.

    It answers only when it digests to EVERY offer this run recorded and was
    made for the pairs this command asks for; otherwise the plan is made
    again and the gates refuse it stale if it moved.
    """
    from cratekit.core import held_plan

    planned, digest, extra, why = held_plan.load(
        run_id, HELD_KIND, registry=_held_classes(), digest_of=lambda one: one.digest
    )
    if planned is None:
        return None, 0, why
    if not isinstance(planned, Plan):
        return None, 0, "the held plan is not a plan of this verb"
    moved = sorted(gate for gate, offer in offered.items() if offer != digest)
    if moved:
        return None, 0, f"the held plan is not the plan {', '.join(moved)} showed"
    if extra.get("asked") != dict(asked) and extra.get("asked") != _asked_before(
        run_id, asked, planned, digest
    ):
        # THE SAME RUN, OTHER PAIRS: another playlist named, or a pair marked or forgotten.
        return None, 0, "the held plan was made for other pairs than this command asks for"
    calls = extra.get("plan_calls")
    return planned, calls if isinstance(calls, int) and calls >= 0 else 0, ""



def _asked_before(
    run_id: str, asked: Mapping[str, Any], planned: Plan, digest: str
) -> dict[str, Any]:
    """What this command asks for, read as it was before this run's own write began (U210).

    A write stopped part way has made and marked pairs, so a sync of every
    pair would no longer ask what the held plan was made for though only this
    run moved it. The pairs its recorded steps account for are read back as
    the plan read them: a made side's new pair left out, a touched pair with
    the plan's mark.
    """
    from cratekit.core import held_plan

    steps, _why = held_plan.load_steps(run_id, digest)
    if not steps.started():
        return dict(asked)
    made_for: set[str] = set()
    made_from: set[str] = set()
    marked: dict[str, bool] = {}
    for one in planned.pairs:
        record = _steps_of(steps, one)
        if one.target.new and record.has(STEP_MAKING):
            made_for.add(one.target.rekordbox_id)
        elif one.target.rekordbox_new and record.has(STEP_REKORDBOX):
            made_from.add(one.target.account_id)
        elif one.target.account_id and steps.done.get(one.target.key):
            marked[one.target.account_id] = one.target.marked
    targets = []
    for account_id, rekordbox_id, mark in asked.get("targets") or ():
        if rekordbox_id in made_for or account_id in made_from:
            continue
        targets.append([account_id, rekordbox_id, marked.get(account_id, mark)])
    return {**dict(asked), "targets": targets}



def _hold(run_id: str, planned: Plan, calls: int, asked: Mapping[str, Any]) -> str:
    """Hold this command's plan under its run, and answer why not, or the empty string."""
    from cratekit.core import held_plan

    return held_plan.hold(
        run_id,
        HELD_KIND,
        planned,
        registry=_held_classes(),
        digest=planned.digest,
        extra={"plan_calls": calls, "asked": dict(asked)},
    )



def _release(run_id: str) -> None:
    from cratekit.core import held_plan

    held_plan.release(run_id)



#: The side a made rekordbox playlist's home is named on when it moved.
HOME_SIDE = "rekordbox-home"



@dataclass(frozen=True, slots=True)
class Moved:
    """One list the check before the write found other than the plan read it (U209)."""

    side: str
    playlist_id: str
    name: str
    why: str

    def shown(self) -> dict[str, str]:
        return {
            "side": self.side,
            "playlist_id": self.playlist_id,
            "name": self.name,
            "why": self.why,
        }

    def said(self) -> str:
        from cratekit.modules.outbound.pairs import ACCOUNT_SIDE
        if self.side == HOME_SIDE:
            return f"the rekordbox playlist to be made at {self.name!r}: {self.why}"
        where = "the account playlist" if self.side == ACCOUNT_SIDE else "the rekordbox playlist"
        if self.side == "account-folder":
            where = "the account folder"
        if self.side == "library":
            where = "the acquisitions queued for"
        named = f"{where} {self.name!r} ({self.playlist_id})" if self.playlist_id else (
            f"{where} {self.name!r}"
        )
        return f"{named} {self.why}"



def check(
    cfg: config.Config, planned: Plan, steps: Any = None, *, store, unread: str = ""
) -> dict[str, tuple[str, ...]]:
    """Refuse a write whose lists moved since the plan the gates showed, before anything is written.

    U209. A held plan is not made again, so this reads every list the write
    is merged from against what the plan read: rekordbox memberships, account
    listings with their shortfall, rows to add, a made side's folder or home,
    and where a product paired playlist stands. EVERY PAIR, whichever gate
    applied, since each side's writes were merged from both. It never matches
    a track. Anything moved refuses ``decision-stale`` naming every list.

    Answers each account listing as read, every unread track in its place
    (R-1264), so a pair with nothing to write there keeps it as its snapshot.

    ``steps`` (U210) is what an earlier command of the run wrote. A done pair
    is not read; a part written pair is read only for what its own write
    could not have done.
    """
    from cratekit.label import catalogue
    from cratekit.modules.outbound import pairs
    from cratekit.modules.outbound.pairs import ACCOUNT_SIDE, REKORDBOX_SIDE

    def of(one: PairPlan) -> PairSteps:
        return PairSteps(steps, one.target.key)

    # THE PAIRS DOCUMENT AS THE WRITE WILL FIND IT, read once.
    document = pairs.PairStore(cfg)._document()
    todo = [one for one in planned.pairs if not of(one).has(STEP_DONE)]
    begun = steps is not None and steps.started()
    # U210. THE ACCOUNT PLAYLISTS THIS RUN MADE, recorded made or begun and reserved here.
    ours: dict[str, str] = {}
    for one in planned.pairs:
        if not one.target.new:
            continue
        made_id = of(one).get(STEP_MADE)
        if isinstance(made_id, str) and made_id:
            ours[one.target.key] = made_id
        elif of(one).has(STEP_MAKING):
            for pair in document.pairs.values():
                if _made_here(pair, one):
                    ours[one.target.key] = pair.account_id
                    break
    # And the root folders it made: a folder a made pair began in, recorded.
    our_folders = {
        one.place.folder: document.folders[one.place.folder].folder_id
        for one in planned.pairs
        if one.target.new
        and one.place is not None
        and one.place.action == FOLDER_CREATE
        and of(one).has(STEP_MAKING)
        and one.place.folder in document.folders
    }
    moved: list[Moved] = []
    listed: dict[str, tuple[str, ...]] = {}
    on_account = [one for one in todo if not one.target.new or one.target.key in ours]
    if on_account:
        found = catalogue.resolve(cfg)
        for one in on_account:
            account_id = one.target.account_id or ours[one.target.key]
            try:
                # READ AS THE PLAN READ IT (R-1264), with its unpaged read beside (U226).
                listing = intake_cli.list_playlist_readable(found, account_id, current=True)
            except CratekitError as exc:
                if exc.cause.reason not in BROUGHT_REASONS:
                    raise
                moved.append(
                    Moved(
                        ACCOUNT_SIDE,
                        account_id,
                        one.name,
                        f"could not be listed ({exc.cause.message})",
                    )
                )
                continue
            if listing.window == provider_listing.WINDOW_LAGS:
                # U226. Neither read is the playlist as it stands: read as moved.
                moved.append(
                    Moved(
                        ACCOUNT_SIDE,
                        account_id,
                        one.name,
                        "reads one way through its pages and another through the "
                        "provider's unpaged read, so it may lag a recent change",
                    )
                )
                continue
            now = pair_merge.distinct(listing.tracks)
            withheld = listing.short.block() if listing.short is not None else None
            # AS A SET (R-1264): where an unread track sits decides nothing the merge did.
            unread_moved = set(listing.unread) != {named.remote_id for named in one.unread}
            #: R-1264. Said when only the tracks it cannot read moved.
            unread_said = "lists a different set of tracks it cannot read than the plan read"
            if one.target.new or of(one).has(STEP_ACCOUNT):
                # U210. PART WRITTEN BY THIS RUN: only its own write's doing.
                why = _beyond(one, now, ordering=_ordered_by_this_run(one, of(one)))
                if why:
                    moved.append(Moved(ACCOUNT_SIDE, account_id, one.name, why))
                elif not one.target.new and withheld != one.withheld:
                    moved.append(
                        Moved(
                            ACCOUNT_SIDE,
                            account_id,
                            one.name,
                            "withholds a different number of tracks than the plan read",
                        )
                    )
                elif unread_moved:
                    moved.append(Moved(ACCOUNT_SIDE, account_id, one.name, unread_said))
                else:
                    # U220. The listing a refused order is checked against (R-1264).
                    listed[account_id] = tuple(listing.order)
            elif now != tuple(one.account_now):
                moved.append(
                    Moved(ACCOUNT_SIDE, account_id, one.name, _differs(one.account_now, now))
                )
            elif withheld != one.withheld:
                moved.append(
                    Moved(
                        ACCOUNT_SIDE,
                        account_id,
                        one.name,
                        "withholds a different number of tracks than the plan read",
                    )
                )
            elif unread_moved:
                moved.append(Moved(ACCOUNT_SIDE, account_id, one.name, unread_said))
            else:
                # EVERY ID IN ITS PLACE (R-1264), the snapshot a pair with nothing to write keeps.
                listed[account_id] = tuple(listing.order)
    brought = [one for one in todo if one.target.rekordbox_new and one.home is not None]
    folders = document.folders
    made = [
        one
        for one in todo
        if one.target.new and one.place is not None and one.target.key not in ours
    ]
    if brought:
        from cratekit.modules.outbound import account as outbound_account

        remote = outbound_account.resolve(cfg)
        seen: dict[str, dict[str, str]] = {}
        for one in brought:
            recorded = folders.get(one.target.folder)
            listing: dict[str, str] = {}
            if recorded is not None:
                if recorded.folder_id not in seen:
                    seen[recorded.folder_id] = dict(remote.folder_playlists(recorded.folder_id))
                listing = seen[recorded.folder_id]
            if listing.get(one.target.account_id) != one.target.title:
                # TAKEN OUT OF THE SYNCED FOLDER OR RETITLED since the plan.
                moved.append(
                    Moved(
                        ACCOUNT_SIDE,
                        one.target.account_id,
                        one.name,
                        f"is no longer titled {one.target.title!r} in the account folder "
                        f"{one.target.folder!r}",
                    )
                )
    # U210. A JOB THIS RUN QUEUED is its own, never another sync's.
    asking = [one for one in todo if one.acquire and not of(one).has(STEP_QUEUED)]
    if asking:
        # R-1385. EVERY PAIR'S JOBS, since a plan made now would name a track
        # any of them holds as awaiting.
        now = {
            str(item)
            for job in pair_jobs(cfg, store)
            for item in (job.payload or {}).get(intake_cli.TRACKS) or {}
        }
        for one in asking:
            owner = one.target.account_id
            again = sorted(set(one.acquire) & now)
            if again:
                # ANOTHER SYNC QUEUED THEM SINCE THE PLAN; never queued twice.
                moved.append(
                    Moved(
                        "library",
                        owner,
                        one.name,
                        f"include {len(again)} track(s) another sync queued since the plan",
                    )
                )
    if made:
        from cratekit.modules.outbound import account as outbound_account

        remote = outbound_account.resolve(cfg)
        root: dict[str, str] | None = None
        inside: dict[str, dict[str, str]] = {}
        for one in made:
            place = one.place
            assert place is not None
            # U210. A FOLDER THIS RUN MADE for an earlier pair counts as found.
            folder_id = place.folder_id or our_folders.get(place.folder, "")
            if folder_id:
                if root is None:
                    root = dict(remote.folders())
                if folder_id not in root:
                    moved.append(
                        Moved(
                            "account-folder",
                            folder_id,
                            place.folder,
                            "is no longer a root folder on the account",
                        )
                    )
                    continue
                if folder_id not in inside:
                    inside[folder_id] = dict(remote.folder_playlists(folder_id))
                if place.title in inside[folder_id].values():
                    moved.append(
                        Moved(
                            "account-folder",
                            folder_id,
                            place.folder,
                            f"now holds a playlist titled {place.title!r}",
                        )
                    )
            elif place.action == FOLDER_CREATE:
                if root is None:
                    root = dict(remote.folders())
                if place.folder in root.values():
                    moved.append(
                        Moved(
                            "account-folder",
                            "",
                            place.folder,
                            "is now a root folder on the account, which the plan was to make",
                        )
                    )
    from cratekit.core import active_taxonomy, tree_registry
    from cratekit.favorites import placement
    from cratekit.sync import pair_discover, pair_reverse

    taxonomy = active_taxonomy.load(cfg)
    favorites = placement.source_name(taxonomy)
    skip = cfg.outbound.pair_skip_folders
    tops = generated_tops(taxonomy, tree_registry.read(cfg))
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        discovered: dict[str, Any] = {}
        if any(one.place is not None for one in planned.pairs):
            made_here = set(ours.values())
            discovered = {
                found.rekordbox_id: found
                for found in pair_discover.discover(
                    db,
                    tops=tops,
                    favorites=favorites,
                    skip=skip,
                    # U210. NOT THE PAIRS THIS RUN MADE, found unpaired by the plan.
                    paired=(
                        pair.rekordbox_id
                        for pair in document.pairs.values()
                        if pair.account_id not in made_here
                    ),
                    released=document.released.rekordbox,
                ).found
            }
        for one in todo:
            landed = of(one).get(STEP_REKORDBOX)
            landed = landed if isinstance(landed, dict) and landed.get("playlist_id") else None
            if landed is not None:
                # U210. A COMMIT THIS RUN LANDED is read against what it left.
                _landed_moved(db, one, landed, moved)
                continue
            if one.target.rekordbox_new:
                # U202. THE HOME IT IS MADE AT, read now so a change stops the
                # sync before any pair is written.
                try:
                    pair_reverse.recheck(db, one.home, one.change.order)
                except CratekitError as exc:
                    if exc.cause.reason != "decision-stale":
                        raise
                    moved.append(Moved(HOME_SIDE, "", one.home.where, _reworded(exc.cause.message)))
                    continue
                now = pair_discover.home_of(
                    db, one.target.folder, one.target.title, tops=tops, favorites=favorites, skip=skip
                )
                if now != one.home:
                    moved.append(
                        Moved(
                            HOME_SIDE,
                            "",
                            one.home.where,
                            "its place moved since the plan"
                            + (f" ({now})" if isinstance(now, str) else f", it now goes at {now.where!r}"),
                        )
                    )
                continue
            there = playlist_pair.read_playlist(db, one.target.rekordbox_id)
            if there is None or there.removed or not there.plain:
                moved.append(
                    Moved(
                        REKORDBOX_SIDE,
                        one.target.rekordbox_id,
                        one.rekordbox_name,
                        "is no longer a live plain playlist",
                    )
                )
                continue
            if there.memberships() != tuple(tuple(row) for row in one.rekordbox_before):
                moved.append(
                    Moved(
                        REKORDBOX_SIDE,
                        one.target.rekordbox_id,
                        one.rekordbox_name,
                        _differs(
                            [content for content, _row in one.rekordbox_before],
                            [content for content, _row in there.memberships()],
                            rows=True,
                        ),
                    )
                )
                continue
            if one.place is not None:
                # A DISCOVERED PLAYLIST IS READ AS DISCOVERY READS IT NOW, still
                # found under the same account folder and title.
                now_found = discovered.get(one.target.rekordbox_id)
                if now_found is None or (now_found.folder, now_found.title) != (
                    one.place.folder,
                    one.place.title,
                ):
                    moved.append(
                        Moved(
                            REKORDBOX_SIDE,
                            one.target.rekordbox_id,
                            one.rekordbox_name,
                            "was moved since the plan, and "
                            + (
                                f"would now be made as {now_found.title!r} in "
                                f"{now_found.folder!r}"
                                if now_found is not None
                                else "is no longer one a sync of every pair would make"
                            ),
                        )
                    )
                    continue
            held = document.pairs.get(one.target.account_id)
            if held is not None and held.made:
                # A PLAYLIST THE PRODUCT PAIRS BY ITSELF IS KEPT ONLY WHERE
                # DISCOVERY WOULD FIND IT (U198); one moved away since is never written.
                why = pair_discover.left_behind(db, there, favorites=favorites, skip=skip)
                if why:
                    moved.append(
                        Moved(
                            REKORDBOX_SIDE,
                            one.target.rekordbox_id,
                            one.rekordbox_name,
                            f"was moved since the plan and is now {why}",
                        )
                    )
                    continue
            gone = sorted(set(one.change.adds) - set(playlist_pair.content(db, one.change.adds)))
            if gone:
                moved.append(
                    Moved(
                        REKORDBOX_SIDE,
                        one.target.rekordbox_id,
                        one.rekordbox_name,
                        f"would gain {len(gone)} row(s) that are no longer live rows of the "
                        f"collection",
                    )
                )
        for lost in planned.unpaired:
            if lost.gone != REKORDBOX_SIDE:
                continue
            # A MADE PAIR LET GO FOR ITS REKORDBOX SIDE is let go only while
            # that side is still gone or still where no pair is kept.
            there = playlist_pair.read_playlist(db, lost.rekordbox_id)
            if there is None or there.removed or not there.plain:
                continue
            if not pair_discover.left_behind(db, there, favorites=favorites, skip=skip):
                moved.append(
                    Moved(
                        REKORDBOX_SIDE,
                        lost.rekordbox_id,
                        lost.rekordbox_name or there.name,
                        "is back where its pair is kept since the plan, which unpaired it",
                    )
                )
    finally:
        rb_writer.close_db(db)
    if moved:
        raise refuse(
            "decision-stale",
            f"{len(moved)} list(s) moved since the plan the gates showed, so nothing "
            f"{'more ' if begun else ''}was written: "
            + "; ".join(one.said() for one in moved)
            # U210. Unreadable steps are why every list was read as the plan read it.
            + (f"; {unread}, so every list was read as the plan read it" if unread else ""),
            steps=(
                "run crate sync pair again and answer both gates over the plan it shows now",
            ),
            origin=_ORIGIN,
            detail={"moved": [one.shown() for one in moved]},
        )
    return listed



def _landed_moved(db: Any, one: PairPlan, landed: Mapping[str, Any], moved: list[Moved]) -> None:
    """Read a rekordbox playlist this run's commit landed against what it left (U210)."""
    from cratekit.modules.outbound.pairs import REKORDBOX_SIDE
    playlist_id = str(landed["playlist_id"])
    there = playlist_pair.read_playlist(db, playlist_id)
    expected = tuple(tuple(row) for row in landed.get("rows") or ())
    if there is None or there.removed or not there.plain:
        moved.append(
            Moved(REKORDBOX_SIDE, playlist_id, one.rekordbox_name, "is no longer a live plain playlist")
        )
    elif there.memberships() != expected:
        said = _differs(
            [content for content, _row in expected],
            [content for content, _row in there.memberships()],
            rows=True,
        )
        moved.append(
            Moved(
                REKORDBOX_SIDE,
                playlist_id,
                one.rekordbox_name,
                said.replace("since the plan", "since this run wrote it"),
            )
        )



def _ordered_by_this_run(one: PairPlan, steps: PairSteps) -> bool:
    """Whether a part written pair's account order can be this run's own doing, so the check leaves it unread.

    U210. Once moves were sent its order is theirs. R-1420. AN ORDER WHOSE
    MOVES NEVER BEGAN (no ``moving`` step) moved nothing, so it is judged,
    and a person's reorder before a continue refuses rather than being
    written over. A FINISH OF A STOPPED ORDER is held at the adapter instead
    (R-1411), since the check's listing can lag the earlier moves.
    """
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)



def _beyond(one: PairPlan, now: Sequence[str], *, ordering: bool = False) -> str:
    """What an account playlist part written by this run holds beyond its own write, or ``""``.

    U210. Only the plan's tracks less its removals, plus its additions, may
    be there. Until ``ordering``, the order is read too, the plan's order then
    the additions, so a person's reorder refuses rather than being written over.
    """
    before = set(one.account_now)
    held = set(now)
    added = set(one.account_adds) - before
    gained = held - before - added
    lost = (before - set(one.account_removes)) - held
    parts = []
    if gained:
        parts.append(f"holds {len(gained)} track(s) this run neither read nor added")
    if lost:
        parts.append(f"lost {len(lost)} track(s) this run was not taking off")
    if not parts and not ordering:
        kept = [track for track in now if track not in added]
        tail = [track for track in now if track in added]
        if kept != [track for track in one.account_now if track in held] or (
            list(now) != kept + tail
        ):
            parts.append("was reordered")
    return " and ".join(parts) + (" since the plan" if parts else "")



def _reworded(message: str) -> str:
    """A recheck's refusal as a line of the check's own, without its closing advice."""
    head = message.split("; sync the pairs again", 1)[0]
    return head.replace(", so nothing was made", "")



def _differs(before: Sequence[str], now: Sequence[str], *, rows: bool = False) -> str:
    """How a list moved, in words: what it gained, what it lost, or that it was reordered."""
    gained = len(set(now) - set(before))
    lost = len(set(before) - set(now))
    parts = []
    if gained:
        parts.append(f"gained {gained} track(s)")
    if lost:
        parts.append(f"lost {lost} track(s)")
    if parts:
        return "has " + " and ".join(parts) + " since the plan"
    if list(before) != list(now):
        return "was reordered since the plan"
    return (
        "holds the same tracks in other membership rows than the plan read"
        if rows
        else "changed since the plan"
    )



def _with_calls(data: Mapping[str, Any], calls: Mapping[str, int]) -> dict[str, Any]:
    """The plan payload with each phase's provider calls in its totals, since ``plan/1`` is closed."""
    return {**data, "totals": {**data["totals"], "calls": dict(calls)}}



def _calls_said(calls: Mapping[str, int], *, held: bool) -> str:
    plan = f"{calls['plan']} to plan" + (" (in the command that planned)" if held else "")
    return (
        f"provider calls: {plan}, {calls['check']} to check the lists before writing, "
        f"{calls['write']} to write"
    )



def _steps_of(steps: Any, one: PairPlan) -> PairSteps:
    return PairSteps(steps, one.target.key)
