"""Custom playlist twins: the permanent rekordbox copy of a downloaded custom playlist (U149).

Decided by Phillip on 2026-10-15
(``docs/plans/2026-10-15-1330-feat-rekordbox-tidal-parity-plan.md``, R6 to
R10). A custom playlist the author builds on the account is swept, lands as an
INBOX playlist, is marked (held as taken since U242, prefixed ``DOWNLOADED ``
before it) and filed into the account's
``<year>`` folder for good, while its INBOX copy rotates out of rekordbox. The
TWIN is the copy that stays: one plain playlist named as the account playlist
less any old prefix, in the top level folder ``Custom Playlists <year>``, holding
the rows the library owns for its tracks in the account's order, and paired
with the account playlist so ``crate sync pair`` keeps the two one list.

**TWO MAKERS, ONE RULE.** ``crate sync twins`` backfills every taken
custom playlist the account already holds in a year folder, once; the native
landing of an account playlist pass writes the twin of each account playlist
it writes an INBOX playlist for, in the same commit. Both take the folder, the
name and the refusals from here.

**THE FOLDER IS NOT A TREE.** It is not declared in the taxonomy and no
registry records it, so the pair rule, which refuses a rekordbox playlist under
one of Cratekit's own trees, lets a twin pair, and the rotation, the mirror and
the adoption never read it. It is found by name at the top level, live, and
made there once when absent. Two live top level folders of one year's name
leave that year's twins unplanned and named, since which one is the year's is
not something a name decides.

**A NAME THE FOLDER HOLDS IS REFUSED, NEVER COUNTED.** A twin is the one
playlist of its name in its folder. A playlist already there under that name
may be a twin an interrupted run wrote and could not pair, and a second one
beside it, ``Phil 9-30-26 2``, would be a copy nobody pairs. So the twin is
left and named, and ``crate sync pair`` pairs the one there by hand. Two
account playlists of one name in one year leave the second the same way.

**ADD ONLY.** A folder, a playlist and its memberships are made; nothing is
renamed, moved or removed, in rekordbox or on the account. A twin whose
account playlist later disappears is unpaired by ``crate sync pair`` and left
where it is, named.

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cratekit.acquire import match
from cratekit.cli.output import digest_of
from cratekit.core import config, convergence, rb_writer, session, snapshot, tree_registry
from cratekit.core.cause import CratekitError, refuse
from cratekit.sync.playlists import PER_PLAYLIST_REASONS, is_taken, untaken_name
from cratekit.write import playlist_pair, trees

#: The folder's name before its year, decided on 2026-10-15.
FOLDER_PREFIX = "Custom Playlists"

#: The session workflow the backfill is recorded under, and the stable key its
#: commit is counted under, since the folder is no registered tree.
WORKFLOW = "custom-playlist-twins"
RECORD_KEY = "custom-playlist-twins"

#: A root folder on the account whose title is a year, the plain ``<year>``
#: the filing step moves a marked custom playlist into (U116).
YEAR = re.compile(r"[0-9]{4}")

#: What becomes of one planned twin.
CREATE = "create"
LEFT = "left"

#: Why a track of the account playlist is not in its twin.
NOT_OWNED = "the library holds no row for it"
AMBIGUOUS = "more than one library row carries it, so none was chosen"
#: Said after what the reader found wanting in a track it would not read (U213).
UNREAD_NOT_FOUND = "and no recorded link or ISRC finds its row"

_ORIGIN = ("sync", "twins")


def folder_name(year: str | int) -> str:
    """The twin folder for one year, ``Custom Playlists 2026``."""
    return f"{FOLDER_PREFIX} {year}"


def twin_name(account_name: str) -> str:
    """The twin's name: the account playlist's, less the old ``DOWNLOADED `` prefix."""
    return untaken_name(account_name)


# ---------------------------------------------------------------------------
# The folder, read in rekordbox
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Folder:
    """One year's twin folder as a plan found it."""

    year: str
    name: str
    #: The live folder's row, or empty when the write makes it.
    folder_id: str = ""
    #: Every live node name directly inside it, which a twin may not take.
    held: frozenset[str] = frozenset()
    #: Set when the year cannot be placed, and then none of its twins is made.
    why: str = ""

    def identity(self) -> dict[str, Any]:
        return {"year": self.year, "name": self.name, "folder_id": self.folder_id, "why": self.why}


def _live_top_folders(db: Any, name: str) -> tuple[str, ...]:
    from sqlalchemy import bindparam, text

    statement = text(
        f"SELECT ID FROM {rb_writer.PLAYLIST_TABLE} WHERE Name = :name AND Attribute = 1 "
        f"AND COALESCE(ParentID, '') IN :roots "
        f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 ORDER BY ID"
    ).bindparams(bindparam("roots", expanding=True))
    return tuple(
        str(row[0])
        for row in db.session.execute(
            statement, {"name": name, "roots": list(rb_writer.ROOT_PARENT_SENTINELS)}
        ).fetchall()
    )


def _live_children(db: Any, folder_id: str) -> frozenset[str]:
    from sqlalchemy import text

    return frozenset(
        str(row[0] or "")
        for row in db.session.execute(
            text(
                f"SELECT Name FROM {rb_writer.PLAYLIST_TABLE} WHERE ParentID = :parent "
                f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0"
            ),
            {"parent": str(folder_id)},
        ).fetchall()
    )


def find_folder(db: Any, year: str | int) -> Folder:
    """One year's twin folder: the one live at the top level, none, or too many to choose."""
    year = str(year)
    name = folder_name(year)
    found = _live_top_folders(db, name)
    if len(found) > 1:
        return Folder(
            year=year,
            name=name,
            why=(
                f"rekordbox holds {len(found)} top level folders named {name!r}, so "
                f"which one is the year's is not something its name decides"
            ),
        )
    if found:
        return Folder(year=year, name=name, folder_id=found[0], held=_live_children(db, found[0]))
    return Folder(year=year, name=name)


# ---------------------------------------------------------------------------
# One twin, planned
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Miss:
    """One track of the account playlist its twin does not hold, and why."""

    position: int
    remote_id: str
    artist: str
    title: str
    why: str

    def identity(self) -> dict[str, Any]:
        return {
            "position": self.position,
            "remote_id": self.remote_id,
            "artist": self.artist,
            "title": self.title,
            "why": self.why,
        }

    def said(self) -> str:
        return f"{self.artist} - {self.title} ({self.why})"

    def held_as(self) -> str:
        """The words its twin's hold records it by (U221)."""
        return f"{self.artist} - {self.title}"


@dataclass(frozen=True, slots=True)
class Twin:
    """One twin a backfill plans, with the rows it holds and the tracks it does not."""

    account_id: str
    account_name: str
    name: str
    folder: Folder
    action: str
    #: The library rows it holds, in the account playlist's order, each once.
    rows: tuple[str, ...] = ()
    #: Each account track matched to the row it holds, remote id to content id.
    links: tuple[tuple[str, str], ...] = ()
    #: The account playlist's tracks as listed, in order, for the pair's snapshot.
    account: tuple[str, ...] = ()
    misses: tuple[Miss, ...] = ()
    #: Whether the account listed the whole playlist, which a snapshot needs.
    whole: bool = True
    #: Why it is not made, when ``action`` is :data:`LEFT`.
    why: str = ""
    #: The refusal that left it, when its listing was refused (U213). The plan's
    #: digest carries this and not ``why``, whose words are the provider's own
    #: and may differ between the run that asked and the run that writes.
    refused: str = ""

    def identity(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "account_name": self.account_name,
            "name": self.name,
            "folder": self.folder.identity(),
            "action": self.action,
            "rows": list(self.rows),
            "links": [list(one) for one in self.links],
            "account": list(self.account),
            "misses": [one.identity() for one in self.misses],
            "whole": self.whole,
            "why": self.refused or self.why,
        }


def place(name: str, folder: Folder, taken: set[str]) -> str:
    """Why a twin of ``name`` cannot go in ``folder``, or ``""`` when it can.

    ``taken`` is the names this plan already gave in that folder, and is added
    to when the answer is yes.
    """
    if folder.why:
        return folder.why
    if not name:
        return "its name is only the downloaded prefix, so a twin would have no name"
    if name in folder.held:
        return (
            f"{folder.name!r} already holds a playlist named {name!r}; pair it by hand "
            f"with crate sync pair, or rename it, and the next run makes the twin"
        )
    if name in taken:
        return f"another account playlist this run makes a twin for is also named {name!r}"
    taken.add(name)
    return ""


# ---------------------------------------------------------------------------
# An account track, found in the library
# ---------------------------------------------------------------------------


@dataclass
class Library:
    """Every way the backfill finds an account track's row, read once.

    In order, the first that answers deciding: the account mirror's recorded
    link to that very track (U147), the database's ISRC, the ISRC the mirror
    recorded for a row whose file carries it, and the rows of the INBOX
    playlists a landing made for that account playlist (U128). A row the
    library removed is never an answer.
    """

    by_remote: Mapping[str, tuple[str, ...]]
    by_isrc: Mapping[str, tuple[str, ...]]
    by_mirror_isrc: Mapping[str, tuple[str, ...]]
    landed: Mapping[str, Mapping[str, tuple[str, ...]]] = field(default_factory=dict)

    def find(self, account_id: str, remote_id: str, isrc: str) -> tuple[str, ...]:
        code = match.isrc_token(isrc)
        for answer in (
            self.by_remote.get(remote_id, ()),
            self.by_isrc.get(code, ()) if code else (),
            self.by_mirror_isrc.get(code, ()) if code else (),
            (self.landed.get(account_id) or {}).get(code, ()) if code else (),
        ):
            if answer:
                return answer
        return ()


def _grouped(pairs: Iterable[tuple[str, str]], live: Iterable[str]) -> dict[str, tuple[str, ...]]:
    alive = set(live)
    found: dict[str, list[str]] = {}
    for key, content_id in pairs:
        if key and content_id in alive and content_id not in found.setdefault(key, []):
            found[key].append(content_id)
    return {key: tuple(ids) for key, ids in found.items() if ids}


def read_library(cfg: config.Config, db: Any, account_ids: Iterable[str]) -> Library:
    """The library's answers for the account playlists named, read on ``db``."""
    from cratekit.modules.outbound import ledger
    from cratekit.sync import pair_cli

    # MATERIALIZED ONCE: a generator read inside the comprehension below is
    # spent by its first account, and every later one would lose its source.
    wanted = set(account_ids)
    links = ledger.mirror_links(cfg)
    live = playlist_pair.content(db, links)
    # THE UNREAD HALF IS DROPPED HERE BY THIS READER'S OWN POLICY (R-1383).
    # The backfill holds a track it finds no row for and queues nothing, and
    # its write refuses at the session gate on any entry the log cannot read,
    # so an unread record never reaches a download; the gate before that
    # write shows its misses with no word of the record (a residual).
    mirrors, _unread = pair_cli.landed_inbox_playlists(cfg)
    landed = {
        account_id: pair_cli.landed_isrcs(cfg, db, playlist_ids)
        for account_id, playlist_ids in mirrors.items()
        if account_id in wanted
    }
    return Library(
        by_remote=_grouped(((remote, row) for row, (remote, _code) in links.items()), live),
        by_isrc=playlist_pair.rows_by_isrc(db, match.isrc_token),
        by_mirror_isrc=_grouped(
            ((match.isrc_token(code), row) for row, (_remote, code) in links.items()), live
        ),
        landed=landed,
    )


def matched(
    account_id: str,
    tracks: Mapping[str, Mapping[str, Any]],
    library: Library,
    unread: Mapping[str, str] | None = None,
) -> tuple[tuple[str, ...], tuple[tuple[str, str], ...], tuple[Miss, ...]]:
    """The account playlist's tracks as rows in its order, the links, and the misses.

    ``tracks`` is the listing as the intake reader folds it, each track once,
    so a miss's position counts the folded listing, a track listed twice once.

    ``unread`` names, by id, each track the reader would not read and what it
    found wanting (U213). Such a track is still found by its recorded link
    and its ISRC, which never needed its title, and joins its twin when one
    row answers; when none does, its miss says why it could not be read.
    """
    unread = unread or {}
    rows: list[str] = []
    links: list[tuple[str, str]] = []
    misses: list[Miss] = []
    for position, (remote_id, said) in enumerate(tracks.items(), start=1):
        found = library.find(account_id, remote_id, str(said.get("isrc") or ""))
        if len(found) == 1:
            links.append((remote_id, found[0]))
            if found[0] not in rows:
                rows.append(found[0])
            continue
        misses.append(
            Miss(
                position=position,
                remote_id=remote_id,
                artist=str(said.get("artist") or ""),
                title=str(said.get("title") or ""),
                why=(
                    AMBIGUOUS
                    if found
                    else f"{unread[remote_id]}, {UNREAD_NOT_FOUND}"
                    if remote_id in unread
                    else NOT_OWNED
                ),
            )
        )
    return tuple(rows), tuple(links), tuple(misses)


# ---------------------------------------------------------------------------
# The backfill's plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Backfill:
    """Every twin a backfill plans, and the account playlists it read and left alone."""

    twins: tuple[Twin, ...] = ()
    #: Downloaded playlists in a year folder that are already paired.
    paired: int = 0

    @property
    def made(self) -> tuple[Twin, ...]:
        return tuple(one for one in self.twins if one.action == CREATE)

    @property
    def left(self) -> tuple[Twin, ...]:
        return tuple(one for one in self.twins if one.action == LEFT)

    @property
    def writes(self) -> bool:
        return bool(self.made)

    @property
    def digest(self) -> str:
        return digest_of({"kind": "sync.twins", "twins": [one.identity() for one in self.twins]})


def candidates(
    remote: Any, own: Mapping[str, str], excluded: Iterable[str], taken: Iterable[str] = ()
) -> list[tuple[str, str, str]]:
    """Every downloaded custom playlist in a year folder, as ``(year, id, name)``, by year then name.

    ``own`` is the account playlists listed as the author's, id to name, and
    ``excluded`` the ones a label, a set or the mirror keeps. A playlist in two
    year folders is read once, under its first year. DOWNLOADED MEANS TAKEN
    (U242): one ``taken``, the record's taken ledger, holds, or one whose
    title still carries the old prefix.
    """
    kept = set(excluded)
    held = frozenset(taken)
    seen: set[str] = set()
    found: list[tuple[str, str, str]] = []
    for folder_id, title in sorted(remote.folders().items(), key=lambda one: (one[1], one[0])):
        year = str(title or "").strip()
        if not YEAR.fullmatch(year):
            continue
        for playlist_id in sorted(remote.folder_playlists(folder_id)):
            name = own.get(playlist_id)
            if name is None or playlist_id in kept or playlist_id in seen:
                continue
            if not is_taken(playlist_id, name, held):
                continue
            seen.add(playlist_id)
            found.append((year, playlist_id, name))
    return sorted(found, key=lambda one: (one[0], one[2], one[1]))


def plan_backfill(
    cfg: config.Config,
    db: Any,
    *,
    remote: Any,
    found: Any,
    own: Mapping[str, str],
    excluded: Iterable[str],
    paired: Iterable[str],
) -> Backfill:
    """Decide a twin for every downloaded custom playlist the account holds that has none.

    Reads the account and the database and writes nothing. A playlist already
    paired, as a twin or by hand, is counted and never planned again, which is
    what makes a second run plan nothing.
    """
    from cratekit.intake import cli as intake_cli
    from cratekit.sync import pair_merge
    from cratekit.sync.playlists import taken_ids

    held = set(paired)
    listed = candidates(remote, own, excluded, taken_ids(cfg))
    wanted = [one for one in listed if one[1] not in held]
    if not wanted:
        return Backfill(paired=len(listed))
    library = read_library(cfg, db, (one[1] for one in wanted))
    folders: dict[str, Folder] = {}
    taken: dict[str, set[str]] = {}
    twins: list[Twin] = []
    for year, account_id, account_name in wanted:
        folder = folders.get(year)
        if folder is None:
            folder = folders[year] = find_folder(db, year)
        name = twin_name(account_name)
        # ONE PLAYLIST'S LISTING NEVER STOPS THE OTHERS (U213). A playlist the
        # provider cannot list, or whose rows carry no id, is left and named,
        # the refusals the sweep of every playlist already takes per playlist;
        # a track the reader would not read is named in its twin, below.
        try:
            listing = intake_cli.list_playlist_readable(found, account_id)
        except CratekitError as exc:
            if exc.cause.reason not in PER_PLAYLIST_REASONS:
                raise
            twins.append(
                Twin(
                    account_id=account_id,
                    account_name=account_name,
                    name=name,
                    folder=folder,
                    action=LEFT,
                    why=f"the account playlist could not be read: {exc.cause.message}",
                    refused=exc.cause.reason,
                )
            )
            continue
        why = place(name, folder, taken.setdefault(year, set()))
        tracks = {
            ref: listing.tracks[ref] if ref in listing.tracks else listing.unread[ref].said()
            for ref in listing.order
        }
        rows, links, misses = matched(
            account_id,
            tracks,
            library,
            {ref: one.why for ref, one in listing.unread.items()},
        )
        twins.append(
            Twin(
                account_id=account_id,
                account_name=account_name,
                name=name,
                folder=folder,
                action=LEFT if why else CREATE,
                rows=rows,
                links=links,
                account=pair_merge.distinct(tracks),
                misses=misses,
                whole=listing.short is None,
                why=why,
            )
        )
    return Backfill(twins=tuple(twins), paired=len(listed) - len(wanted))


def payload(planned: Backfill) -> dict[str, Any]:
    """The plan as the gate shows it: each twin, and each track a twin will not hold."""
    items: list[dict[str, Any]] = []
    for one in planned.twins:
        entry: dict[str, Any] = {
            "action": one.action,
            "folder": one.folder.name,
            "playlist": one.name,
            "account_id": one.account_id,
            "account_name": one.account_name,
            "tracks": len(one.rows),
            "missing": len(one.misses),
        }
        if one.action == CREATE and not one.folder.folder_id:
            entry["folder_made"] = True
        if one.why:
            entry["why"] = one.why
        items.append(entry)
        items.extend(
            {
                "action": "missing",
                "playlist": one.name,
                "account_id": one.account_id,
                **miss.identity(),
            }
            for miss in one.misses
        )
    made = planned.made
    return {
        "digest": planned.digest,
        "items": items,
        "totals": {
            "count": len(items),
            "twins": len(made),
            "left": len(planned.left),
            "folders_made": len({one.folder.year for one in made if not one.folder.folder_id}),
            "tracks": sum(len(one.rows) for one in made),
            "missing": sum(len(one.misses) for one in made),
            "already_paired": planned.paired,
        },
        "chunk": None,
    }


def facts(planned: Backfill) -> dict[str, Any]:
    """The lines beside the items on the gate screen."""
    made = planned.made
    shown: dict[str, Any] = {
        "twins": (
            "; ".join(
                f"{one.folder.name} / {one.name}: {len(one.rows)} track(s)"
                + (f", {len(one.misses)} missing" if one.misses else "")
                for one in made
            )
            or "none"
        ),
        "already paired": planned.paired,
    }
    if planned.left:
        shown["left"] = "; ".join(f"{one.account_name}: {one.why}" for one in planned.left)
    return shown


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


def addition_violations(
    before: rb_writer.NodeTables,
    after: rb_writer.NodeTables,
    *,
    folders: Mapping[str, str],
    playlists: Mapping[str, tuple[str, str, frozenset[str]]],
) -> list[str]:
    """Every difference between two readings that the twins this write made do not explain.

    ``folders`` maps each folder row the write made to its name, and
    ``playlists`` each playlist row it made to ``(name, parent row, the
    content rows it holds)``. Empty means the write was confined. PURE, so
    every branch is reachable with literal readings. What it explains, and
    nothing more:

    * no content row and no existing membership row differs, appears or goes;
    * the playlist rows added are exactly the folders and playlists made, live,
      a folder at the top level and a plain playlist under its planned parent;
    * no existing playlist row disappears, and one may move only its
      bookkeeping, and only when it sits at the top level beside a folder made
      or inside a folder a twin was made in;
    * every membership row added is live and puts a planned row in its twin.
    """
    violations: list[str] = []
    if before.content != after.content:
        violations.append(f"a {rb_writer.CONTENT_TABLE} row changed, and a twin touches no track")
    cols = before.playlist_columns
    marker_at = cols.index(rb_writer.SOFT_DELETE_COLUMN)
    parent_at = cols.index("ParentID")
    name_at = cols.index("Name")
    kind_at = cols.index("Attribute")
    made = {**{key: None for key in folders}, **{key: None for key in playlists}}
    for key in sorted(set(before.playlists) - set(after.playlists)):
        violations.append(f"the {rb_writer.PLAYLIST_TABLE} row {key!r} disappeared")
    for key in sorted(set(after.playlists) - set(before.playlists) - set(made)):
        violations.append(f"an unplanned {rb_writer.PLAYLIST_TABLE} row {key!r} was added")
    for key, name in sorted(folders.items()):
        row = after.playlists.get(key)
        if (
            row is None
            or str(row[name_at]) != name
            or str(row[parent_at] or "") not in rb_writer.ROOT_PARENT_SENTINELS
            or row[marker_at]
            or int(row[kind_at] or 0) != 1
        ):
            violations.append(
                f"the {rb_writer.PLAYLIST_TABLE} row {key!r} is not a live top level "
                f"folder named {name!r}"
            )
    for key, (name, parent, _rows) in sorted(playlists.items()):
        row = after.playlists.get(key)
        if (
            row is None
            or str(row[name_at]) != name
            or str(row[parent_at]) != str(parent)
            or row[marker_at]
            or int(row[kind_at] or 0) != playlist_pair.PLAIN_PLAYLIST
        ):
            violations.append(
                f"the {rb_writer.PLAYLIST_TABLE} row {key!r} is not a live plain playlist "
                f"named {name!r} under {parent!r}"
            )
    parents = {str(parent) for _name, parent, _rows in playlists.values()}
    beside_top = bool(folders)
    for key in sorted(set(before.playlists) & set(after.playlists)):
        changed = {
            column
            for column, old, new in zip(cols, before.playlists[key], after.playlists[key])
            if old != new
        }
        if not changed:
            continue
        where = str(before.playlists[key][parent_at] or "")
        allowed = (
            _BOOKKEEPING
            if where in parents or (beside_top and where in rb_writer.ROOT_PARENT_SENTINELS)
            else frozenset()
        )
        if changed - allowed:
            violations.append(
                f"the {rb_writer.PLAYLIST_TABLE} row {key!r} changed {sorted(changed - allowed)}, "
                f"which the twins made do not explain"
            )
    m_cols = before.membership_columns
    owner_at = m_cols.index("PlaylistID")
    content_at = m_cols.index("ContentID")
    m_marker = m_cols.index(rb_writer.SOFT_DELETE_COLUMN)
    for key in sorted(set(before.memberships) - set(after.memberships)):
        violations.append(f"the {rb_writer.MEMBERSHIP_TABLE} row {key!r} disappeared")
    for key in sorted(set(before.memberships) & set(after.memberships)):
        if before.memberships[key] != after.memberships[key]:
            violations.append(
                f"the {rb_writer.MEMBERSHIP_TABLE} row {key!r} changed, and a twin changes "
                f"no membership it did not make"
            )
    for key in sorted(set(after.memberships) - set(before.memberships)):
        row = after.memberships[key]
        owner, content_id = str(row[owner_at]), str(row[content_at])
        wanted = playlists.get(owner)
        if row[m_marker] or wanted is None or content_id not in wanted[2]:
            violations.append(
                f"the {rb_writer.MEMBERSHIP_TABLE} row {key!r} puts row {content_id!r} in "
                f"playlist {owner!r}, which no twin planned"
            )
    return violations


#: What an existing playlist row may change while a twin is made beside it.
_BOOKKEEPING = frozenset({"Seq", "updated_at", "usn", "rb_local_usn"})


def assert_confined(
    db: Any,
    before: rb_writer.NodeTables,
    *,
    folders: Mapping[str, str],
    playlists: Mapping[str, tuple[str, str, frozenset[str]]],
) -> None:
    """Refuse, before the commit, a change the twins made do not explain, read from SQL."""
    db.session.flush()
    violations = addition_violations(
        before, rb_writer.node_tables(db), folders=folders, playlists=playlists
    )
    if violations:
        db.rollback()
        raise refuse(
            "whitelist-violation",
            "the twins' write reached rows the plan did not name, read from SQL before "
            "the commit, so nothing was written:\n  - " + "\n  - ".join(violations),
            origin=_ORIGIN,
            detail={"violations": violations},
        )


@dataclass(frozen=True, slots=True)
class Made:
    """One twin a write made, read back after the commit."""

    account_id: str
    name: str
    folder: str
    playlist_id: str
    read_back: tuple[playlist_pair.Row, ...] = ()


@dataclass(frozen=True, slots=True)
class Written:
    """What one backfill wrote."""

    twins: tuple[Made, ...]
    folders_made: tuple[str, ...]
    session_id: str
    added: int


def _stale(message: str, **detail: Any) -> Exception:
    return refuse(
        "decision-stale",
        message + "; run it again and approve what it shows now",
        origin=_ORIGIN,
        detail=dict(detail),
    )


def recheck(db: Any, twins: Sequence[Twin]) -> None:
    """Refuse a write whose folders, names or rows moved since the plan was approved."""
    years: dict[str, Folder] = {}
    for one in twins:
        now = years.get(one.folder.year)
        if now is None:
            now = years[one.folder.year] = find_folder(db, one.folder.year)
        if now.folder_id != one.folder.folder_id or now.why != one.folder.why:
            raise _stale(
                f"the folder {one.folder.name!r} is not as the approved plan read it, so "
                f"nothing was written",
                folder=one.folder.name,
            )
        if one.name in now.held:
            raise _stale(
                f"{one.folder.name!r} holds a playlist named {one.name!r} now, so nothing "
                f"was written",
                playlist=one.name,
            )
    wanted = {row for one in twins for row in one.rows}
    gone = sorted(wanted - set(playlist_pair.content(db, wanted)))
    if gone:
        raise _stale(
            f"{len(gone)} row(s) a twin holds are no longer live rows of the collection, "
            f"so nothing was written",
            gone=gone,
        )


def _record_twins_commit(record: session.SessionRecord, *, created: int, cfg: config.Config) -> None:
    if created <= 0:
        return
    session.record_commit(
        record,
        RECORD_KEY,
        session.ChangeSummary((session.TreeChange(tree=RECORD_KEY, created=created),)),
        cfg,
    )


def write(
    cfg: config.Config,
    db: Any,
    planned: Backfill,
    *,
    analysis_roots: Iterable[Path | str],
) -> Written:
    """Make every planned twin, its folder when absent, and its memberships, in one guarded commit.

    THE SESSION SPINE IS CALLED, NOT REBUILT, as every database membership
    writer calls it: the gates with a record kept, a capture verified before
    anything is written, the analysis watch over the roots named, the commit
    witness, and the guarded commit. The folders, names and rows are read
    again on this handle first, and the commit is CONFINED FROM SQL before it
    lands, so the write cannot reach a row the plan did not name.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    made_twins = planned.made
    recheck(db, made_twins)
    # THE FOLDER IS NO TREE, so an out of band restore is detected and marked,
    # never refused, as the Favorites writers do.
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))
    created: list[tuple[Twin, str]] = []
    folders_made: dict[str, str] = {}
    added = 0
    with session.assert_gates(
        cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
    ) as gates:
        record = gates.record
        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)
        with rb_writer.commit_witness(db) as witness:
            try:
                before = rb_writer.node_tables(db)
                parents: dict[str, Any] = {}
                planned_rows: dict[str, tuple[str, str, frozenset[str]]] = {}
                for one in made_twins:
                    year = one.folder.year
                    parent = parents.get(year)
                    if parent is None:
                        if one.folder.folder_id:
                            parent = db.get_playlist(ID=one.folder.folder_id)
                        else:
                            parent = db.create_playlist_folder(one.folder.name)
                            db.session.flush()
                            folders_made[str(parent.ID)] = one.folder.name
                        parents[year] = parent
                    playlist = db.create_playlist(one.name, parent=parent)
                    db.session.flush()
                    added += len(rb_writer.add_memberships(db, playlist, one.rows))
                    planned_rows[str(playlist.ID)] = (
                        one.name,
                        str(parent.ID),
                        frozenset(one.rows),
                    )
                    created.append((one, str(playlist.ID)))
                assert_confined(db, before, folders=folders_made, playlists=planned_rows)
                rb_writer.commit_guarded(db)
            except BaseException:
                trees._rollback_quietly(db)
                if witness.landed:
                    _record_twins_commit(record, created=added + len(created), cfg=cfg)
                raise
        _record_twins_commit(record, created=added + len(created), cfg=cfg)
        convergence.record_fingerprint(cfg, db)
        session_id = record.session_id
    return Written(
        twins=tuple(
            Made(
                account_id=one.account_id,
                name=one.name,
                folder=one.folder.name,
                playlist_id=playlist_id,
                read_back=playlist_pair.members(db, playlist_id),
            )
            for one, playlist_id in created
        ),
        folders_made=tuple(folders_made.values()),
        session_id=session_id,
        added=added,
    )


def assert_read_back(planned: Backfill, written: Written) -> None:
    """Refuse an answer the database does not hold: each twin's rows, in the account's order."""
    by_account = {one.account_id: one for one in planned.made}
    wrong: list[str] = []
    for made in written.twins:
        wanted = list(by_account[made.account_id].rows)
        read = list(dict.fromkeys(row.content_id for row in made.read_back))
        if read != wanted:
            wrong.append(f"{made.folder} / {made.name}: {len(read)} read, {len(wanted)} planned")
    if wrong:
        raise refuse(
            "session-committed-unverified",
            "the twins read back from the database are not the ones planned, and the "
            f"commit landed in session {written.session_id}: " + "; ".join(wrong),
            origin=_ORIGIN,
            detail={"wrong": wrong, "session": written.session_id},
        )


def pair_backfilled(cfg: config.Config, planned: Backfill, written: Written) -> int:
    """Mark each twin's pair, and record both snapshots when its account listing was whole.

    The backfill read the whole account playlist and wrote its twin and read
    it back, which is what a whole sync is, so the next ``sync pair`` merges
    both ways from here. A short listing marks the pair with its links alone,
    so its first sync adds only. Each twin's misses are recorded as its hold
    (U221), so ``sync pair`` names them and queues none until ``sync release``
    lets that twin's go. Answers how many pairs were marked.
    """
    from cratekit.modules.outbound import pairs

    store = pairs.PairStore(cfg)
    by_account = {one.account_id: one for one in planned.made}
    marked = 0
    for made in written.twins:
        one = by_account[made.account_id]
        # U221. EVERY TRACK THE TWIN WAS MADE WITHOUT IS HELD for the author's
        # choice, recorded with the mark, so no sync queues it on its own. A
        # SHORT LISTING RECORDS NO HOLD: a track the account withheld from it
        # is in no miss, so the pair is read by time instead, as one paired
        # before U221, which holds every track listed before the mark (the
        # review's round one).
        store.mark(
            one.account_id,
            made.playlist_id,
            name=one.account_name,
            twin=True,
            on_hold=(
                {miss.remote_id: miss.held_as() for miss in one.misses} if one.whole else None
            ),
        )
        marked += 1
        store.record(
            one.account_id,
            account=list(one.account) if one.whole else None,
            rekordbox=(
                [pairs.Membership(row.content_id, row.row_id) for row in made.read_back]
                if one.whole
                else None
            ),
            links=dict(one.links),
            name=one.account_name,
        )
    return marked


# ---------------------------------------------------------------------------
# The landing's twins, in the landing's own commit
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class LandingTwin:
    """One twin a native landing plans beside the INBOX playlist of an account playlist.

    It holds what that INBOX playlist holds, the rows this landing made and
    the ones the library owned, in the account playlist's order, so the rows
    are the landing's and are not planned here.
    """

    account_id: str
    account_name: str
    name: str
    folder: Folder
    action: str
    why: str = ""

    def identity(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "name": self.name,
            "folder": self.folder.identity(),
            "action": self.action,
            "why": self.why,
        }


def plan_landing(
    db: Any, accounts: Sequence[tuple[str, str]], *, year: str | int, paired: Iterable[str]
) -> tuple[LandingTwin, ...]:
    """The twin of each account playlist a landing writes an INBOX playlist for.

    ``accounts`` is ``(account id, the account's name)`` per INBOX playlist the
    landing plans. An account playlist already paired, as a twin or by hand,
    gets none: its pair brings this landing's new rows at the next
    ``sync pair``, which finds them through the landing's own record (U128).
    """
    held = set(paired)
    wanted = [(account_id, name) for account_id, name in accounts if account_id not in held]
    if not wanted:
        return ()
    folder = find_folder(db, year)
    taken: set[str] = set()
    planned: list[LandingTwin] = []
    for account_id, account_name in wanted:
        name = twin_name(account_name)
        why = place(name, folder, taken)
        planned.append(
            LandingTwin(
                account_id=account_id,
                account_name=account_name,
                name=name,
                folder=folder,
                action=LEFT if why else CREATE,
                why=why,
            )
        )
    return tuple(planned)


def recheck_landing(db: Any, planned: Sequence[LandingTwin]) -> None:
    """Refuse a landing whose twin folder or names moved since its plan was approved."""
    made = [one for one in planned if one.action == CREATE]
    if not made:
        return
    now = find_folder(db, made[0].folder.year)
    if now.folder_id != made[0].folder.folder_id or now.why != made[0].folder.why:
        raise _stale(
            f"the folder {made[0].folder.name!r} is not as the approved plan read it, so "
            f"nothing was written",
            folder=made[0].folder.name,
        )
    held = sorted(one.name for one in made if one.name in now.held)
    if held:
        raise _stale(
            f"{made[0].folder.name!r} holds a playlist named {held[0]!r} now, so nothing "
            f"was written",
            playlist=held[0],
        )


@dataclass(frozen=True, slots=True)
class LandedTwin:
    """One twin a landing's commit wrote."""

    account_id: str
    account_name: str
    name: str
    folder: str
    playlist_id: str
    tracks: int


def write_landing(
    db: Any, planned: Sequence[LandingTwin], rows: Mapping[str, Sequence[str]]
) -> tuple[LandedTwin, ...]:
    """Make each planned twin in the landing's open transaction, holding its INBOX rows.

    ``rows`` maps an account id to the content rows its INBOX playlist was
    given, in order. A twin whose INBOX playlist holds nothing is not made.
    Nothing is committed here: the landing's one guarded commit carries it.
    """
    made = [one for one in planned if one.action == CREATE and rows.get(one.account_id)]
    if not made:
        return ()
    folder = made[0].folder
    parent = (
        db.get_playlist(ID=folder.folder_id)
        if folder.folder_id
        else db.create_playlist_folder(folder.name)
    )
    written: list[LandedTwin] = []
    for one in made:
        playlist = db.create_playlist(one.name, parent=parent)
        count = len(rb_writer.add_memberships(db, playlist, rows[one.account_id]))
        written.append(
            LandedTwin(
                account_id=one.account_id,
                account_name=one.account_name,
                name=one.name,
                folder=folder.name,
                playlist_id=str(playlist.ID),
                tracks=count,
            )
        )
    return tuple(written)


def pair_landed(cfg: config.Config, written: Sequence[LandedTwin]) -> list[dict[str, str]]:
    """Mark each landed twin's pair, with no snapshot, and say what could not be.

    The landing read the account's tracks from its intake job rather than from
    the account, so no snapshot is recorded: the pair's first ``sync pair``
    adds only, and records both sides. A pair that cannot be marked is a
    warning naming the twin and the hand step, never a failed landing, since
    the landing's commit has already landed.
    """
    from cratekit.core.cause import CratekitError
    from cratekit.modules.outbound import pairs

    if not written:
        return []
    store = pairs.PairStore(cfg)
    unpaired: list[str] = []
    for one in written:
        try:
            # U221. A LANDING'S TWIN HOLDS NOTHING: the sweep that landed it
            # was the choice to download that playlist.
            store.mark(
                one.account_id, one.playlist_id, name=one.account_name, twin=True, on_hold={}
            )
        except CratekitError as exc:
            unpaired.append(
                f"{one.folder} / {one.name} ({exc.cause.message}); pair it with crate sync "
                f"pair {one.account_id} --rekordbox {one.playlist_id}"
            )
    notes = [
        {
            "code": LANDED,
            "message": (
                f"{len(written) - len(unpaired)} custom playlist twin(s) written and paired: "
                + ", ".join(f"{one.folder} / {one.name} ({one.tracks})" for one in written)
            ),
        }
    ]
    if unpaired:
        notes.append(
            {
                "code": LANDED_UNPAIRED,
                "message": (
                    f"{len(unpaired)} twin(s) were written and not paired: "
                    + "; ".join(unpaired)
                ),
            }
        )
    return notes


#: The landing's notes on its twins.
LANDED = "custom-playlist-twins-landed"
LANDED_UNPAIRED = "custom-playlist-twins-unpaired"


__all__ = [
    "AMBIGUOUS",
    "CREATE",
    "LANDED",
    "LANDED_UNPAIRED",
    "FOLDER_PREFIX",
    "LEFT",
    "NOT_OWNED",
    "RECORD_KEY",
    "WORKFLOW",
    "Backfill",
    "Folder",
    "LandedTwin",
    "LandingTwin",
    "Library",
    "Made",
    "Miss",
    "Twin",
    "Written",
    "addition_violations",
    "assert_confined",
    "assert_read_back",
    "candidates",
    "facts",
    "find_folder",
    "folder_name",
    "matched",
    "pair_backfilled",
    "pair_landed",
    "plan_landing",
    "payload",
    "place",
    "plan_backfill",
    "read_library",
    "recheck",
    "recheck_landing",
    "twin_name",
    "write",
    "write_landing",
]
