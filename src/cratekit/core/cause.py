"""The structured cause: what failed, how bad it is, and what fixes it.

KTD25's second half. Five boundaries sit between the thing that failed and the
exit code:

1. the acquisition adapter to the acquisition driver,
2. the driver to a job item's row,
3. a job worker subprocess to the job engine (KTD26, a real process boundary),
4. the job to the per-source aggregate that decides whether a watermark
   advances,
5. the aggregate to the CLI, the only place a cause becomes a status.

A cause that collapses at any hop cannot be recovered downstream, so this type
crosses every hop intact, and ``inner`` lets boundary 5 read boundary 1's cause.

Two rules:

* ``remediation`` is not optional; a failure with nothing to do about it is
  "read stderr and guess".
* ``reason`` comes from the closed registry in this file, so two modules cannot
  invent two slugs for one failure.

Layer note: FOUNDATION. It carries remediation tokens, never command text (D2).
"""

from __future__ import annotations

import errno
import json
import os
import sqlite3
import stat
from dataclasses import dataclass, field, replace
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Iterator, Mapping, Sequence

from cratekit.core.exit_codes import ExitCode, Remedy, meaning_of

#: The errnos that mean this account does not hold the permission. Named as
#: numbers too, because an ``OSError`` rebuilt across a boundary can arrive as
#: the base class carrying only its number.
PERMISSION_ERRNOS: frozenset[int] = frozenset({errno.EACCES, errno.EPERM})

#: The errno that means the medium refuses every writer, not this account. No
#: grant fixes it; the act is to remount read write or unlock the card.
READ_ONLY_ERRNOS: frozenset[int] = frozenset({errno.EROFS})

#: SQLite's names for "the file system would not give me this file". They
#: arrive as ``sqlite3.OperationalError``, not ``OSError``, with no errno or
#: filename, so an errno rule alone is blind to them (``sqlite_errorname``).
DATABASE_ACCESS_ERRORNAMES: tuple[str, ...] = (
    "SQLITE_CANTOPEN",
    "SQLITE_READONLY",
    "SQLITE_PERM",
)

#: Where a driver records which file its error was about, since the exception
#: carries no path. See :func:`name_the_database`.
DATABASE_PATH_ATTRIBUTE = "cratekit_database_path"


class AccessKind(StrEnum):
    """Which kind of refusal the operating system made, because the acts differ.

    Full Disk Access fixes only a permission; it never makes a read only volume
    writable or clears Finder's Locked checkbox.
    """

    #: This account is not allowed. Granting it access is the fix.
    PERMISSION = "permission"
    #: The volume refuses every writer. Remounting or unlocking the medium is.
    READ_ONLY = "read-only"
    #: A per-file immutable flag, which is what Finder's "Locked" checkbox sets.
    LOCKED = "locked"


#: The declared reason slug for each kind. They share an exit code, and the slug
#: keeps the distinction.
ACCESS_REASONS: Mapping[AccessKind, str] = MappingProxyType(
    {
        AccessKind.PERMISSION: "path-permission-denied",
        AccessKind.READ_ONLY: "path-read-only",
        AccessKind.LOCKED: "path-locked",
    }
)

ACCESS_REMEDIES: Mapping[AccessKind, Remedy] = MappingProxyType(
    {
        AccessKind.PERMISSION: Remedy.GRANT_PATH_ACCESS,
        AccessKind.READ_ONLY: Remedy.REMOUNT_WRITABLE,
        AccessKind.LOCKED: Remedy.UNLOCK_PATH,
    }
)


@dataclass(frozen=True, slots=True)
class AccessRefusal:
    """One refusal by the operating system, with the path it was about.

    ``path`` is required: a refusal with no filename (a privileged socket bind,
    ``os.setuid``) gives the user nothing to act on, so it cannot be built.
    """

    kind: AccessKind
    path: str

    @property
    def reason(self) -> str:
        return ACCESS_REASONS[self.kind]

    @property
    def remedy(self) -> Remedy:
        return ACCESS_REMEDIES[self.kind]


def _chain(exc: BaseException | None) -> Iterator[BaseException]:
    """``exc`` and its declared causes, once each.

    ``__cause__`` is followed and ``__context__`` is not: ``raise X from exc``
    says this failure is that one, while a context only says it happened while
    handling that, and reading it would call a defect raised after a recovered
    refusal a refusal. The ``seen`` set ends a cycle, since ``__cause__`` is
    assignable and the walk would otherwise hang.
    """
    seen: set[int] = set()
    current = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        yield current
        current = current.__cause__


def failure_links(exc: BaseException) -> Iterator[tuple[BaseException, bool]]:
    """``exc`` and every error it was raised from or raised while handling, once each (R-1305).

    Each comes with whether it was reached by declared causes alone. Declared
    causes come first, then off that chain each link's own cause before its
    context, depth first, so :func:`nearest_status` reads what a wrapper says it
    is before what it met. Read by the rejected session checks
    (``acquire.provider_session._rejected``, the outbound ``_session_refused``)
    and by :func:`nearest_status` (R-1313); it lives here because the
    acquisition adapter's classifier reads it too.

    Unlike :func:`_chain` it reads context, because the provider client decodes
    an error body inside its own handler, so a 401 with a body that is not JSON
    surfaces as a decode error with the HTTP error only in context (tidalapi
    0.8.11).

    Two limits keep ``_chain``'s reason: off the declared chain the walk never
    enters a ``CratekitError``, whose 401 would make an outage read as a
    rejection, and a link reached only as context is trusted for its answered
    status, never its type or name (R-704). The ``walked`` set ends a cycle.
    """
    walked: set[int] = set()
    declared: list[BaseException] = []
    current: BaseException | None = exc
    while current is not None and id(current) not in walked:
        walked.add(id(current))
        declared.append(current)
        yield current, True
        current = current.__cause__
    pending = [one.__context__ for one in reversed(declared)]
    while pending:
        one = pending.pop()
        if one is None or id(one) in walked or isinstance(one, CratekitError):
            continue
        walked.add(id(one))
        yield one, False
        # Context pushed first so the cause is taken first.
        pending.extend((one.__context__, one.__cause__))


def answered_status(exc: BaseException) -> Any:
    """The HTTP status the client attached to ``exc``, or None."""
    return getattr(getattr(exc, "response", None), "status_code", None)


#: The status a provider answers for a resource it holds nothing under.
NOT_FOUND_STATUS = 404


def nearest_status(exc: BaseException) -> Any:
    """The status the provider answered for this failure, or None (R-1313).

    The status on the first link :func:`failure_links` reaches that carries one.
    The nearest, not any: a server error met while handling a not found is the
    server error, or an outage would be remembered as an answer.
    """
    for link, _declared in failure_links(exc):
        status = answered_status(link)
        if status is not None:
            return status
    return None


def answered_not_found(exc: BaseException) -> bool:
    """Whether the status nearest this failure says the provider holds nothing (R-1313).

    Read through :func:`nearest_status`, so a 404 whose body surfaced as a
    decode error still counts, and one under a handled product refusal does not.
    """
    return nearest_status(exc) == NOT_FOUND_STATUS


def _immutable(path: str) -> bool:
    """Whether a per-file immutable flag is set on ``path``.

    ``chflags uchg`` is what Finder's Locked checkbox sets. ``st_flags`` exists
    only on BSD, so its absence answers False. ``ValueError`` (an embedded null)
    is caught too, because this runs inside the dispatcher's refusal handler,
    where an escaping exception would replace an actionable refusal with a
    traceback.
    """
    try:
        flags = getattr(os.lstat(path), "st_flags", 0)
    except (OSError, ValueError):
        return False
    return bool(flags & (getattr(stat, "UF_IMMUTABLE", 0) | getattr(stat, "SF_IMMUTABLE", 0)))


def _spelled(candidate: Any) -> str | None:
    """One filename off an ``OSError``, as text, or None when it carries none."""
    if candidate is None:
        return None
    if isinstance(candidate, bytes):
        return os.fsdecode(candidate)
    return str(candidate)


def _refused_path(exc: OSError) -> str | None:
    """The path the refusal was about, destination first.

    ``os.replace`` puts the destination in ``filename2``, and the guarded writer
    renames a temporary file over every target, so ``filename`` alone would name
    a temporary path that no longer exists.
    """
    for candidate in (exc.filename2, exc.filename):
        spelled = _spelled(candidate)
        if spelled is not None:
            return spelled
    return None


def _refused_of_two(exc: OSError, fallback: str) -> str:
    """Which of two named paths the operating system actually refused.

    Destination first is right for ``os.replace``, ``os.rename``, ``os.symlink``
    and ``shutil.move`` but wrong for ``os.link``, and for ``os.rename`` when the
    source side is refused. So each path is probed, destination first, and the
    source is named only when the destination is not refused and the source is.
    Only for a permission or a lock, never a read only volume (see
    :func:`_from_os_error`).
    """
    for candidate in (exc.filename2, exc.filename):
        spelled = _spelled(candidate)
        if spelled is None:
            continue
        if _probe_readable(spelled) is not None:
            return spelled
    return fallback


def _from_os_error(exc: BaseException) -> AccessRefusal | None:
    if not isinstance(exc, OSError):
        return None
    path = _refused_path(exc)
    if path is None:
        # A refusal with no path gives nobody an act, so it is not claimed.
        return None
    if exc.errno in READ_ONLY_ERRNOS:
        # The destination, unmeasured: read only is a property of the medium,
        # and a two path call across filesystems answers EXDEV instead.
        return AccessRefusal(kind=AccessKind.READ_ONLY, path=path)
    if isinstance(exc, PermissionError) or exc.errno in PERMISSION_ERRNOS:
        for candidate in (exc.filename2, exc.filename):
            spelled = _spelled(candidate)
            if spelled is not None and _immutable(spelled):
                return AccessRefusal(kind=AccessKind.LOCKED, path=spelled)
        if exc.filename2 is not None and exc.filename is not None:
            path = _refused_of_two(exc, path)
        return AccessRefusal(kind=AccessKind.PERMISSION, path=path)
    return None


def _from_copy_error(exc: BaseException) -> AccessRefusal | None:
    """The refusal inside a ``shutil`` copy that gave up on individual members.

    ``shutil.copytree`` raises one ``shutil.Error`` listing ``(source,
    destination, why)`` triples, ``why`` already rendered to text, with no
    errno, filename or ``__cause__``, so no errno rule sees it. The paths
    survive, so each source is probed; a member merely gone claims nothing.
    """
    if type(exc).__module__ != "shutil" or type(exc).__name__ != "Error":
        return None
    entries = exc.args[0] if exc.args else ()
    if not isinstance(entries, (list, tuple)):
        return None
    for entry in entries:
        if not isinstance(entry, (list, tuple)) or not entry:
            continue
        found = _probe_readable(str(entry[0]))
        if found is not None:
            return found
    return None


# Why two probes, and why only the read one opens anything. This module is on
# the reports allowlist, whose argument is that nothing it admits can touch a
# file, so it may hold one ``os.open`` and it must be a read. The guard reads
# the flags from the call's own argument and cannot resolve a name, so they are
# spelled inline, ``os.O_NONBLOCK`` included. Do not fold the two into one
# function taking ``writing: bool``: that brings back both the unreadable flags
# and the write handle (R-80, R-102).


def _probe_readable(path: str) -> AccessRefusal | None:
    """Ask the operating system whether ``path`` can be read.

    A driver level error does not say whether it was a permission, so the file
    is opened as the driver would and the ``OSError`` supplies the errno and
    filename; a successful open answers None. ``ValueError`` is caught for
    :func:`_immutable`'s reason. Not measured: a hung network mount, which
    ``O_NONBLOCK`` does not cover.
    """
    try:
        handle = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError as probe:
        return _from_os_error(probe)
    except ValueError:
        return None
    os.close(handle)
    return None


def _probe_writable(path: str) -> AccessRefusal | None:
    """Say why a write to ``path`` was refused, without opening a write handle.

    Called only by :func:`_from_database_error` for ``SQLITE_READONLY`` and
    ``SQLITE_PERM``, where the driver already tried the write, so this
    attributes a refusal from metadata rather than predicting one. It must not
    open ``os.O_RDWR`` again (R-80): this module is on the reports allowlist.

    Order: the read probe first, since an unreadable file is already classified
    by its errno; then a read only volume, a property of the medium; then the
    immutable flag before the mode, since only a mode is something chmod fixes.
    ``effective_ids`` is used where available, because the refused write used
    the effective identity. Not measured on a network volume, where cached
    metadata may disagree with the server.
    """
    refused = _probe_readable(path)
    if refused is not None:
        return refused
    effective = os.access in os.supports_effective_ids
    try:
        if os.statvfs(path).f_flag & os.ST_RDONLY:
            return AccessRefusal(kind=AccessKind.READ_ONLY, path=path)
        if _immutable(path):
            return AccessRefusal(kind=AccessKind.LOCKED, path=path)
        if not os.access(path, os.W_OK, effective_ids=effective):
            return AccessRefusal(kind=AccessKind.PERMISSION, path=path)
    except (OSError, ValueError):
        # :func:`_probe_readable`'s two guards, for the same reason.
        return None
    return None


def _from_database_error(exc: BaseException) -> AccessRefusal | None:
    if not isinstance(exc, sqlite3.Error):
        return None
    name = getattr(exc, "sqlite_errorname", "") or ""
    if not name.startswith(DATABASE_ACCESS_ERRORNAMES):
        return None
    path = getattr(exc, DATABASE_PATH_ATTRIBUTE, None)
    if path is None:
        return None
    if name.startswith("SQLITE_CANTOPEN"):
        return _probe_readable(str(path))
    return _probe_writable(str(path))


def name_the_database(exc: BaseException, path: Any) -> BaseException:
    """Record which file a driver level error was about, and return it unchanged.

    The connection site knows the path and the driver's error never carries
    one, so one attribute is set here and read by :func:`access_refusal`. The
    same exception is returned, keeping its traceback and class. It is set along
    the whole declared chain, because the object mapper re-raises its own type
    ``from`` the ``sqlite3`` error, and only that inner one carries
    ``sqlite_errorname``.
    """
    try:
        spelled = os.fspath(path)
    except TypeError:  # pragma: no cover - defensive
        return exc
    for current in _chain(exc):
        try:
            setattr(current, DATABASE_PATH_ATTRIBUTE, spelled)
        except AttributeError:  # pragma: no cover - defensive
            continue
    return exc


def access_refusal(exc: BaseException | None) -> AccessRefusal | None:
    """The refusal by the operating system inside ``exc``, with its path, or None.

    One decision, made once, because per call site handling kept failing review.
    A path this interpreter may not open, write or replace is a machine state
    the user can act on, not a defect; on macOS it is the routine first run for
    anything under Documents, Desktop, Downloads or an external volume without
    Full Disk Access. ``Path.exists`` and ``Path.is_dir`` re raise under EPERM,
    so a line that reads like a question can throw, which is why this is a
    classification and not a handler. It covers SQLite refusals, which are not
    ``OSError``, and answers with a kind, because sending a read only volume or
    a locked file to Full Disk Access is as wrong as calling it a bug.
    """
    for current in _chain(exc):
        found = (
            _from_copy_error(current)
            or _from_os_error(current)
            or _from_database_error(current)
        )
        if found is not None:
            return found
    return None


def permission_denied(exc: BaseException | None) -> OSError | None:
    """The permission this account does not hold, inside ``exc``, or None.

    Narrower than :func:`access_refusal`, on purpose: it answers whether this is
    the class of failure raised when an account is not allowed, for callers
    deciding whether to re-raise or answer False (``preflight``,
    ``backup_facts``). None of them tells a user anything, so none needs a path;
    anything that renders a refusal asks :func:`access_refusal`.
    """
    for current in _chain(exc):
        if isinstance(current, PermissionError):
            return current
        if isinstance(current, OSError) and current.errno in PERMISSION_ERRNOS:
            return current
    return None


def access_remedy(exc: BaseException | None, *, otherwise: Remedy) -> Remedy:
    """The act for a failure that might be one the operating system refused.

    Every site calls this instead of writing ``Remedy.REPORT_DEFECT`` beside a
    caught ``OSError``; it answers with the act for the kind found.
    """
    found = access_refusal(exc)
    return found.remedy if found is not None else otherwise


class Scope(StrEnum):
    """How much of the work a cause condemns.

    Read at boundary 4 to decide whether a watermark may advance. Declared,
    never derived from the exit code: an unavailable track and an expired
    credential can share a code and must not share a scope. Declaration order is
    the blast radius, narrowest first, and only :func:`widest_scope` may compare
    two: a ``StrEnum`` compares as text, where ``"run"`` sorts before
    ``"session"``.
    """

    ITEM = "item"
    SOURCE = "source"
    SESSION = "session"
    RUN = "run"


def widest_scope(*scopes: Scope) -> Scope:
    """The widest of the given scopes, by declaration order.

    A wrapper may widen what it wraps and never narrow it: a scope narrower than
    the inner cause tells the aggregate the rest may proceed, and the watermark
    it then advances is the damage.
    """
    order = list(Scope)
    return max(scopes, key=order.index)


class Outcome(StrEnum):
    """How a run ended, at the granularity a person cares about.

    Separate from the exit code: ``OK`` and ``NO_OP`` share status 0, and the
    difference belongs in the envelope.
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

    ``remedy`` is the token. ``steps`` carries sentences for a fix that is not a
    command, such as quitting an application. ``doc`` is a repository-relative
    path, never a URL, so it resolves offline. The constructor requires a remedy
    or at least one step.
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


# The closed reason registry: slug to the exit code it always maps to. Slugs may
# share a code, and the slug keeps the distinction in the envelope; one slug can
# never mean two codes. S4: every refusal the guarded writer (U7) can raise has a
# slug here, checked both ways by ``tests/test_cli_contract.py`` and the writer's
# own suite.

REASONS: Mapping[str, ExitCode] = MappingProxyType(
    {
        # ── Process ──
        "internal-error": ExitCode.INTERNAL,
        # U56. A catalogue page the parser no longer recognises: a defect here,
        # but its own slug, since a moved scraper target is expected over time.
        "catalogue-parse-broken": ExitCode.INTERNAL,
        # U27. The OS refused this account at an unguarded call. No defect, so
        # not ``internal-error``; the installation band, as the path is unknown.
        "path-permission-denied": ExitCode.PRECONDITION,
        # Same band, own slugs: no grant fixes a read only volume or an immutable
        # flag, so Full Disk Access must not be named for them.
        "path-read-only": ExitCode.PRECONDITION,
        "path-locked": ExitCode.PRECONDITION,
        # U295. ``crate schedule`` on launchd: no launchd, crate not executable,
        # launchctl failed, plist not written, or the agent unreadable or not the
        # night's. Facts about this machine, so the installation band.
        "schedule-platform-unsupported": ExitCode.PRECONDITION,
        "schedule-crate-unresolved": ExitCode.PRECONDITION,
        "schedule-launchctl-failed": ExitCode.PRECONDITION,
        "schedule-agent-unwritten": ExitCode.PRECONDITION,
        "schedule-agent-unusable": ExitCode.PRECONDITION,
        "no-evidence": ExitCode.INTERNAL,
        # R-391. A failed job whose permanent item failures do not share a
        # reason, so no single band is honest; each item cause carries its code.
        "mixed-permanent-failures": ExitCode.INTERNAL,
        "snapshot-integrity-failed": ExitCode.INTERNAL,
        "smoke-test-failed": ExitCode.INTERNAL,
        # ── Gates ──
        "decision-required": ExitCode.DECISION_REQUIRED,
        "decision-unknown-gate": ExitCode.DECISION_REQUIRED,
        # The writer could not read Cloud Library Sync state, so a person decides
        # (S4). Not ``decision-unknown-gate``, an undeclared gate and a defect.
        "cloud-sync-unreadable": ExitCode.DECISION_REQUIRED,
        "decision-stale": ExitCode.DECISION_STALE,
        "awaiting-import": ExitCode.PENDING_HUMAN,
        "awaiting-human-action": ExitCode.PENDING_HUMAN,
        "blocked-by-pending-action": ExitCode.PENDING_HUMAN,
        # U19. Placements decided and not landed, so closing would report tracks
        # in no playlist. Unlike ``awaiting-import``, the routing pass is owed.
        "routing-outstanding": ExitCode.PENDING_HUMAN,
        # ── The library's state ──
        "session-lock-held": ExitCode.LIBRARY_BUSY,
        # The writer's cross-process lock. Each held slug names what is held,
        # which is what tells a person how long to wait.
        "write-lock-held": ExitCode.LIBRARY_BUSY,
        # The job engine's one driver per job lock (U10).
        "job-driver-held": ExitCode.LIBRARY_BUSY,
        # U293. Another pass holds the staging lock; two passes staging at once
        # would each land the other's tracks.
        "staging-held": ExitCode.LIBRARY_BUSY,
        # R-705. The provider's one call at a time lock, held past any call.
        "provider-gate-held": ExitCode.LIBRARY_BUSY,
        "rekordbox-running": ExitCode.REKORDBOX_OPEN,
        # U211. A live process could not be read, so rekordbox's absence is not
        # established and the act is to wait, not quit. The one refusal outside
        # the gates that keeps its run (``cli.gates``).
        "rekordbox-absence-unconfirmed": ExitCode.REKORDBOX_OPEN,
        "library-volume-unmounted": ExitCode.LIBRARY_UNAVAILABLE,
        # U27. A directory on the way to the library root cannot be opened, so
        # none of the positive claims below was made; its own remedy token.
        "library-root-unreachable": ExitCode.LIBRARY_UNAVAILABLE,
        "library-volume-mismatch": ExitCode.LIBRARY_UNAVAILABLE,
        # A volume a prefix rule points at. Own slugs, since "mount the library
        # volume" is false here: the act is on another disk or in one rule.
        "mapped-volume-unmounted": ExitCode.LIBRARY_UNAVAILABLE,
        "mapped-volume-mismatch": ExitCode.LIBRARY_UNAVAILABLE,
        "library-directory-missing": ExitCode.LIBRARY_UNAVAILABLE,
        "library-database-missing": ExitCode.LIBRARY_UNAVAILABLE,
        # R-663. The file at the path holds no rekordbox tables. Not the canary's
        # slug: nothing is damaged, the path is wrong, so setup is the act.
        "library-database-not-rekordbox": ExitCode.LIBRARY_UNAVAILABLE,
        "pyrekordbox-pin-drift": ExitCode.VERSION_PIN,
        "db-schema-pin-drift": ExitCode.VERSION_PIN,
        "app-version-pin-drift": ExitCode.VERSION_PIN,
        # S2: an unrecorded application pin refuses, never adopted from the
        # machine, since a pin copied from what is installed refuses nothing.
        "app-version-pin-unrecorded": ExitCode.VERSION_PIN,
        "tree-unconverged": ExitCode.UNCONVERGED,
        "database-open-failed": ExitCode.LIBRARY_UNREADABLE,
        "canary-read-failed": ExitCode.LIBRARY_UNREADABLE,
        # U8. A commit's read back disagreed. No post-commit rollback exists, so
        # every further write refuses until a person has looked.
        "session-committed-unverified": ExitCode.LIBRARY_UNREADABLE,
        # Sync genuinely on, answered by ``DISABLE_CLOUD_SYNC``; unreadable is above.
        "cloud-sync-active": ExitCode.EXTERNAL_WRITER,
        "mytag-category-template-missing": ExitCode.LIBRARY_PREREQUISITE,
        # U18. A catalog import named a tree the taxonomy does not declare. The
        # fix is a declaration in the template, so it carries the config token.
        "catalog-tree-undeclared": ExitCode.LIBRARY_PREREQUISITE,
        # U111. ``inbox rotate`` needs ``[intake_old]`` declared, and held once.
        # The remedy is a declaration or a folder, never configuration.
        "intake-old-undeclared": ExitCode.LIBRARY_PREREQUISITE,
        # U134. A refill's INBOX mirror playlist was moved out of INBOX.
        "refill-playlist-outside-inbox": ExitCode.LIBRARY_PREREQUISITE,
        # U121. ``[inspiration]`` is undeclared or held twice.
        "inspiration-folder-undeclared": ExitCode.LIBRARY_PREREQUISITE,
        # U121. The set's playlist could not be named (no uploader, title or
        # date) and no flag stood in. A fact about the recording, not USAGE.
        "set-playlist-unnamed": ExitCode.PRECONDITION,
        # U119. No playlist derived sub class is declared, or its source playlist
        # is absent or doubled. Two slugs: the template versus rekordbox.
        "favorites-class-undeclared": ExitCode.LIBRARY_PREREQUISITE,
        "favorites-source-missing": ExitCode.LIBRARY_PREREQUISITE,
        # A32. The row probe refuses before its gate: a malformed triple, an
        # unknown row, a value no live row holds, or one held by a minority.
        "link-probe-invalid": ExitCode.PRECONDITION,
        "link-row-unknown": ExitCode.PRECONDITION,
        "link-value-unheld": ExitCode.PRECONDITION,
        "link-value-minority": ExitCode.PRECONDITION,
        # U126. No ContentLink is held by a majority of live rows, so a native
        # landing has none to give; rekordbox's own imports are the remedy.
        "link-majority-unclear": ExitCode.LIBRARY_PREREQUISITE,
        # ── This installation ──
        "doctor-check-failed": ExitCode.PRECONDITION,
        # One slug for every unusable configuration; the remedy token says which.
        "config-unusable": ExitCode.PRECONDITION,
        # R-414. A rating cut that is neither an export byte nor a star, so the
        # planner cannot say how many stars it means; refused at plan time.
        "rating-scale-unknown": ExitCode.PRECONDITION,
        "module-extras-missing": ExitCode.MODULE_UNAVAILABLE,
        # U181. ``crate sync land`` stopped because the vocal model cannot score.
        # Not the extra's code: what is missing may be the model's files.
        "vocal-scoring-unavailable": ExitCode.PRECONDITION,
        "credential-missing": ExitCode.PRECONDITION,
        # The ``core.secrets`` presence sidecar is unreadable: no answer, unlike
        # ``credential-missing`` (R-116). An OS refusal reclassifies it.
        "credential-index-unreadable": ExitCode.PRECONDITION,
        # U10. A job not in the queue, or a queue from another build. Not USAGE,
        # which is argparse's; steps, since neither fix is a command.
        "job-unknown": ExitCode.PRECONDITION,
        "job-schema-mismatch": ExitCode.PRECONDITION,
        # R-390. A resume of a job whose failures are permanent. The job is known
        # exactly, so not ``job-unknown``.
        "job-not-retryable": ExitCode.PRECONDITION,
        # U168. The answer is recorded and the run kept no command line to
        # continue. Not ``decision-required``, which would ask again.
        "run-not-continuable": ExitCode.PRECONDITION,
        # R-1349. ``run decide`` named a plan gate the run has not reached. Not
        # ``decision-required``, which would invite the answer just refused.
        "gate-not-reached": ExitCode.PRECONDITION,
        # U11, the review queue: one code, a slug per place a person is sent.
        "review-item-unknown": ExitCode.PRECONDITION,
        # The queue refusing to overwrite a decision; clear the verdict first.
        "review-already-resolved": ExitCode.PRECONDITION,
        # Only a declared adjudication queue may take items.
        "review-queue-undeclared": ExitCode.PRECONDITION,
        "review-option-unknown": ExitCode.PRECONDITION,
        "review-schema-mismatch": ExitCode.PRECONDITION,
        # A selection naming nothing, two things, or an empty identity, which
        # would answer a whole backlog.
        "review-selection-invalid": ExitCode.PRECONDITION,
        # An export or decision store unusable. Not config's slug: the file is
        # data a person may have carried between machines.
        "review-file-unusable": ExitCode.PRECONDITION,
        "backup-acknowledgment-missing": ExitCode.ACK_REQUIRED,
        # U8. No controlling terminal to mint the acknowledgment; that caller is
        # the one R34 forbids from satisfying this gate.
        "backup-acknowledgment-no-terminal": ExitCode.ACK_REQUIRED,
        # U138. A session answered and a backup portion is five days old or of
        # unknown age; the act is a backup.
        "backup-acknowledgment-backup-too-old": ExitCode.ACK_REQUIRED,
        # U8. The backup ages the gate must show cannot be read, so minting would
        # record a person as shown a clean sheet they never saw.
        "backup-facts-unreadable": ExitCode.ACK_REQUIRED,
        # ── Upstream ──
        "auth-failed": ExitCode.UPSTREAM_AUTH,
        "adapter-broken": ExitCode.UPSTREAM_UNAVAILABLE,
        "unavailable-transient": ExitCode.UPSTREAM_UNAVAILABLE,
        # The provider refused the client itself (forbidden, a bot challenge, a
        # wait that is a refusal). A retry is the harm: steps, ``retryable=False``.
        "provider-blocked": ExitCode.UPSTREAM_UNAVAILABLE,
        # R-705. Rate limited past the retry ladder, or a cooldown still holds.
        # It lifts at a named time; every opener asks before it logs in.
        "provider-cooldown": ExitCode.UPSTREAM_UNAVAILABLE,
        # U193. One command reached its call ceiling: the person's own line, so
        # the policy code. A park, continued with a higher ceiling for one run.
        "provider-call-ceiling": ExitCode.REFUSED_BY_POLICY,
        # U278. An identity reached its hourly line across every command, or
        # ``--calls`` asked past it. It frees at a named minute.
        "provider-budget": ExitCode.REFUSED_BY_POLICY,
        # U293. The night pass spent what was left of the night's budget; the
        # next night's pass continues.
        "provider-night-budget": ExitCode.REFUSED_BY_POLICY,
        # U56. No public catalogue could be read, which is not no match; a
        # tagging job never reports done over a network never reached.
        "catalogue-unreachable": ExitCode.UPSTREAM_UNAVAILABLE,
        "unavailable-permanent": ExitCode.REFUSED_BY_POLICY,
        "refused-by-policy": ExitCode.REFUSED_BY_POLICY,
        "whitelist-violation": ExitCode.REFUSED_BY_POLICY,
        # U8, R17's runtime surface. A destructive session found an analysis
        # file moved; the whitelist governs rows and cannot see that write.
        "anlz-modified": ExitCode.REFUSED_BY_POLICY,
        "lossy-refused": ExitCode.REFUSED_BY_POLICY,
        # ── Lifecycle ──
        "cancelled": ExitCode.INTERRUPTED,
        # ── U19's refusals, appended ──
        # Blocks from here on are appended, not filed under a section, so two
        # units adding keys conflict textually instead of merging a duplicate.
        #
        # The routing ledger is unreadable in any way. One slug, as for config,
        # because the remedy travels on the remediation.
        "routing-ledger-unusable": ExitCode.PRECONDITION,
        # The tree registry is unreadable; one slug, as above (P5).
        "tree-registry-unusable": ExitCode.PRECONDITION,
        # A row cannot say whether it is a tombstone, and the permissive default
        # would place a deleted track.
        "soft-delete-marker-unreadable": ExitCode.LIBRARY_UNREADABLE,
        # The destination folder was renamed between decision and write, and
        # writing would file the track twice; only a person can choose.
        "routing-destination-renamed": ExitCode.UNCONVERGED,
        # U36. The convergence record is unreadable, so nothing can be said of
        # any tree and no rebuild answers it; hence not UNCONVERGED.
        "tree-convergence-unusable": ExitCode.LIBRARY_UNREADABLE,
        # U36. The taxonomy declares part of a tree the rebuild cannot derive,
        # which would be reported converged with a dimension missing.
        "rebuild-derivation-incomplete": ExitCode.LIBRARY_PREREQUISITE,
        # U36. The derivation placed nothing, so there is nothing to compare;
        # never read as converged.
        "rebuild-derivation-empty": ExitCode.LIBRARY_PREREQUISITE,
        # U36. The database's identity numbers are unreadable, so whether it is
        # the one last written cannot be answered.
        "library-fingerprint-unreadable": ExitCode.LIBRARY_UNREADABLE,
        # ── U32's refusals ──
        # The capture store is full. The library is fine; steps, since freeing
        # disk is not a command this product runs.
        "snapshot-store-full": ExitCode.PRECONDITION,
        # The reconciliation record is unreadable; one slug, as for config.
        "restore-record-unusable": ExitCode.PRECONDITION,
        # A bare-metal target that is not one: the library is reachable, the
        # target is a mount stub, or it holds a library nobody named.
        "recovery-target-refused": ExitCode.PRECONDITION,
        # Restoring would discard a later committed session: a decision, carrying
        # the trees and counts at stake.
        "restore-discards-committed-work": ExitCode.DECISION_REQUIRED,
        # A restore left markers undispositioned or trees unrebuilt.
        "restore-reconciliation-outstanding": ExitCode.UNCONVERGED,
        # A restore step failed on the machine (full, unwritable, drive error);
        # put right and repeated, never a raw OSError mid restore.
        "restore-step-failed": ExitCode.PRECONDITION,
        # Staging already holds a companion file under this name. Not
        # ``internal-error``: a fresh attempt takes a fresh staging directory.
        "restore-staging-occupied": ExitCode.PRECONDITION,
        # ── U34's refusals ──
        # A collection export unusable. Not the review file's slug: rekordbox
        # wrote this one, and the remedy is to export again.
        "library-export-unusable": ExitCode.PRECONDITION,
        # The declared intake flow is not in the export. Refused, since an empty
        # report would look like nothing to do.
        "intake-flow-absent": ExitCode.LIBRARY_PREREQUISITE,
        # ── U24's refusals ──
        # The deletion watermark is unreadable. Read as unset it would present
        # every historical removal as new, and the answer moves files.
        "deletion-watermark-unusable": ExitCode.PRECONDITION,
        # An active row that will not resolve or stat, so unreferenced would pass
        # on absence of evidence (R37). Names the rows, so its own slug.
        "deletion-reference-set-incomplete": ExitCode.PRECONDITION,
        # No usable Trash on the file's volume. R18 allows only the move to the
        # Trash, so there is no fallback, and never an unlink.
        "trash-unavailable": ExitCode.PRECONDITION,
        # A soft deleted row's removal sequence is unreadable; a guess either way
        # re-offers every removal or hides one for ever.
        "removal-sequence-unreadable": ExitCode.LIBRARY_UNREADABLE,
        # A walk an answer is read from came back short (membership, or an
        # anchor that moved). About no row, so not the reference set's slug.
        "deletion-evidence-incomplete": ExitCode.PRECONDITION,
        # ── U16's refusal ──
        # The external list is not one this build reads. Not USAGE: the parser
        # accepted the path, and what it points at is the problem.
        "intake-list-unusable": ExitCode.PRECONDITION,
        # U23. An adoption document (applied ledger or revert log) is unreadable.
        # Read as empty it would re-apply a plan or deny an undo.
        "adoption-ledger-unusable": ExitCode.PRECONDITION,
        # U23. A file to be tagged cannot be identified, so its original cannot
        # be recorded first. Per item; the library's state is wrong.
        "adoption-file-unidentifiable": ExitCode.PRECONDITION,
        # ── U22's refusals ──
        # The per-source watermark is unreadable; read as never synced, the next
        # increment would look like a first run.
        "sync-watermark-unusable": ExitCode.PRECONDITION,
        # Every listing for one source failed. Raised, never an empty catalogue,
        # which would advance a watermark over an unread playlist (KTD11).
        "sync-source-lookups-failed": ExitCode.UPSTREAM_UNAVAILABLE,
        # A remote mark asked for before the local file existed. Marks wait, so a
        # crash cannot leave the provider believing the run finished.
        "sync-marks-blocked": ExitCode.PRECONDITION,
        # The artifact registry is unreadable; empty would make debris intake.
        "sync-artifacts-unusable": ExitCode.PRECONDITION,
        # R-838. Sync mark's rename record is unreadable; empty would let no mark
        # be taken off.
        "sync-mark-record-unusable": ExitCode.PRECONDITION,
        # U320. The record of synced playlists answered not found is unreadable
        # or locked; empty would forget every retirement and first sighting.
        "sync-unavailable-record-unusable": ExitCode.PRECONDITION,
        # ── U20's refusals ──
        # A tree cannot flip with a run open, an intake XML pending, no Fresh
        # Export, or no snapshot.
        "cutover-open-run": ExitCode.PRECONDITION,
        "cutover-xml-pending": ExitCode.PRECONDITION,
        "cutover-export-missing": ExitCode.PRECONDITION,
        "cutover-snapshot-missing": ExitCode.PRECONDITION,
        # The rebuild needs a named person; an empty actor is the product
        # answering for the user.
        "rebuild-actor-required": ExitCode.PRECONDITION,
        # A tree still on the bridge; the next import would overwrite the rebuild.
        "rebuild-tree-not-native": ExitCode.PRECONDITION,
        # U219. A tree the derivation does not describe would get the routing
        # tree's folders (R-789); the routing tree is the one to name.
        "rebuild-tree-not-derivable": ExitCode.PRECONDITION,
        # U219. A resort derived adds other than the gate's, so the plan is stale.
        "resort-plan-stale": ExitCode.DECISION_STALE,
        # ── U37's refusals ──
        # A U22 stub listing given to the collection emitter as a Fresh Export (R-130).
        "intake-export-is-stub": ExitCode.PRECONDITION,
        # Recognition about to spend without the recorded keys or the helper
        # binary. Presence only; SET_CREDENTIAL, not AUTHENTICATE_PROVIDER.
        "intake-recognition-unready": ExitCode.PRECONDITION,
        # Files still in download staging; importing would stamp dead staging
        # paths (the 2026-06-29 flood).
        "intake-staging-refused": ExitCode.PRECONDITION,
        # ── U26's refusals ──
        # The curated label list is unreadable; empty would drop followed labels.
        "label-intent-unusable": ExitCode.PRECONDITION,
        # A label name, rename or registry field the registry cannot store (U99).
        "label-name-invalid": ExitCode.PRECONDITION,
        # The operator named a label the registry does not hold.
        "label-unknown": ExitCode.PRECONDITION,
        # The per-label last pulled document is unreadable.
        "label-watermark-unusable": ExitCode.PRECONDITION,
        # U176. The Bandcamp purchase record is unreadable or cannot be locked;
        # empty would fetch every purchase again.
        "bandcamp-record-unusable": ExitCode.PRECONDITION,
        # Harvest could not list the playlist; an invented label list is a guess.
        "label-playlist-unreadable": ExitCode.UPSTREAM_UNAVAILABLE,
        # ── U33's refusals ──
        # The outbound ledger is unreadable; empty would make a second remote
        # playlist for one already exported.
        "outbound-ledger-unusable": ExitCode.PRECONDITION,
        # Export invoked without a playlist identifier; not USAGE.
        "export-playlist-unknown": ExitCode.PRECONDITION,
        # ── U27's report refusals ──
        # The declared routing tree is not in the export. Not the intake slug,
        # so no consumer branches on message text.
        "governed-tree-absent": ExitCode.LIBRARY_PREREQUISITE,
        # An as-of value that is not a date. Refused, never defaulted to today.
        "report-as-of-invalid": ExitCode.PRECONDITION,
        # ── U27's off-machine restore refusals ──
        # The ``modules.tools.backup`` refusals, each on the code
        # ``cli.exit_codes`` reserves for it (P3), a slug per remedy.
        "rclone-missing": ExitCode.PRECONDITION,
        "remote-not-configured": ExitCode.PRECONDITION,
        "destination-not-configured": ExitCode.PRECONDITION,
        "library-root-absent": ExitCode.LIBRARY_UNAVAILABLE,
        # R-1761. A root that is there and not proven to be the library.
        "library-root-foreign": ExitCode.LIBRARY_UNAVAILABLE,
        "library-root-unproven": ExitCode.LIBRARY_UNAVAILABLE,
        "database-absent": ExitCode.LIBRARY_UNAVAILABLE,
        # Resumable once the decision naming this library and snapshot is recorded.
        "restore-not-confirmed": ExitCode.DECISION_REQUIRED,
        "restore-target-absent": ExitCode.LIBRARY_UNAVAILABLE,
        "no-snapshot-available": ExitCode.PRECONDITION,
        # R-388. A remote listing failed, which is not the absence above.
        "snapshot-listing-failed": ExitCode.PRECONDITION,
        # ── R-368's rehearsal target refusals ──
        # The target is the live library, holds it, sits in it, or would land on it.
        "restore-target-is-live-root": ExitCode.PRECONDITION,
        # The invocation is wrong (a target without the pull, or beside a capture
        # rollback); its own slug, since the directory is not the mistake.
        "restore-target-invalid": ExitCode.PRECONDITION,
        # A pull flag typed without asking for the pull; the verb's own.
        "restore-flag-needs-pull": ExitCode.PRECONDITION,
        # The transfer's return code, read since U27's second fix round.
        "restore-transfer-failed": ExitCode.PRECONDITION,
        # R-154. A stamp that is not one, a snapshot marked for another volume,
        # and a newest snapshot with no marker: three acts, three slugs.
        "snapshot-name-invalid": ExitCode.PRECONDITION,
        "snapshot-library-mismatch": ExitCode.PRECONDITION,
        "snapshot-identity-unrecorded": ExitCode.PRECONDITION,
        # ── U40's refusal ──
        # An empty folder for the destructive genre correction; never defaulted
        # to the working directory.
        "tag-retag-folder-unknown": ExitCode.PRECONDITION,
        # ── U43's refusals ──
        # The set builder was given an empty anchor.
        "setbuild-anchor-unknown": ExitCode.PRECONDITION,
        # The anchor is outside the library root, a different act from below.
        "setbuild-anchor-outside-library": ExitCode.PRECONDITION,
        # In the library and not indexed: absent, not audio, no Camelot key, or
        # in a folder the index leaves out (U279). The message says which.
        "setbuild-anchor-not-indexed": ExitCode.PRECONDITION,
        # R-187. ``--named`` matched several owned tracks or a longer version;
        # the opposite act to ``not-indexed``.
        "setbuild-anchor-ambiguous": ExitCode.PRECONDITION,
        # U98. An unowned anchor with no key, or a key or tempo beside a path
        # anchor, which would be ignored. Two acts, two slugs.
        "setbuild-unowned-key-missing": ExitCode.PRECONDITION,
        "setbuild-supplied-needs-unowned": ExitCode.PRECONDITION,
        # ── U44's refusals ──
        # The mastering refusals ``cli/exit_codes.py`` has reserved since U35.
        # ``restore-transfer-failed`` sits among them there and is declared
        # above; a duplicate key would resolve silently.
        "source-missing": ExitCode.PRECONDITION,
        "source-unsupported": ExitCode.PRECONDITION,
        "output-exists": ExitCode.PRECONDITION,
        "archive-holds-a-different-recording": ExitCode.PRECONDITION,
        "archive-verify-failed": ExitCode.PRECONDITION,
        "encoder-missing": ExitCode.PRECONDITION,
        "encoder-failed": ExitCode.PRECONDITION,
        # ── U45's refusals ──
        # The backup shell's whole run verdicts, raised only by
        # ``cratekit.backup.cli.refusal_for``, and not reserved, as shell refusals.
        "backup-transfer-failed": ExitCode.PRECONDITION,
        "backup-nothing-ran": ExitCode.PRECONDITION,
        # ── U51's refusals ──
        # The outbound verbs need a collection export to derive items from.
        "outbound-export-required": ExitCode.PRECONDITION,
        # Several playlists carry the typed name, a different act from unknown.
        "export-playlist-ambiguous": ExitCode.PRECONDITION,
        # No writable track. The zero item rule: a job with no items reports
        # SUCCEEDED, so it is refused here.
        "export-playlist-empty": ExitCode.PRECONDITION,
        # No adapter binds a stored credential to an outbound account: a stated
        # gap in the product, not ``credential-missing``.
        "outbound-account-unbound": ExitCode.PRECONDITION,
        # The frozen export lost a queued track; export again and queue fresh.
        "outbound-item-absent": ExitCode.PRECONDITION,
        # ── U55's refusals ──
        # The collection lost a queued scan row; the library moved since the census.
        "adopt-item-absent": ExitCode.PRECONDITION,
        # Plan entries failed to apply; without this the job would succeed over
        # an adoption that placed nothing.
        "adopt-entries-failed": ExitCode.PRECONDITION,
        # ── U52's refusals ──
        # No catalogue adapter for the label package: a stated gap, not
        # ``credential-missing``, and not the outbound slug.
        "label-catalogue-unbound": ExitCode.PRECONDITION,
        # No favourite label registered; the zero item rule again.
        "label-registry-empty": ExitCode.PRECONDITION,
        # Some releases could not be offered, so the item fails. Not upstream:
        # the item is resumable state, and the raise site carries RESUME_JOB.
        "label-sweep-incomplete": ExitCode.PRECONDITION,
        # ── U107's refusals ──
        # The guided label sync record is unreadable or locked; empty would ask
        # every question again.
        "label-sync-unusable": ExitCode.PRECONDITION,
        # A terminal question got no usable answer; ``--next`` and ``--answer``
        # are the scriptable path.
        "label-sync-unanswerable": ExitCode.PRECONDITION,
        # R-1114. ``label sync --next`` could read no label; a total failure is
        # not nothing new (the ``no-evidence`` rule).
        "label-sync-unlisted": ExitCode.PRECONDITION,
        # ── U109's refusal ──
        # A verb whose queueing was retired, ``crate sync labels`` first; the
        # steps name the replacing command.
        "verb-retired": ExitCode.PRECONDITION,
        # ── U58's refusals ──
        # A restamp over a library never calibrated has no level to stamp.
        "energy-calibration-missing": ExitCode.PRECONDITION,
        # The calibration file is unreadable, never folded into never calibrated.
        "energy-calibration-unreadable": ExitCode.PRECONDITION,
        # R-342. The vocal cut file is unreadable or not finite; a missing file
        # still means the default.
        "vocal-calibration-unreadable": ExitCode.PRECONDITION,
        # U90. A vocal cut outside 0 to 100 or not finite; not USAGE.
        "vocal-cut-out-of-range": ExitCode.PRECONDITION,
        # R-372. Most active rows match neither the root nor a prefix rule, as
        # after a drive rename; setup run again offers the rule.
        "library-paths-majority-unresolved": ExitCode.PRECONDITION,
        # An analysed track's tag write or rename failed; the item fails rather
        # than report values the file lacks. The audio is untouched.
        "analysis-write-failed": ExitCode.PRECONDITION,
        # ── U57's refusals ──
        # Recognition would exceed its caps or quota: a fact about money, never
        # a miss about the audio.
        "intake-recognition-spend-bound": ExitCode.REFUSED_BY_POLICY,
        # Recognition unreachable or unclassifiable; the chunk retries next run.
        "intake-recognition-failed": ExitCode.UPSTREAM_UNAVAILABLE,
        # ── U67's refusal ──
        # ``name apply`` could not read the collection; never empty, which would
        # strand every row. The site carries the inner cause's remedy.
        "collection-unreadable": ExitCode.LIBRARY_UNREADABLE,
        # ── U75's refusal ──
        # ``label approved`` could not build the list; a no-op would look like a
        # library already holding every approved release.
        "label-list-unusable": ExitCode.PRECONDITION,
        # U80. ``acquire fallback`` could not resolve ``yt-dlp``, raised in this
        # verb's vocabulary with the binaries module's remedy token.
        "yt-dlp-missing": ExitCode.PRECONDITION,
        # ── R-500's refusal ──
        # ``name apply`` met a row under an unmapped volume whose file is absent;
        # a rename could strand it. Configuration is the fix.
        "collection-row-unmapped": ExitCode.PRECONDITION,
        # ── R-172's answer ──
        # ``name apply`` could not do every planned rename, the rest did happen.
        # Ok would be the answer for ever, as every sweep meets the collision.
        "rename-incomplete": ExitCode.PRECONDITION,
        # ── U105's refusal ──
        # ``crate master --lufs`` outside loudnorm's range or not finite; refused
        # at queue time.
        "target-lufs-out-of-range": ExitCode.PRECONDITION,
        # ── R-229's refusal ──
        # A confirmed outbound update whose ledger record moved by drive time.
        # Never created as a second remote playlist; queue again.
        "outbound-record-moved": ExitCode.PRECONDITION,
        # ── R-235's refusals ──
        # The tree named is not declared by the taxonomy.
        "cutover-tree-undeclared": ExitCode.PRECONDITION,
        # Not exactly one folder of the tree's name under the playlist root.
        # Never created or chosen; the count is in the detail.
        "cutover-root-unresolved": ExitCode.PRECONDITION,
        # A revert of a tree that took a native write; the database owns it now.
        "cutover-native-write-taken": ExitCode.PRECONDITION,
        # The registry already records the tree as native; never replaced.
        "cutover-already-recorded": ExitCode.PRECONDITION,
        # ── R-799's refusal ──
        # An approved genre correction a file did not take; raised after the
        # others were written, and a second run plans the rest.
        "tag-remap-unwritten": ExitCode.PRECONDITION,
        # ── U114's refusal ──
        # An approved suggested genre a file did not take; its row is left
        # without one so file and row agree.
        "tag-suggest-unwritten": ExitCode.PRECONDITION,
        # ── R-835's refusals ──
        # A label's catalogue was not read in full; refused before the gate.
        "label-playlists-incomplete": ExitCode.PRECONDITION,
        # R-1091. A label's kept release reads are unreadable; never read as empty.
        "label-playlists-reads-unusable": ExitCode.PRECONDITION,
        # U217. A label roster's kept listing is unreadable, on R-1091's rule.
        "label-listing-kept-unusable": ExitCode.PRECONDITION,
        # Two account root folders share the label's name; the fix is on the account.
        "label-playlists-ambiguous": ExitCode.PRECONDITION,
        # The label's folder is not on the account yet (U117); it comes first.
        "label-new-playlists-no-folder": ExitCode.PRECONDITION,
        # ── R-837's refusal ──
        # Two account root folders share the year's name.
        "export-set-ambiguous": ExitCode.PRECONDITION,
        # U140. A set's account playlist could not follow its INSPIRATION name;
        # another verb comes first.
        "export-set-rename-unresolved": ExitCode.PRECONDITION,
        # ── R-836's refusal ──
        # A remote removal refused unsent: not product made, or positions unread.
        "outbound-remove-refused": ExitCode.PRECONDITION,
        # ── R-228's refusal ──
        # No live Pink colour row, so the favourites sweep cannot tell pink rows.
        "favorites-pink-colour-missing": ExitCode.PRECONDITION,
        # ── U123's refusals ──
        # ``label heard`` was given a year or date that is not one.
        "label-heard-invalid": ExitCode.PRECONDITION,
        # No go took a release of the label on that day.
        "label-heard-no-releases": ExitCode.PRECONDITION,
        # A ``--release`` not in the dated playlist.
        "label-heard-not-in-playlist": ExitCode.PRECONDITION,
        # Two playlists share the dated or the year's name.
        "label-heard-ambiguous": ExitCode.PRECONDITION,
        # The dated playlist is not product made; it is merged by hand.
        "label-heard-not-product-made": ExitCode.PRECONDITION,
        # No year playlist; ``label playlists`` builds it first.
        "label-heard-no-year-playlist": ExitCode.PRECONDITION,
        # ── U130's refusals ──
        # The playlist pairs document is unreadable or locked.
        "sync-pair-store-unusable": ExitCode.PRECONDITION,
        # U210. A pair write could not record a step, so it stopped; earlier
        # writes are kept.
        "sync-pair-steps-unwritten": ExitCode.PRECONDITION,
        # An unmarked account playlist with no partner, or one a side lacks.
        "sync-pair-unknown": ExitCode.PRECONDITION,
        # A playlist a pair may not hold: the hearts, a label's or set's, a
        # folder, or one under Cratekit's own trees.
        "sync-pair-out-of-scope": ExitCode.PRECONDITION,
        # U226. Paged and unpaged reads disagree, so the account may lag; a run
        # a few minutes later reads it again.
        "sync-pair-account-lagging": ExitCode.UPSTREAM_UNAVAILABLE,
        # U231. A pair whose account order was sent and is not yet read as landed.
        "sync-pair-account-settling": ExitCode.UPSTREAM_UNAVAILABLE,
        # One of the two playlists is already paired.
        "sync-pair-conflict": ExitCode.PRECONDITION,
        # ── U221's refusals ──
        # ``sync release`` named a playlist with no custom twin pair.
        "sync-release-not-a-twin": ExitCode.PRECONDITION,
        # ``sync release`` named no twin and no ``--all``, or both.
        "sync-release-unnamed": ExitCode.PRECONDITION,
        # ── U147's refusal ──
        # A mirrored folder's name is doubled on the account or in the tree.
        "account-mirror-ambiguous": ExitCode.PRECONDITION,
        # ── U167's refusals ──
        # ``analyze check`` found rekordbox's result wrong; analyse again. Its own
        # slug so a skill tells it from waiting, which exits 12.
        "analysis-suspect": ExitCode.LIBRARY_PREREQUISITE,
        # ``analyze check`` named an unknown landing; an empty scope would exit 0.
        "analysis-check-landing-unknown": ExitCode.PRECONDITION,
        # ── U178's refusal ──
        # ``tag folder`` had a genre the file would not take; the item fails.
        "tag-folder-unwritten": ExitCode.PRECONDITION,
        # ── U177's refusal ──
        # A staged Bandcamp file would not take the label tag; the item fails.
        "bandcamp-label-unwritten": ExitCode.PRECONDITION,
        # ── R-1103's refusal ──
        # ``tag retag`` had a specific genre the file would not take.
        "tag-retag-unwritten": ExitCode.PRECONDITION,
        # ── U169's refusal ──
        # A ``--root`` that is not there; an empty plan would read as nothing to do.
        "root-folder-missing": ExitCode.PRECONDITION,
        # ── U194's refusals ──
        # A genre word ``taxonomy alias`` or ``taxonomy folder`` cannot take;
        # refused before the gate.
        "taxonomy-word-refused": ExitCode.PRECONDITION,
        # An alias names a genre folder the taxonomy does not declare.
        "taxonomy-genre-unknown": ExitCode.PRECONDITION,
        # An approved alias a file did not take; a second run plans the rest.
        "taxonomy-word-unwritten": ExitCode.PRECONDITION,
        # ── R-1677's refusal ──
        # No temporary room for the integrity copy; refused naming the volume,
        # never a failed check. Steps, as for ``snapshot-store-full``.
        "snapshot-check-temp-full": ExitCode.PRECONDITION,
    }
)


class UnknownReason(KeyError):
    """A cause was built with a slug the registry does not declare."""


@dataclass(frozen=True, slots=True)
class Cause:
    """One failure, carried whole across every boundary between its origin and the CLI.

    ``origin`` is append-only and every hop appends; a one element trail at the
    CLI means a hop re-created the cause and lost what was below. ``detail`` is
    never read for control flow; anything a caller branches on is a declared
    field.
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
        """The status this cause exits with, looked up so it cannot disagree with the slug."""
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

        Boundary 3 is a process boundary, so a cause must round trip through
        JSON to cross it.
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


def classified(cause: Cause, exc: BaseException | None) -> Cause:
    """``cause``, corrected if the operating system is what actually refused.

    The correction is made here, in the constructor every structured refusal
    passes through, not only where one escapes: most ``except OSError`` sites
    raise a refusal no blanket handler ever sees, so no site needs an edit and a
    new one is right by default. It reads the declared cause chain only
    (``raise refuse(...) from exc``), never ``__context__``. It changes the slug
    and the act, never the words (D2), and a site whose act is already right
    keeps its better slug.
    """
    refusal = access_refusal(exc)
    if refusal is None or cause.remediation.remedy is refusal.remedy:
        return cause
    return replace(
        cause,
        reason=refusal.reason,
        remediation=replace(cause.remediation, remedy=refusal.remedy),
        detail={
            **dict(cause.detail),
            "path": refusal.path,
            "access": str(refusal.kind),
            # The site's own reading, kept to be read and never branched on.
            "declared_reason": cause.reason,
        },
    )


class CratekitError(Exception):
    """The one exception type that carries a cause across a raise.

    Every refusal in the package raises this or a subclass, so no catcher has to
    parse a message string.
    """

    def __init__(self, cause: Cause) -> None:
        super().__init__(cause.message)
        self._declared = cause

    @property
    def cause(self) -> Cause:
        """The cause as the reader gets it, classified against what caused it.

        A property because ``raise X from exc`` sets ``__cause__`` after this
        object is built, so ``__init__`` cannot see it. Every consumer reaches
        the cause through this name.
        """
        return classified(self._declared, self.__cause__)

    @property
    def declared_cause(self) -> Cause:
        """The cause exactly as the raising site wrote it, unclassified.

        For the test that proves the correction happened.
        """
        return self._declared


class JobBlocked(CratekitError):
    """A queued job parked, leaving its verb through the refusal exit as blocked.

    ``jobs.drive`` returns normally for a park and the job is ``blocked``, an
    open state, so a normal envelope reported it ``ok`` and exited 0 (R-290).
    ``jobs.raise_for_state`` raises this and the dispatcher reads it as
    ``Outcome.BLOCKED``. A type and not a test on the cause, because the cause
    is the adapter's own and the same slugs fail items in jobs never parked. It
    lives here, not in ``core.jobs``, only to avoid an import cycle with the
    dispatcher. A hop that rebuilds the refusal must rebuild this type, through
    :func:`rebuilt`, or blocked silently turns into failed.
    """


class JobCancelled(CratekitError):
    """A queued job somebody stopped, leaving its verb as cancelled and not failed.

    ``jobs.raise_for_state`` raises this for a cancelled job and the dispatcher
    reads it as ``Outcome.CANCELLED``. A type for :class:`JobBlocked`'s reason:
    one way of carrying a job's ending, so one rule for every hop, :func:`rebuilt`.
    """


#: The types whose whole meaning is the type. Order is irrelevant, no job is both.
_CARRIED: tuple[type[CratekitError], ...] = (JobBlocked, JobCancelled)


def rebuilt(error: CratekitError, cause: Cause) -> CratekitError:
    """The refusal ``error`` carrying ``cause`` instead, keeping what its type says.

    The one owner of a reworded refusal: a new ``CratekitError`` would drop the
    bit :class:`JobBlocked` and :class:`JobCancelled` carry, and
    ``tests/test_job_outcome.py`` refuses a rebuild spelled any other way. Only
    the carried types survive, since other subclasses take constructor arguments
    of their own and no reader branches on them.
    """
    for kind in _CARRIED:
        if isinstance(error, kind):
            return kind(cause)
    return CratekitError(cause)


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
    """Build the exception for a refusal, with its remediation defaulted.

    The default is the remedy the exit code declares, so a caller spells one out
    only when this failure has a better answer than its class, and raise sites
    do not each invent their own wording.
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
    "ACCESS_REASONS", "ACCESS_REMEDIES", "DATABASE_ACCESS_ERRORNAMES", "DATABASE_PATH_ATTRIBUTE",
    "NOT_FOUND_STATUS", "PERMISSION_ERRNOS", "READ_ONLY_ERRNOS", "REASONS", "AccessKind",
    "AccessRefusal", "Cause", "CratekitError", "JobBlocked", "JobCancelled", "Outcome",
    "Remediation", "Scope", "UnknownReason", "access_refusal", "access_remedy",
    "answered_not_found", "answered_status", "classified", "failure_links", "name_the_database",
    "nearest_status", "permission_denied", "rebuilt", "refuse", "widest_scope",
]
