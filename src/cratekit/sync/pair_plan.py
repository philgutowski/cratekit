"""One pair planned: both sides read, matched, merged against the last sync and decided (U130, U304)."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from datetime import timedelta
from typing import Any

from cratekit.acquire import listing as provider_listing
from cratekit.acquire import match
from cratekit.cli.output import timestamp
from cratekit.core import config
from cratekit.core.cause import refuse
from cratekit.intake import cli as intake_cli
from cratekit.sync import pair_merge, pair_model, pair_read, pair_stopped
from cratekit.sync.pair_model import (
    _ORIGIN,
    NO_ISRC,
    NO_MATCH,
    ORDER_FOLDER,
    QUEUED_HERE,
    SETTLING,
    Named,
    PairPlan,
    Target,
    _lagging,
    _scope_account,
    _scope_rekordbox,
    _settling,
    remote_key,
    remote_of,
    row_key,
)
from cratekit.sync.pair_read import _mirror_isrcs, _owned_by_jobs, _Reader
from cratekit.write import playlist_pair


def plan_pair(reader: _Reader, target: Target, held, *, home: Any = None) -> PairPlan:
    """Read both sides of one pair, match them, merge them, and say what to write.

    ``home`` is where a new rekordbox side is made (U202).
    """
    from cratekit.favorites import placeholders
    cfg = reader.cfg
    if target.new:
        # U198. The account side is made by this sync, so it holds nothing yet.
        name = target.title
    else:
        name = _scope_account(
            target.account_id, reader.listed, reader.label_owned, reader.set_built, reader.mirrored
        )
    if target.rekordbox_new:
        # U202. The rekordbox side is made by this sync, so it holds nothing yet.
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
    #: R-1264. Unreadable account tracks by id, and every listed id once, in order.
    unread: Mapping[str, Any] = {}
    listed_order: tuple[str, ...] = ()
    if target.new:
        tracks: Mapping[str, Any] = {}
        short = None
    else:
        # R-1264. A track with no title or artist is kept unread by its id, so
        # it never refuses the whole listing.
        # U226. The windowed read may serve an order minutes old, so the pair is
        # held when neither it nor the unpaged read can be trusted.
        listing = intake_cli.list_playlist_readable(
            reader.found, target.account_id, current=True
        )
        if listing.window == provider_listing.WINDOW_LAGS:
            raise _lagging(target.account_id, name)
        tracks, short, dates, unread, listed_order = (
            listing.tracks,
            listing.short,
            listing.dates,
            listing.unread,
            listing.order,
        )
    account_now = pair_merge.distinct(tracks)

    # ── the links, kept only while their rows are live ──────────────────────
    recorded = dict(held.links) if held is not None else {}
    live = playlist_pair.content(reader.db, recorded.values())
    links = {remote: row for remote, row in recorded.items() if row in live}
    made: dict[str, str] = {}

    # ── rekordbox now, as keys ──────────────────────────────────────────────
    template = None
    # ONE ROW, ONE KEY (U208). Every release linked to a row is read as the
    # lowest numbered one's key, so the merge sees one track on each side and
    # a removal on either side takes every release of it.
    by_row: dict[str, str] = {}
    for remote, row in links.items():
        if row not in by_row or _lower(remote, by_row[row]):
            by_row[row] = remote
    seen_remote: dict[str, str] = {}
    rekordbox_keys: list[str] = []
    names: dict[str, Named] = {}
    content_of: dict[str, str] = {}
    unmatched: list[Named] = []
    tied: list[Named] = []
    #: Each unlinked row's ISRC as it was asked under, read once.
    asked_under: dict[str, str] = {}
    rows = playlist_pair.by_content(rekordbox.rows)
    # THE ACCOUNT PLAYLIST'S OWN TRACKS FIRST, by ISRC: asking the provider
    # could name another release, which the account would gain beside the first.
    on_account: dict[str, list[str]] = {}
    for remote_id in account_now:
        code = match.isrc_token(tracks[remote_id].get("isrc"))
        if code:
            on_account.setdefault(code, []).append(remote_id)
    # R-1264. An unread track is still on the account, so a row is matched to it.
    for remote_id, one in unread.items():
        code = match.isrc_token(one.isrc)
        if code:
            on_account.setdefault(code, []).append(remote_id)
    linked = set(links)
    # U207. Each unlinked row's code and album, read once up front, so the
    # codes to ask are screened in batches before any is asked.
    identities: dict[str, tuple[str, str]] = {}
    for row in rows.values():
        if by_row.get(row.content_id, ""):
            continue
        code = match.isrc_token(row.isrc)
        album = ""
        if not code:
            code, album = pair_read.file_identity(cfg, row.path)
        identities[row.content_id] = (code, album)

    def held_on_account(code: str) -> list[str]:
        return [one for one in on_account.get(code, ()) if one not in linked]

    asked = [
        code
        for content_id, (code, _album) in identities.items()
        if code
        and not held_on_account(code)
        and _remembered_miss(reader, content_id, code) is None
    ]
    if asked:
        reader.remote.screen_isrcs(asked)
    for row in rows.values():
        remote_id = by_row.get(row.content_id, "")
        reason = ""
        broke = False
        if not remote_id:
            from cratekit.core import naming
            from cratekit.modules.outbound import source

            if template is None:
                template = source.name_template(cfg)
            isrc, album = identities[row.content_id]
            asked_under[row.content_id] = isrc
            held_there = held_on_account(isrc)
            if isrc and len(held_there) == 1:
                remote_id = held_there[0]
            elif isrc and held_there:
                # U208. Several releases on the account already: the lowest
                # numbered, never a new one the provider names.
                remote_id = min(held_there, key=_order_of)
                broke = True
            elif not isrc:
                reason = NO_ISRC
            else:
                remote_id, reason, broke = _ask(
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
        elif broke:
            tied.append(names[key])
    known = {**links, **made}
    canon = {**by_row, **{row: remote for remote, row in made.items()}}
    # FROZEN HERE, BEFORE THE MERGE (U208): the library lookup below adds to
    # ``known``, and keys read from it then would not be the merge's keys.
    aliased = {
        remote_id: remote_key(canon[row])
        for remote_id, row in known.items()
        if row in canon and canon[row] != remote_id
    }

    def alias(remote_id: str) -> str:
        """The key an account track is read as: its row's one key when linked."""
        return aliased.get(remote_id) or remote_key(remote_id)

    # ── the account now, as keys ────────────────────────────────────────────
    readable_keys = {alias(remote_id) for remote_id in account_now}
    # R-1264. Each key at its first release's place, an unread release
    # included, as the base places it, so nobody's edit reads as a reorder.
    account_keys = list(
        pair_merge.distinct(
            alias(remote_id)
            for remote_id in (listed_order or account_now)
            if alias(remote_id) in readable_keys
        )
    )
    # R-1264. An unread track is never read as taken off the account, nor
    # offered to it, since the account already lists it.
    unread_keys = {alias(remote_id) for remote_id in unread} - readable_keys
    siblings: dict[str, Named] = {}
    for remote_id in account_now:
        key = alias(remote_id)
        said = tracks[remote_id]
        shown = Named(
            key=key,
            artist=str(said.get("artist") or ""),
            title=str(said.get("title") or ""),
            remote_id=remote_id,
            content_id=known.get(remote_id, ""),
        )
        if key != remote_key(remote_id):
            siblings[remote_id] = shown
        if key not in names:
            names[key] = shown

    # ── the bases ───────────────────────────────────────────────────────────
    base: pair_merge.Base | None = None
    readded: set[str] = set()
    unseen: set[str] = set()
    # U202. Each side's moments, used only where a base exists. A row held
    # as two releases was added when the later was.
    account_added: dict[str, Any] = {}
    for remote_id, said in dates.items():
        moment = placeholders.parse_hearted(said)
        key = alias(remote_id)
        if moment is not None and (key not in account_added or moment > account_added[key]):
            account_added[key] = moment
    account_readded: set[str] = set()
    rekordbox_added: dict[str, Any] = {}
    rekordbox_removed: dict[str, Any] = {}
    # U225. A write on this pair that stopped part way through its order never
    # recorded its links, so a row it linked still reads as that account track.
    stopped_write = reader.stopped_write(target.account_id, held)
    # R-1376. A first sync reads the stop on its account playlist too, else the
    # stopped write's scramble would lead and go into rekordbox. Its order is
    # finished below; nothing is folded into a base.
    first_sync = held is None or held.first
    if stopped_write is None and first_sync:
        stopped_write = reader.first_stop(target.account_id)
    if stopped_write is not None and stopped_write.pending:
        # U231. An order sent with no read back is pending, so this raises to
        # hold the pair while no reading can be trusted (a first sync too, R-1376).
        _pending(reader, target, held, name, stopped_write, tuple(listed_order or account_now))
    stopped_links = (
        {row: remote for remote, row in stopped_write.links.items()}
        if stopped_write is not None
        else {}
    )

    def as_key(content_id: str) -> str:
        remote_id = canon.get(content_id, "")
        if not remote_id and content_id in stopped_links:
            return alias(stopped_links[content_id])
        return remote_key(remote_id) if remote_id else row_key(content_id)

    # U225. When the stopped write committed rekordbox too, the bases are what
    # it left; otherwise neither moves (both or neither). A first sync has no
    # base, so nothing is folded (R-1376), and
    # the gate never names a fold that was not made.
    folded = stopped_write is not None and stopped_write.written and not first_sync
    if not first_sync:
        started = set(stopped_write.start) if folded else set()
        base_account = pair_merge.distinct(
            alias(one)
            for one in (
                # Its order narrowed to what landed, so a track that never
                # landed is not read as taken off since.
                [
                    held_id
                    for held_id in pair_merge.placed(stopped_write.target, stopped_write.start)
                    if held_id in started
                ]
                if folded
                else held.account or ()
            )
        )
        if short is not None:
            # A WITHHELD TRACK IS NOT A REMOVED ONE. Which tracks were left out
            # is not known, so none is read as gone nor offered as an addition.
            served = set(account_keys)
            unseen = {key for key in base_account if key not in served}
            base_account = tuple(key for key in base_account if key not in unseen)
        if unread_keys:
            unseen |= {key for key in base_account if key in unread_keys}
            base_account = tuple(key for key in base_account if key not in unread_keys)
        # A RE-ADD IS A TRACK NONE OF WHOSE BASE MEMBERSHIPS SURVIVES, so a
        # track held twice that lost one copy was not taken out and put back.
        from cratekit.modules.outbound import pairs as _pairs

        base_members = (
            tuple(_pairs.Membership(content_id, row_id) for content_id, row_id in stopped_write.rekordbox)
            if folded
            else tuple(held.rekordbox or ())
        )
        base_rows: dict[str, set[str]] = {}
        for member in base_members:
            base_rows.setdefault(member.content_id, set()).add(member.row_id)
        current_rows: dict[str, set[str]] = {}
        for row in rekordbox.rows:
            current_rows.setdefault(row.content_id, set()).add(row.row_id)
        base_rekordbox = tuple(as_key(member.content_id) for member in base_members)
        readded = {
            as_key(content_id)
            for content_id, row_ids in current_rows.items()
            if content_id in base_rows and not (row_ids & base_rows[content_id])
        }
        # A folded base dates from when the stopped write began.
        synced = stopped_write.at if folded else placeholders.parse_hearted(held.synced)
        # R-990. Re-added on the account: dated later than both the base's own
        # date for it and the base's sync. One the base never dated is not.
        if synced is not None:
            for remote_id in account_now:
                key = alias(remote_id)
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
        # REKORDBOX'S MOMENTS: a live row's ``created_at`` is its add, a base
        # row marked removed carries its removal in ``updated_at``. A row gone
        # outright, or under a track the collection lost, says no moment.
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

    # U225. The account's order is read as the stopped write's target, each
    # side's change of order against what the write left.
    # U234. Also when it stands off the moves' path, unless settled readings
    # after the stop show the person moved it: an off path order alone may be
    # the provider's partial state.
    stopped: pair_merge.Stopped | None = None
    off_path = False
    reordered_since_stop = False
    moved_nothing = False
    unread_moved = False
    moved_unread: frozenset[str] = frozenset()
    unread_unsent = False
    if stopped_write is not None:
        reading = tuple(listed_order or account_now)
        off_path = not pair_stopped.reached(
            stopped_write.start, _toward(stopped_write), reading
        )
        # A write that sent no move left no partial state, so an order off its
        # path is a person's (R-1420).
        moved_nothing = off_path and stopped_write.sent_nothing
        reordered_since_stop = moved_nothing or _moved_since_stop(
            reader, target, name, held, stopped_write, reading, off_path=off_path, unread=unread
        )
        # R-1446. A MOVE OF UNREAD TRACKS ALONE IS NO REORDER: the merge reads
        # no unread track, so the stopped write is still finished, else its half
        # done order would go into rekordbox. A moved unread track keeps its place.
        kept_after = _kept_after(held, stopped_write)
        if (
            reordered_since_stop
            and unread
            and not _readable_moved(
                stopped_write, kept_after, reading, unread, moved_nothing=moved_nothing
            )
        ):
            # Only the moved unread tracks keep their place.
            moved_unread = _unread_moved(
                stopped_write, kept_after, reading, unread, moved_nothing=moved_nothing
            )
            unread_unsent = moved_nothing
            reordered_since_stop = False
            moved_nothing = False
            unread_moved = True
    if stopped_write is not None and not reordered_since_stop:
        holding = set(account_keys)
        finishing_keys = pair_merge.distinct(
            alias(one) for one in stopped_write.target if alias(one) in holding
        )
        # As the write would have left it had it finished, a track added since
        # staying where it stood.
        account_keys = list(
            pair_merge.distinct(
                alias(one)
                for one in pair_stopped.finished(
                    listed_order or account_now, stopped_write.target
                )
                if alias(one) in holding
            )
        )
        stopped = pair_merge.Stopped(
            account=finishing_keys,
            rekordbox=tuple(
                as_key(content_id) for content_id, _row in stopped_write.rekordbox
            ),
            leader=stopped_write.leader,
        )
    # U231, R-1416. Read once, before the merge, so the merge and the account
    # write agree; a first sync whose order is not kept is led by rekordbox.
    order_kept = _keeps_order(cfg, rekordbox, home)
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
        stopped=stopped,
        order_kept=order_kept,
    )

    # ── what rekordbox is asked: adds need a live row, never a row without a file
    rekordbox_held = set(rekordbox_keys) - set(merged.remove_rekordbox)
    adds: list[str] = []
    acquire: dict[str, dict[str, Any]] = {}
    awaiting: list[Named] = []
    on_hold: list[Named] = []
    landing_unread: list[Named] = []
    ambiguous: list[Named] = []
    lacking = [
        remote_of(key) for key in merged.add_rekordbox if remote_of(key) not in known
    ]
    def here() -> dict[str, tuple[str, ...]]:
        """ISRC to this playlist's own rows, from the database or else the row's file."""
        codes: dict[str, list[str]] = {}
        for row in rows.values():
            code = asked_under.get(row.content_id)
            if code is None:
                code = match.isrc_token(row.isrc) or pair_read.file_identity(cfg, row.path)[0]
            if code:
                codes.setdefault(code, []).append(row.content_id)
        return {code: tuple(ids) for code, ids in codes.items()}

    found_rows = _owned(reader, target.account_id, tracks, lacking, here=here)
    # Live and staying: a second membership would be the same track twice.
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
        elif held_for_choice(held, remote_id, dates):
            # U221. A twin's missing track waits for the author's choice until
            # ``sync release``; asked before another pair's job (R-1385).
            on_hold.append(names[key])
        elif (
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]
        ):
            # R-1383. AN UNREADABLE LANDING RECORD IS NEVER NO LANDING: it may
            # have brought this track in, found by ISRC, so the track waits.
            landing_unread.append(names[key])
        elif why := _queued_elsewhere(reader, target, remote_id):
            # R-1385. ONE DOWNLOAD FOR THE LIBRARY, whichever pairs list it.
            awaiting.append(_with_reason(names[key], why))
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
        remote_of(key)
        for key in merged.add_account
        if remote_of(key) and key not in unseen and key not in unread_keys
    )
    account_removes: tuple[str, ...] = ()
    account_order: tuple[str, ...] | None = None
    account_before: tuple[str, ...] = ()
    order_unkept = False
    if short is None:
        # U208. Every release of a removed track goes.
        account_removes = tuple(
            dict.fromkeys(
                one
                for key in merged.remove_account
                for one in (
                    [held for held in account_now if alias(held) == key] or [remote_of(key)]
                )
            )
        )
        # R-1264. Every listed id, unread ones included, so the order is whole.
        after = pair_merge.appended(listed_order or account_now, account_removes, account_adds)
        firsts = pair_merge.distinct(
            alias(one) for one in after if alias(one) not in unread_keys
        )
        wanted_keys = pair_merge.as_held(merged.order, set(firsts))
        # U231. Only a pair that keeps the account's order has it written.
        order_unkept = wanted_keys != firsts and not order_kept
        if wanted_keys != firsts and not order_unkept:
            # A row's releases move together. R-1432: a finish places an unread
            # track where the stopped write was taking it. R-1446: except one
            # the person moved, and when none can be told apart, all keep place.
            account_order = _with_unread_placed(
                [one for key in wanted_keys for one in after if alias(one) == key],
                after,
                (
                    stopped_write.target
                    if not unread_moved
                    else tuple(one for one in stopped_write.target if one not in moved_unread)
                    if moved_unread
                    else ()
                )
                if stopped is not None and stopped_write is not None
                else (),
            )
            account_before = tuple(listed_order or account_now)

    for remote_id in acquire:
        reader.asked.setdefault(remote_id, (target.key, name))
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
        on_hold=tuple(on_hold),
        landing_unread=tuple(landing_unread),
        ambiguous=tuple(ambiguous),
        tied=tuple(tied),
        siblings=siblings,
        links=made,
        names=names,
        content_of=content_of,
        withheld=short.block() if short is not None else None,
        unread=tuple(
            Named(
                key=alias(remote_id),
                artist=one.artist,
                title=one.title,
                remote_id=remote_id,
                content_id=known.get(remote_id, ""),
                reason=one.why,
            )
            for remote_id, one in unread.items()
        ),
        home=home,
        account_dates=dict(dates),
        account_before=account_before,
        finishing=(
            stopped_write.run_id
            if (folded or stopped is not None or reordered_since_stop)
            else ""
        ),
        finishing_order=stopped is not None,
        finishing_off_path=stopped is not None and off_path,
        reordered_since_stop=reordered_since_stop,
        finishing_folded=folded,
        stop_moved_nothing=moved_nothing,
        stop_unread_moved=unread_moved,
        stop_unread_others=bool(moved_unread) and bool(set(unread) - moved_unread),
        stop_unread_unsent=unread_unsent,
        order_unkept=order_unkept,
    )



def _kept_after(held: Any, write: pair_stopped.StoppedWrite) -> Any:
    """The ``pairs.StopReading`` kept on this pair after ``write`` stopped, or None (U234).

    Only one kept for that run and read at or after its moves began counts.
    """
    from cratekit.favorites import placeholders
    kept = getattr(held, "stop_seen", None) if held is not None else None
    if kept is None or kept.run != write.run_id:
        return None
    seen_at = placeholders.parse_hearted(kept.at)
    began = write.moving_at or write.at
    if seen_at is None or seen_at < began:
        return None
    return kept



def _toward(write: pair_stopped.StoppedWrite) -> tuple[str, ...]:
    """Where the moves ``write`` sent could have taken the account (R-1434).

    A write that sent no move stands at its start, so any other order is a
    person's (R-1420); any other write is read along its path to its target.
    """
    return tuple(write.start) if write.sent_nothing else tuple(write.target)



def _readable_moved(
    write: pair_stopped.StoppedWrite,
    kept: Any,
    reading: Sequence[str],
    unread: Iterable[str],
    *,
    moved_nothing: bool,
) -> bool:
    """Whether the reorder read after ``write``'s stop moved a readable track (R-1446).

    ``unread`` ids are left out, since the merge reads none of them. Compared
    with the moves' path for a write that sent no move, else with the settled
    reading ``kept``; with none to compare, the reorder stands.
    """
    left_out = set(unread)
    readable = [one for one in reading if one not in left_out]
    if moved_nothing:
        return not pair_stopped.reached(write.start, _toward(write), readable)
    if kept is None or not kept.settled:
        return True
    return pair_stopped.reordered(
        [one for one in kept.order if one not in left_out], readable
    )



def _unread_moved(
    write: pair_stopped.StoppedWrite,
    kept: Any,
    reading: Sequence[str],
    unread: Iterable[str],
    *,
    moved_nothing: bool,
) -> frozenset[str]:
    """The unread ids the person moved since ``write``'s stop (R-1446).

    Compared with the settled reading ``kept``, or with the start for a write
    that sent no move, over the ids both hold. The unmoved ids are the
    heaviest common run, each readable id weighed above all unread ones
    together, so the readable tracks hold still and an unread id outside the
    run is moved. With nothing to compare, none is.
    """
    if moved_nothing:
        before: Sequence[str] = write.start
    elif kept is not None and kept.settled:
        before = kept.order
    else:
        return frozenset()
    common = set(before) & set(reading)
    left_out = set(unread)
    was = [one for one in dict.fromkeys(before) if one in common]
    now = [one for one in dict.fromkeys(reading) if one in common]
    place = {one: index for index, one in enumerate(was)}
    heavy = len(now) + 1
    # The heaviest chain through ``now`` rising in ``was``, via a Fenwick tree.
    tree: list[tuple[int, int]] = [(0, -1)] * (len(was) + 1)
    back: list[int] = []
    best: list[int] = []
    for index, one in enumerate(now):
        at, top = place[one], (0, -1)
        while at > 0:
            top = max(top, tree[at])
            at -= at & -at
        value = top[0] + (1 if one in left_out else heavy)
        best.append(value)
        back.append(top[1])
        at = place[one] + 1
        while at <= len(was):
            tree[at] = max(tree[at], (value, index))
            at += at & -at
    held: set[str] = set()
    step = max(range(len(now)), key=best.__getitem__, default=-1)
    while step >= 0:
        held.add(now[step])
        step = back[step]
    return frozenset(one for one in now if one in left_out and one not in held)



def _moved_since_stop(
    reader: _Reader,
    target: Target,
    name: str,
    held: Any,
    write: pair_stopped.StoppedWrite,
    reading: tuple[str, ...],
    *,
    off_path: bool,
    unread: Iterable[str] = (),
) -> bool:
    """Whether settled readings after ``write``'s stop show the person reordered the account (U234).

    ONE READING OFF THE MOVES' PATH SHOWS NOTHING, since it may be the
    provider's partial state or an older order it still serves. The first
    off path reading is kept and settles when one in the same order comes at
    least :data:`AGREE_AFTER` later; a reading on the path is finished and
    never kept, since it may lag the whole write. Once settled, an off path
    reading in another order is kept as the order after and holds the pair
    until a reading :data:`AGREE_AFTER` later agrees, and only then does the
    account lead. A pair with no record keeps nothing, so never leads.
    """
    from dataclasses import replace

    from cratekit.favorites import placeholders
    from cratekit.modules.outbound import pairs

    if held is None:
        return False
    kept = _kept_after(held, write)
    if not off_path:
        # ON THE PATH THE STOP IS FINISHED and nothing is kept, since it may
        # lag the whole write. It ends
        # any order held as the one after, so that order waits afresh.
        if kept is not None and kept.after is not None:
            reader.see_stop(target.account_id, replace(kept, after=None, after_at=""))
        return False
    stamp = timestamp()
    if kept is None:
        reader.see_stop(target.account_id, pairs.StopReading(write.run_id, reading, stamp))
        return False
    first = placeholders.parse_hearted(kept.at)
    if not kept.settled:
        if pair_stopped.reordered(kept.order, reading):
            reader.see_stop(target.account_id, pairs.StopReading(write.run_id, reading, stamp))
        elif first is not None and pair_model._now() - first >= AGREE_AFTER:
            reader.see_stop(target.account_id, replace(kept, settled=True))
        return False
    if not pair_stopped.reordered(kept.order, reading):
        # BACK AT THE SETTLED ORDER: the stop is finished, and an order held
        # as the one after waits afresh if it is read again.
        if kept.after is not None:
            reader.see_stop(target.account_id, replace(kept, after=None, after_at=""))
        return False
    since = placeholders.parse_hearted(kept.after_at) if kept.after is not None else None
    if (
        kept.after is not None
        and since is not None
        and not pair_stopped.reordered(kept.after, reading)
        and pair_model._now() - since >= AGREE_AFTER
    ):
        return True
    if kept.after is None or since is None or pair_stopped.reordered(kept.after, reading):
        reader.see_stop(target.account_id, replace(kept, after=reading, after_at=stamp))
    raise refuse(
        SETTLING,
        f"the account playlist {name or target.account_id}'s order changed since a sync "
        f"read it settled after run {write.run_id}'s write stopped part way through its "
        f"order, and the provider may still be serving an older order: the pair was not "
        f"synced this run, and nothing is written until a reading at least "
        f"{int(AGREE_AFTER.total_seconds() // 60)} minutes later agrees, when "
        + (
            # R-1434. Says what the plan then does (unread moves never lead).
            "each track the account lists with no title or no artist stays where you "
            "put it and the others are finished in the stopped order"
            if unread and not _readable_moved(write, kept, reading, unread, moved_nothing=False)
            else "the account's order is read as yours"
        ),
        steps=("sync the pair again in a few minutes",),
        origin=_ORIGIN,
        detail={
            "account_id": target.account_id,
            "run_id": write.run_id,
            "problem": "order-moved-since-stop",
        },
    )



def _pending(
    reader: _Reader,
    target: Target,
    held: Any,
    name: str,
    write: pair_stopped.StoppedWrite,
    now: tuple[str, ...],
) -> None:
    """Return when this plan may read a pending order's account as it stands, else hold the pair (U231).

    SHOWN AS THE MOVES LEAVE IT, the order has landed, since no lag can serve
    it before every move did.

    ANY OTHER READING MUST AGREE with one kept by an earlier run, taken after
    the moves were sent and at least :data:`AGREE_AFTER` before it, since the
    provider serves older orders for minutes. Until then the pair is held and
    the reading kept; an equal reading too soon keeps the older one.

    EXCEPT SHORT OF WHERE THE MOVES CAN HAVE LEFT IT (R-1394): an agreed
    reading on the path before ``write.sent`` moves may only be a lag, and
    moving from it would land the remaining moves on the wrong tracks. Held,
    and the reading not kept again.
    """
    from cratekit.favorites import placeholders
    if pair_stopped.shows(write.end, now):
        return
    assert write.moving_at is not None
    # R-1376. A first sync by hand has no record to keep a reading on, so it
    # is held until the account shows where the moves leave it.
    seen_at = (
        placeholders.parse_hearted(held.seen_at)
        if held is not None and held.seen is not None
        else None
    )
    kept = seen_at is not None and seen_at >= write.moving_at and tuple(held.seen) == now
    agreed = kept and pair_model._now() - seen_at >= AGREE_AFTER
    if agreed:
        at = pair_stopped.positions(write.start, write.target, now)
        if not at or max(at) >= write.sent:
            return
        raise _settling(target.account_id, name, write.run_id, lag=True, write=write, at=max(at))
    if not kept:
        reader.see(target.account_id, now)
    raise _settling(target.account_id, name, write.run_id, lag=False)



def _keeps_order(cfg: config.Config, rekordbox: playlist_pair.Playlist, home: Any) -> bool:
    """Whether this pair's account playlist is put in rekordbox's order (U231).

    Only under :data:`ORDER_FOLDER`, unless ``outbound.pair_order_every_pair``.
    """
    if cfg.outbound.pair_order_every_pair:
        return True
    if rekordbox.playlist_id:
        # UNDER THE FOLDER, never a root playlist of its name.
        return bool(rekordbox.ancestors) and rekordbox.top[1] == ORDER_FOLDER
    path = tuple(getattr(home, "path", ()) or ())
    return len(path) > 1 and path[0] == ORDER_FOLDER



def _with_unread_placed(
    ordered: list[str], listed: Sequence[str], target: Sequence[str] = ()
) -> tuple[str, ...]:
    """``ordered`` with every id of ``listed`` it lacks put back after its neighbour (R-1264).

    The merge cannot read an unread track, so it keeps its place behind the
    track listed before it, or the front, and the written order is whole.

    R-1432. At a finish, each unread id ``target`` names is placed first,
    behind the track ``target`` puts before it, since the listing is where
    interrupted moves left it. Other ids keep their listed place; an id the
    listing no longer holds is never put back.
    """
    placed = list(ordered)
    held = set(placed)

    def behind(before: Sequence[str]) -> int:
        for one in reversed(before):
            if one in held:
                return placed.index(one) + 1
        return 0

    holding = set(listed)
    for index, one in enumerate(target):
        if one in held or one not in holding:
            continue
        placed.insert(behind(target[:index]), one)
        held.add(one)
    for index, one in enumerate(listed):
        if one in held:
            continue
        placed.insert(behind(listed[:index]), one)
        held.add(one)
    return tuple(placed)



def _remembered_miss(reader: _Reader, content_id: str, isrc: str) -> Any:
    """The miss remembered for this row under this ISRC that a plan reuses, or None.

    Shared by :func:`_ask` and the screen (U207) so the two cannot drift. A
    tie remembered before U208 is asked again, since ``any_agreeing`` matches it.
    """
    from cratekit.modules.outbound.service import AGREEING_RELEASES

    held = reader.misses.get(content_id)
    if held is not None and held.isrc == isrc and AGREEING_RELEASES not in held.reason:
        return held
    return None



def _order_of(remote_id: str) -> tuple[int, str]:
    """A provider identifier's place, numbers by value, as a tie's ``_lowest`` orders them."""
    return (len(remote_id), remote_id)



def _lower(one: str, other: str) -> bool:
    return _order_of(one) < _order_of(other)



def _ask(
    reader: _Reader, row: Any, *, isrc: str, title: str, album: str
) -> tuple[str, str, bool]:
    """The account track for one unlinked row, or why there is none, and whether a tie chose it.

    U198. A miss is remembered with its ISRC and reused without a request
    until the ISRC changes. An unreadable candidate says nothing of the row,
    so it is never remembered.

    A TIE TAKES ONE RELEASE (U208): asked with ``any_agreeing``, a row whose
    ISRC names several agreeing releases matches the hearted one, else the
    lowest numbered after the album narrowed them, linked like any match.
    """
    from cratekit.modules.outbound.service import AGREEING_RELEASES, UNREADABLE_CANDIDATE

    held = reader.misses.get(row.content_id)
    reused = _remembered_miss(reader, row.content_id, isrc)
    if reused is not None:
        return "", reused.reason, False
    remote = reader.remote
    remote_id = str(
        remote.match_track(
            identity=row.content_id,
            isrc=isrc,
            title=title,
            artist=row.artist,
            album=album,
            any_agreeing=True,
        )
        or ""
    )
    if remote_id:
        if held is not None:
            reader.matched.add(row.content_id)
        return remote_id, "", bool(remote.tie_broken(row.content_id))
    reason = remote.unmatched_reason(row.content_id) or NO_MATCH
    # Never remembered: an unreadable release may agree tomorrow.
    if UNREADABLE_CANDIDATE not in reason and AGREEING_RELEASES not in reason:
        from cratekit.modules.outbound import pairs

        reader.fresh[row.content_id] = pairs.Miss(isrc, reason)
    return "", reason, False



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
    *,
    here: Callable[[], Mapping[str, tuple[str, ...]]] | None = None,
) -> dict[str, tuple[str, ...]]:
    """Each lacking account track's library rows: by ISRC, by an intake job, by its landing.

    This pair's own jobs and landings first, then every other pair's (U229).
    ``here`` is the pair's own rows by ISRC, a file's included, asked only for
    what the database names nowhere (U208): a second release of a tied row is
    that row, never a track to acquire.
    """
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
    rest = {remote_id for remote_id in lacking if remote_id not in found and codes.get(remote_id)}
    if rest and here is not None:
        own = here()
        for remote_id in rest:
            if own.get(codes[remote_id]):
                found[remote_id] = own[codes[remote_id]]
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
    # U229. WHAT ANOTHER ACCOUNT PLAYLIST BROUGHT IN IS STILL THE LIBRARY'S,
    # asked only for what this pair's own left lacking.
    rest = {remote_id for remote_id in lacking if remote_id not in found}
    if rest:
        mine = {job.job_id for job in reader.jobs_for(account_id)}
        others = tuple(job for job in reader.pair_jobs if job.job_id not in mine)
        for remote_id, content_id in _owned_by_jobs(reader, others, rest, own=False).items():
            found[remote_id] = (content_id,)
    rest = {remote_id for remote_id in lacking if remote_id not in found and codes.get(remote_id)}
    if rest:
        landed = reader.landed_anywhere
        for remote_id in rest:
            if landed.get(codes[remote_id]):
                found[remote_id] = landed[codes[remote_id]]
    return found



def held_for_choice(pair: Any, remote_id: str, dates: Mapping[str, str]) -> bool:
    """Whether an account track the library lacks waits for the author's choice (U221).

    Only a twin's pair holds: exactly its recorded tracks, or with none
    recorded, every track not dated after the mark. An undated track or an
    unreadable mark holds.
    """
    from cratekit.favorites import placeholders
    if pair is None or not getattr(pair, "twin", False):
        return False
    recorded = getattr(pair, "on_hold", None)
    if recorded is not None:
        return remote_id in recorded
    marked = placeholders.parse_hearted(getattr(pair, "marked", ""))
    added = placeholders.parse_hearted(dates.get(remote_id))
    if marked is None or added is None:
        return True
    return not added > marked



def _queued(reader: _Reader, account_id: str) -> frozenset[str]:
    """Every track an intake job this verb queued for the pair still holds or resolved."""
    return frozenset(
        remote_id
        for remote_id, held in reader.held_by_jobs.items()
        if any(source == account_id for source, _name in held)
    )



def _queued_elsewhere(reader: _Reader, target: Target, remote_id: str) -> str:
    """Why a track another pair's job or an earlier pair of this plan holds is awaited, or ``""``.

    R-1385. A track is downloaded once for the library, never queued twice.
    """
    for source, name in reader.held_by_jobs.get(remote_id, ()):
        if source != target.account_id:
            return f"queued for {name}"
    asked = reader.asked.get(remote_id)
    if asked is not None and asked[0] != target.key:
        return f"{QUEUED_HERE} {asked[1]}"
    return ""



#: U231. How far apart two readings must be to agree, since the provider serves
#: older orders for minutes after a change.
AGREE_AFTER = timedelta(minutes=5)
