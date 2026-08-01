"""The versioned output envelope: one machine contract for every verb (R32).

The source system has all five surfaces R32 names, and not one of them is
versioned. Plans are a side file with no schema field, matches are two CSVs
whose column order is the contract, review sets are fourteen more CSVs a human
hand-edits, job state derives its whole status from an exit code, and
diagnostics exist only as a list of dictionaries rendered into one HTML page.
The single versioned artifact in the entire repository is the run manifest.

So three decisions are made here, before any verb exists to disagree with them:

1. **Two version numbers, not one.** ``envelope`` versions the outer frame,
   which changes rarely. ``schema`` versions the payload, per surface, as
   ``"<name>/<major>"``. One shared integer would force every payload to bump
   when one of them changed, and that is exactly the pressure that makes people
   skip a bump.
2. **Human rendering is a separate function, never a field.** The source system
   stores its rendered gate text INSIDE the plan JSON, which makes every wording
   change a schema change. Here ``cratekit.cli.render`` consumes an envelope; the
   envelope never carries prose meant for a screen.
3. **``pending_human_action`` and ``cause`` are REQUIRED KEYS with nullable
   values.** A consumer never has to tell absent from empty. The pending field
   exists because the XML half of a run completes only after a person imports,
   and the source system says so eleven different ways in eleven different
   places, three of them on stdout, four on stderr, and one on both.

Layer note: FOUNDATION, and ``tests/test_layering.py`` pins it there explicitly.
Every layer emits envelopes, so ranking this as CLI would forbid every layer
from using the one output contract they are all required to use.
"""

from __future__ import annotations

import hashlib
import json
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from cratekit.core.cause import Cause, Outcome, Remediation, Scope
from cratekit.core.exit_codes import ExitCode, Remedy

#: The outer contract version. Bumped only when the frame itself changes, which
#: should be close to never.
ENVELOPE_VERSION = 1

#: The five payload surfaces R32 names, shipped here as versioned contracts even
#: though their producers land in later units. Reserving them now is what stops
#: six units inventing six shapes for "a plan" and then discovering they
#: disagree at the boundary where a job engine has to read one.
#:
#: Each value is the field name mapped to a JSON type name. Deliberately a plain
#: declaration rather than a generated model: this file is imported on every
#: ``crate`` invocation including ``--help``, so it stays cheap and dependency
#: free, and a hand-written declaration that a test hashes is as tamper-evident
#: as a generated one.
_PAYLOAD_FIELDS: Mapping[str, Mapping[str, str]] = MappingProxyType(
    {
        "plan": MappingProxyType(
            {
                # The digest is what makes a decision refuse when the world moved
                # between the preview and the answer. Ported from the source
                # system's plan digest, which is the one part of that machinery
                # worth keeping verbatim.
                "digest": "string",
                "items": "array",
                "totals": "object",
                # Non-null when the plan was offered in pieces, so a decision can
                # name which piece it is answering.
                "chunk": "object|null",
            }
        ),
        "match": MappingProxyType(
            {
                # THREE states from version 1, not two (R11). The source writes
                # owned.csv and missing.csv and has no representation at all for
                # "this is a different version of the same track, a person must
                # look". Adding it later would be a schema break for every
                # consumer; reserving it now costs an empty array.
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
                # Present so the engine reads a CAUSE rather than deriving status
                # from a child's exit code, which is the collapse KTD25 is about.
                "cause": "object|null",
                "progress": "object",
            }
        ),
        "diagnostic": MappingProxyType(
            {
                # {key, title, status, detail, remedy} per check: the source
                # system's doctor shape, with its ``fix`` string replaced by a
                # remediation token the CLI renders (D2).
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

#: The envelope's own required keys, in the order they serialize. Derived by the
#: conformance suite rather than restated there, so a key added here is a key the
#: suite immediately requires of every verb.
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

    Deliberately plain: a type per field plus the required list. It is the
    artifact the lock file hashes, so what matters is that it changes whenever
    the payload changes and not that it is expressible in any particular schema
    dialect.
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

    Returns every problem rather than the first, for the same reason config
    validation does: one round trip per missing field turns a fix into a
    conversation.
    """
    fields = _PAYLOAD_FIELDS.get(name)
    if fields is None:
        return [f"{name!r} is not a declared payload surface"]
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
        # A boolean is an int in Python and is never an integer here: writing
        # True where a count belongs is a defect the type check should catch.
        if isinstance(value, bool) and expected == (int,):
            continue
        if isinstance(value, expected):
            return True
    return False


# ---------------------------------------------------------------------------
# Identity and time
# ---------------------------------------------------------------------------


def new_run_id(now: datetime | None = None) -> str:
    """A stable, sortable, addressable identifier for one run.

    Timestamp plus four random hex characters, matching the stamp convention the
    source system already uses. The random tail exists because two runs can start
    inside the same second, and a collision would let one run's decisions answer
    another run's gate.

    U5 ships before the job engine, so this is the identifier space U10 adopts
    rather than a second one it invents.
    """
    moment = now or datetime.now(timezone.utc)
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(2)}"


def timestamp(now: datetime | None = None) -> str:
    """An ISO-8601 instant with an explicit offset. Never a naive one."""
    moment = now or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.isoformat()


def digest_of(identity: Any) -> str:
    """The stable digest of whatever a gate showed the user.

    Ported in substance from the source system's plan digest, which hashes a
    canonical projection of the plan (slugs with counts, identifiers with sizes,
    totals) rather than the whole rendered object. That is the load-bearing part:
    the digest has to move when the world moves and stay put when only the
    wording does, or a decision refuses for no reason a user can see.
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

    ``verify_verb`` is mandatory and names a registered verb. A pending action
    nobody can verify is precisely what the source system's eleven printed
    instructions already are: the tool says something and forgets. Making the
    verification a command is what turns the field from advice into a state.

    ``blocks`` is what makes it load-bearing rather than advisory. A verb whose
    name appears in an unverified pending action's ``blocks`` refuses before
    doing anything, so an unimported XML cannot be silently overtaken by the
    next run.
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

    ``exit_code`` is carried here AND is the integer the process exits with, and
    a test asserts the two agree. Without it, a caller that reads an envelope
    from a file has no status, and a caller that reads the process status has no
    cause: exactly the split the source system's job records live with.
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

    Two rules here are the whole reason the function exists, and both are
    two-directional so neither half can rot:

    * a non-null ``pending_human_action`` implies outcome ``pending`` and status
      ``PENDING_HUMAN``, AND the converse;
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

    A pending action with no cause supplied gets one, because a pending outcome
    is a non-success outcome and KTD25 admits no non-success result without a
    structured cause. The default is not a guess: the cause for "a person has to
    do something" is always the same, and its remediation is the steps the
    pending action already carries. Leaving each verb to build it by hand is how
    eleven printed variants of one instruction happen.
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

    This is boundary 5, the only place a cause becomes a status. Everywhere
    upstream it is a value that gets carried, and that is the difference between
    a failure that can be recovered downstream and one that cannot.

    A refusal reports on the DIAGNOSTIC surface unless the caller names another,
    even when the verb would have emitted a plan. There is no plan: the verb
    refused before producing one, and emitting an empty plan payload would tell a
    consumer that a plan was computed and came back empty.
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


__all__ = [
    "ENVELOPE_KEYS",
    "ENVELOPE_VERSION",
    "PENDING_KINDS",
    "Envelope",
    "PendingHumanAction",
    "SchemaError",
    "build",
    "canonical_json",
    "current_schema",
    "digest_of",
    "envelope_problems",
    "from_cause",
    "new_pending_id",
    "new_run_id",
    "payload_problems",
    "schema_document",
    "schema_fingerprint",
    "schema_names",
    "timestamp",
]
