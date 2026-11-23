"""Take rekordbox's key and tempo into a landed track's head, after the visit (U327).

Cratekit stamps a head before rekordbox has analysed anything; this corrects it
afterwards, on Phillip's decision of 2026-11-22 that rekordbox's key and tempo
are the more reliable. **The key is the Key column's**, padded Camelot, and
wins on any difference, one step included. **The tempo is the BPM column's**,
rounded half up, and wins only when the head is more than one beat away.
Only those two spans of the leading head are spliced: every other byte of a
title, the lossy marker and the body included, stays as it was.

THREE SURFACES, ONE ANSWER: the database ``Title``, the file's title tag (its
own head spliced, so a run stopped after the files is continued by planning
again) and the file's ``initialkey``. THE FILE NAME IS NEVER CHANGED, since no
verb renames a file the collection references; every reader of a head that
would put the file name's old head back reads the title tag's first.

WHAT IS NEVER WRITTEN: ``KeyID``, the BPM column, a grid, a tempo tag or an
average tempo, in any container. The tempo appears only as text in the head,
as the naming engine writes it (R17). The database write is ``Title`` and
nothing else, under :data:`cratekit.write.metadata.ADOPT_REKORDBOX_HEAD`.

THE SCOPE is ``analyze check``'s: a named pass or landing session, else INBOX /
Analyze. When that playlist is empty the scope is empty, never the check's fall
back to every unanalysed row, so the back catalogue is never in scope unasked.

Layer: modules. It opens no database of its own and names no verb.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.analysis import agreement
from cratekit.analysis import rekordbox_check as rc
from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    locations,
    rb_writer,
    session,
    tags,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import NameTemplate, parse_camelot, parse_head, split_head
from cratekit.intake import analyzed, native
from cratekit.write import metadata, row_defaults, trees

_ORIGIN = ("analysis", "head_adopt")

#: The name a session record carries for this write, and a digest is kinded by.
WORKFLOW = "analyze-adopt"

#: What the row write is filed under in a session record's change summary.
CHANGE_KEY = "content.title"

#: Where the session record keeps every surface's value before the write, so a
#: restore can put the files back beside the database.
RECORD_KEY = "head_adopt_before"

#: What each row in scope comes to, in the order a summary lists them.
ADOPT = "adopt"
AGREE = "agree"
HELD_OUT = "held-out"
NOT_ANALYSED = "not-analysed"
GONE = "gone"
NO_HEAD = "no-head"
NO_REFERENCE = "no-reference"
TAG_DIFFERS = "title-tag-differs"
FILE_MISSING = "file-missing"
FILE_UNREADABLE = "file-unreadable"
PATH_UNMAPPED = "path-unmapped"
NO_PATH = "no-path"

OUTCOMES: tuple[str, ...] = (
    ADOPT, AGREE, HELD_OUT, NOT_ANALYSED, GONE, NO_HEAD, NO_REFERENCE, TAG_DIFFERS,
    FILE_MISSING, FILE_UNREADABLE, PATH_UNMAPPED, NO_PATH,
)

#: The outcomes of a row that is left alone, each named with why.
LEFT: tuple[str, ...] = OUTCOMES[2:]

#: Why one half of rekordbox's answer could not be read: the other half still
#: counts, so these are notes on an item, never its outcome alone.
KEY_EMPTY = "key-empty"
KEY_NOT_CAMELOT = "key-not-camelot"
TEMPO_ZERO = "tempo-zero"
NOTES: tuple[str, ...] = (KEY_EMPTY, KEY_NOT_CAMELOT, TEMPO_ZERO)

#: What an item whose row is not written says it does.
LEAVE_ACTION = "leave"

#: How far, in whole beats, a head's tempo may sit from rekordbox's and stand:
#: the check's own rule, so the two never disagree about which rows differ.
TEMPO_TOLERANCE = rc.TEMPO_TOLERANCE
tempo_differs = rc.tempo_differs


# The answer, pure.


def reference_key(key_id: Any, scale_name: str | None) -> tuple[str | None, str]:
    """rekordbox's key as padded Camelot, or None and why: no key, or no Camelot key.

    Either notation of the Key column reads (``8A``, ``08A``, ``Am``).
    """
    if key_id in rb_writer.FIELD_EMPTIES["KeyID"] or not str(scale_name or "").strip():
        return None, KEY_EMPTY
    camelot = agreement.camelot_from_scale_name(scale_name)
    if camelot is None:
        return None, KEY_NOT_CAMELOT
    return camelot, ""


def reference_tempo(hundredths: Any) -> tuple[int | None, str]:
    """rekordbox's tempo as the whole number a head carries, or None and why.

    The column holds hundredths; 124.84 is 125, and 126.50 is 127.
    """
    tempo = rc.reference_tempo(hundredths)
    return (tempo, "") if tempo is not None else (None, TEMPO_ZERO)


def adopted(
    name: str, *, key: str | None, tempo: int | None, template: NameTemplate
) -> str | None:
    """``name`` with its leading head carrying ``key`` and ``tempo``, or None for no head.

    Only the key's span and the tempo's span are replaced, the key when it is
    another key than ``key`` (an unpadded spelling of the same key stands), the
    tempo when :func:`tempo_differs`. A ``None`` answer leaves its span alone.
    A body that itself begins like a head is body, never spliced.
    """
    parsed = parse_head(name, template=template)
    head, body = split_head(name, template=template)
    if not parsed or "key" not in parsed or "bpm" not in parsed or not head:
        return None
    # THE KEY LEADS THE HEAD (a tempo cannot, ``naming``'s anchor rule), so its
    # first occurrence is its span, and the tempo's is the first after it.
    written_key, written_tempo = parsed["key"], parsed["bpm"]
    key_start = head.find(written_key)
    key_end = key_start + len(written_key)
    tempo_start = head.find(written_tempo, key_end)
    tempo_end = tempo_start + len(written_tempo)
    new_key = written_key
    if key is not None and parse_camelot(written_key) != parse_camelot(key):
        new_key = key
    new_tempo = written_tempo
    if tempo is not None and tempo_differs(int(written_tempo), tempo):
        new_tempo = str(tempo)
    spliced = (
        head[:key_start]
        + new_key
        + head[key_end:tempo_start]
        + new_tempo
        + head[tempo_end:]
    )
    return spliced + body


# The plan.


@dataclass(frozen=True, slots=True)
class Item:
    """One row in scope: its three surfaces before and after, rekordbox's answer,
    and what the plan does with it. An after equal to its before is not written."""

    content_id: str
    action: str
    reason: str = ""
    notes: tuple[str, ...] = ()
    path: str = ""
    title: str = ""
    new_title: str = ""
    tag_title: str = ""
    new_tag_title: str = ""
    initialkey: str = ""
    new_initialkey: str = ""
    head_key: str | None = None
    key: str | None = None
    relation: str = rc.KEY_UNKEYED
    head_tempo: int | None = None
    #: rekordbox's tempo as the column holds it, in hundredths, and as the head would carry it.
    tempo_hundredths: int | None = None
    tempo: int | None = None

    @property
    def writes_title(self) -> bool:
        return self.new_title != self.title

    @property
    def writes_file(self) -> bool:
        return self.new_tag_title != self.tag_title or self.new_initialkey != self.initialkey

    def digested(self) -> dict[str, Any]:
        """What the digest covers: every value written and why a row is not.
        NOTHING THAT NAMES A COPY, so a rehearsal digests equal to the live plan."""
        return {
            "content_id": self.content_id,
            "action": self.action,
            "reason": self.reason,
            "notes": list(self.notes),
            "title": self.title,
            "new_title": self.new_title,
            "tag_title": self.tag_title,
            "new_tag_title": self.new_tag_title,
            "initialkey": self.initialkey,
            "new_initialkey": self.new_initialkey,
            "head_key": self.head_key,
            "key": self.key,
            "relation": self.relation,
            "head_tempo": self.head_tempo,
            "tempo_hundredths": self.tempo_hundredths,
            "tempo": self.tempo,
        }

    def to_json(self) -> dict[str, Any]:
        """The item as the gate shows it, with the file it was read from."""
        return {**self.digested(), "path": self.path}

    def before(self) -> dict[str, str]:
        """Every surface this item writes, as it stood, for the session record."""
        return {
            "content_id": self.content_id,
            "path": self.path,
            "title": self.title,
            "tag_title": self.tag_title,
            "initialkey": self.initialkey,
        }


@dataclass(frozen=True, slots=True)
class AdoptPlan:
    """Every row in scope as one item, the count of every outcome and note, and
    the ``--leave`` identifiers that named no row this plan writes."""

    scope: rc.Scope
    items: tuple[Item, ...]
    counts: Mapping[str, int]
    notes: Mapping[str, int]
    leave_unmatched: tuple[str, ...] = ()

    @property
    def writes(self) -> tuple[Item, ...]:
        return tuple(item for item in self.items if item.action == ADOPT)

    @property
    def rows(self) -> int:
        return len(self.items)

    @property
    def digest(self) -> str:
        """The fingerprint an approval is bound to: the scope, the items, the
        counts, never a path or a time."""
        return digest_of(
            {
                "kind": WORKFLOW,
                "scope": [self.scope.kind, self.scope.name],
                "items": [item.digested() for item in self.items],
                "counts": dict(self.counts),
                "notes": dict(self.notes),
                "leave_unmatched": list(self.leave_unmatched),
            }
        )

    def relations(self) -> dict[str, int]:
        """The key relation of every row whose head was compared with a key."""
        seen = Counter(item.relation for item in self.items if item.head_key and item.key)
        return {name: seen.get(name, 0) for name in (rc.KEY_EQUAL, rc.KEY_ONE_STEP, rc.KEY_FAR)}


def resolve_scope(
    cfg: config.Config,
    db: Any,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
    pass_name: str | None = None,
    session_id: str | None = None,
) -> rc.Scope:
    """The check's scope, less its fall back: an empty INBOX / Analyze is an empty scope."""
    if pass_name is not None or session_id is not None:
        return rc.resolve_scope(
            cfg, db, declared=declared, registry=registry, pass_name=pass_name, session_id=session_id
        )
    members, why = rc._analyze_members(db, declared, registry)
    return rc.Scope(
        kind=rc.SCOPE_ANALYZE,
        name=f"INBOX / {native.ANALYZE}",
        content_ids=members,
        passed_over=(why,) if why else (),
    )


def _resolved(cfg: config.Config, content: Any, rules: Sequence[Any]) -> tuple[Path | None, str]:
    """The row's file on this machine, or why there is none."""
    recorded = str(getattr(content, "FolderPath", "") or "")
    if not recorded:
        return None, NO_PATH
    try:
        decoded = locations.location_to_path(recorded)
    except ValueError:
        return None, NO_PATH
    resolved = locations.resolve_recorded_path(
        decoded, root=Path(cfg.library.root), prefix_map=rules
    )
    if resolved.resolution is locations.Resolution.NOT_A_PATH:
        return None, NO_PATH
    if resolved.path is None:
        return None, PATH_UNMAPPED
    path = Path(resolved.path)
    try:
        present = path.is_file()
    except (OSError, ValueError):
        return path, FILE_UNREADABLE
    return (path, "") if present else (path, FILE_MISSING)


def _file_tags(path: Path) -> tuple[str, str, str]:
    """The file's title tag and ``initialkey``, or why they could not be read."""
    try:
        read = tags.read_tags_checked(path, ("title", "initialkey"))
    except (tags.TagReadFailed, ValueError):
        return "", "", FILE_UNREADABLE
    return str(read["title"] or ""), str(read["initialkey"] or ""), ""


def plan_row(
    cfg: config.Config,
    content_id: str,
    content: Any,
    *,
    keys: Mapping[str, str | None],
    template: NameTemplate,
    rules: Sequence[Any],
) -> Item:
    """One row's item: left with why, agreeing, or adopting. Reads the row's file."""
    judged = analyzed.judge(content_id, content)
    if judged.why in (analyzed.NO_ROW, analyzed.ROW_REMOVED):
        return Item(content_id, LEAVE_ACTION, reason=GONE, title=judged.title)
    title = str(getattr(content, "Title", "") or "")
    if judged.action != analyzed.CLEAR:
        return Item(content_id, LEAVE_ACTION, reason=NOT_ANALYSED, title=title)
    key_id = getattr(content, "KeyID", None)
    key, key_note = reference_key(key_id, keys.get(str(key_id)) if key_id else None)
    hundredths = getattr(content, "BPM", None)
    tempo, tempo_note = reference_tempo(hundredths)
    parsed = parse_head(title, template=template) or {}
    head_tempo = int(parsed["bpm"]) if "bpm" in parsed else None
    common = {
        "title": title,
        "new_title": title,
        "notes": tuple(note for note in (key_note, tempo_note) if note),
        "head_key": parsed.get("key"),
        "key": key,
        "relation": rc.key_relation(parsed.get("key"), key),
        "head_tempo": head_tempo,
        "tempo_hundredths": int(hundredths) if tempo is not None else None,
        "tempo": tempo,
    }
    new_title = adopted(title, key=key, tempo=tempo, template=template)
    if new_title is None:
        return Item(content_id, LEAVE_ACTION, reason=NO_HEAD, **common)
    if key is None and tempo is None:
        return Item(content_id, LEAVE_ACTION, reason=NO_REFERENCE, **common)
    common["new_title"] = new_title
    path, missing = _resolved(cfg, content, rules)
    shown = str(path) if path is not None else ""
    if missing:
        return Item(content_id, LEAVE_ACTION, reason=missing, path=shown, **common)
    tag_title, initialkey, unreadable = _file_tags(path)
    if unreadable:
        return Item(content_id, LEAVE_ACTION, reason=unreadable, path=shown, **common)
    on_file = {"path": shown, "tag_title": tag_title, "new_tag_title": tag_title,
               "initialkey": initialkey, "new_initialkey": initialkey}
    new_tag = adopted(tag_title, key=key, tempo=tempo, template=template)
    if new_tag is None or split_head(tag_title, template=template)[1] != split_head(
        title, template=template
    )[1]:
        return Item(content_id, LEAVE_ACTION, reason=TAG_DIFFERS, **common, **on_file)
    on_file["new_tag_title"] = new_tag
    if new_title == title and new_tag == tag_title:
        # A TITLE THAT AGREES IS LEFT WHOLE, its key tag too: this verb corrects a
        # head, and a key tag beside an agreeing head is not its to fill.
        return Item(content_id, AGREE, **common, **on_file)
    if key is not None and parse_camelot(initialkey) != parse_camelot(key):
        on_file["new_initialkey"] = key
    return Item(content_id, ADOPT, **common, **on_file)


def plan_adopt(
    cfg: config.Config,
    db: Any,
    scope: rc.Scope,
    *,
    template: NameTemplate,
    leave: Iterable[str] = (),
) -> AdoptPlan:
    """Read every row the scope names, once, and plan each.

    Only values are returned, so the handle may be a read one closed before the
    gate. Items keep the scope's order.
    """
    held = frozenset(str(content_id) for content_id in leave)
    keys = {str(key.ID): key.ScaleName for key in db.get_key()}
    rows = dict(scope.read)
    rows.update(rc._content_rows(db, [c for c in scope.content_ids if c not in rows]))
    rules = locations.prefix_rules(cfg.resolved_prefix_map())
    items: list[Item] = []
    for content_id in scope.content_ids:
        item = plan_row(
            cfg, content_id, rows.get(content_id), keys=keys, template=template, rules=rules
        )
        if item.action == ADOPT and content_id in held:
            item = _held(item)
        items.append(item)
    counts = dict.fromkeys(OUTCOMES, 0)
    for item in items:
        counts[item.reason or item.action] += 1
    notes = dict.fromkeys(NOTES, 0)
    for item in items:
        for note in item.notes:
            notes[note] += 1
    held_out = {item.content_id for item in items if item.reason == HELD_OUT}
    return AdoptPlan(
        scope=scope,
        items=tuple(items),
        counts=MappingProxyType(counts),
        notes=MappingProxyType(notes),
        leave_unmatched=tuple(sorted(held - held_out)),
    )


def _held(item: Item) -> Item:
    """An adopting item held out by ``--leave``, its before and after kept for the screen."""
    return Item(
        item.content_id,
        LEAVE_ACTION,
        reason=HELD_OUT,
        notes=item.notes,
        path=item.path,
        title=item.title,
        new_title=item.new_title,
        tag_title=item.tag_title,
        new_tag_title=item.new_tag_title,
        initialkey=item.initialkey,
        new_initialkey=item.new_initialkey,
        head_key=item.head_key,
        key=item.key,
        relation=item.relation,
        head_tempo=item.head_tempo,
        tempo_hundredths=item.tempo_hundredths,
        tempo=item.tempo,
    )


def assert_plan_unchanged(approved: AdoptPlan, again: AdoptPlan) -> None:
    """Refuse, writing nothing, when the plan taken again on the write handle is
    not the plan approved: a title, a tag or rekordbox's answer moved between."""
    if again.digest == approved.digest:
        return
    was = {item.content_id: item.digested() for item in approved.items}
    now = {item.content_id: item.digested() for item in again.items}
    moved = sorted(
        content_id for content_id in set(was) | set(now) if was.get(content_id) != now.get(content_id)
    )
    raise refuse(
        "decision-stale",
        f"{len(moved)} row(s) of {again.scope.name} are not as the approved plan read "
        f"them, so nothing was written: " + row_defaults.named(moved or ["the plan's totals"]),
        steps=("run the verb again and approve the plan as it is now",),
        origin=_ORIGIN,
        detail={"moved": moved},
    )


# The write.


@dataclass(frozen=True, slots=True)
class FilesWritten:
    """Each file the apply set out to write: read back as planned, not written, or
    written and reading back otherwise. A row whose file did not read back is not written."""

    read_back: tuple[str, ...] = ()
    failed: tuple[str, ...] = ()
    wrong: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Written(row_defaults.RowsWritten):
    """What one apply did, files and rows; see :func:`assert_read_back`."""

    files: FilesWritten = FilesWritten()


def write_files(items: Sequence[Item]) -> FilesWritten:
    """Write each item's title tag and ``initialkey`` where they change, then read
    both back. Nothing raises for one file. An item whose file is already as
    planned writes nothing and reads back."""
    read_back: list[str] = []
    failed: list[str] = []
    wrong: list[str] = []
    for item in items:
        path = Path(item.path)
        if item.writes_file:
            fields: dict[str, object] = {}
            if item.new_tag_title != item.tag_title:
                fields["title"] = item.new_tag_title
            if item.new_initialkey != item.initialkey:
                fields["initialkey"] = item.new_initialkey
            if not tags.write_tags(path, fields):
                failed.append(item.content_id)
                continue
        title, initialkey, unreadable = _file_tags(path)
        if unreadable or title != item.new_tag_title or initialkey != item.new_initialkey:
            wrong.append(item.content_id)
            continue
        read_back.append(item.content_id)
    return FilesWritten(tuple(read_back), tuple(failed), tuple(wrong))


def row_changes(items: Iterable[Item]) -> metadata.Plan:
    """The ``Title`` writes of the items given, under the one operation that owns them."""
    owner = metadata.ADOPT_REKORDBOX_HEAD
    return metadata.Plan(
        owner,
        tuple(
            metadata.Change(item.content_id, owner, "Title", item.title, item.new_title)
            for item in items
            if item.writes_title
        ),
    )


def judge(
    items: Sequence[Item],
    before: Mapping[str, Mapping[str, Any]],
    after: Mapping[str, Mapping[str, Any]],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """What the read back found wrong: (wrong, moved), a row not carrying its new
    title, and one with a column beside ``Title`` and the bookkeeping changed."""
    wrong: list[str] = []
    moved: list[str] = []
    for item in items:
        was, now = before.get(item.content_id), after.get(item.content_id)
        if was is None or now is None:
            wrong.append(f"{item.content_id}: the row could not be read")
            continue
        if str(now.get("Title") or "") != item.new_title:
            wrong.append(f"{item.content_id}: reads {now.get('Title')!r}, not {item.new_title!r}")
        changed = row_defaults.moved_columns(was, now, planned=("Title",))
        if changed:
            moved.append(f"{item.content_id}: {', '.join(changed)}")
    return tuple(wrong), tuple(moved)


def apply_adopt(
    cfg: config.Config,
    db: Any,
    plan: AdoptPlan,
    *,
    analysis_roots: Iterable[Path | str],
) -> Written:
    """Write the plan inside one guarded session: the before values into the
    record, the files, then the rows whose files read back, committed behind the
    guard and read back.

    THE CALLER TOOK THE PLAN AGAIN ON THIS HANDLE (:func:`assert_plan_unchanged`),
    so the rows are the rows approved. The analysis file watch is armed over the
    roots given, so a write that touched a grid fails the session.
    """
    watched = row_defaults.watched_roots(analysis_roots)
    writes = plan.writes
    content_ids = [item.content_id for item in writes]
    mapped = row_defaults.read_mapped(db, content_ids)
    # THE EVIDENCE IS READ BEFORE IT IS REPLACED, as every content row write reads it.
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))
    metadata.enable((metadata.ADOPT_REKORDBOX_HEAD,))
    # THE POLICY IS ASKED OF THE WHOLE PLAN BEFORE THE FIRST FILE, so a plan
    # naming a column the operation does not own writes no file either.
    metadata.assert_within_policy(row_changes(writes))
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        # BEFORE THE CAPTURE IS ATTACHED, WHICH PERSISTS THE RECORD: every
        # surface's old value is on disk before the first file is written.
        gates.record.detail[RECORD_KEY] = [item.before() for item in writes]
        record, _capture = trees.attached_capture(gates, cfg, db)
        files = write_files(writes)
        landed = frozenset(files.read_back)
        rowed = [item for item in writes if item.content_id in landed and item.writes_title]
        changes = row_changes(rowed)
        ids = [item.content_id for item in rowed]
        before = row_defaults.read_columns(db, ids)
        written = 0
        try:
            report = metadata.write_plan(changes, mapped)
            written = len(report.written)
            rb_writer.commit_guarded(db)
        except BaseException:
            trees.rollback_quietly(db)
            # AN EXCEPTION IS NOT PROOF NOTHING LANDED: the witness is the engine's answer.
            if witness.landed:
                row_defaults.record_commit(record, CHANGE_KEY, written, cfg)
            raise
        row_defaults.record_commit(record, CHANGE_KEY, written, cfg)
        convergence.record_fingerprint(cfg, db)
        after = row_defaults.read_columns(db, ids)
        session_id = record.session_id
    wrong, moved = judge(rowed, before, after)
    return Written(
        session_id=session_id,
        written=written,
        read_back=len(rowed) - len(wrong),
        wrong=wrong,
        moved=moved,
        files=files,
    )


def assert_read_back(written: Written) -> None:
    """Refuse when the database does not say what the plan said it would, naming
    the session that undoes the durable write."""
    if not written.wrong and not written.moved:
        return
    undo = (f"the write is durable; restore session {written.session_id} to undo it",)
    if written.moved:
        raise refuse(
            "whitelist-violation",
            "a row written for its title has another column changed after the commit, "
            "which the guard should have refused before it: " + row_defaults.named(written.moved),
            remedy=Remedy.REPORT_DEFECT,
            steps=undo,
            origin=_ORIGIN,
            detail={"moved": list(written.moved), "session": written.session_id},
        )
    raise refuse(
        "internal-error",
        f"{len(written.wrong)} of {written.written} row(s) written do not read back with "
        f"their new title: " + row_defaults.named(written.wrong),
        remedy=Remedy.REPORT_DEFECT,
        steps=undo,
        origin=_ORIGIN,
        detail={"wrong": list(written.wrong), "session": written.session_id},
    )


__all__: Sequence[str] = (
    "ADOPT", "AGREE", "CHANGE_KEY", "FILE_MISSING", "FILE_UNREADABLE", "GONE", "HELD_OUT",
    "KEY_EMPTY", "KEY_NOT_CAMELOT", "LEAVE_ACTION", "LEFT", "NOTES", "NOT_ANALYSED", "NO_HEAD",
    "NO_PATH", "NO_REFERENCE", "OUTCOMES", "PATH_UNMAPPED", "RECORD_KEY", "TAG_DIFFERS",
    "TEMPO_TOLERANCE", "TEMPO_ZERO", "WORKFLOW", "AdoptPlan", "FilesWritten", "Item", "Written",
    "adopted", "apply_adopt", "assert_plan_unchanged", "assert_read_back", "judge", "plan_adopt",
    "plan_row", "reference_key", "reference_tempo", "resolve_scope", "row_changes",
    "tempo_differs", "write_files",
)
