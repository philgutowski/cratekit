"""The backup-age fact: a FILE core reads, never a module core imports.

R15 requires every write session to warn that the database and the music files
should be backed up, and to feed that warning with the backup age when the
backup module is enabled. That sentence contains a trap, and this module exists
to avoid it.

THE TRAP. The obvious implementation is for the session code to call the backup
module and ask. That makes core depend on a toggleable feature module, which
KTD23 forbids in general and which breaks concretely here: the backup module is
opt-in, so on a slim install the import fails, and it fails inside a warning
that runs immediately before the riskiest operation in the product. The plan
states the shape instead: backup PUBLISHES its age into library-scoped state,
and the warning READS a fact. Nothing imports upward, and a library whose backup
module was never installed answers "never recorded" rather than raising.

WHY THE ANSWER IS PER PORTION AND NOT ONE TIMESTAMP. The database portion of a
backup refuses outright while rekordbox or its background agent is running,
because a copy taken mid-write is a torn database that opens cleanly and is
silently wrong. The file mirror has no such constraint and completes anyway. So
the normal state of a library backed up without quitting rekordbox first is
"files current, database stale", and a single aggregate timestamp reports that
library as fully backed up. The one thing R15's warning exists to tell a user is
exactly the thing the aggregate would hide.

WHY "NEVER RECORDED" IS ITS OWN ANSWER AND NOT A VERY LARGE AGE. They have
different remediations. An unrecorded portion means the backup module has not
run here at all, and the fix is to run it. A very old age means it ran and has
not run since, and the fix is to run it again, possibly after quitting
rekordbox. Collapsing them costs the caller the ability to say which.

WHY A FUTURE TIMESTAMP IS A THIRD ANSWER. Any caller comparing an age against a
maximum treats a negative age as the freshest possible value, so a record
written by a machine with a skewed clock, or edited by hand, silently satisfies
the check it was meant to fail. Naming it is the only way a caller can refuse it.

This module reads and writes one small JSON file through the shared atomic
writer, so it inherits that writer's explicit mode: a state file whose mode came
from the umask is the defect P1 records, and this one names when a user's data
was last protected.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType

from cratekit.core import cause, config

#: The state entry this module owns. Named once, so the resolver and every
#: caller cannot disagree about which file is meant.
STATE_KEY = "backup_facts"

#: Bumped only when the on-disk shape changes incompatibly. A file carrying a
#: newer version is not read: guessing at a shape a later build wrote is how a
#: record of when the user's music was last protected turns into a wrong answer,
#: and a wrong answer here is worse than no answer.
SCHEMA_VERSION = 1

#: How far ahead of "now" a recorded completion may sit before it is treated as
#: skewed rather than fresh. Two machines writing to one library will not agree
#: on the second, and a network time correction can move a clock by minutes; an
#: hour is comfortably past both and far short of any real backup interval.
FUTURE_TOLERANCE = timedelta(hours=1)

#: The top level key holding when the file mirror last compared the library
#: with the remote folder by folder (R-757). Beside ``portions`` and not inside
#: a portion's entry, because it is not a backup: it is how the last backup of
#: the files looked at the remote.
FULL_COMPARISON_KEY = "full_comparison"


class Portion(StrEnum):
    """The two halves of a library backup, each with its own gate.

    Exactly two, because R15 names exactly two things a user is warned about:
    the database and the music files. Anything else a backup happens to copy
    (rekordbox's own application settings, for instance) travels with one of
    these rather than becoming a third answer nobody was warned about.
    """

    #: The music files and everything else on the volume EXCEPT the database
    #: fileset, which never rides a live mirror.
    FILES = "files"
    #: The rekordbox database and its SQLite sidecars, captured as one matched
    #: set with no rekordbox process running.
    DATABASE = "database"


class AgeState(StrEnum):
    """Why an age is or is not usable. Three answers, three remediations."""

    KNOWN = "known"
    NEVER_RECORDED = "never-recorded"
    RECORDED_IN_THE_FUTURE = "recorded-in-the-future"


class Remedy(StrEnum):
    """What to do about an unreadable fact file, as a TOKEN not a command (D2).

    THE THIRD MEMBER IS NOT A CORRUPTION. A file this account may not open and a
    file whose contents are damaged are two conditions with opposite fixes, and
    one token over both told a user to repair or reset the record of when their
    music was last protected in order to fix a permission. The file may be
    perfectly intact, and resetting library state is a destructive answer to a
    question that was never asked.
    """

    REPAIR_BACKUP_FACTS = "repair-backup-facts"
    UPGRADE_CRATEKIT = "upgrade-cratekit"
    GRANT_PATH_ACCESS = "grant-path-access"


class BackupFactsUnreadable(Exception):
    """The fact file exists and cannot be understood.

    Deliberately NOT collapsed into "no backup recorded". A caller that treated
    an unreadable record as an absent one would report a library with a perfectly
    good backup as never backed up, and the user's fix (repair one small file) has
    nothing to do with the fix the report implies (run a backup). KTD25: the
    cause travels, the caller decides.
    """

    def __init__(self, message: str, *, path: Path, remedy: Remedy) -> None:
        super().__init__(message)
        self.path = path
        self.remedy = remedy


@dataclass(frozen=True, slots=True)
class BackupFact:
    """One portion's last successful completion.

    ``destination`` is recorded because "backed up" is meaningless without
    "where": a user who reconfigured their remote last month has a fresh-looking
    age describing a destination they no longer use.
    """

    portion: Portion
    completed_at: datetime
    destination: str


@dataclass(frozen=True, slots=True)
class PortionAge:
    """The answer for one portion, with the reasoning kept rather than discarded."""

    portion: Portion
    state: AgeState
    age: timedelta | None = None
    completed_at: datetime | None = None
    destination: str | None = None

    @property
    def usable(self) -> bool:
        return self.state is AgeState.KNOWN


def path_for(cfg: config.Config) -> Path:
    """Where the fact file lives, resolved through the state inventory.

    Through ``state_path`` rather than composed here, because a module that
    builds its own path under a state root has invented a state file the
    inventory does not know about, and nothing that walks the inventory will
    find it, snapshot it, or clear it.
    """
    return config.state_path(STATE_KEY, cfg)


def read_facts(cfg: config.Config) -> dict[Portion, BackupFact]:
    """Every recorded fact, keyed by portion. An absent file is an empty dict.

    The portions half of :func:`_read`, which is the one reader of the file.
    """
    return _read(cfg)[0]


#: What :func:`_read` hands back for the full comparison when the file does not
#: carry the key at all, which is a different answer from carrying it as null.
_ABSENT = object()


def _read(cfg: config.Config) -> tuple[dict[Portion, BackupFact], object]:
    """The file, read once: every portion's fact, and the full comparison AS HELD.

    ONE READER OF THE FILE, so a document the portions reader refuses cannot
    answer a question about the full comparison.

    THE FULL COMPARISON IS RETURNED UNPARSED, and that is deliberate. It feeds
    one informational line, and the portions feed the age a destructive session
    reads and the publish at the end of a transfer. Parsed here, a damaged
    entry under that one key would refuse every reader of the file, and a
    backup would fail after its transfer over a date nothing depends on.
    :func:`full_comparison_age` parses it and is the only reader it can refuse.

    THE PORTIONS, as :func:`read_facts` has always returned them:

    Absent is normal and is not an error: it is the state of every library
    before the backup module has run once. A file that exists but cannot be
    parsed is an error, for the reason in :class:`BackupFactsUnreadable`.

    Unknown portion names are IGNORED rather than raising, so a record written
    by a build that knows a portion this one does not stays readable for the
    portions both builds share. A newer SCHEMA_VERSION is a different matter and
    does raise: an unknown portion is extra information, an unknown shape is a
    reading this build cannot vouch for.
    """
    path = path_for(cfg)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return {}, _ABSENT
    except OSError as exc:
        # TWO CONDITIONS, TWO SENTENCES, TWO ACTS. A permission is not a
        # corruption, and it does not establish that the file is there either: an
        # untraversable PARENT raises exactly this, and nothing under such a
        # parent has been observed at all. "Exists but could not be read" with
        # "repair or reset them" beside it sent a user to reset library state
        # over a directory their operating system would not open.
        if cause.permission_denied(exc) is not None:
            raise BackupFactsUnreadable(
                f"{path} could not be read: {exc}. Whether the file is even "
                f"there was not established, because a directory on the way to "
                f"it that this account cannot open fails the same way",
                path=path,
                remedy=Remedy.GRANT_PATH_ACCESS,
            ) from exc
        raise BackupFactsUnreadable(
            f"{path} exists but could not be read: {exc}",
            path=path,
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        ) from exc

    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BackupFactsUnreadable(
            f"{path} is not readable as JSON: {exc}",
            path=path,
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        ) from exc
    if not isinstance(data, dict):
        raise BackupFactsUnreadable(
            f"{path} does not hold an object at its top level",
            path=path,
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )

    version = data.get("schema_version")
    if not isinstance(version, int):
        raise BackupFactsUnreadable(
            f"{path} carries no integer schema_version, so nothing can be said "
            f"about the shape of what follows it",
            path=path,
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )
    if version > SCHEMA_VERSION:
        raise BackupFactsUnreadable(
            f"{path} was written at schema version {version}; this build "
            f"understands {SCHEMA_VERSION}",
            path=path,
            remedy=Remedy.UPGRADE_CRATEKIT,
        )

    entries = data.get("portions")
    if not isinstance(entries, dict):
        raise BackupFactsUnreadable(
            f"{path} has no portions table",
            path=path,
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )

    facts: dict[Portion, BackupFact] = {}
    known = {p.value for p in Portion}
    for name, entry in entries.items():
        if name not in known or not isinstance(entry, dict):
            continue
        facts[Portion(name)] = _fact(Portion(name), entry, named=name, path=path)

    return facts, data.get(FULL_COMPARISON_KEY, _ABSENT)


def _as_held(fact: BackupFact | None) -> dict | None:
    """One fact in the shape the file holds it under the full comparison key."""
    if fact is None:
        return None
    return {
        "completed_at": fact.completed_at.isoformat(),
        "destination": fact.destination,
    }


def _full_comparison(
    cfg: config.Config, facts: dict[Portion, BackupFact], held: object
) -> BackupFact | None:
    """The last full comparison, parsed, or a refusal naming what cannot be read.

    AN ABSENT KEY IS A FILE FROM A BUILD THAT HAD ONE MODE. Every build that
    does not write this key lists the remote folder by folder, so the files
    fact it left IS the last full comparison. Answering "never" there would
    tell a person whose every backup so far was a full one that none ever ran.
    """
    if held is _ABSENT:
        return facts.get(Portion.FILES)
    if held is None:
        return None
    path = path_for(cfg)
    if not isinstance(held, dict):
        raise BackupFactsUnreadable(
            f"{path} holds something other than an object or null under "
            f"{FULL_COMPARISON_KEY!r}",
            path=path,
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )
    return _fact(Portion.FILES, held, named=FULL_COMPARISON_KEY, path=path)


def _fact(portion: Portion, entry: dict, *, named: str, path: Path) -> BackupFact:
    """One recorded completion, or a refusal naming what about it cannot be read."""
    stamp = entry.get("completed_at")
    try:
        completed = datetime.fromisoformat(str(stamp))
    except (TypeError, ValueError) as exc:
        raise BackupFactsUnreadable(
            f"{path} records {named!r} as completing at {stamp!r}, which is "
            f"not an ISO timestamp",
            path=path,
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        ) from exc
    if completed.tzinfo is None:
        # A naive timestamp is unanswerable, not merely awkward: two
        # installations of one library can sit in different zones, so the
        # same text would describe two different instants.
        raise BackupFactsUnreadable(
            f"{path} records {named!r} without a time zone offset, so the "
            f"instant it names depends on who reads it",
            path=path,
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )
    return BackupFact(
        portion=portion,
        completed_at=completed,
        destination=str(entry.get("destination") or ""),
    )


def _age_of(portion: Portion, fact: BackupFact | None, moment: datetime) -> PortionAge:
    """One fact as an age, in the three answers :class:`AgeState` names."""
    if fact is None:
        return PortionAge(portion=portion, state=AgeState.NEVER_RECORDED)
    delta = moment - fact.completed_at
    state = (
        AgeState.RECORDED_IN_THE_FUTURE
        if delta < -FUTURE_TOLERANCE
        else AgeState.KNOWN
    )
    return PortionAge(
        portion=portion,
        state=state,
        age=delta if state is AgeState.KNOWN else None,
        completed_at=fact.completed_at,
        destination=fact.destination,
    )


def full_comparison_age(cfg: config.Config, *, now: datetime | None = None) -> PortionAge:
    """How long ago the file mirror last compared folder by folder (R-757).

    The same three answers a portion's age has, and for the same reasons. It is
    an age of the FILES portion's comparison, so that is the portion it names.
    """
    moment = now or datetime.now(timezone.utc)
    facts, held = _read(cfg)
    return _age_of(Portion.FILES, _full_comparison(cfg, facts, held), moment)


def ages(cfg: config.Config, *, now: datetime | None = None) -> tuple[PortionAge, ...]:
    """One answer per declared portion, always, in declaration order.

    The set is DERIVED from :class:`Portion` rather than enumerated here, so a
    portion added later cannot be silently absent from the report that decides
    whether a user is warned (P3).
    """
    moment = now or datetime.now(timezone.utc)
    facts = read_facts(cfg)
    return tuple(_age_of(portion, facts.get(portion), moment) for portion in Portion)


def oldest_usable_age(
    cfg: config.Config, *, now: datetime | None = None
) -> timedelta | None:
    """The age R15's warning quotes, or None when any portion has no usable one.

    None rather than "the oldest of whatever happened to be readable", because
    the warning's whole job is to say how well protected the library is, and a
    number derived from half the portions describes a library that is half
    protected as though it were fully protected.
    """
    reported = ages(cfg, now=now)
    if any(not entry.usable for entry in reported):
        return None
    return max(entry.age for entry in reported if entry.age is not None)


def record(
    cfg: config.Config,
    portion: Portion,
    *,
    completed_at: datetime,
    destination: str,
    full_comparison: bool = False,
) -> Path:
    """Record one portion's successful completion, leaving the others alone.

    ``full_comparison`` says this completion compared the library with the
    remote folder by folder, and moves that fact to this instant. Without it
    the fact is carried through as it was read, INCLUDING the one a file from
    an earlier build implies, so the first fast run after an upgrade does not
    erase the date of the last full one.

    Read-modify-write rather than a whole-file overwrite. The two portions
    complete independently and often in the same run, and a writer that replaced
    the file would erase the database portion's record every time the file mirror
    finished on its own, which is the exact case this file exists to distinguish.

    Refuses a naive timestamp at the boundary rather than storing one and
    refusing at read time, so the failure lands on the code that produced the
    value instead of on the user reading a warning weeks later.
    """
    if completed_at.tzinfo is None:
        raise ValueError(
            "completed_at must carry a time zone offset; a naive timestamp names "
            "a different instant to every reader, and two installations of one "
            "library legitimately sit in different zones"
        )
    read, held = _read(cfg)
    facts = dict(read)
    if held is _ABSENT:
        # BEFORE THE NEW FACT REPLACES THE OLD ONE, because what an earlier
        # build's file implies is the files fact it wrote, not this one.
        held = _as_held(read.get(Portion.FILES))
    facts[portion] = BackupFact(
        portion=portion, completed_at=completed_at, destination=destination
    )
    if full_comparison:
        held = _as_held(facts[portion])
    payload = {
        "schema_version": SCHEMA_VERSION,
        # ALWAYS WRITTEN, null included. Its absence is how a file from a build
        # with one mode is recognised, so a build with two must never leave it
        # out, or its own fast run would be read as a full one.
        #
        # CARRIED THROUGH AS IT WAS HELD when this record is not a full
        # comparison, damaged or not. Replacing an entry nobody could read
        # with null would turn "cannot be read" into "never ran".
        FULL_COMPARISON_KEY: held,
        "portions": {
            fact.portion.value: {
                "completed_at": fact.completed_at.isoformat(),
                "destination": fact.destination,
            }
            # Sorted so the bytes are a function of the content alone. An
            # unordered dump makes every write a diff even when nothing changed,
            # which is noise in exactly the file somebody reads to find out
            # whether anything changed.
            for fact in sorted(facts.values(), key=lambda f: f.portion.value)
        },
    }
    path = path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


#: The portions, exposed as an immutable mapping for callers that want to render
#: a name per portion without re-deriving the set.
PORTIONS: MappingProxyType = MappingProxyType({p.value: p for p in Portion})


# ---------------------------------------------------------------------------
# What a queued backup item ran (R-349)
# ---------------------------------------------------------------------------

#: The inventory key of the per item outcome directory.
OUTCOMES_KEY = "backup_outcomes"

#: The ``progress`` field both ``job show`` and ``backup run --job`` carry the
#: outcomes under. ``job_state/1`` closes its top level, so it rides inside.
OUTCOMES_FIELD = "outcomes"

#: The key :func:`read_outcomes` reports under when a job's directory exists and
#: cannot be listed. Not a portion name, so it cannot be read as one item.
UNLISTABLE = "(unlistable)"


def outcome_path(job_id: str, item_id: str) -> Path:
    """Where one queued item's outcome lives, keyed by job and item.

    HERE AND NOT IN THE BACKUP MODULE, for the reason the module docstring gives
    for the age: ``job show`` reads this, and ``job show`` is core CLI that must
    not import a toggleable feature module (KTD23, KTD26). One path function
    serves the writer and the reader, so the two cannot name different files.
    """
    return config.state_path(OUTCOMES_KEY) / job_id / f"{item_id}.json"


def write_outcome(job_id: str, item_id: str, payload: dict) -> Path:
    """Write one item's outcome now, atomically, owner only (P1).

    The FAILURE channel. A successful item's outcome is staged and handed to the
    job engine's commit instead, because that commit is what completes the item.
    """
    path = outcome_path(job_id, item_id)
    config.atomic_write_bytes(encode_outcome(payload), path)
    return path


def clear_outcome(job_id: str, item_id: str) -> None:
    """Remove one item's record before a new attempt at that item.

    A retried item that fails some other way, before any transfer or on a fact
    file it cannot write, reaches neither channel. Without this the previous
    attempt's failed commands would sit beside the new attempt's different
    cause, and a person would debug a failure that did not happen this time.
    """
    outcome_path(job_id, item_id).unlink(missing_ok=True)


def encode_outcome(payload: dict) -> bytes:
    """The bytes both channels write, so a staged success and a direct failure
    are the same format."""
    return json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def read_outcomes(job_id: str) -> dict[str, dict] | None:
    """Every recorded item outcome for one job, keyed by item, or None.

    NONE MEANS NO ITEM OF THIS JOB EVER RECORDED ONE, which is every job that is
    not a backup and every backup whose items have not run. The caller omits the
    field on None rather than printing an empty mapping, so a job of another verb
    does not grow a backup field.

    A FILE THAT CANNOT BE READ IS REPORTED AS UNREADABLE, NOT SKIPPED. Skipping
    it would print the other item's commands alone, and a reader would take the
    missing item for one that never ran. Staged files are not outcomes and are
    ignored: a staged file is one the engine had not yet committed.
    """
    directory = config.state_path(OUTCOMES_KEY) / job_id
    if not directory.is_dir():
        return None
    try:
        # ``iterdir`` and not ``glob``: on 3.12 ``glob`` swallows a permission
        # error on the directory and yields nothing, which is the "nothing ran"
        # reading this branch exists to refuse. Measured in review, 2026-09-21.
        files = sorted(p for p in directory.iterdir() if p.suffix == ".json")
    except OSError as exc:
        # A directory that exists and cannot be listed is not "nothing ran".
        return {UNLISTABLE: {"unreadable": f"{directory}: {exc}"}}
    found: dict[str, dict] = {}
    for path in files:
        try:
            found[path.stem] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            found[path.stem] = {"unreadable": f"{path}: {exc}"}
    return found or None


__all__ = [
    "FULL_COMPARISON_KEY",
    "FUTURE_TOLERANCE",
    "OUTCOMES_FIELD",
    "OUTCOMES_KEY",
    "PORTIONS",
    "SCHEMA_VERSION",
    "STATE_KEY",
    "UNLISTABLE",
    "AgeState",
    "BackupFact",
    "BackupFactsUnreadable",
    "Portion",
    "PortionAge",
    "Remedy",
    "ages",
    "clear_outcome",
    "encode_outcome",
    "full_comparison_age",
    "oldest_usable_age",
    "outcome_path",
    "path_for",
    "read_facts",
    "read_outcomes",
    "record",
    "write_outcome",
]
