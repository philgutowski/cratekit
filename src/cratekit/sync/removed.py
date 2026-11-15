"""Which downloaded tracks the account no longer lists, and which would leave the collection (U287).

A pass sweeps the playlists the author made on the streaming account, and its
landing gives each an INBOX playlist of the tracks the library holds (U113,
U128). When Phillip later takes a track off one of those playlists on the
account, nothing in Cratekit noticed: ``sync pair`` refuses a playlist under
INBOX by design, and the INBOX refill (U134) reads the pass's recorded reports,
never the account. This module is the noticing. It reads every downloaded
playlist again, finds each track its pass recorded that the account no longer
lists, resolves it to its collection row, and answers each row as OFFERED for
removal from the collection or KEPT, with why. It writes nothing anywhere: no
row, no file, no account write, no record. U288's gate shows this plan and
binds to its digest.

WHAT IS DOWNLOADED. An account playlist an ``intake.playlist`` job with a
recorded name succeeded for, whose pass has a standing landing record naming
it by the account's identifier and the pass (U128's ``inbox_playlists``
entry). A job no landing names is not downloaded, since nothing of it reached
the collection. What is SYNCED, for the question "is it still on another
synced playlist", is wider: every playlist the sweep's cursor holds, every one
the mark record holds as taken, every one ``sync pair`` keeps, every
downloaded one, and the account's hearts, which the favourites source brings
into All Favorites.

A PARTIAL READ OFFERS NOTHING, the deletion pass's rule (R37) applied to the
account. "Still on another synced playlist" is a claim about every synced
playlist, and a playlist that could not be read, read short of the count the
provider declares, or read with no tracks while nothing says it holds none,
contributes nothing to it, so the claim would pass on absence of evidence. So
while any synced playlist is not read whole, every row that would be offered
is kept, and the plan says which playlists stopped it. A playlist the
account's own listing no longer names, and that cannot be opened by its id
either, is GONE: two reads agreeing, since the listing alone stops on an empty
page with no total to check it against (R-385). Its tracks are offered
nothing, since deleting a playlist whole is not taking a track off it, and it
keeps no other track. A playlist the listing omits and its id still opens is
read as any other.

A TRACK IS REMOVED when its playlist's listing holds no row of its provider
id, and no read row of it carries its ISRC or its artist and title as the
matcher folds a recording, version excluded. The same rule says whether
another synced playlist still holds it. Each test can only say "still there",
so every one of them errs toward keeping.

EACH ROW GETS ONE ANSWER, the first that holds of these:

* ``left``: the library holds no row for the track, two rows claim its file,
  or a person's question about it is unanswered, as the backfill's resolver
  says (U121, U144), or the report never carried a file at all;
* ``kept, held before the pass``: the report says the library already owned it
  when the job ran, so a person or another pass brought it in;
* ``kept, not this pass's file``: the row's file is not under a folder a
  standing landing of its pass recorded filing into (``filed_batch``), so the
  match found a file this pass did not bring;
* ``kept, on another synced playlist``;
* ``kept, in a playlist of yours``: a live membership anywhere but the intake
  tree, the routing tree, a label year playlist its pass's landing recorded,
  or the custom playlist twin a landing recorded for a playlist it left;
* ``offered``.

One collection row reached from two playlists, or two passes, is one answer
naming each playlist it left, and it is offered when ANY report says its pass
brought the file, since a later pass reads an earlier pass's download as
owned.

Layer: modules. It reads configuration through the objects it is handed and
opens no database of its own; the verb hands it a read only copy.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import Any

from cratekit.acquire import match
from cratekit.cli.output import digest_of
from cratekit.core import config, jobs, locations, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.intake import account_playlists, ingest, label_filing, native, refill, set_playlist
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from cratekit.sync import playlists, twins
from cratekit.sync.watermarks import WatermarkStore

#: The three answers a row can get.
OFFERED = "offered"
KEPT = "kept"
LEFT = "left"

#: Why a removed track's row is kept, as the screen says it.
HELD_BEFORE = "held before the pass"
NOT_THIS_PASS = "not this pass's file"
ON_ANOTHER = "on another synced playlist"
IN_YOURS = "in a playlist of yours"
PARTIAL_READ = "not offered while a synced playlist could not be read whole"

#: Why a removed track has no row to answer, beside the resolver's own reasons.
NOT_CARRIED = "the pass never downloaded it"
OWNED_NO_ROW = "held before the pass, and no collection row holds its file now"

#: How each synced playlist read. Only ``read`` answers anything; ``gone`` is an
#: answer about the playlist, and the other three are a read that is not whole.
READ = "read"
GONE = "gone"
UNREADABLE = "unreadable"
SHORT = "short"
EMPTY = "empty"
NOT_WHOLE = frozenset({UNREADABLE, SHORT, EMPTY})

_STANDING = frozenset(
    {
        session.SessionState.AWAITING_IMPORT,
        session.SessionState.COMMITTED_UNVERIFIED,
        session.SessionState.CLOSED,
    }
)


@dataclass(frozen=True, slots=True)
class Downloaded:
    """One account playlist a pass downloaded and landed, every report in the account's order."""

    account: str
    name: str
    pass_name: str
    job_id: str
    rows: tuple[account_playlists.Row, ...] = ()


@dataclass(frozen=True, slots=True)
class Listing:
    """One synced playlist as the account lists it now, or why it could not say."""

    account: str
    name: str
    state: str
    why: str = ""
    #: Every provider id the listing holds, a refused row's included.
    refs: frozenset[str] = frozenset()
    isrcs: frozenset[str] = frozenset()
    #: Every read row's artist and title, folded as a recording, version excluded.
    recordings: frozenset[str] = frozenset()

    def holds(self, wanted: match.Wanted) -> bool:
        """Whether this listing still holds the track, by any of the three tests."""
        if self.state != READ:
            return False
        if wanted.ref and wanted.ref in self.refs:
            return True
        if wanted.isrc and wanted.isrc.strip().upper() in self.isrcs:
            return True
        return recording(wanted) in self.recordings

    def identity(self) -> dict[str, Any]:
        return {"account": self.account, "name": self.name, "state": self.state, "why": self.why}


@dataclass(frozen=True, slots=True)
class Answer:
    """One collection row a removal reached, or one removed track with no row, and its answer."""

    answer: str
    why: str
    artist: str
    title: str
    content_id: str = ""
    file: str = ""
    #: The account playlists the track was taken off, by name, each once.
    removed_from: tuple[str, ...] = ()
    #: What keeps it: the other synced playlists, or the rekordbox playlists.
    kept_by: tuple[str, ...] = ()

    def identity(self) -> dict[str, Any]:
        return {
            "answer": self.answer,
            "why": self.why,
            "artist": self.artist,
            "title": self.title,
            "content_id": self.content_id,
            "file": self.file,
            "removed_from": list(self.removed_from),
            "kept_by": list(self.kept_by),
        }


@dataclass(frozen=True, slots=True)
class RemovedPlan:
    """What ``sync removed`` found, every playlist and every row named, digested."""

    listings: tuple[Listing, ...] = ()
    answers: tuple[Answer, ...] = ()
    #: A synced playlist was not read whole, so nothing is offered.
    partial: bool = False
    #: Session records that could not be read; a record names what the pass made.
    unreadable: int = 0
    digest: str = ""

    @property
    def offered(self) -> tuple[Answer, ...]:
        return tuple(one for one in self.answers if one.answer == OFFERED)

    def count(self, answer: str) -> int:
        return sum(1 for one in self.answers if one.answer == answer)


def identity(plan: RemovedPlan) -> dict[str, Any]:
    """What the digest covers: every playlist read, every answer, and the partial flag."""
    return {
        "kind": "sync-removed",
        "playlists": [one.identity() for one in plan.listings],
        "answers": [one.identity() for one in plan.answers],
        "partial": plan.partial,
        "unreadable": plan.unreadable,
    }


def recording(wanted: match.Wanted) -> str:
    """The track's artist and title folded as a recording, version excluded."""
    return match.recording_identity(wanted.artist, wanted.title)


def _standing(records: Iterable[session.SessionRecord]) -> list[session.SessionRecord]:
    return [
        one
        for one in records
        if one.workflow == ingest.INTAKE_WORKFLOW and one.state in _STANDING
    ]


def downloaded(cfg: config.Config, records: Sequence[session.SessionRecord]) -> tuple[Downloaded, ...]:
    """Every account playlist a pass downloaded and a standing landing of that pass names.

    THE LANDING RECORD DECIDES, never the job alone: a pass whose files never
    landed put nothing in the collection to remove. Only an entry carrying the
    account's identifier counts, which every landing since U128 writes.
    """
    entries = [one for one in refill.recorded_entries(records) if one.account and one.pass_name]
    found: list[Downloaded] = []
    named: list[tuple[jobs.Job, str, str]] = []
    for pass_name in dict.fromkeys(one.pass_name for one in entries):
        for job, name in account_playlists.playlist_jobs(cfg, pass_name):
            account = account_playlists.account_of(job)
            if account and any(
                refill.ours(one, pass_name=pass_name, account=account, name=name)
                for one in entries
            ):
                named.append((job, name, pass_name))
    if not named:
        return ()
    with jobs.open_store() as store:
        for job, name, pass_name in named:
            source = account_playlists.read_source(store, job, name)
            found.append(
                Downloaded(
                    account=source.playlist_id,
                    name=name,
                    pass_name=pass_name,
                    job_id=job.job_id,
                    rows=source.rows,
                )
            )
    return tuple(found)


def synced(
    cfg: config.Config, found: Sequence[Downloaded], *, paired: Iterable[str] = ()
) -> tuple[str, ...]:
    """Every synced account playlist, the downloaded ones first, each once.

    THE TAKEN RECORD IS READ, AND REFUSES WHEN IT CANNOT BE: an unread record
    is a set of synced playlists nobody can name, and "on no other synced
    playlist" would be claimed over it.
    """
    existing = WatermarkStore(cfg).read(playlists.SOURCE_ID)
    swept = tuple(existing.swept) if existing is not None else ()
    taken = tuple(sorted(playlists.taken_ids(cfg)))
    return tuple(
        dict.fromkeys(
            [
                *(one.account for one in found),
                *swept,
                *taken,
                *sorted(str(one) for one in paired),
            ]
        )
    )


def read_one(
    found: catalogue.Catalogue, account: str, listed: Mapping[str, catalogue.AccountPlaylist]
) -> Listing:
    """One synced playlist read through the sweep's own reader, or why it is not read whole."""
    shown = listed.get(account)
    name = shown.name if shown is not None else ""
    try:
        readable = intake_cli.list_playlist_readable(found, account)
    except CratekitError as exc:
        if exc.cause.reason not in playlists.PER_PLAYLIST_REASONS:
            raise
        if shown is None:
            # GONE ONLY WHEN TWO READS AGREE. The account's list stops on an
            # empty page and publishes no total (R-385), so its silence alone
            # is weak evidence, and a gone playlist keeps no other track; a
            # playlist it omits is opened by its id as well.
            return Listing(
                account=account,
                name=name,
                state=GONE,
                why="the account no longer lists it, and it cannot be opened by its id",
            )
        return Listing(account=account, name=name, state=UNREADABLE, why=exc.cause.message)
    if readable.short is not None:
        block = readable.short.block()
        return Listing(
            account=account,
            name=name,
            state=SHORT,
            why=f"listed {block.get('listed')} of the {block.get('declared')} tracks it declares",
        )
    if not readable.order and (shown is None or shown.tracks != 0):
        # AN EMPTY READ IS TRUSTED ONLY WHEN THE ACCOUNT'S OWN LISTING SAYS NONE,
        # two answers agreeing; an unknown count beside an empty read is the
        # shape a provider fault takes, and every track would read removed.
        return Listing(
            account=account,
            name=name,
            state=EMPTY,
            why="read with no tracks and nothing says it holds none",
        )
    wanted = [intake_cli.thawed(one) for one in readable.tracks.values()]
    return Listing(
        account=account,
        name=name,
        state=READ,
        refs=frozenset(str(one) for one in readable.order),
        isrcs=frozenset(one.isrc.strip().upper() for one in wanted if one.isrc),
        recordings=frozenset(recording(one) for one in wanted),
    )


def account_listing(found: catalogue.Catalogue) -> dict[str, catalogue.AccountPlaylist]:
    """The account's own playlists by identifier, or the sweep's refusal for an unread list.

    AN UNREAD LIST REFUSES THE WHOLE VERB rather than reading every playlist
    as gone, which is the shape a provider fault would otherwise take.
    """
    return {one.playlist_id: one for one in playlists.account_listing(found)}


#: The account's hearts, read as one more synced listing.
HEARTS = "hearts"
HEARTS_NAME = "the account's hearts"


def read_hearts(found: catalogue.Catalogue) -> Listing:
    """The account's hearts as one more synced listing, through the favourites source's reader.

    A HEART KEEPS A TRACK as a synced playlist does: the favourites source
    brings every heart into All Favorites, and a heart made since the last
    ``sync favorites`` is in no rekordbox playlist yet. Read whole or not at
    all, by the rules a playlist is: unreadable, short of what the account
    declares, or empty, and nothing is offered.
    """
    try:
        frozen, short = intake_cli.list_favorites(found)
    except CratekitError as exc:
        if exc.cause.reason not in playlists.PER_PLAYLIST_REASONS:
            raise
        return Listing(account=HEARTS, name=HEARTS_NAME, state=UNREADABLE, why=exc.cause.message)
    if short is not None:
        return Listing(
            account=HEARTS,
            name=HEARTS_NAME,
            state=SHORT,
            why="listed fewer hearts than the account declares",
        )
    if not frozen:
        return Listing(
            account=HEARTS,
            name=HEARTS_NAME,
            state=EMPTY,
            why="read with no hearts and nothing says it holds none",
        )
    wanted = [intake_cli.thawed(one) for one in frozen.values()]
    return Listing(
        account=HEARTS,
        name=HEARTS_NAME,
        state=READ,
        refs=frozenset(str(one) for one in frozen),
        isrcs=frozenset(one.isrc.strip().upper() for one in wanted if one.isrc),
        recordings=frozenset(recording(one) for one in wanted),
    )


def read_account(
    found: catalogue.Catalogue,
    wanted: Sequence[str],
    *,
    listed: Mapping[str, catalogue.AccountPlaylist],
) -> dict[str, Listing]:
    """Each playlist in ``wanted`` read once, against the account's listing read once."""
    return {account: read_one(found, account, listed) for account in dict.fromkeys(wanted)}


def removals(
    found: Sequence[Downloaded], reads: Mapping[str, Listing]
) -> tuple[tuple[Downloaded, account_playlists.Row], ...]:
    """Every recorded report whose playlist was read and no longer holds it, in the account's order."""
    return tuple(
        (one, row)
        for one in found
        if one.account in reads and reads[one.account].state == READ
        for row in one.rows
        if not reads[one.account].holds(row.wanted)
    )


def _filed_folders(records: Iterable[session.SessionRecord]) -> dict[str, tuple[str, ...]]:
    """The batch folders each pass's standing landings recorded filing into, by pass."""
    folders: dict[str, list[str]] = {}
    for record in _standing(records):
        pass_name = str(record.detail.get(native.PASS_KEY) or "")
        filed = record.detail.get(native.FILED_BATCH_KEY)
        if pass_name and isinstance(filed, Mapping) and filed.get("folder"):
            folders.setdefault(pass_name, []).append(str(filed["folder"]))
    return {key: tuple(dict.fromkeys(value)) for key, value in folders.items()}


def _under(path: str, folders: Iterable[str]) -> bool:
    """Whether ``path`` sits under one of ``folders``, compared in one Unicode form."""
    held = locations.norm_for_compare(str(path))
    for folder in folders:
        root = locations.norm_for_compare(str(folder)).rstrip("/\\")
        if root and (held.startswith(root + "/") or held.startswith(root + "\\")):
            return True
    return False


def _label_years(records: Iterable[session.SessionRecord]) -> dict[str, frozenset[str]]:
    """The label year playlists each pass's standing landings recorded filing into, by pass."""
    years: dict[str, set[str]] = {}
    for record in _standing(records):
        pass_name = str(record.detail.get(native.PASS_KEY) or "")
        filed = record.detail.get(label_filing.RECORD_KEY)
        if not pass_name or not isinstance(filed, list):
            continue
        for entry in filed:
            if isinstance(entry, Mapping) and entry.get("id"):
                years.setdefault(pass_name, set()).add(str(entry["id"]))
    return {key: frozenset(value) for key, value in years.items()}


def _twins(records: Iterable[session.SessionRecord]) -> dict[str, frozenset[str]]:
    """The custom playlist twins standing landings recorded, by the account playlist they copy."""
    found: dict[str, set[str]] = {}
    for record in _standing(records):
        entries = record.detail.get(twins.RECORD_KEY)
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if (
                isinstance(entry, Mapping)
                and entry.get("id")
                and entry.get(ingest.INBOX_ACCOUNT_KEY)
            ):
                found.setdefault(str(entry[ingest.INBOX_ACCOUNT_KEY]), set()).add(str(entry["id"]))
    return {key: frozenset(value) for key, value in found.items()}


def _routing_nodes(db: Any, declared: taxonomy.Taxonomy, registry: tree_registry.Registry) -> frozenset[str]:
    """Every live node of the routing tree, when the registry holds it database native.

    A ROUTING TREE STILL ON THE BRIDGE, OR ONE WHOSE ROOT CANNOT BE ANCHORED,
    NAMES NOTHING: its playlists cannot be told from a person's by identifier,
    so a membership in one keeps the row, which is the side that removes less.
    """
    tree_id = declared.tree.id
    if not registry.is_database_native(tree_id):
        return frozenset()
    try:
        root = tree_registry.anchored_root(
            tree_id, registry, root_exists=lambda root_id: db.get_playlist(ID=root_id) is not None
        )
    except CratekitError:
        return frozenset()
    return frozenset({str(root), *(str(row.ID) for row in native.inbox_nodes(db, str(root)))})


def memberships(db: Any, content_ids: Iterable[str]) -> dict[str, tuple[tuple[str, str], ...]]:
    """Each row's live memberships in live playlists, as (playlist id, name), from SQL."""
    from sqlalchemy import bindparam, text

    wanted = sorted({str(one) for one in content_ids})
    if not wanted:
        return {}
    statement = text(
        f"SELECT sp.ContentID, sp.PlaylistID, p.Name FROM {rb_writer.MEMBERSHIP_TABLE} sp "
        f"JOIN {rb_writer.PLAYLIST_TABLE} p ON p.ID = sp.PlaylistID "
        f"WHERE COALESCE(sp.{rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 "
        f"AND COALESCE(p.{rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 "
        f"AND sp.ContentID IN :ids ORDER BY sp.ContentID, p.ID"
    ).bindparams(bindparam("ids", expanding=True))
    held: dict[str, list[tuple[str, str]]] = {}
    for content_id, playlist_id, name in db.session.execute(statement, {"ids": wanted}).fetchall():
        held.setdefault(str(content_id), []).append((str(playlist_id), str(name or "")))
    return {key: tuple(value) for key, value in held.items()}


@dataclass
class _Reached:
    """Everything the removals said about one collection row, gathered before it is answered."""

    content_id: str
    file: str
    artist: str
    title: str
    passes: list[str] = field(default_factory=list)
    accounts: list[str] = field(default_factory=list)
    removed_from: list[str] = field(default_factory=list)
    wanted: list[match.Wanted] = field(default_factory=list)
    brought: bool = False
    carried: bool = False


def plan_removed(
    cfg: config.Config,
    db: Any,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
    records: Sequence[session.SessionRecord],
    found: Sequence[Downloaded],
    reads: Mapping[str, Listing],
    unreadable: int = 0,
) -> RemovedPlan:
    """Answer every removed track against the library as it is now. Reads, writes nothing."""
    listings = tuple(reads.values())
    partial = any(one.state in NOT_WHOLE for one in listings)
    removed = removals(found, reads)
    answers: list[Answer] = []
    reached: dict[str, _Reached] = {}
    if removed:
        intake_root = refill.anchored_root(db, declared.intake.id, registry)
        own_nodes = frozenset(
            {str(intake_root), *(str(row.ID) for row in native.inbox_nodes(db, str(intake_root)))}
        ) | _routing_nodes(db, declared, registry)
        folders = _filed_folders(records)
        collection = set_playlist.collection_rows(cfg, db)
        matches = set_playlist.library_matches(cfg, db)
        for one, row in removed:
            wanted = row.wanted
            if row.state == account_playlists.OWNED:
                content_id, path, why = collection(row.paths)
            elif row.carried:
                content_id, path, why = matches(wanted)
            else:
                content_id, path, why = "", "", row.state or NOT_CARRIED
            if not content_id:
                answers.append(
                    Answer(
                        answer=LEFT,
                        why=(OWNED_NO_ROW if row.state == account_playlists.OWNED else why),
                        artist=wanted.artist,
                        title=wanted.listed,
                        removed_from=(one.name,),
                    )
                )
                continue
            held = reached.setdefault(
                content_id,
                _Reached(content_id=content_id, file=path, artist=wanted.artist, title=wanted.listed),
            )
            held.passes.append(one.pass_name)
            held.accounts.append(one.account)
            held.removed_from.append(one.name)
            held.wanted.append(wanted)
            if row.carried:
                held.carried = True
                if _under(path, folders.get(one.pass_name, ())):
                    held.brought = True
        years = _label_years(records)
        made = _twins(records)
        members = memberships(db, reached)
        for held in reached.values():
            own = own_nodes.union(
                *(years.get(name, frozenset()) for name in held.passes),
                *(made.get(account, frozenset()) for account in held.accounts),
            )
            answers.append(
                _answer(held, reads=listings, held_by=members.get(held.content_id, ()), own=own, partial=partial)
            )
    plan = RemovedPlan(
        listings=listings,
        answers=tuple(answers),
        partial=partial,
        unreadable=unreadable,
    )
    return replace(plan, digest=digest_of(identity(plan)))


def _answer(
    held: _Reached,
    *,
    reads: Sequence[Listing],
    held_by: Sequence[tuple[str, str]],
    own: frozenset[str],
    partial: bool,
) -> Answer:
    """The one answer a reached row gets, the first of the kept reasons that holds."""
    shown = Answer(
        answer=KEPT,
        why="",
        artist=held.artist,
        title=held.title,
        content_id=held.content_id,
        file=held.file,
        removed_from=tuple(dict.fromkeys(held.removed_from)),
    )
    if not held.carried:
        return replace(shown, why=HELD_BEFORE)
    if not held.brought:
        return replace(shown, why=NOT_THIS_PASS)
    still = tuple(
        dict.fromkeys(
            one.name or one.account
            for one in reads
            if any(one.holds(wanted) for wanted in held.wanted)
        )
    )
    if still:
        return replace(shown, why=ON_ANOTHER, kept_by=still)
    yours = tuple(dict.fromkeys(name or playlist_id for playlist_id, name in held_by if playlist_id not in own))
    if yours:
        return replace(shown, why=IN_YOURS, kept_by=yours)
    if partial:
        return replace(shown, why=PARTIAL_READ)
    return replace(shown, answer=OFFERED)


__all__ = [
    "EMPTY",
    "GONE",
    "HEARTS",
    "HELD_BEFORE",
    "IN_YOURS",
    "KEPT",
    "LEFT",
    "NOT_THIS_PASS",
    "OFFERED",
    "ON_ANOTHER",
    "PARTIAL_READ",
    "READ",
    "SHORT",
    "UNREADABLE",
    "Answer",
    "Downloaded",
    "Listing",
    "RemovedPlan",
    "account_listing",
    "downloaded",
    "identity",
    "memberships",
    "plan_removed",
    "read_account",
    "read_hearts",
    "read_one",
    "recording",
    "removals",
    "synced",
]
