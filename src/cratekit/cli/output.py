"""The versioned output envelope: one machine contract for every verb (R32).

Two version numbers: ``envelope`` versions the outer frame and ``schema``
versions each payload surface as ``"<name>/<major>"``, so one payload changing
never forces the others to bump. Human rendering lives in ``cratekit.cli.render``
and never in a field, so a wording change is never a schema change.
``pending_human_action`` and ``cause`` are required keys with nullable values,
so a consumer never has to tell absent from empty. Ranked FOUNDATION, because
every layer emits envelopes.
"""

from __future__ import annotations

import hashlib
import json
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from cratekit.core import config
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy

#: The outer contract version, bumped only when the frame itself changes.
ENVELOPE_VERSION = 1

#: The five payload surfaces R32 names, reserved here so no unit invents its own
#: shape. Each maps a field name to a JSON type name, a plain declaration that a
#: test hashes, since this module is imported on every ``crate`` invocation.
_PAYLOAD_FIELDS: Mapping[str, Mapping[str, str]] = MappingProxyType(
    {
        "plan": MappingProxyType(
            {
                # Makes a decision refuse when the world moved since the preview.
                "digest": "string",
                "items": "array",
                "totals": "object",
                # Non-null when the plan was offered in pieces.
                "chunk": "object|null",
            }
        ),
        "match": MappingProxyType(
            {
                # Three states from version 1, since adding one later is a
                # schema break (R11).
                "matched": "array",
                "needs_review": "array",
                "missing": "array",
            }
        ),
        "review_set": MappingProxyType(
            {
                "queue": "string",
                "items": "array",
                "unresolved": "integer",
            }
        ),
        "job_state": MappingProxyType(
            {
                "job_id": "string",
                "state": "string",
                # The engine reads a cause rather than a child's exit code
                # (KTD25).
                "cause": "object|null",
                "progress": "object",
            }
        ),
        "diagnostic": MappingProxyType(
            {
                # {key, title, status, detail, remedy} per check, the remedy a
                # token the CLI renders (D2).
                "checks": "array",
                "summary": "object",
            }
        ),
    }
)

#: The current major for each payload surface. A bump lands here and in the
#: committed lock file together, or the schema test fails.
_PAYLOAD_MAJORS: Mapping[str, int] = MappingProxyType(
    {"plan": 1, "match": 1, "review_set": 1, "job_state": 1, "diagnostic": 1}
)

#: The progress stream's events (U963), declared beside the payload surfaces
#: and never one of them: no envelope carries an event, so ``schema_names``
#: stays the five R32 names. Every event carries the common fields and its
#: kind's own, nothing else; ``tests/schemas/progress.v1.json`` pins the
#: document, so a change to a field is a change to that file.
PROGRESS_SCHEMA = "progress/1"

_PROGRESS_COMMON: Mapping[str, str] = MappingProxyType(
    {"schema": "string", "verb": "string", "run_id": "string", "at": "string", "kind": "string"}
)

_PROGRESS_KINDS: Mapping[str, Mapping[str, str]] = MappingProxyType(
    {
        # A chain's step by its place in the verb's order; ``command`` is the
        # verb a step runs, ``detail`` what a step says that is not a command.
        "step": MappingProxyType(
            {
                "index": "integer",
                "of": "integer",
                "name": "string",
                "command": "string|null",
                "detail": "string|null",
            }
        ),
        # A job a chain drives, its counts as ``job_state``'s progress carries them.
        "job": MappingProxyType(
            {"step": "string", "job_id": "string", "state": "string", "progress": "object"}
        ),
        # A progress call with no structure yet, its text as human output says it.
        "line": MappingProxyType({"text": "string"}),
        # The last event, written just before the envelope.
        "end": MappingProxyType({"exit_code": "integer"}),
    }
)


def progress_document() -> dict[str, Any]:
    """The machine description of a ``progress/1`` event, kind by kind."""
    return {
        "schema": PROGRESS_SCHEMA,
        "type": "object",
        "common": {key: {"type": value} for key, value in sorted(_PROGRESS_COMMON.items())},
        "kinds": {
            kind: {
                "properties": {key: {"type": value} for key, value in sorted(fields.items())},
                "required": sorted(fields),
            }
            for kind, fields in sorted(_PROGRESS_KINDS.items())
        },
        "additionalProperties": False,
    }


def progress_event(kind: str, *, verb: str, run_id: str, **fields: Any) -> dict[str, Any]:
    """One event, its common fields first, stamped now."""
    return {
        "schema": PROGRESS_SCHEMA,
        "verb": verb,
        "run_id": run_id,
        "at": timestamp(),
        "kind": kind,
        **fields,
    }


def progress_problems(event: Mapping[str, Any]) -> list[str]:
    """Validate one event against its kind's declaration. Empty means valid."""
    kind = event.get("kind")
    own = _PROGRESS_KINDS.get(kind) if isinstance(kind, str) else None
    if own is None:
        return [f"{kind!r} is not a declared progress kind"]
    problems = _field_problems({**_PROGRESS_COMMON, **own}, event)
    if event.get("schema") != PROGRESS_SCHEMA:
        problems.append(f"schema is {event.get('schema')!r}, not {PROGRESS_SCHEMA!r}")
    return problems

#: The envelope's required keys, in serialization order. The conformance suite
#: derives its requirements from this.
ENVELOPE_KEYS: tuple[str, ...] = (
    "envelope",
    "schema",
    "verb",
    "run_id",
    "outcome",
    "exit_code",
    "started",
    "ended",
    "pending_human_action",
    "cause",
    "warnings",
    "resumable",
    "data",
)

#: The closed set of things a person can be waiting to do.
PENDING_KINDS: frozenset[str] = frozenset(
    {"rekordbox_import", "review", "manual_move", "credential", "backup_ack", "external_step"}
)


class SchemaError(ValueError):
    """A payload surface or version that is not declared here."""


def schema_names() -> tuple[str, ...]:
    """Every declared payload surface, sorted."""
    return tuple(sorted(_PAYLOAD_FIELDS))


def current_schema(name: str) -> str:
    """The current ``"<name>/<major>"`` identifier for one surface."""
    try:
        return f"{name}/{_PAYLOAD_MAJORS[name]}"
    except KeyError:
        raise SchemaError(
            f"{name!r} is not a declared payload surface. Declared: "
            f"{', '.join(schema_names())}. R32 names five, and a sixth is a "
            f"decision rather than an oversight."
        ) from None


def schema_document(name: str) -> dict[str, Any]:
    """The machine description of one payload surface, at its current major.

    A type per field plus the required list; it is what the lock file hashes,
    so it must change whenever the payload does.
    """
    fields = _PAYLOAD_FIELDS[name] if name in _PAYLOAD_FIELDS else None
    if fields is None:
        raise SchemaError(f"{name!r} is not a declared payload surface")
    return {
        "schema": current_schema(name),
        "type": "object",
        "properties": {key: {"type": value} for key, value in sorted(fields.items())},
        "required": sorted(fields),
        "additionalProperties": False,
    }


def canonical_json(document: Mapping[str, Any]) -> str:
    """The one serialization the lock file hashes: sorted keys, no whitespace."""
    return json.dumps(document, sort_keys=True, separators=(",", ":"))


def schema_fingerprint(name: str) -> str:
    """The hash a change to a payload has to move, and a bump has to record."""
    return hashlib.sha256(canonical_json(schema_document(name)).encode()).hexdigest()


def payload_problems(name: str, data: Mapping[str, Any]) -> list[str]:
    """Validate a payload against its declared surface. Empty means valid.

    Returns every problem, so one fix is not one round trip per field.
    """
    fields = _PAYLOAD_FIELDS.get(name)
    if fields is None:
        return [f"{name!r} is not a declared payload surface"]
    return _field_problems(fields, data)


def _field_problems(fields: Mapping[str, str], data: Mapping[str, Any]) -> list[str]:
    """Every field missing, undeclared or of the wrong type, against ``fields``."""
    problems = [f"missing required field {key!r}" for key in sorted(fields) if key not in data]
    problems += [f"undeclared field {key!r}" for key in sorted(set(data) - set(fields))]
    for key, declared in sorted(fields.items()):
        if key in data and not _matches_type(data[key], declared):
            problems.append(f"{key!r} should be {declared}, got {type(data[key]).__name__}")
    return problems


_JSON_TYPES: Mapping[str, tuple[type, ...] | None] = {
    "string": (str,),
    "integer": (int,),
    "number": (int, float),
    "boolean": (bool,),
    "array": (list, tuple),
    "object": (dict,),
    "null": None,
}


def _matches_type(value: Any, declared: str) -> bool:
    """Whether a value satisfies a declared type, which may be a union."""
    for alternative in declared.split("|"):
        expected = _JSON_TYPES.get(alternative.strip())
        if expected is None:
            if value is None:
                return True
            continue
        # A boolean is never an integer here: True where a count belongs is a
        # defect.
        if isinstance(value, bool) and expected == (int,):
            continue
        if isinstance(value, expected):
            return True
    return False


def count_of(value: Any) -> int | None:
    """A count as a stored document carries one, or None for anything else.

    A whole number that is not negative, and never a boolean, the rule
    :func:`payload_problems` holds a payload to.
    """
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


# ---------------------------------------------------------------------------
# Identity and time
# ---------------------------------------------------------------------------


def new_run_id(now: datetime | None = None) -> str:
    """A stable, sortable, addressable identifier for one run.

    A second's timestamp plus a random tail, so two runs in the same second
    never collide and answer each other's gates. The tail is sixty four bits,
    the width ``snapshot.new_stamp`` carries, because one ``sync land`` pass
    mints many identifiers inside a second (U235, R-22). The stamp is
    unchanged, so an older narrower identifier still reads and sorts.
    """
    moment = now or datetime.now(timezone.utc)
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"


def timestamp(now: datetime | None = None) -> str:
    """An ISO-8601 instant with an explicit offset. Never a naive one."""
    moment = now or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.isoformat()


def digest_of(identity: Any) -> str:
    """The stable digest of whatever a gate showed the user.

    Hash a canonical projection, never rendered text, so the digest moves when
    the world moves and stays put when only the wording does.
    """
    return hashlib.sha256(
        json.dumps(identity, sort_keys=True, default=str).encode()
    ).hexdigest()[:16]


# ---------------------------------------------------------------------------
# The envelope
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class PendingHumanAction:
    """Something a person must do outside the tool before the run is complete.

    ``verify_verb`` is mandatory, so the action is a state a command can prove
    rather than a printed instruction. A verb named in an unverified action's
    ``blocks`` refuses before doing anything, so an unimported XML is never
    overtaken by the next run.
    """

    kind: str
    id: str
    summary: str
    verify_verb: str
    artifact: str | None = None
    steps: tuple[str, ...] = ()
    blocks: tuple[str, ...] = ()
    expires: str | None = None

    def __post_init__(self) -> None:
        if self.kind not in PENDING_KINDS:
            raise ValueError(
                f"{self.kind!r} is not a pending-action kind. Declared: "
                f"{', '.join(sorted(PENDING_KINDS))}."
            )
        if not self.verify_verb:
            raise ValueError(
                "a pending human action must name the verb that proves it done; "
                "without one it is a printed instruction, which is the thing "
                "this field replaces."
            )

    def to_json(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "id": self.id,
            "summary": self.summary,
            "artifact": self.artifact,
            "steps": list(self.steps),
            "verify_verb": self.verify_verb,
            "blocks": list(self.blocks),
            "expires": self.expires,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> PendingHumanAction:
        return cls(
            kind=data["kind"],
            id=data["id"],
            summary=data["summary"],
            verify_verb=data["verify_verb"],
            artifact=data.get("artifact"),
            steps=tuple(data.get("steps") or ()),
            blocks=tuple(data.get("blocks") or ()),
            expires=data.get("expires"),
        )


def new_pending_id(run_id: str) -> str:
    """An addressable identifier for a pending action, derived from its run."""
    return f"pha_{run_id}"


@dataclass(frozen=True, slots=True)
class Envelope:
    """One verb's machine-readable result. Constructed once, at the boundary.

    ``exit_code`` is also the integer the process exits with, and a test
    asserts they agree, so a reader of either half gets status and cause.
    """

    schema: str
    verb: str
    run_id: str
    outcome: Outcome
    exit_code: ExitCode
    started: str
    ended: str
    data: Mapping[str, Any] = field(default_factory=dict)
    cause: Cause | None = None
    pending_human_action: PendingHumanAction | None = None
    warnings: tuple[Mapping[str, str], ...] = ()
    resumable: bool = False

    def to_json(self) -> dict[str, Any]:
        return {
            "envelope": ENVELOPE_VERSION,
            "schema": self.schema,
            "verb": self.verb,
            "run_id": self.run_id,
            "outcome": str(self.outcome),
            "exit_code": int(self.exit_code),
            "started": self.started,
            "ended": self.ended,
            "pending_human_action": (
                self.pending_human_action.to_json()
                if self.pending_human_action is not None
                else None
            ),
            "cause": self.cause.to_json() if self.cause is not None else None,
            "warnings": [dict(w) for w in self.warnings],
            "resumable": self.resumable,
            "data": dict(self.data),
        }

    def to_text(self) -> str:
        """The exact bytes that go to stdout in machine mode: one JSON object."""
        return json.dumps(self.to_json(), sort_keys=True)


def envelope_problems(document: Mapping[str, Any]) -> list[str]:
    """Validate a serialized envelope. Empty means valid.

    Both central rules run in both directions:

    * a non-null ``pending_human_action`` implies outcome ``pending`` and status
      ``PENDING_HUMAN``, and the converse;
    * a ``cause`` is present exactly when the outcome is not a success.
    """
    problems = [f"missing required key {key!r}" for key in ENVELOPE_KEYS if key not in document]
    if problems:
        return problems

    if document["envelope"] != ENVELOPE_VERSION:
        problems.append(
            f"envelope version {document['envelope']!r} is not {ENVELOPE_VERSION}"
        )

    name, _, major = str(document["schema"]).partition("/")
    if name not in _PAYLOAD_FIELDS:
        problems.append(f"{document['schema']!r} names no declared payload surface")
    elif major != str(_PAYLOAD_MAJORS[name]):
        problems.append(
            f"{document['schema']!r} is not the current major for {name!r} "
            f"({current_schema(name)})"
        )
    else:
        problems += payload_problems(name, document["data"])

    try:
        outcome = Outcome(document["outcome"])
    except ValueError:
        problems.append(f"{document['outcome']!r} is not a declared outcome")
        return problems

    try:
        code = ExitCode(document["exit_code"])
    except ValueError:
        problems.append(f"exit code {document['exit_code']!r} is outside the vocabulary")
        return problems

    pending = document["pending_human_action"]
    if (pending is not None) != (code is ExitCode.PENDING_HUMAN):
        problems.append(
            "a pending human action and exit code PENDING_HUMAN imply each "
            "other; one without the other means a consumer reading either half "
            "gets a different answer"
        )
    if (pending is not None) != (outcome is Outcome.PENDING):
        problems.append("a pending human action implies outcome 'pending', and the converse")
    if pending is not None and not pending.get("verify_verb"):
        problems.append("a pending human action must name the verb that verifies it")

    succeeded = outcome in (Outcome.OK, Outcome.NO_OP)
    if succeeded and document["cause"] is not None:
        problems.append("a successful outcome carries no cause")
    if not succeeded and document["cause"] is None:
        problems.append(
            "every non-success outcome carries a structured cause with a "
            "remediation (KTD25)"
        )
    if succeeded and code is not ExitCode.OK:
        problems.append(f"outcome {outcome} must exit 0, not {int(code)}")
    if not succeeded and code is ExitCode.OK:
        problems.append(f"outcome {outcome} must not exit 0")
    return problems


def build(
    *,
    verb: str,
    run_id: str,
    schema: str,
    started: str,
    outcome: Outcome = Outcome.OK,
    code: ExitCode = ExitCode.OK,
    data: Mapping[str, Any] | None = None,
    cause: Cause | None = None,
    pending: PendingHumanAction | None = None,
    warnings: Sequence[Mapping[str, str]] = (),
    resumable: bool = False,
    ended: str | None = None,
) -> Envelope:
    """Assemble an envelope, filling in the fields nobody should have to repeat.

    A pending action with no cause gets the standard one, since KTD25 admits no
    non-success result without a structured cause, and its remediation is the
    pending action's own steps.
    """
    if pending is not None and cause is None:
        cause = Cause(
            reason="awaiting-human-action",
            message=pending.summary,
            remediation=Remediation(
                remedy=Remedy.COMPLETE_PENDING_ACTION, steps=pending.steps
            ),
            scope=Scope.RUN,
            retryable=True,
            origin=("cli",),
            detail={"pending_id": pending.id, "verify_verb": pending.verify_verb},
        )
    return Envelope(
        schema=schema,
        verb=verb,
        run_id=run_id,
        outcome=outcome,
        exit_code=code,
        started=started,
        ended=ended or timestamp(),
        data=dict(data or {}),
        cause=cause,
        pending_human_action=pending,
        warnings=tuple(warnings),
        resumable=resumable,
    )


def from_cause(
    *,
    verb: str,
    run_id: str,
    started: str,
    cause: Cause,
    schema: str | None = None,
    resumable: bool = False,
    outcome: Outcome = Outcome.FAILED,
    data: Mapping[str, Any] | None = None,
) -> Envelope:
    """The failure envelope, with the exit code taken FROM the cause.

    Boundary 5, the only place a cause becomes a status. A refusal reports on
    the DIAGNOSTIC surface unless the caller names another, because an empty
    plan would claim a plan was computed.
    """
    return build(
        verb=verb,
        run_id=run_id,
        schema=schema or current_schema("diagnostic"),
        started=started,
        outcome=outcome,
        code=cause.code,
        data=data or {"checks": [], "summary": {}},
        cause=cause.at("cli"),
        resumable=resumable,
    )


# ---------------------------------------------------------------------------
# What every verb's shell needs, written once (U298)
# ---------------------------------------------------------------------------
#
# Here because a verb beside its domain may import this module and no other
# part of the shell.

def load_config(origin: Sequence[str]) -> config.Config:
    """Read config, turning a configuration failure into the typed cause.

    ``origin`` is the verb's own, so the refusal names the verb that met it.
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=origin,
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def declared_gate(entry, name: str):
    """The verb's own gate by name, never by position, or a ``RuntimeError``.
    By name, because a shared gate may sit beside it on the entry.
    """
    for spec in entry.gates:
        if spec.name == name:
            return spec
    raise RuntimeError(f"registry entry {entry.name!r} declares no gate {name!r}")


def confirm_gate(entry, name: str, *, origin: Sequence[str]):
    """The gate a verb asks before it writes, by name, or the typed refusal.

    Kept apart from :func:`declared_gate` because these callers end
    ``internal-error`` with a remedy rather than a traceback.
    """
    for spec in entry.gates:
        if spec.name == name:
            return spec
    raise refuse(
        "internal-error",
        f"{entry.name} declares no gate named {name!r}, so there is no "
        f"question to ask before it writes",
        remedy=Remedy.REPORT_DEFECT,
        origin=origin,
        detail={"verb": entry.name, "gate": name},
    )


def approving_actor(ctx, spec) -> str:
    """Who the run record says answered ``spec``'s gate, or the empty string.

    Off the recorded decision, not ``ctx.gate.actor``, which reads ``"cli"``
    for a run nobody decided.
    """
    decision = ctx.run.decisions.get(spec.name)
    return decision.actor if decision is not None else ""


def no_job(state: str, **progress: Any) -> dict[str, Any]:
    """The ``job_state`` payload for a run that correctly queued nothing.

    ``job_id`` is the empty string, since the surface types it as a string
    (R-234).
    """
    return {"job_id": "", "state": state, "cause": None, "progress": dict(progress)}


__all__ = [
    "ENVELOPE_KEYS",
    "ENVELOPE_VERSION",
    "PENDING_KINDS",
    "PROGRESS_SCHEMA",
    "Envelope",
    "PendingHumanAction",
    "SchemaError",
    "approving_actor",
    "build",
    "canonical_json",
    "confirm_gate",
    "count_of",
    "current_schema",
    "declared_gate",
    "digest_of",
    "envelope_problems",
    "from_cause",
    "load_config",
    "new_pending_id",
    "new_run_id",
    "no_job",
    "payload_problems",
    "progress_document",
    "progress_event",
    "progress_problems",
    "schema_document",
    "schema_fingerprint",
    "schema_names",
    "timestamp",
]
