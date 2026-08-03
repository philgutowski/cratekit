"""Applying a plan: approval first, one entry at a time, and resumable.

WHAT MAKES THIS RESUMABLE, precisely. Not a counter, and not a position. The
ledger records the IDENTIFIER of every entry that landed, and the next run's work
is the plan's applicable entries minus the ones the ledger already holds. A
counter would be wrong in the two ways that matter: it assumes the plan is the
same plan, and it assumes the entries are in the same order. Both are false after
somebody answers a genre question between two runs, which is the ordinary case
this feature exists for. An identifier is a fact about the work rather than about
the run, so a plan that grew, shrank, or reordered still resumes correctly.

THE ORDER PER ENTRY IS: PLACE, RECORD THE ORIGINAL, WRITE THE TAG, MARK APPLIED.
The first step is the one that moved, and it moved because of what sits behind
each of these two writes. A membership row goes into the rekordbox database,
which is snapshotted before every write session and restorable afterwards (KTD21b,
R30). A genre string goes into a file on disk, which is outside all of that: no
snapshot holds it, no re-import puts it back, and the value it replaced is gone
the instant the write returns. Doing the recoverable write first and the
irrecoverable one second is the only order where a refusal costs nothing.

WHAT THE REVERSE ORDER COST, MEASURED. With the tag write first, a systemic
refusal raised inside ``place`` (rekordbox running, a backup gate unanswered, a
snapshot not verified) was caught per entry and the loop continued, so a plan of
six files came back ``applied=0 failed=6`` with an empty applied ledger and all
six files on disk holding adoption's genre instead of their own. Every gate that
stands in front of a destructive run is structurally DOWNSTREAM of this module's
own irreversible write, so the per-entry catch multiplied one refusal into one
file rewrite per entry in the plan.

THE ORDER IS THE WHOLE FIX, AND THE LOOP STILL NEVER STOPS. A first attempt
paired the reordering with a break when the refusal's declared scope was wider
than one item. That was wrong for a reason worth writing down, because it reads
so plausibly: :func:`cratekit.core.cause.refuse` DEFAULTS to ``Scope.RUN`` and
nothing in :mod:`cratekit.write` declares ``ITEM`` at all, so the default was
doing all the work and an ordinary per-track refusal ended the pass with later
entries never attempted. That is exactly the per-track versus per-pass failure
U19 paid for and the one :func:`membership_plan` says this module refuses to
have. Nothing was gained by it either: once the irreversible write is second, a
systemic refusal costs zero file writes however many times it is reported.

WHAT A SECOND RUN DOES AFTER A CRASH AT EACH STEP, stated rather than implied,
because "idempotent" asserted in a docstring is what a green suite cannot check:

* Crash BEFORE ``place``. Nothing was written. The re-run proceeds. No loss.
* Crash BETWEEN ``place`` and the revert record. The membership landed and the
  entry is not marked, so the re-run places it again, which the membership
  writer's own dedup makes a no-op, and carries on. No file was touched at all.
* Crash BETWEEN the revert record and the tag write. The ledger holds an original
  identical to what the file still has, so reverting is a no-op that restores the
  same bytes. The re-run finds the record already there, keeps it, and writes the
  tag. No loss.
* Crash BETWEEN the tag write and the applied record. The file carries the new
  value and the entry is not marked applied, so the re-run applies it again. The
  revert record is NOT refreshed, which is the property that makes this safe: a
  refresh would record the value adoption just wrote as the original, and the
  revert would then restore the thing it was supposed to undo.
* Crash BETWEEN the applied record and the end of the run. Nothing is
  outstanding for that entry, so the re-run skips it. Correct.

The record and the tag write are ONE act rather than two adjacent ones, through
:func:`cratekit.adopt.revert.write_tag_with_record`. Adjacent is not good enough:
a revert issued in the window between them takes the record away and the write
then lands on a file with nothing behind it.

WHY THE MEMBERSHIP WRITE ARRIVES AS A PARAMETER. The two media a tree can be
written in belong to :mod:`cratekit.write.trees`, and which one is correct for a
given tree at a given moment is the tree registry's answer, not this module's.
:func:`membership_plan` builds the ONE mapping both of those entry points take,
so the destination display names are resolved once, from the active taxonomy, at
write time. What this module owns is the approval, the order, and the ledger; a
second implementation of the byte splice or the row write here would be a third
answer to a question that already has two.

Layer: modules.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from cratekit.adopt import revert
from cratekit.adopt.approval import require_approval
from cratekit.adopt.plan import AdoptionPlan, PlanEntry
from cratekit.cli.output import timestamp
from cratekit.core import config, tags, taxonomy
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope
from cratekit.core.exit_codes import Remedy
from cratekit.write.routing_pass import destination

#: The state entry this module owns.
STATE_KEY = "adoption_ledger"

#: The declared lock directory, shared with the revert ledger.
LOCK_KEY = "adoption_locks"

#: Bumped only when the on-disk shape changes incompatibly.
SCHEMA_VERSION = 1

#: The tag field adoption writes when it writes one at all. Named once, because
#: it is also the field the revert ledger keys its records on and the two must
#: not be able to disagree about which field was overwritten.
ADOPTED_TAG_FIELD = "genre"


class AppliedLedgerUnreadable(CratekitError):
    """The applied ledger exists and cannot be understood.

    Deliberately NOT collapsed into "nothing applied yet", which is the reading
    that makes it dangerous rather than merely absent: an empty ledger re-applies
    an approved plan from its first entry against a library that already holds
    most of it, and every membership write is a write session with a snapshot in
    front of it. Positive recognition, field by field, and a refusal for
    everything else.
    """

    def __init__(self, message: str, *, path: Path, remedy: Remedy) -> None:
        super().__init__(
            Cause(
                reason="adoption-ledger-unusable",
                message=message,
                remediation=Remediation(remedy=remedy),
                scope=Scope.RUN,
                origin=("adopt",),
                detail={"path": str(path), "document": STATE_KEY},
            )
        )
        self.path = path
        self.remedy = remedy


@dataclass(frozen=True, slots=True)
class AppliedEntry:
    """One plan entry that landed, and who was responsible for it.

    ``digest`` is the plan digest the approval was recorded against. It is kept
    per record rather than once per file so that a ledger holding work from two
    approvals can say which approval each piece of work belongs to, which is what
    R34's "each write session records which actor asserted" needs at the
    granularity a resume actually reads.
    """

    entry_id: str
    tree: str
    content_id: str
    bucket: str
    sub: str
    actor: str
    digest: str
    applied: str

    def to_json(self) -> dict[str, Any]:
        return {
            "entry": self.entry_id,
            "tree": self.tree,
            "content": self.content_id,
            "bucket": self.bucket,
            "sub": self.sub,
            "actor": self.actor,
            "digest": self.digest,
            "applied": self.applied,
        }


@dataclass(frozen=True, slots=True)
class AppliedLedger:
    """Everything adoption has already applied to this library.

    A TUPLE rather than a mapping keyed by entry, for the reason the tree
    registry gives for the same choice: it keeps the identifier out of every key
    position, so nothing here is tempted to key on something a user can rename.
    """

    applied: tuple[AppliedEntry, ...] = ()

    def has(self, entry_id: str) -> bool:
        return any(entry.entry_id == entry_id for entry in self.applied)

    def entry_ids(self) -> frozenset[str]:
        return frozenset(entry.entry_id for entry in self.applied)

    def with_applied(self, entry: AppliedEntry) -> AppliedLedger:
        """This ledger plus ``entry``, replacing any record with the same id."""
        kept = tuple(held for held in self.applied if held.entry_id != entry.entry_id)
        return AppliedLedger(
            tuple(sorted((*kept, entry), key=lambda held: held.entry_id))
        )


#: What an absent file resolves to. Named, because "nothing applied yet" is a
#: real answer rather than a missing one.
EMPTY = AppliedLedger()


def path_for(cfg: config.Config) -> Path:
    """Where the ledger lives, resolved through the state inventory.

    Through ``state_path`` rather than composed here. A module that builds its own
    path under a state root has invented a state file the inventory does not know
    about, so nothing that walks the inventory will snapshot it, and this entry is
    COUPLED precisely so a restore rolls it back with the memberships it records.
    """
    return config.state_path(STATE_KEY, cfg)


def lock_path(cfg: config.Config) -> Path:
    """The sibling lock, in the declared never-restored lock directory."""
    return config.state_path(LOCK_KEY, cfg) / f"{STATE_KEY}.lock"


def read(cfg: config.Config) -> AppliedLedger:
    """The effective ledger for this library. An absent file is the empty one."""
    path = path_for(cfg)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return EMPTY
    except OSError as exc:
        raise AppliedLedgerUnreadable(
            f"{path} exists and could not be read: {exc}",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        ) from exc

    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AppliedLedgerUnreadable(
            f"{path} is not readable as JSON: {exc}", path=path, remedy=Remedy.RUN_DOCTOR
        ) from exc
    if not isinstance(data, dict):
        raise AppliedLedgerUnreadable(
            f"{path} holds a {type(data).__name__} at its top level rather than an "
            f"adoption ledger",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    version = data.get("schema_version")
    if not isinstance(version, int):
        raise AppliedLedgerUnreadable(
            f"{path} carries no integer schema_version, so nothing can be said "
            f"about the shape of what follows it",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    if version > SCHEMA_VERSION:
        raise AppliedLedgerUnreadable(
            f"{path} was written at schema version {version}; this build "
            f"understands {SCHEMA_VERSION}",
            path=path,
            remedy=Remedy.UPGRADE_CRATEKIT,
        )
    entries = data.get("applied")
    if not isinstance(entries, list):
        raise AppliedLedgerUnreadable(
            f"{path} has no applied array; its records are a "
            f"{type(entries).__name__}",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )

    records: list[AppliedEntry] = []
    seen: set[str] = set()
    for position, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise AppliedLedgerUnreadable(
                f"{path} holds a record at position {position} that is a "
                f"{type(entry).__name__} rather than an object",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        for name in ("entry", "tree", "content", "actor"):
            if not isinstance(entry.get(name), str) or not entry[name]:
                raise AppliedLedgerUnreadable(
                    f"{path} holds a record at position {position} with no "
                    f"{name}; a record that cannot say what it applied, or who "
                    f"approved it, is worse than no record because it still "
                    f"suppresses the work",
                    path=path,
                    remedy=Remedy.RUN_DOCTOR,
                )
        record = AppliedEntry(
            entry_id=str(entry["entry"]),
            tree=str(entry["tree"]),
            content_id=str(entry["content"]),
            bucket=str(entry.get("bucket") or ""),
            sub=str(entry.get("sub") or ""),
            actor=str(entry["actor"]),
            digest=str(entry.get("digest") or ""),
            applied=str(entry.get("applied") or ""),
        )
        if record.entry_id in seen:
            raise AppliedLedgerUnreadable(
                f"{path} holds two records for the entry {record.entry_id!r}; a "
                f"ledger that gives two answers for one piece of work cannot say "
                f"who applied it, and resolving that by line order picks an actor",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        seen.add(record.entry_id)
        records.append(record)
    return AppliedLedger(tuple(sorted(records, key=lambda held: held.entry_id)))


def write(cfg: config.Config, ledger: AppliedLedger) -> Path:
    """Persist ``ledger`` atomically and owner only, through the shared writer."""
    payload = {
        "schema_version": SCHEMA_VERSION,
        "applied": [
            entry.to_json()
            for entry in sorted(ledger.applied, key=lambda held: held.entry_id)
        ],
    }
    path = path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


def mark_applied(cfg: config.Config, entry: AppliedEntry) -> AppliedLedger:
    """Record that one entry landed. Read, modify, write, UNDER THE LOCK.

    Read, modify, write rather than a whole-file overwrite, because more than one
    plan accumulates in one ledger and a writer that replaced the file would
    erase every other plan's record on each call.

    UNDER AN EXCLUSIVE LOCK, because a read-modify-write is not atomic and the
    atomic rename around it protects only the rename. Two processes interleaving
    drop a record that was fully written, and a dropped record here re-applies a
    membership write and re-writes a tag: the second write then sees the value
    adoption already wrote, and the revert ledger's first-write-wins rule is the
    only thing standing between that and a lost original.
    """
    with config._exclusive_lock(lock_path(cfg)):
        updated = read(cfg).with_applied(entry)
        write(cfg, updated)
    return updated


def outstanding(plan: AdoptionPlan, ledger: AppliedLedger) -> tuple[PlanEntry, ...]:
    """The plan's applicable entries that have not landed, in plan order.

    DERIVED from the two records rather than stored as a third. A stored
    "remaining" count and the rows it counts can disagree after a crash, which is
    the same argument :func:`cratekit.core.review.count_unresolved` makes for
    being a query rather than a counter.
    """
    done = ledger.entry_ids()
    return tuple(entry for entry in plan.applicable() if entry.entry_id not in done)


def membership_plan(
    entries: Sequence[PlanEntry], declared: taxonomy.Taxonomy
) -> dict[tuple[str, str], list[str]]:
    """The mapping both tree writers take: (folder, sub) to the rows going in it.

    THE DISPLAY NAMES ARE RESOLVED HERE AND NEVER STORED. R19 and D5 both require
    it, and the concrete reason is that a person may rename a folder in rekordbox
    between the plan and the apply; resolving at write time from the active
    taxonomy means the rename changes where the tracks go and orphans nothing.
    Through :func:`cratekit.write.routing_pass.destination`, which already knows
    the five shapes a sub identifier can take, rather than a second resolution
    here that would eventually answer one of them differently.

    An entry whose destination the taxonomy no longer declares is SKIPPED rather
    than raised out of the whole mapping. One record naming a sub that a template
    edit dropped would otherwise cost every other entry in the run, which is the
    per-track-versus-per-pass lesson U19 paid for.
    """
    grouped: dict[tuple[str, str], list[str]] = {}
    for entry in entries:
        try:
            folder, sub = destination(declared, entry.bucket, entry.sub)
        except KeyError:
            continue
        grouped.setdefault((folder, sub), []).append(entry.content_id)
    return grouped


@dataclass(frozen=True, slots=True)
class ApplyReport:
    """What one apply landed, what it skipped, and where a resume starts.

    ``resumed_at`` is the ORDINAL of the first entry this run had work for, which
    is the number a person recognizes from the plan they approved. It is derived
    from the outstanding set rather than counted, so it is correct after a plan
    has grown or shrunk between two runs.

    THERE IS NO "STOPPED HERE" FIELD, and its absence is now the design rather
    than an omission. One briefly existed, set when a refusal wider than one item
    ended the loop. Both halves were wrong: the loop must not end (see
    :func:`apply_plan`), so the field could only ever be None, and a field that is
    always None is a promise a reader will eventually rely on.

    EVERY OUTSTANDING ENTRY IS ATTEMPTED, so ``applied`` plus ``failed`` accounts
    for all of them. That is the property a caller can use, and it is stronger
    than a marker saying where a run gave up.
    """

    tree: str
    actor: str
    digest: str
    applied: tuple[str, ...] = ()
    already_applied: tuple[str, ...] = ()
    failed: Mapping[str, str] = field(default_factory=dict)
    resumed_at: int | None = None

    def __len__(self) -> int:
        return len(self.applied)


def apply_plan(
    cfg: config.Config,
    plan: AdoptionPlan,
    declared: taxonomy.Taxonomy,
    *,
    approval: object,
    place: Callable[[PlanEntry, str, str], None],
    tag_value: Callable[[PlanEntry, taxonomy.Taxonomy], str | None] | None = None,
    now: datetime | None = None,
) -> ApplyReport:
    """Apply an approved plan, one entry at a time, resuming where it left off.

    ``place`` writes ONE entry's membership and is handed the display names this
    module resolved, so the caller that owns a database or an export does the
    write and this module owns the order. It is called per entry rather than per
    batch deliberately: the ledger record has to follow the write it describes,
    and a batch call cannot say which half of a batch landed before it failed.

    A ``CratekitError`` FROM ``place`` FAILS THAT ENTRY AND NOTHING ELSE, and its
    declared scope is not consulted. A caller does not have to reach for
    ``Scope.ITEM`` to keep the rest of its plan alive, which matters because the
    scope every existing refusal in this repository carries is the default one,
    ``Scope.RUN``. If the refusal really does condemn the run, the caller sees it
    against every entry and the run costs nothing but time: no file is rewritten,
    because the tag write is downstream of this call.

    ``tag_value`` says what, if anything, adoption should write onto the file for
    an entry. Returning None writes no tag, which is the correct answer for a
    library whose files already carry the right value and for every entry the
    plan routes purely by membership. There is no default that writes: a tag
    write is the one operation no restore can undo, so it happens because a
    caller asked for it rather than because nobody turned it off.

    THE APPROVAL IS CHECKED BEFORE ANYTHING IS READ OR WRITTEN, and it is checked
    against the plan in hand rather than against a flag (R34). Nothing below this
    line runs for an unapproved plan, so a refused apply leaves the disk exactly
    as it found it.

    THE DESTRUCTIVE-SESSION BOUNDARY IS THE CALLER'S, and saying so is the honest
    version of a gap rather than a design. R29 declares the boundary as one
    source per run and :func:`cratekit.write.trees.write_tree_membership` owns its
    own session for that reason, refusing a caller-supplied gates factory. So
    this loop takes no session and no library lock: two apply runs racing over
    one plan would each see the same entries outstanding, and what stops them
    reaching the database twice is R31's lock, taken one layer up.

    THE TAG WRITE IS OUTSIDE THAT LOCK, WHICH IS THE RESIDUE, and it is now
    written down where somebody will find it rather than only here: residual
    finding R-20, and the obligation rides with the apply command line in
    ``tests/_pending.py``. Two runs both writing the same value to the same file
    is harmless, and the revert ledger's first-write-wins rule is what keeps the
    original safe if they are not. What is genuinely missing is a session and a
    library lock AROUND this loop, which only the verb can open, because R29 says
    one source per run and this module is not a run.

    IT IS NO LONGER THE CASE THAT A GATE REFUSAL COSTS A FILE WRITE, which is the
    half of that gap that was not honest. ``place`` runs first, so a caller whose
    gates refuse gets zero files rewritten however many entries the plan holds.
    The refusal is reported once per entry and the loop does not stop, for the
    reason given above and in the module docstring.
    """
    granted = require_approval(plan, approval)
    ledger = read(cfg)
    pending = outstanding(plan, ledger)
    already = tuple(
        entry.entry_id for entry in plan.applicable() if ledger.has(entry.entry_id)
    )
    report_resumed = pending[0].ordinal if pending else None

    applied: list[str] = []
    failed: dict[str, str] = {}
    for entry in pending:
        try:
            folder, sub = destination(declared, entry.bucket, entry.sub)
        except KeyError as exc:
            # PER ENTRY, never out of the run. See ``membership_plan``.
            failed[entry.entry_id] = str(exc)
            continue

        wanted = None if tag_value is None else tag_value(entry, declared)
        target = Path(entry.path) if entry.path else None
        if wanted is not None and target is not None:
            try:
                # ASKED BEFORE ANYTHING AT ALL HAPPENS FOR THIS ENTRY, membership
                # included. ``write_tags`` raises this from OUTSIDE its own try
                # block, so an unsupported container used to raise out of this
                # function entirely: no report, later entries never attempted,
                # and every re-run dying on the same file. Asking after ``place``
                # fixed that and bought a second problem, which is that the entry
                # got its membership, was then failed, and could never reach
                # applied, so every re-run placed it again. Asked here, one
                # awkward container costs exactly one entry and changes nothing.
                tags.dialect_of(target.suffix.lower())
            except tags.UnsupportedContainer as exc:
                failed[entry.entry_id] = str(exc)
                continue

        # THE RECOVERABLE WRITE GOES FIRST. A membership row is inside the
        # database snapshot; the tag write below is outside every safety net this
        # product has. See the module docstring for what the other order cost.
        #
        # AND A REFUSAL HERE COSTS EXACTLY THIS ENTRY, whatever it condemns. An
        # earlier version broke the loop when the cause's scope was wider than
        # one item, which reads well and is wrong twice over:
        # :func:`cratekit.core.cause.refuse` DEFAULTS to ``Scope.RUN`` and
        # nothing in :mod:`cratekit.write` declares ``ITEM``, so an ordinary
        # per-track refusal ended the pass and later entries were never
        # attempted. That is the per-track versus per-pass failure U19 paid for
        # and the one ``membership_plan`` says this module refuses to have. The
        # property that made the break look necessary was never the break: it is
        # the ORDER above, which is what makes a refusal cost no file write at
        # all. A systemic refusal is now reported once per entry, which is noise
        # in a report rather than damage on a disk.
        try:
            place(entry, folder, sub)
        except CratekitError as exc:
            failed[entry.entry_id] = exc.cause.message
            continue

        if wanted is not None and target is not None:
            # THE ORIGINAL AND THE WRITE ARE ONE ACT. See the module docstring:
            # a revert landing between them leaves the write with no record.
            _record, landed = revert.write_tag_with_record(
                cfg,
                target,
                field=ADOPTED_TAG_FIELD,
                written=wanted,
                entry_id=entry.entry_id,
                now=now,
            )
            if not landed:
                failed[entry.entry_id] = "the container refused the tag write"
                continue
        # MARKED ONLY AFTER THE WRITE. A mark that ran first would suppress the
        # work on the next run while the library never received it, which is the
        # order U19 established for exactly this shape and the one direction that
        # is not recoverable by re-running.
        ledger = mark_applied(
            cfg,
            AppliedEntry(
                entry_id=entry.entry_id,
                tree=entry.tree,
                content_id=entry.content_id,
                bucket=entry.bucket,
                sub=entry.sub,
                actor=granted.actor,
                digest=granted.digest,
                applied=timestamp(now),
            ),
        )
        applied.append(entry.entry_id)
    return ApplyReport(
        tree=plan.tree,
        actor=granted.actor,
        digest=granted.digest,
        applied=tuple(applied),
        already_applied=already,
        failed=failed,
        resumed_at=report_resumed,
    )


__all__ = [
    "ADOPTED_TAG_FIELD",
    "EMPTY",
    "LOCK_KEY",
    "SCHEMA_VERSION",
    "STATE_KEY",
    "AppliedEntry",
    "AppliedLedger",
    "AppliedLedgerUnreadable",
    "ApplyReport",
    "apply_plan",
    "lock_path",
    "mark_applied",
    "membership_plan",
    "outstanding",
    "path_for",
    "read",
    "write",
]
