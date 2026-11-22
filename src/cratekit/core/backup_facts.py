"""The backup-age fact: a FILE core reads, never a module core imports (R15, KTD23).

Importing the opt-in backup module would fail on a slim install, inside the
warning before the riskiest operation, so backup publishes and core reads.
Ages are PER PORTION, since files current and database stale is the normal
state; never recorded and a future timestamp are answers of their own, each
with its own remediation. Written through the shared atomic writer (P1).
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType

from cratekit.core import cause, config

#: The state entry this module owns, named once so no caller means another file.
STATE_KEY = "backup_facts"

#: A newer version is not read, since a guessed shape is worse than no answer.
SCHEMA_VERSION = 1

#: How far ahead of now a completion may sit before it reads as clock skew.
FUTURE_TOLERANCE = timedelta(hours=1)

#: When the file mirror last compared folder by folder (R-757), beside ``portions``.
FULL_COMPARISON_KEY = "full_comparison"

#: When the file mirror last ran a FULL CHECK of every file on both sides (U317).
FULL_CHECK_KEY = "full_check"

#: How old the last full check may be before the next backup runs one (2026-11-21).
FULL_CHECK_DAYS = 7

#: A completed portion's ``kind``, files ``full``, ``quick`` or ``skipped``, and
#: database ``snapshot`` or ``unchanged``.
KIND_FULL = "full"
KIND_QUICK = "quick"
KIND_SKIPPED = "skipped"
KIND_SNAPSHOT = "snapshot"
KIND_UNCHANGED = "unchanged"
KINDS = (KIND_FULL, KIND_QUICK, KIND_SKIPPED, KIND_SNAPSHOT, KIND_UNCHANGED)


class Portion(StrEnum):
    """The two halves of a library backup, exactly the two R15 warns about."""

    #: The music files, EXCEPT the database fileset, which never rides a live mirror.
    FILES = "files"
    #: The database and its SQLite sidecars, one matched set with rekordbox closed.
    DATABASE = "database"


class AgeState(StrEnum):
    """Why an age is or is not usable. Three answers, three remediations."""

    KNOWN = "known"
    NEVER_RECORDED = "never-recorded"
    RECORDED_IN_THE_FUTURE = "recorded-in-the-future"


class Remedy(StrEnum):
    """What to do about an unreadable fact file, as a TOKEN not a command (D2).

    THE THIRD MEMBER IS NOT A CORRUPTION, since a permission is never fixed by a reset.
    """

    REPAIR_BACKUP_FACTS = "repair-backup-facts"
    UPGRADE_CRATEKIT = "upgrade-cratekit"
    GRANT_PATH_ACCESS = "grant-path-access"


class BackupFactsUnreadable(Exception):
    """The fact file exists and cannot be understood.

    Never collapsed into no backup recorded, since the fixes differ (KTD25).
    """

    def __init__(self, message: str, *, path: Path, remedy: Remedy) -> None:
        super().__init__(message)
        self.path = path
        self.remedy = remedy


@dataclass(frozen=True, slots=True)
class BackupFact:
    """One portion's last successful completion, and where, since an age needs its destination."""

    portion: Portion
    completed_at: datetime
    destination: str
    #: One of :data:`KINDS` (U317), or None from an earlier build, always a full run.
    kind: str | None = None
    #: What that run changed and how long it took, or None where not recorded.
    summary: Mapping[str, object] | None = None


@dataclass(frozen=True, slots=True)
class PortionAge:
    """The answer for one portion, with the reasoning kept rather than discarded."""

    portion: Portion
    state: AgeState
    age: timedelta | None = None
    completed_at: datetime | None = None
    destination: str | None = None
    kind: str | None = None
    summary: Mapping[str, object] | None = None
    #: Files portion only (U317), when the next full check is due, or None when the
    #: next backup runs one, and why it does, or an empty string.
    full_check_due: datetime | None = None
    full_check_overdue: str = ""

    @property
    def usable(self) -> bool:
        return self.state is AgeState.KNOWN


def path_for(cfg: config.Config) -> Path:
    """Where the fact file lives, through ``state_path`` so the inventory knows it."""
    return config.state_path(STATE_KEY, cfg)


def read_facts(cfg: config.Config) -> dict[Portion, BackupFact]:
    """Every recorded fact, keyed by portion. An absent file is an empty dict."""
    return _read(cfg)[0]


#: The full comparison of a file lacking the key, which differs from a null one.
_ABSENT = object()

#: Keys held beside the portions, read unparsed and parsed by their own readers.
_HELD_KEYS = (FULL_COMPARISON_KEY, FULL_CHECK_KEY)


def _read(cfg: config.Config) -> tuple[dict[Portion, BackupFact], dict[str, object]]:
    """The file, read once: every portion's fact, and the held keys AS HELD.

    THE HELD KEYS ARE RETURNED UNPARSED, so a damaged informational entry cannot
    refuse the age a destructive session reads. An absent file is normal, an
    unknown portion is ignored, and a newer SCHEMA_VERSION raises.
    """
    path = path_for(cfg)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return {}, {key: _ABSENT for key in _HELD_KEYS}
    except OSError as exc:
        # TWO CONDITIONS, TWO SENTENCES, TWO ACTS. A permission is not a corruption,
        # and an untraversable PARENT raises this too, so the file may not exist.
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

    return facts, {key: data.get(key, _ABSENT) for key in _HELD_KEYS}


def _as_held(fact: BackupFact | None) -> dict | None:
    """One fact in the shape the file holds it under the full comparison key."""
    if fact is None:
        return None
    return {
        "completed_at": fact.completed_at.isoformat(),
        "destination": fact.destination,
    }


def _full_comparison(
    cfg: config.Config,
    facts: dict[Portion, BackupFact],
    held: object,
    key: str = FULL_COMPARISON_KEY,
) -> BackupFact | None:
    """The last full comparison, parsed, or a refusal naming what cannot be read.

    AN ABSENT KEY IS A FILE FROM A BUILD THAT HAD ONE MODE, so its files fact answers.
    """
    if held is _ABSENT:
        return facts.get(Portion.FILES)
    if held is None:
        return None
    path = path_for(cfg)
    if not isinstance(held, dict):
        raise BackupFactsUnreadable(
            f"{path} holds something other than an object or null under "
            f"{key!r}",
            path=path,
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )
    return _fact(Portion.FILES, held, named=key, path=path)


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
        # A naive timestamp is unanswerable, since installations can sit in different zones.
        raise BackupFactsUnreadable(
            f"{path} records {named!r} without a time zone offset, so the "
            f"instant it names depends on who reads it",
            path=path,
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )
    kind = entry.get("kind")
    summary = entry.get("summary")
    return BackupFact(
        portion=portion,
        completed_at=completed,
        destination=str(entry.get("destination") or ""),
        # Read loosely; a missing kind sends the next files run full.
        kind=kind if kind in KINDS else None,
        summary=dict(summary) if isinstance(summary, dict) else None,
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
        kind=fact.kind,
        summary=fact.summary,
    )


def full_comparison_age(cfg: config.Config, *, now: datetime | None = None) -> PortionAge:
    """How long ago the file mirror last compared folder by folder (R-757), as a files age."""
    moment = now or datetime.now(timezone.utc)
    facts, held = _read(cfg)
    return _age_of(
        Portion.FILES, _full_comparison(cfg, facts, held[FULL_COMPARISON_KEY]), moment
    )


def full_check_age(cfg: config.Config, *, now: datetime | None = None) -> PortionAge:
    """How long ago the last full check ran (U317); an absent key answers the files fact."""
    moment = now or datetime.now(timezone.utc)
    facts, held = _read(cfg)
    return _age_of(
        Portion.FILES,
        _full_comparison(cfg, facts, held[FULL_CHECK_KEY], key=FULL_CHECK_KEY),
        moment,
    )


def took(seconds: object) -> str:
    """How long a recorded run took, one spelling for the verb's report and doctor."""
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
        return ""
    if seconds < 1:
        return " in under a second"
    return f" in {seconds:.0f} seconds"


def full_check_due(answer: PortionAge) -> datetime | None:
    """When the next full check is due, or None when one is due at once."""
    if answer.state is not AgeState.KNOWN or answer.completed_at is None:
        return None
    return answer.completed_at + timedelta(days=FULL_CHECK_DAYS)


def ages(cfg: config.Config, *, now: datetime | None = None) -> tuple[PortionAge, ...]:
    """One answer per declared portion, DERIVED from :class:`Portion` so none goes missing (P3)."""
    moment = now or datetime.now(timezone.utc)
    facts, held = _read(cfg)
    out = [_age_of(portion, facts.get(portion), moment) for portion in Portion]
    due, overdue = _full_check_schedule(cfg, facts, held, moment)
    return tuple(
        replace(entry, full_check_due=due, full_check_overdue=overdue)
        if entry.portion is Portion.FILES
        else entry
        for entry in out
    )


def _full_check_schedule(
    cfg: config.Config, facts: dict[Portion, BackupFact], held: dict[str, object], moment: datetime
) -> tuple[datetime | None, str]:
    """When the next full check is due and why the next backup runs one (U317).

    A DAMAGED FULL CHECK ENTRY IS A REASON, NEVER A REFUSAL, so ``ages`` still answers.
    """
    try:
        fact = _full_comparison(cfg, facts, held[FULL_CHECK_KEY], key=FULL_CHECK_KEY)
    except BackupFactsUnreadable as exc:
        return None, f"the record of the last full check could not be read: {exc}"
    answer = _age_of(Portion.FILES, fact, moment)
    if answer.state is AgeState.NEVER_RECORDED:
        return None, "no full check is on record"
    if answer.state is AgeState.RECORDED_IN_THE_FUTURE:
        return None, "the last full check is recorded ahead of now"
    due = full_check_due(answer)
    if answer.destination != str(cfg.backup.dest or ""):
        return None, "the last full check was of another mirror"
    if answer.age is None or answer.age >= timedelta(days=FULL_CHECK_DAYS):
        days = answer.age.days if answer.age is not None else "an unknown number of"
        return None, f"the last full check was {days} days ago"
    return due, ""


def oldest_usable_age(
    cfg: config.Config, *, now: datetime | None = None
) -> timedelta | None:
    """The age R15's warning quotes, or None when any portion has no usable one.

    Never the oldest readable age, which would call a half protected library protected.
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
    full_check: bool = False,
    kind: str | None = None,
    summary: Mapping[str, object] | None = None,
) -> Path:
    """Record one portion's successful completion, leaving the others alone.

    Read, modify, write, since the portions complete independently. Held keys this
    completion does not move carry through as read, and a naive timestamp is
    refused here, at the code that made it.
    """
    if completed_at.tzinfo is None:
        raise ValueError(
            "completed_at must carry a time zone offset; a naive timestamp names "
            "a different instant to every reader, and two installations of one "
            "library legitimately sit in different zones"
        )
    if kind is not None and kind not in KINDS:
        raise ValueError(f"{kind!r} is not a kind of backup run; the kinds are {KINDS}")
    read, held_keys = _read(cfg)
    facts = dict(read)
    held = held_keys[FULL_COMPARISON_KEY]
    checked = held_keys[FULL_CHECK_KEY]
    if held is _ABSENT:
        # BEFORE THE NEW FACT REPLACES THE OLD ONE, which an earlier build's file implies.
        held = _as_held(read.get(Portion.FILES))
    if checked is _ABSENT:
        # The same reading for the full check, for the same reason.
        checked = _as_held(read.get(Portion.FILES))
    facts[portion] = BackupFact(
        portion=portion,
        completed_at=completed_at,
        destination=destination,
        kind=kind,
        summary=dict(summary) if summary is not None else None,
    )
    if full_comparison:
        held = _as_held(facts[portion])
    if full_check:
        checked = _as_held(facts[portion])
    payload = {
        "schema_version": SCHEMA_VERSION,
        # ALWAYS WRITTEN, null included, since absence marks a one mode build, and
        # CARRIED THROUGH AS IT WAS HELD, so cannot be read never becomes never ran.
        FULL_COMPARISON_KEY: held,
        # Always written, null included, for the reason the key above is.
        FULL_CHECK_KEY: checked,
        "portions": {
            fact.portion.value: {
                "completed_at": fact.completed_at.isoformat(),
                "destination": fact.destination,
                **({"kind": fact.kind} if fact.kind is not None else {}),
                **({"summary": dict(fact.summary)} if fact.summary is not None else {}),
            }
            # Sorted so the bytes are a function of the content alone.
            for fact in sorted(facts.values(), key=lambda f: f.portion.value)
        },
    }
    path = path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


#: The portions as an immutable mapping, for rendering a name per portion.
PORTIONS: MappingProxyType = MappingProxyType({p.value: p for p in Portion})


# What a queued backup item ran (R-349)

#: The inventory key of the per item outcome directory.
OUTCOMES_KEY = "backup_outcomes"

#: The ``progress`` field the outcomes ride inside, as ``job_state/1`` closes its top level.
OUTCOMES_FIELD = "outcomes"

#: Where :func:`read_outcomes` reports an unlistable job directory; never a portion name.
UNLISTABLE = "(unlistable)"


def outcome_path(job_id: str, item_id: str) -> Path:
    """One queued item's outcome file, here so core ``job show`` imports no module (KTD23)."""
    return config.state_path(OUTCOMES_KEY) / job_id / f"{item_id}.json"


def write_outcome(job_id: str, item_id: str, payload: dict) -> Path:
    """Write one item's outcome now, atomically, owner only (P1), the FAILURE channel."""
    path = outcome_path(job_id, item_id)
    config.atomic_write_bytes(encode_outcome(payload), path)
    return path


def clear_outcome(job_id: str, item_id: str) -> None:
    """Remove one item's record before a new attempt, so an old failure is not read as new."""
    outcome_path(job_id, item_id).unlink(missing_ok=True)


def encode_outcome(payload: dict) -> bytes:
    """The bytes both channels write, so success and failure share one format."""
    return json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def read_outcomes(job_id: str) -> dict[str, dict] | None:
    """Every recorded item outcome for one job, keyed by item, or None when none was recorded.

    A FILE THAT CANNOT BE READ IS REPORTED AS UNREADABLE, NOT SKIPPED; staged files are ignored.
    """
    directory = config.state_path(OUTCOMES_KEY) / job_id
    if not directory.is_dir():
        return None
    try:
        # ``iterdir`` and not ``glob``, which swallows a permission error on 3.12.
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
    "FULL_CHECK_DAYS",
    "FULL_CHECK_KEY",
    "FULL_COMPARISON_KEY",
    "KINDS",
    "KIND_FULL",
    "KIND_QUICK",
    "KIND_SKIPPED",
    "KIND_SNAPSHOT",
    "KIND_UNCHANGED",
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
    "full_check_age",
    "full_check_due",
    "took",
    "full_comparison_age",
    "oldest_usable_age",
    "outcome_path",
    "path_for",
    "read_facts",
    "read_outcomes",
    "record",
    "write_outcome",
]
