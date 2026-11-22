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

    ``home`` is where the rekordbox side is made, for a pair whose rekordbox
    side is new (U202); that side then holds nothing yet.
    """
    from cratekit.favorites import placeholders
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
    #: R-1264. Account tracks the reader would not read, by id, and every id
    #: the account lists, each once at its first place, unread ones included.
    unread: Mapping[str, Any] = {}
    listed_order: tuple[str, ...] = ()
    if target.new:
        tracks: Mapping[str, Any] = {}
        short = None
    else:
        # ROW BY ROW, AS THE TWINS BACKFILL READS IT (R-1264): one track the
        # account lists with no title or no artist used to refuse the whole
        # listing, so the pair never synced again. It is unread now, kept by
        # its id, and every other track reads exactly as it did.
        # U226. THE UNPAGED READ BESIDE THE WINDOW, which may serve an order
        # minutes old: planned from the unpaged rows when they are the whole
        # playlist, and the pair held when neither read can be.
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
    # ONE ROW, ONE KEY, HOWEVER MANY RELEASES ARE LINKED TO IT (U208). A tie
    # links one release and a person may add another of the same recording on
    # the account, which the library lookup links to the same row. Every
    # release linked to a row is read as that row's one key, the lowest
    # numbered release's, so the merge sees one track on each side: a removal
    # on either side takes every release of it, and a release taken off the
    # account while another stays keeps the row.
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
    # THE ACCOUNT PLAYLIST'S OWN TRACKS FIRST, by ISRC, when exactly one of
    # them carries the row's code: the account already holds that recording,
    # and asking the provider would choose among its releases and could name
    # another one, which the account would then gain beside the first.
    on_account: dict[str, list[str]] = {}
    for remote_id in account_now:
        code = match.isrc_token(tracks[remote_id].get("isrc"))
        if code:
            on_account.setdefault(code, []).append(remote_id)
    # AN UNREAD TRACK IS STILL ON THE ACCOUNT (R-1264): a row carrying its code
    # is matched to it, never to another release the provider would name.
    for remote_id, one in unread.items():
        code = match.isrc_token(one.isrc)
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
                # SEVERAL RELEASES OF IT ON THE ACCOUNT ALREADY (U208): one of
                # those, the lowest numbered, and never a release the provider
                # names that the account does not hold, which would be a third.
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
    # FROZEN HERE, BEFORE THE MERGE, and never read from ``known`` again: the
    # library lookup below links more account tracks into ``known`` after the
    # merge has decided, and a removal or an order computed under those new
    # links would be in another key space than the one the merge decided in
    # (U208, the review's round two).
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
    # EACH KEY AT ITS FIRST RELEASE'S PLACE IN THE LISTING (R-1264, the
    # review's round two), an unread release included: a row whose first
    # release the account lists unreadably and a later one readably sits where
    # the base, which aliases every recorded id, places it, so nobody's edit
    # reads as a reorder. With nothing unread this is ``account_now``'s order.
    account_keys = list(
        pair_merge.distinct(
            alias(remote_id)
            for remote_id in (listed_order or account_now)
            if alias(remote_id) in readable_keys
        )
    )
    # R-1264. AN UNREAD TRACK IS A WITHHELD TRACK WHOSE ID IS KNOWN: never read
    # as taken off the account, so a row linked to it stays in rekordbox, and
    # never offered to the account, which already lists it.
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
    # U202. THE MOMENTS EACH SIDE CAN GIVE, read only where a base exists,
    # since a first sync adds only and decides nothing by time.
    # A row held as two releases was added on the account when the later was.
    account_added: dict[str, Any] = {}
    for remote_id, said in dates.items():
        moment = placeholders.parse_hearted(said)
        key = alias(remote_id)
        if moment is not None and (key not in account_added or moment > account_added[key]):
            account_added[key] = moment
    account_readded: set[str] = set()
    rekordbox_added: dict[str, Any] = {}
    rekordbox_removed: dict[str, Any] = {}
    # U225. A WRITE ON THIS PAIR STOPPED PART WAY THROUGH ITS ORDER since the
    # snapshot, and the rows its links name: it never reached the snapshot
    # that would have recorded them, so a row it linked and that is gone from
    # rekordbox since is still read as the account track it was.
    stopped_write = reader.stopped_write(target.account_id, held)
    # R-1376. A FIRST SYNC READS THE STOP ON ITS ACCOUNT PLAYLIST WHATEVER THE
    # MARK: a pair released after a stop and paired again, or marked and never
    # written whole, has no snapshot, so its account order, the stopped
    # write's scramble, would lead and be put into rekordbox. Its order is
    # finished below as any stop's is; nothing of it is folded into a base.
    first_sync = held is None or held.first
    if stopped_write is None and first_sync:
        stopped_write = reader.first_stop(target.account_id)
    if stopped_write is not None and stopped_write.pending:
        # U231. AN ORDER SENT WITH NO READ BACK is pending until it is read:
        # raises to hold the pair whole while no reading can be trusted. A
        # first sync's stop is held the same way (R-1376), after it is read.
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

    # U225. WHEN THE STOPPED WRITE COMMITTED REKORDBOX as well, both sides
    # hold what it wrote, so the bases are what it left, the snapshot it would
    # have recorded; when it did not, neither base moves (record both or
    # neither). A first sync has no base, so nothing is folded (R-1376), and
    # the gate never names a fold that was not made.
    folded = stopped_write is not None and stopped_write.written and not first_sync
    if not first_sync:
        started = set(stopped_write.start) if folded else set()
        base_account = pair_merge.distinct(
            alias(one)
            for one in (
                # THE ORDER IT ASKED, NARROWED TO WHAT ITS ADDITIONS AND
                # REMOVALS LEFT: a track it asked for that never landed is not
                # in its base, so it is never read as taken off since.
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
            # A WITHHELD TRACK IS NOT A REMOVED ONE. Which tracks the provider
            # left out is not known, so no track the base held is read as gone,
            # and none of them is offered to the account as an addition either:
            # it may be on the playlist, served to nobody.
            served = set(account_keys)
            unseen = {key for key in base_account if key not in served}
            base_account = tuple(key for key in base_account if key not in unseen)
        if unread_keys:
            unseen |= {key for key in base_account if key in unread_keys}
            base_account = tuple(key for key in base_account if key not in unread_keys)
        # A RE-ADD IS A TRACK NONE OF WHOSE BASE MEMBERSHIPS SURVIVES. A track
        # the playlist holds twice that lost one copy still holds the other,
        # which the base saw, so it was not taken out and put back.
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
        # A FOLDED BASE WAS TAKEN WHEN THE STOPPED WRITE BEGAN, so a moment
        # before that is no change since it.
        synced = stopped_write.at if folded else placeholders.parse_hearted(held.synced)
        # A TRACK TAKEN OUT AND PUT BACK ON THE ACCOUNT (R-990, closed by
        # U202): the base held it with one added date and the account dates it
        # later now, and later than the base's own sync, so the putting back
        # was done since. A track the base dated nowhere is never read so.
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

    # U225. THE ACCOUNT'S ORDER IS THE STOPPED WRITE'S when it stands where
    # that write's moves could have left it: the merge reads it in the order
    # the write was putting it in, each track added since after the track it
    # follows, and each side's change of order against what the write left.
    #
    # U234. AND WHEN IT STANDS WHERE NONE OF THOSE MOVES LEAVES IT, off their
    # path, unless readings kept after the stop show the person moved it:
    # Sitting 87 read accounts the stopped write's refused and misplaced moves
    # left off the path, the provider's partial state, and read alone as the
    # person's reorder they put it into rekordbox.
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
        # A WRITE KNOWN TO HAVE SENT NO MOVE left no partial state, so an order
        # off its path is a person's, as before U234 (R-1420's refused order).
        moved_nothing = off_path and stopped_write.sent_nothing
        reordered_since_stop = moved_nothing or _moved_since_stop(
            reader, target, name, held, stopped_write, reading, off_path=off_path, unread=unread
        )
        # R-1446. A MOVE OF UNREAD TRACKS ALONE IS NO REORDER OF THE READABLE
        # ONES: neither side's merge reads an unread track, so a person who
        # moved only one is not read as reordering the account, and the
        # stopped write is still finished. Read as theirs, the account led
        # with its readable tracks in the stopped write's half done order and
        # put that into rekordbox over the DJ's reorder. The unread track
        # keeps the place the person gave it.
        kept_after = _kept_after(held, stopped_write)
        if (
            reordered_since_stop
            and unread
            and not _readable_moved(
                stopped_write, kept_after, reading, unread, moved_nothing=moved_nothing
            )
        ):
            # Only the unread tracks the person moved keep their place; any
            # other is still put where the stopped write was taking it.
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
        # AS THE WRITE WOULD HAVE LEFT IT HAD IT FINISHED: its remaining moves
        # applied to the playlist as it stands, a track added since staying
        # where it stood among the tracks the write kept.
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
    # U231 and R-1416. WHETHER THE ACCOUNT IS PUT IN THE MERGED ORDER, read
    # before the merge, since a first sync whose order is not kept is led by
    # rekordbox, and read once, so the merge and the account write agree.
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
        elif held_for_choice(held, remote_id, dates):
            # U221. A TWIN'S MISSING TRACK WAITS FOR THE AUTHOR'S CHOICE, named
            # and never queued, until ``sync release`` lets its twin's go.
            # Asked before another pair's job, so a plain pair listing it
            # leaves the twin's choice where it was (R-1385).
            on_hold.append(names[key])
        elif (
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]
        ):
            # R-1383. A LANDING RECORD THE LOG CANNOT READ IS NEVER NO LANDING.
            # Any of them may have brought this track in, and a landed row is
            # found by its ISRC, so a track carrying one waits, named, until
            # every record reads; a track carrying none no landing could name.
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
        # EVERY RELEASE OF A REMOVED TRACK GOES (U208), the one a tie linked
        # and any other of it the account holds.
        account_removes = tuple(
            dict.fromkeys(
                one
                for key in merged.remove_account
                for one in (
                    [held for held in account_now if alias(held) == key] or [remote_of(key)]
                )
            )
        )
        # EVERY ID THE ACCOUNT LISTS, an unread one included (R-1264), so the
        # order is read and written whole.
        after = pair_merge.appended(listed_order or account_now, account_removes, account_adds)
        firsts = pair_merge.distinct(
            alias(one) for one in after if alias(one) not in unread_keys
        )
        wanted_keys = pair_merge.as_held(merged.order, set(firsts))
        # U231. ONLY A PAIR THAT KEEPS THE ACCOUNT'S ORDER has it written there.
        order_unkept = wanted_keys != firsts and not order_kept
        if wanted_keys != firsts and not order_unkept:
            # A ROW'S RELEASES MOVE TOGETHER, in the order the account holds them.
            # R-1432. A FINISH PLACES AN UNREAD TRACK WHERE THE STOPPED WRITE
            # WAS TAKING IT, as it reads every readable track, and not where
            # an interrupted move left it.
            # R-1446. EXCEPT AN UNREAD TRACK THE PERSON MOVED since the stop,
            # which keeps the place they gave it. One nobody moved is still
            # placed by the target, and when no moved one can be told apart
            # every unread track keeps its place.
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
    """The readings plans kept on this pair after ``write`` stopped, a ``pairs.StopReading``, or None (U234).

    Kept for that run, and first read at or after its moves began, so a
    reading kept for another stop, or before this one, says nothing of this
    one.
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
    """Where the moves ``write`` sent could have taken the account (R-1434, round two's review).

    A write known to have sent no move moved nothing, so its one state is
    its start, and any other order is a person's (R-1420): read against its
    whole path, a drag of one track to the top, where its first move would
    have put it, was finished over. Any other write is read along its path
    toward its target.
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
    """Whether the reorder read after ``write``'s stop moved a track the account lists readably (R-1446).

    Read over ``reading`` with every id of ``unread`` left out, so a person
    who moved only tracks the provider cannot read (R-1264) is not read as
    reordering the tracks both sides' merge reads. For a write known to have
    sent no move, whether the readable tracks stand off its moves' path;
    otherwise whether they stand in another order than the reading settled
    after the stop, ``kept``. With no settled reading to compare, the
    reorder stands as it was read.
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

    Compared with the reading settled after the stop, ``kept``, or for a
    write known to have sent no move with where it began, over the ids both
    orders hold. The ids that kept their order are the longest run both
    orders share, every readable id weighed above all the unread ones
    together, so the readable tracks are held where they stand; an unread id
    outside that run is moved. So a block of unread tracks dragged together
    is moved whole, and one nobody moved stays unmoved whatever lands next
    to it. An id either order lacks is not read as moved. With nothing to
    compare, none is.
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
    # The heaviest chain through ``now`` whose places in ``was`` rise, kept in
    # a tree over those places so each step reads the best chain before it.
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

    ONE READING OFF THE MOVES' PATH SHOWS NOTHING: the provider's partial
    state stands there as often as a person's edit. Nor do two readings
    that differ, since the provider serves a playlist's older orders for
    minutes after a change (Sitting 86, round one's review). So the first
    reading after the stop off the moves' path is kept on the pair, and a
    reading in the same order at least :data:`AGREE_AFTER` later settles it;
    a reading on the path is finished and never kept, since it may be a lag
    of the whole write (round two's review); while it is not
    settled, a reading in another order starts it again. Once it is
    settled, a reading off the path in another order is kept as the order
    after it and holds the pair, nothing written, until a reading at least
    :data:`AGREE_AFTER` later agrees with it: only then is it the person's,
    and the account leads. Every other reading is finished as the stopped
    write's. A pair with no record, a hand pairing, keeps nothing, so
    nothing it reads leads on its own. The plan then asks whether the
    reorder moved a readable track (:func:`_readable_moved`, R-1446), so a
    move of unread tracks alone still finishes the stop.
    """
    from dataclasses import replace

    from cratekit.favorites import placeholders
    from cratekit.modules.outbound import pairs

    if held is None:
        return False
    kept = _kept_after(held, write)
    if not off_path:
        # ON THE PATH THE STOP IS FINISHED, and nothing is kept: a reading on
        # the moves' path may be a lag of the whole write, so it is never the
        # order a later one is measured against (round two's review). It ends
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
            # R-1434. A move of unread tracks alone never leads (R-1446), so
            # the hold says what the plan then does.
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

    SHOWN AS THE MOVES LEAVE IT, the order is read as landed, since no lag
    can serve that order before every move landed: the plan goes on, and
    U225's reading of the stopped write finishes the pair with nothing moved.

    ANY OTHER READING MUST AGREE with one kept on the pair, taken after the
    moves were sent and at least :data:`AGREE_AFTER` before this one, by a
    run before this (Sitting 86 read two or three orders 3 s apart, 28
    minutes after the moves). Until then the pair is held and this reading
    kept for the next run; a reading equal to the one kept but too soon after
    it keeps the older, so the next run can agree with it. Agreed, the plan
    goes on: an order on the moves' path is a stopped write U225 finishes
    from the side that led, and so is one off it (U234), unless settled
    readings kept after the stop show it moved to another order, the
    person's change, merged as theirs (:func:`_moved_since_stop`).

    EXCEPT SHORT OF WHERE THE MOVES CAN HAVE LEFT IT (R-1394). The write
    recorded how many moves the provider accepted and how many may have
    reached it, so the account, unless a person moved it, stands at one of
    the orders ``write.landed`` to ``write.sent`` moves leave. An agreed
    reading on their path before ``write.sent`` moves is finished from only
    when it stands at or past them: before ``write.landed`` it can only lag
    them, however long it agrees (every move accepted is the case where
    ``write.landed`` is all of them), and at a move whose landing is not
    known it may be that lag too. Moved again from either, the remaining
    moves land by position on the wrong tracks. Held, and the reading not
    kept again.
    """
    from cratekit.favorites import placeholders
    if pair_stopped.shows(write.end, now):
        return
    assert write.moving_at is not None
    # A FIRST SYNC BY HAND HAS NO RECORD to keep a reading on (R-1376), so it
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

    Only under the top folder :data:`ORDER_FOLDER`, the one played from, unless
    ``outbound.pair_order_every_pair`` keeps every pair's.
    """
    if cfg.outbound.pair_order_every_pair:
        return True
    if rekordbox.playlist_id:
        # UNDER THE FOLDER, never a playlist of its name at the root, which
        # is its own top (round one's review).
        return bool(rekordbox.ancestors) and rekordbox.top[1] == ORDER_FOLDER
    path = tuple(getattr(home, "path", ()) or ())
    return len(path) > 1 and path[0] == ORDER_FOLDER



def _with_unread_placed(
    ordered: list[str], listed: Sequence[str], target: Sequence[str] = ()
) -> tuple[str, ...]:
    """``ordered`` with every id of ``listed`` it lacks put back after its neighbour (R-1264).

    An unread track is never moved by the merge, which cannot read it, so it
    keeps its place behind the track the account listed before it, or the
    front when none was. The order is then the whole playlist, and an account
    reorder written from it leaves no track for the provider to place.

    R-1432. AT A FINISH OF A STOPPED ORDER ``target`` is the order the
    stopped write was putting the account in, and the listing is where its
    interrupted moves left it, so an unread track one of them moved stands
    where no order wanted it. Each unread id ``target`` names is placed
    first, in its order, behind the track ``target`` puts before it, or the
    front when none of those is held; an id it does not name, one listed
    since, keeps its place behind the track listed before it. An id of
    ``target`` the listing no longer holds is never put back.
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

    The one test :func:`_ask` reuses a miss by, and the one the screen before
    it leaves a row out by (U207), so the two cannot drift: a row whose miss
    is reused is never asked, and is never screened either. A TIE REMEMBERED
    BEFORE U208 IS ASKED AGAIN, once, since asking with ``any_agreeing`` no
    longer misses on it, and its match forgets the miss.
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

    R-988, closed by U198. A row the account had no track for is remembered
    with the ISRC it was asked under and its answer, and a plan meeting it
    again under the same ISRC reuses the answer without a request, so the
    three plans one sync makes ask once, and a sync of every pair does not ask
    again each time. A row whose ISRC changed is asked again. An answer that
    says a candidate could not be read is no answer about the row, and is
    never remembered.

    A TIE TAKES ONE RELEASE (U208, decided by Phillip at Sitting 54, as the
    mirror's R-1032). The account is asked with ``any_agreeing``, so a row
    whose ISRC names several releases that all agree with it is matched as
    one of them, the one the account hearts, else the lowest numbered after
    the file's album narrowed them, and the match is linked like any other,
    so no later plan asks about it. The refusals before the tie stand: no
    agreeing release, no row to judge agreement by, a candidate that could
    not be read. The third value says the account broke a tie, for the gate.
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
    # A TIE BESIDE AN UNREADABLE RELEASE STILL MISSES, in words naming both,
    # and is never remembered: the unreadable one may agree tomorrow.
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

    This pair's own intake jobs and landings are asked first, then, for what
    they leave lacking, every intake job this verb queued on the library and
    every INBOX playlist landed on it, for any account playlist (U229): a
    track a landing through another account playlist brought in is that row.

    ``here`` is the pair's own rekordbox rows by ISRC, the database's or else
    the file's, asked only for a track no row's database ISRC names (U208). A
    release the account holds beside the one a tie linked, put there by hand,
    carries the ISRC of a row this playlist already holds, which may be in
    that row's file only, and it is that row, never a track to acquire.
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
    # U229. WHAT ANOTHER ACCOUNT PLAYLIST BROUGHT IN IS STILL THE LIBRARY'S.
    # Asked only for what this pair's own jobs and landings left lacking, so
    # every track they answer is answered as before, and read once per plan.
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

    Only a custom playlist twin's pair holds. One whose hold is recorded holds
    exactly the tracks recorded, the ones its twin was made without. One paired
    before U221 recorded none, so it is read by time: a track is held unless
    the account dates its addition after the pair was marked, so a track put on
    the playlist by hand since the twin was made is queued as any pair's is,
    and one the account dates nowhere, or a mark that does not read, is held.
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

    R-1385. A track the library lacks is downloaded once for the library,
    whichever pairs list it: one any other pair's intake job still holds or
    resolved, or one an earlier pair of this plan asks to acquire, is named
    awaiting with the pair holding it and never queued a second time.
    """
    for source, name in reader.held_by_jobs.get(remote_id, ()):
        if source != target.account_id:
            return f"queued for {name}"
    asked = reader.asked.get(remote_id)
    if asked is not None and asked[0] != target.key:
        return f"{QUEUED_HERE} {asked[1]}"
    return ""



#: U231. How long before a reading a pending order's earlier reading must have
#: been taken for the two to agree, since reads seconds apart served different
#: orders 28 minutes after the moves (Sitting 86).
AGREE_AFTER = timedelta(minutes=5)
