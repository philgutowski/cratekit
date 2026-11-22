"""The native landing's readers of INBOX, the collection and the session log.

Every name here is reached through :mod:`cratekit.intake.native` as well.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from cratekit.core import config, locations, rb_writer, session
from cratekit.intake import set_playlist
from cratekit.intake.native import (
    _ORIGIN,
    ANALYZE,
    BATCH_PLAYLIST_KEY,
    DYN_VALUE,
    INBOX_JOB_KEY,
    PASS_KEY,
    WORKFLOW,
)
from cratekit.write import trees


def _committed(record: session.SessionRecord) -> bool:
    """Whether ``record`` is closed and its source committed."""
    return (
        record.state is session.SessionState.CLOSED
        and str(session.SourceState.COMMITTED) in record.sources.values()
    )


def _live_child(db: Any, playlist_id: str, root_id: str) -> Any | None:
    """The playlist ``playlist_id`` when it is live and directly under the root, else None."""
    row = db.get_playlist(ID=playlist_id)
    if (
        row is None
        or rb_writer.is_folder(row)
        or rb_writer.node_removed(row)
        or str(getattr(row, "ParentID", "") or "") != root_id
    ):
        return None
    return row


def recorded_inbox_playlist(
    cfg: config.Config, db: Any, job_id: str, root_id: str
) -> tuple[str, str] | None:
    """The INBOX playlist an earlier landing made for this set job, its id and name.

    THE SESSION RECORD IS THE JOB'S MEMORY OF IT (U135): the newest committed
    landing whose batch playlist names this job. One gone, removed or moved
    from under the root is no answer, and the write finds or makes one by name.
    """
    records, _unreadable = session.scan_log(cfg)
    found = [
        record
        for record in records
        if _committed(record)
        and isinstance(record.detail.get(BATCH_PLAYLIST_KEY), Mapping)
        and record.detail[BATCH_PLAYLIST_KEY].get(INBOX_JOB_KEY) == job_id
    ]
    for record in sorted(found, key=lambda one: one.session_id, reverse=True):
        kept = record.detail[BATCH_PLAYLIST_KEY]
        playlist_id = str(kept.get("id") or "")
        row = _live_child(db, playlist_id, root_id) if playlist_id else None
        if row is not None:
            return playlist_id, str(getattr(row, "Name", "") or kept.get("name") or "")
    return None


def leftover_set_inbox(
    cfg: config.Config,
    db: Any,
    job_id: str,
    root_id: str,
    set_name: str,
    *,
    keep_id: str = "",
) -> tuple[str, ...]:
    """INBOX playlist names that look like earlier parts of this set from before U135.

    A numbered twin of the set's name (``Name 2``) under the root, or a batch
    playlist an earlier ``--set`` landing of this job wrote before the record
    carried the job key. Shown to the author, never joined automatically.
    """
    named: list[str] = []
    prefix = set_name + " "
    for held in inbox_held(db, root_id):
        if held == set_name:
            continue
        if held.startswith(prefix) and held[len(prefix) :].isdigit():
            named.append(held)
    records, _unreadable = session.scan_log(cfg)
    for record in records:
        if not _committed(record):
            continue
        kept_set = record.detail.get(set_playlist.RECORD_KEY)
        batch = record.detail.get(BATCH_PLAYLIST_KEY)
        if not isinstance(kept_set, Mapping) or kept_set.get("job") != job_id:
            continue
        if not isinstance(batch, Mapping) or batch.get(INBOX_JOB_KEY):
            continue
        playlist_id = str(batch.get("id") or "")
        name = str(batch.get("name") or "")
        if not name or name == set_name or playlist_id == keep_id:
            continue
        if playlist_id:
            row = _live_child(db, playlist_id, root_id)
            if row is None:
                continue
            name = str(getattr(row, "Name", "") or name)
        if name and name not in named:
            named.append(name)
    return tuple(named)


def analyze_playlist(db: Any, root_id: str) -> Any | None:
    """The live, ordinary :data:`ANALYZE` playlist directly under the root, or None (U166).

    THE ONE FIND, for the landing that fills it and the clear that empties it.
    A removed node, a folder or a smart playlist of the name is not it; of two
    live ones the first the table lists is taken.
    """
    for row in list(db.get_playlist(Name=ANALYZE)):
        if str(getattr(row, "ParentID", "") or "") != str(root_id):
            continue
        if rb_writer.node_removed(row) or int(getattr(row, "Attribute", -1)) != 0:
            continue
        return row
    return None


def inbox_held(db: Any, root_id: str) -> tuple[str, ...]:
    """Every name a live node anywhere under the intake root carries (U113).

    What account playlists are named against: every descendant, so a batch
    rotated into ``Old`` still holds its name. A removed node holds none, since
    an account playlist is created and never found by name.
    """
    return tuple(str(getattr(row, "Name", "") or "") for row in inbox_nodes(db, root_id))


def inbox_nodes(db: Any, root_id: str) -> tuple[Any, ...]:
    """Every live node anywhere under the intake root, folders included, in walk order.

    THE ONE WALK of what INBOX holds, for :func:`inbox_held` and the refill
    (U134), from one read of the table.
    """
    children: dict[str, list[Any]] = {}
    for row in list(db.get_playlist()):
        if not rb_writer.node_removed(row):
            children.setdefault(str(getattr(row, "ParentID", "") or ""), []).append(row)
    found: list[Any] = []
    pending = [str(root_id)]
    while pending:
        for row in children.get(pending.pop(), ()):
            found.append(row)
            pending.append(str(row.ID))
    return tuple(found)


def _holding(match: trees.RowMatch) -> str | None:
    """The active row a match names, the first of several when two claim it."""
    if match.content_id:
        return str(match.content_id)
    if match.content_ids:
        return str(match.content_ids[0])
    return None


def candidate_rows(db: Any, names: Iterable[str]) -> list[trees.ContentRow]:
    """The active rows whose stored path ends in one of ``names``, as the matcher reads them.

    A CANDIDATE SET, NOT THE ANSWER: found by the file name, the one part of a
    path the base drive and the mounted spelling share, then put through the
    plan's resolver, so a handful of rows is read instead of the collection.
    """
    from pyrekordbox.db6 import tables

    found: list[trees.ContentRow] = []
    for name in set(names):
        query = db.session.query(tables.DjmdContent).filter(
            tables.DjmdContent.FolderPath.like(f"%{name}")
        )
        for row in query.all():
            found.append(
                trees.ContentRow(
                    content_id=str(row.ID),
                    recorded=str(getattr(row, "FolderPath", "") or ""),
                    deleted=trees.soft_delete_marker(row),
                )
            )
    return found


def _matches(db: Any, cfg: config.Config, paths: Sequence[Path]) -> list[trees.RowMatch]:
    """Each of ``paths`` matched against its candidate rows, by the one rule for a path."""
    prefix_map = [locations.PrefixRule(a, b) for a, b in cfg.resolved_prefix_map()]
    return trees.match_active_rows(
        list(paths),
        candidate_rows(db, (path.name for path in paths)),
        root=cfg.library.root,
        prefix_map=prefix_map,
    )


def content_ids_for(db: Any, cfg: config.Config, paths: Sequence[Path]) -> dict[str, str]:
    """The active row holding each of ``paths``, by path, paths no row holds left out.

    Two active rows on one path answer the first, which the matcher surfaces
    for the person to tidy.
    """
    found: dict[str, str] = {}
    for path, match in zip(paths, _matches(db, cfg, paths)):
        held = _holding(match)
        if held is not None:
            found[str(path)] = held
    return found


def single_rows_for(db: Any, cfg: config.Config, paths: Sequence[Path]) -> dict[str, str]:
    """The one active row holding each of ``paths``, by path, a path two rows claim left out.

    :func:`content_ids_for` WITHOUT ITS FALLBACK, for a reader that must not
    guess: an owned playlist member (U128) or heart (U146) never takes
    whichever duplicate came first.
    """
    return {
        str(path): str(match.content_id)
        for path, match in zip(paths, _matches(db, cfg, paths))
        if match.outcome is trees.MatchOutcome.MATCHED and match.content_id
    }


def dyn_marked(db: Any) -> frozenset[str]:
    """Every content row carrying a live My Tag value named :data:`DYN_VALUE`.

    THE ONE READER OF THE MARK, for ``crate analyze check`` and the landing's
    read back, so the two agree on what is marked.
    """
    marked: set[str] = set()
    for tag in db.get_my_tag(Name=DYN_VALUE):
        if rb_writer.soft_deleted(
            tag,
            message=(
                f"the My Tag row {getattr(tag, 'ID', '?')!r} cannot say whether rekordbox "
                f"removed it, so which rows are marked {DYN_VALUE} was not read"
            ),
            origin=_ORIGIN,
            detail={"my_tag_id": str(getattr(tag, "ID", ""))},
        ):
            continue
        for song in db.get_my_tag_songs(MyTagID=str(tag.ID)):
            if rb_writer.soft_deleted(
                song,
                message=(
                    f"the My Tag membership {getattr(song, 'ID', '?')!r} cannot say whether "
                    f"rekordbox removed it, so which rows are marked {DYN_VALUE} was not read"
                ),
                origin=_ORIGIN,
                detail={"song_my_tag_id": str(getattr(song, "ID", ""))},
            ):
                continue
            marked.add(str(song.ContentID))
    return frozenset(marked)


def live_inbox_named(db: Any, name: str, root_id: str) -> bool:
    """Whether a live (not removed) playlist of ``name`` sits under the intake root."""
    for row in list(db.get_playlist(Name=name)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == str(root_id):
            return True
    return False


def landed_passes(cfg: config.Config) -> tuple[str, ...]:
    """Every pass name a closed native landing committed, in name order (U174).

    The native counterpart of the intake files ``crate organize`` reads
    (R-915), by the rule :func:`landings_of_pass` proves. Every pass's name,
    a label's or a set's too: which a sync pass owns is the mark's to decide.
    Read through :func:`cratekit.core.session.records`, so a log this account
    cannot list refuses rather than reading as no landing (R-1255).
    """
    records = session.records(cfg)
    return tuple(
        sorted(
            {
                str(record.detail.get(PASS_KEY))
                for record in records
                if record.workflow == WORKFLOW
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
        )
    )


def landings_of_pass(cfg: config.Config, name: str) -> tuple[str, ...]:
    """The session ids of every closed native landing that committed ``name``.

    THE PROOF ``sync mark --pass`` WAITS FOR (R-777): a landing refused after
    its moves records no pass, so its files cannot mark a playlist by being on
    disk. A log this account cannot list refuses (R-1255): read as no landing,
    ``sync mark --pass`` would send a person to
    land the pass again.
    """
    records = session.records(cfg)
    return tuple(
        sorted(
            record.session_id
            for record in records
            if record.workflow == WORKFLOW
            and record.state is session.SessionState.CLOSED
            and str(session.SourceState.COMMITTED) in record.sources.values()
            and record.detail.get(PASS_KEY) == name
        )
    )
