"""The structured cause: what failed, how bad it is, and what fixes it.

KTD25's second half. An exit code is one integer at the end of a process, and
five boundaries sit between the thing that actually failed and that integer:

1. the acquisition adapter to the acquisition driver,
2. the driver to a job item's row,
3. a job worker SUBPROCESS to the job engine (KTD26 makes this a real process
   boundary, so the only thing that crosses for free is an integer),
4. the job to the per-source aggregate that decides whether a watermark
   advances,
5. the aggregate to the CLI, which is the ONLY place a cause becomes a status.

The source system collapses the whole failure space at boundary 3
(``status = "succeeded" if code == 0 else "failed"``) and then needs a side
channel to recover the reason. A cause that collapses at any hop cannot be
recovered downstream, which is why this type crosses every hop intact and why
``inner`` exists: boundary 5 can still read boundary 1's cause.

Two rules make the type worth having rather than merely present:

* **``remediation`` is not optional.** A failure with nothing to do about it is
  "read stderr and guess", which is what an entire scheme of the source system
  already is.
* **``reason`` comes from a closed registry in this file.** Two modules inventing
  two slugs for one failure is the same drift that produced five genre resolvers,
  and the antidote is the same: one declaration, everybody reads it.

Layer note: FOUNDATION. It carries remediation TOKENS, never command text (D2).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from cratekit.core.exit_codes import ExitCode, Remedy, meaning_of


class Scope(StrEnum):
    """How much of the work a cause condemns.

    Read by the aggregate at boundary 4 to decide whether a watermark may
    advance. It is DECLARED, never derived from the exit code: one unavailable
    track and an expired credential can share a code and must not share a scope.

    THE DECLARATION ORDER IS THE BLAST RADIUS, narrowest first, and
    :func:`widest_scope` is the only thing that may compare two of them. A
    ``StrEnum`` compares as TEXT, and the text order is wrong: ``"run"`` sorts
    before ``"session"`` while condemning strictly more, so a ``max()`` over the
    members would silently pick the narrower of the two.
    """

    ITEM = "item"
    SOURCE = "source"
    SESSION = "session"
    RUN = "run"


def widest_scope(*scopes: Scope) -> Scope:
    """The widest of the given scopes, by the declaration order above.

    A WRAPPER MAY WIDEN WHAT IT WRAPS AND MAY NEVER NARROW IT. A layer that
    re-raises somebody else's cause under its own scope is asserting a blast
    radius it did not observe: if the inner cause condemned the whole run,
    reporting the wrapper's own narrower scope tells the aggregate that
    everything else may proceed, and the watermark it then advances is the
    damage.
    """
    order = list(Scope)
    return max(scopes, key=order.index)


class Outcome(StrEnum):
    """How a run ended, at the granularity a person cares about.

    Separate from the exit code on purpose. ``OK`` and ``NO_OP`` share status 0
    because both are success, and the difference between "swept and found
    nothing" and "swept and acquired forty tracks" belongs in the envelope where
    it can be read, not in a status byte where it cannot.
    """

    OK = "ok"
    NO_OP = "no_op"
    PENDING = "pending"
    BLOCKED = "blocked"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class Remediation:
    """What the user does next, expressed so the CLI can render it.

    ``remedy`` is the token. ``steps`` carries the human sentences for a fix that
    is not a command at all, such as quitting an application or plugging a drive
    in. ``doc`` is a repository-relative path, never a URL, so it resolves in a
    checkout that has never been online.

    At least one of ``remedy`` or ``steps`` must say something; the constructor
    enforces it. This type is the direct descendant of the source system's
    doctor check, whose ``fix`` field is the one place in that codebase that
    already pairs a failure with its exact remedy. What it never does is reach an
    exit code, which is the gap this closes.
    """

    remedy: Remedy | None = None
    steps: tuple[str, ...] = ()
    doc: str | None = None

    def __post_init__(self) -> None:
        if self.remedy is None and not self.steps:
            raise ValueError(
                "a remediation must carry a remedy token or at least one step. "
                "A cause with nothing to do about it is an error message, and "
                "the whole point of the type is to be more than that."
            )

    def to_json(self) -> dict[str, Any]:
        return {
            "remedy": str(self.remedy) if self.remedy is not None else None,
            "steps": list(self.steps),
            "doc": self.doc,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Remediation:
        remedy = data.get("remedy")
        return cls(
            remedy=Remedy(remedy) if remedy else None,
            steps=tuple(data.get("steps") or ()),
            doc=data.get("doc"),
        )


# ---------------------------------------------------------------------------
# The closed reason registry
# ---------------------------------------------------------------------------
#
# slug -> the exit code that slug always maps to.
#
# The mapping direction matters. Several slugs share a code, which is correct: a
# pyrekordbox pin and a database schema pin are one class of refusal with one
# class of remedy, and the slug is what preserves the distinction where it is
# actually useful, which is the envelope rather than the process status. What is
# forbidden is the reverse, one slug meaning two codes, and that is impossible
# here by construction.
#
# S4: every refusal the guarded writer (U7) can raise has a slug here, reserved
# before that unit is written, because a refusal with no code is exactly the
# defect KTD25 exists to prevent. ``tests/test_cli_contract.py`` names the
# writer's refusal conditions one by one and asserts each has an entry, and the
# writer's own suite asserts the reverse, that every reserved slug is raised.

REASONS: Mapping[str, ExitCode] = MappingProxyType(
    {
        # ── Process ─────────────────────────────────────────────────────────
        "internal-error": ExitCode.INTERNAL,
        "no-evidence": ExitCode.INTERNAL,
        "snapshot-integrity-failed": ExitCode.INTERNAL,
        "smoke-test-failed": ExitCode.INTERNAL,
        # ── Gates ───────────────────────────────────────────────────────────
        "decision-required": ExitCode.DECISION_REQUIRED,
        "decision-unknown-gate": ExitCode.DECISION_REQUIRED,
        # The guarded writer could not READ the Cloud Library Sync state, which
        # is a different fact from finding it switched on and has a different
        # answer. On means "switch it off"; cannot-tell means a person decides
        # whether to proceed, which is what this code already means and what its
        # remedy token already says, so no code is invented for it (S4). It is
        # deliberately NOT ``decision-unknown-gate``: that one means the gate name
        # itself is not declared, which is a defect rather than a decision.
        "cloud-sync-unreadable": ExitCode.DECISION_REQUIRED,
        "decision-stale": ExitCode.DECISION_STALE,
        "awaiting-import": ExitCode.PENDING_HUMAN,
        "awaiting-human-action": ExitCode.PENDING_HUMAN,
        "blocked-by-pending-action": ExitCode.PENDING_HUMAN,
        # U19. A run still holds tracks whose placement was decided and never
        # landed, so closing it would report placed tracks that sit in no
        # playlist. Its own slug rather than ``awaiting-import``: that one means
        # a person has an export still to import, and this one means the routing
        # pass has not been run, or has run and surfaced something nobody has
        # answered for. Same code and same remediation token as its neighbours,
        # because all three are the tool waiting on an act outside this process.
        "routing-outstanding": ExitCode.PENDING_HUMAN,
        # ── The library's state ─────────────────────────────────────────────
        "session-lock-held": ExitCode.LIBRARY_BUSY,
        # The guarded writer's cross-process write lock. Distinct from the
        # session lock above because the holder is a different thing and the
        # wait is a different length, and identical remediation is not identity.
        "write-lock-held": ExitCode.LIBRARY_BUSY,
        # The job engine's one-driver-per-job lock (U10). A third slug on this
        # code for the same stated reason as the second: the remedy is "wait for
        # the holder" in all three cases, and what differs is WHAT is held, which
        # is the only thing that helps a person work out how long to wait.
        "job-driver-held": ExitCode.LIBRARY_BUSY,
        "rekordbox-running": ExitCode.REKORDBOX_OPEN,
        "library-volume-unmounted": ExitCode.LIBRARY_UNAVAILABLE,
        "library-volume-mismatch": ExitCode.LIBRARY_UNAVAILABLE,
        "library-directory-missing": ExitCode.LIBRARY_UNAVAILABLE,
        "library-database-missing": ExitCode.LIBRARY_UNAVAILABLE,
        "pyrekordbox-pin-drift": ExitCode.VERSION_PIN,
        "db-schema-pin-drift": ExitCode.VERSION_PIN,
        "app-version-pin-drift": ExitCode.VERSION_PIN,
        # S2: an unrecorded application pin REFUSES. It is never auto-adopted
        # from whatever happens to be installed, because a pin the software
        # copies from the machine it runs on refuses nothing, forever.
        "app-version-pin-unrecorded": ExitCode.VERSION_PIN,
        "tree-unconverged": ExitCode.UNCONVERGED,
        "database-open-failed": ExitCode.LIBRARY_UNREADABLE,
        "canary-read-failed": ExitCode.LIBRARY_UNREADABLE,
        # U8. A commit landed and the read-back through a fresh connection did
        # not agree. Post-commit rollback does not exist, so what the library
        # holds cannot be vouched for and every further write refuses until a
        # person has looked. It shares this code with the two above because all
        # three mean "the database is there and cannot be trusted to read as
        # expected", and the slug is what keeps the three apart where that
        # matters, which is the envelope rather than the process status.
        "session-committed-unverified": ExitCode.LIBRARY_UNREADABLE,
        # Genuinely ON, which is the case ``DISABLE_CLOUD_SYNC`` is the answer
        # to. The cannot-read case is above, under the decision codes.
        "cloud-sync-active": ExitCode.EXTERNAL_WRITER,
        "mytag-category-template-missing": ExitCode.LIBRARY_PREREQUISITE,
        # U18. A catalog import was asked to write a tree this library's declared
        # taxonomy does not name. Same code as the My Tag template above and for
        # the same reason that code exists: the operation mirrors a structure the
        # library declares rather than fabricating one, and there is nothing here
        # to mirror. Its own slug because the remedy is a different act entirely,
        # and the class remedy is wrong for it: nobody fixes this in rekordbox,
        # they declare the tree in the template, so a cause built here carries
        # the configuration token instead.
        "catalog-tree-undeclared": ExitCode.LIBRARY_PREREQUISITE,
        # ── This installation ───────────────────────────────────────────────
        "doctor-check-failed": ExitCode.PRECONDITION,
        # One slug for every way configuration can be unusable, because the
        # thing that differs between them is the REMEDY and the remedy travels
        # on the remediation. ``config.Remedy`` already distinguishes missing
        # from corrupt from too-new from invalid from locked, and a cause built
        # from one of those carries its token through unchanged.
        "config-unusable": ExitCode.PRECONDITION,
        "module-extras-missing": ExitCode.MODULE_UNAVAILABLE,
        "credential-missing": ExitCode.PRECONDITION,
        # U10. A named job that is not in this installation's queue, and a queue
        # written by a different build of the product. Both are 3x rather than a
        # command-line class because ``USAGE`` belongs to the argument parser and
        # to nothing else, and both carry their remediation as STEPS rather than
        # a token: neither fix is a command, and inventing a token that renders
        # to one would be worse than saying the sentence.
        "job-unknown": ExitCode.PRECONDITION,
        "job-schema-mismatch": ExitCode.PRECONDITION,
        # U11, the review queue. Six slugs on one code, and the code is right for
        # all six: none of them is the library refusing, none is upstream, and
        # none is a command line the parser could have rejected. What differs is
        # the SENTENCE, which is the whole reason a slug exists separately from a
        # code: "no item has that identifier" and "that item is already decided"
        # send a person to two different places.
        "review-item-unknown": ExitCode.PRECONDITION,
        # Not an error in the ordinary sense. It is the queue refusing to
        # overwrite a decision somebody already made, and its remediation is to
        # clear the verdict first, which is a deliberate second act.
        "review-already-resolved": ExitCode.PRECONDITION,
        # The split between an adjudication surface and a plain output, enforced.
        # An output pushed into the queue would ask a person to confirm a result,
        # and a queue nobody declared is a surface with no recorded reasoning.
        "review-queue-undeclared": ExitCode.PRECONDITION,
        "review-option-unknown": ExitCode.PRECONDITION,
        "review-schema-mismatch": ExitCode.PRECONDITION,
        # A selection that names nothing, names two things, or carries an empty
        # identity. All three are "this does not pick out what you meant", and the
        # empty-predicate case is the sharp one: it would answer a whole backlog.
        "review-selection-invalid": ExitCode.PRECONDITION,
        # An export or a decision store that cannot be read or written. Its own
        # slug rather than the config one because the file is data a person may
        # have carried between machines, and the fix is about that file rather
        # than about this installation's configuration.
        "review-file-unusable": ExitCode.PRECONDITION,
        "backup-acknowledgment-missing": ExitCode.ACK_REQUIRED,
        # U8. The acknowledgment cannot be MINTED here, which is a different
        # condition from it being absent when a session consulted it. Minting is
        # a person's act at a controlling terminal, and an invocation with no
        # terminal is usually a detached job or an agent driving the command
        # line, which is exactly the caller R34 forbids from satisfying this
        # gate. Same code, because the class of answer is the same; a separate
        # slug, because "record one" and "you are not the one who can" are
        # different sentences to the same user.
        "backup-acknowledgment-no-terminal": ExitCode.ACK_REQUIRED,
        # U8. The acknowledgment cannot be minted because the ages it must SHOW
        # cannot be read. Same code again, because the answer is still "this gate
        # is not satisfied"; a third slug, because the remedy is a different act
        # entirely. ``backup_facts`` argues at length that an unreadable fact
        # file must never collapse into "nothing recorded", and an acknowledgment
        # minted against one would record a person as having been shown a clean
        # sheet they were never shown.
        "backup-facts-unreadable": ExitCode.ACK_REQUIRED,
        # ── Upstream ────────────────────────────────────────────────────────
        "auth-failed": ExitCode.UPSTREAM_AUTH,
        "adapter-broken": ExitCode.UPSTREAM_UNAVAILABLE,
        "unavailable-transient": ExitCode.UPSTREAM_UNAVAILABLE,
        # The provider refused the CLIENT rather than a request: a forbidden
        # response, a bot challenge, or a wait so long it is a refusal wearing a
        # wait. It shares a code with the transient case because both are
        # upstream saying no, and the slug is what keeps the distinction where it
        # is actually read. What must NOT be shared is the instruction: the
        # class remedy for this code is "retry later", and this is the one member
        # of the class where an automated retry is the harm, so a cause built for
        # it carries explicit steps and ``retryable=False``.
        "provider-blocked": ExitCode.UPSTREAM_UNAVAILABLE,
        "unavailable-permanent": ExitCode.REFUSED_BY_POLICY,
        "refused-by-policy": ExitCode.REFUSED_BY_POLICY,
        "whitelist-violation": ExitCode.REFUSED_BY_POLICY,
        # U8, and the runtime half of R17's fifth surface. The name scan over
        # this package's source forbids every symbol that serialises a rekordbox
        # analysis file, and reading one stays legal by decision, so a grid
        # rewritten through a handle the binding already returned names none of
        # those symbols. A destructive session compares the files themselves and
        # refuses when one moved. Its own slug rather than the whitelist's,
        # because the whitelist governs database ROWS and cannot see a
        # filesystem write at all.
        "anlz-modified": ExitCode.REFUSED_BY_POLICY,
        "lossy-refused": ExitCode.REFUSED_BY_POLICY,
        # ── Lifecycle ───────────────────────────────────────────────────────
        "cancelled": ExitCode.INTERRUPTED,
        # ── U19's remaining refusals, appended ──────────────────────────────
        #
        # APPENDED RATHER THAN FILED UNDER THEIR SECTIONS, deliberately, and for
        # the reason the verb registry gives for the same choice: several units
        # land against this mapping at once, and two entries inserted into
        # different halves of one literal auto-merge, so a duplicate key is
        # resolved silently by whichever line comes last. An append conflicts
        # textually, which is a conflict somebody reads.
        #
        # S4 is why they exist at all. The unit's own vocabulary has to cover
        # EVERY refusal it raises, or the refusal reaches the command line as an
        # internal defect and the remedy it was carrying is discarded.
        #
        # The routing ledger is present and cannot be understood: not valid
        # JSON, no schema version, two records for one run and one track, or a
        # version this build does not know. ONE SLUG FOR ALL OF THEM, exactly as
        # ``config-unusable`` takes one slug for five ways a config can be
        # unusable, because what differs between them is the REMEDY and the
        # remedy travels on the remediation rather than on the code. A ledger
        # from a newer build asks for an upgrade; a corrupt one asks for the
        # doctor.
        "routing-ledger-unusable": ExitCode.PRECONDITION,
        # The tree registry is present and cannot be understood. Its sibling
        # above already argues the shape: one slug for every way one file can be
        # unusable, and the remedy travels on the remediation because a file
        # from a newer build and a corrupt one need different acts. It is here
        # rather than left alone because fixing two of the three refusals in
        # that module and not the third is the same lesson applied in one place
        # and not the other, which is the shape P5 names.
        "tree-registry-unusable": ExitCode.PRECONDITION,
        # The collection row could not say whether it is a tombstone. The column
        # is not exposed, or it is exposed and holds nothing. Its own slug on
        # the library-unreadable code rather than a shared one, because the
        # database is present and readable in every other respect and what
        # cannot be read is one specific fact whose permissive default would let
        # a deleted track be placed and a run close over it.
        "soft-delete-marker-unreadable": ExitCode.LIBRARY_UNREADABLE,
        # The deferred placement's destination folder is not under the tree's
        # adopted root, and the track already sits under that root in a folder
        # the active taxonomy does not declare. Somebody renamed the folder, in
        # rekordbox or in the template, between the decision and the write.
        # Writing would create the destination a second time under the taxonomy
        # name and file the track twice. UNCONVERGED because that is exactly
        # what this is: the tree the library holds and the tree the taxonomy
        # declares have come apart, and only a person can say which is right.
        "routing-destination-renamed": ExitCode.UNCONVERGED,
        # U23. One of adoption's two documents exists and cannot be understood:
        # the record of which plan entries have already been applied, or the
        # record of what each file's tag held before adoption overwrote it.
        # Deliberately NOT collapsed into "no records", which is the reading that
        # makes both of them dangerous rather than merely absent: an empty
        # applied ledger re-applies a plan from its first entry, and an empty
        # revert log reports that nothing can be undone about writes that are
        # sitting in the user's files. One slug for both, on the same code as its
        # two siblings above, because what differs between the ways either file
        # can be wrong is the REMEDY, and the remedy travels on the remediation:
        # a document from a newer build asks for an upgrade and a corrupt one
        # asks for the doctor.
        "adoption-ledger-unusable": ExitCode.PRECONDITION,
        # U23. The file an adoption is about to write a tag into cannot be
        # identified on this machine, so its ORIGINAL cannot be recorded first.
        # A separate slug from the one above because it is about a file rather
        # than about a document, and it is per ITEM: the shape that reaches it is
        # a track that was in the census and was deleted before the apply got to
        # it, which costs that entry and nothing else. PRECONDITION rather than a
        # defect code, because the state of the library is what is wrong.
        "adoption-file-unidentifiable": ExitCode.PRECONDITION,
    }
)


class UnknownReason(KeyError):
    """A cause was built with a slug the registry does not declare."""


@dataclass(frozen=True, slots=True)
class Cause:
    """One failure, carried whole across every boundary between its origin and the CLI.

    ``origin`` is append-only and every hop appends to it. A cause arriving at
    the CLI with a one-element trail means some hop caught it and re-created it,
    which loses everything below and is a defect rather than a style choice.

    ``detail`` is free-form and is NEVER read for control flow. Anything a
    caller must branch on is a declared field, because a consumer reading
    ``detail["kind"]`` has re-invented the untyped failure this type replaces.
    """

    reason: str
    message: str
    remediation: Remediation
    scope: Scope = Scope.RUN
    retryable: bool = False
    origin: tuple[str, ...] = ()
    detail: Mapping[str, Any] = field(default_factory=dict)
    inner: Cause | None = None

    def __post_init__(self) -> None:
        if self.reason not in REASONS:
            raise UnknownReason(
                f"{self.reason!r} is not a declared reason. Add it to "
                f"cause.REASONS with the exit code it maps to. Two modules "
                f"inventing two slugs for one failure is how a vocabulary "
                f"becomes three vocabularies."
            )

    @property
    def code(self) -> ExitCode:
        """The status this cause exits with, looked up rather than stored.

        Storing it alongside the slug would let the two disagree, and a cause
        whose code contradicts its reason is worse than either alone.
        """
        return REASONS[self.reason]

    def at(self, boundary: str) -> Cause:
        """Return a copy with one more boundary appended to the trail."""
        return Cause(
            reason=self.reason,
            message=self.message,
            remediation=self.remediation,
            scope=self.scope,
            retryable=self.retryable,
            origin=(*self.origin, boundary),
            detail=self.detail,
            inner=self.inner,
        )

    def to_json(self) -> dict[str, Any]:
        """A plain dictionary, chained causes included.

        Boundary 3 is a process boundary, so a cause that cannot round-trip
        through JSON cannot cross it, and a cause that cannot cross it is one
        the engine has to reconstruct from an exit code.
        """
        return {
            "reason": self.reason,
            "code": int(self.code),
            "message": self.message,
            "remediation": self.remediation.to_json(),
            "scope": str(self.scope),
            "retryable": self.retryable,
            "origin": list(self.origin),
            "detail": dict(self.detail),
            "inner": self.inner.to_json() if self.inner is not None else None,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Cause:
        inner = data.get("inner")
        return cls(
            reason=data["reason"],
            message=data["message"],
            remediation=Remediation.from_json(data["remediation"]),
            scope=Scope(data.get("scope", Scope.RUN)),
            retryable=bool(data.get("retryable", False)),
            origin=tuple(data.get("origin") or ()),
            detail=dict(data.get("detail") or {}),
            inner=cls.from_json(inner) if inner else None,
        )

    def to_text(self) -> str:
        """Serialize for a transport that carries only strings, such as a pipe."""
        return json.dumps(self.to_json(), sort_keys=True)


class CratekitError(Exception):
    """The one exception type that carries a cause across a raise.

    Every refusal in the package raises this or a subclass. A bare ``RuntimeError``
    forces its catcher to parse a message string, which is the state the source
    system's writer contract is in: its exit codes are documented in a comment,
    in a consumer, and two of the four are already indistinguishable one hop
    downstream.
    """

    def __init__(self, cause: Cause) -> None:
        super().__init__(cause.message)
        self.cause = cause


def refuse(
    reason: str,
    message: str,
    *,
    remedy: Remedy | None = None,
    steps: Sequence[str] = (),
    scope: Scope = Scope.RUN,
    retryable: bool = False,
    origin: Sequence[str] = (),
    detail: Mapping[str, Any] | None = None,
    inner: Cause | None = None,
) -> CratekitError:
    """Build the exception for a refusal, with its remediation defaulted sensibly.

    The default remediation is the one the exit code already declares, so a
    caller only spells one out when this particular failure has a better answer
    than its whole class does. Without the default, "remediation is mandatory"
    would in practice mean "every raise site invents its own wording", which is
    how the source system ended up with eleven prose variants of one instruction.
    """
    if reason not in REASONS:
        raise UnknownReason(
            f"{reason!r} is not a declared reason; add it to cause.REASONS "
            f"with the exit code it maps to."
        )
    if remedy is None and not steps:
        remedy = meaning_of(REASONS[reason]).remedy
    return CratekitError(
        Cause(
            reason=reason,
            message=message,
            remediation=Remediation(remedy=remedy, steps=tuple(steps)),
            scope=scope,
            retryable=retryable,
            origin=tuple(origin),
            detail=dict(detail or {}),
            inner=inner,
        )
    )


__all__ = [
    "REASONS",
    "Cause",
    "CratekitError",
    "Outcome",
    "Remediation",
    "Scope",
    "UnknownReason",
    "refuse",
    "widest_scope",
]
