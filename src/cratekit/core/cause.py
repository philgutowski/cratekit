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

#: The two errno values that mean "this account does not hold that permission".
#: ``PermissionError`` is exactly the ``OSError`` subclass CPython raises for
#: these two, so the class test below is the same rule; the numbers are named as
#: well because an ``OSError`` reconstructed across a boundary can arrive as the
#: base class carrying only its number.
PERMISSION_ERRNOS: frozenset[int] = frozenset({errno.EACCES, errno.EPERM})

#: The errno that means the MEDIUM refuses every writer, not this account.
#: Granting an account more access cannot change it and no amount of Full Disk
#: Access will, so it is a different act with a different sentence: remount the
#: volume read write, or slide the card's write-protect tab back. A library on a
#: read only disk image or a locked SD card is an ordinary DJ arrangement rather
#: than an exotic one, and it used to arrive as an internal defect.
READ_ONLY_ERRNOS: frozenset[int] = frozenset({errno.EROFS})

#: SQLite's own names for "the file system would not give me this file". These
#: arrive as ``sqlite3.OperationalError``, which is NOT an ``OSError``: it
#: carries no errno, no filename and no ``__cause__``, so an errno rule alone is
#: blind to every permission that reaches this program through the C extension
#: it stores its own state in. The names are stable SQLite result-code names
#: exposed by CPython 3.11 and later as ``sqlite_errorname``.
DATABASE_ACCESS_ERRORNAMES: tuple[str, ...] = (
    "SQLITE_CANTOPEN",
    "SQLITE_READONLY",
    "SQLITE_PERM",
)

#: Where a driver records WHICH file its error was about. The driver knows the
#: path and the exception does not carry one, so the knowledge is attached at
#: the one place that has it rather than guessed at the place that does not.
#: See :func:`name_the_database`.
DATABASE_PATH_ATTRIBUTE = "cratekit_database_path"


class AccessKind(StrEnum):
    """Which kind of refusal the operating system made, because the acts differ.

    Three different sentences and three different things for a person to do. The
    vocabulary collapsed all three into "grant this interpreter access, on macOS
    through Full Disk Access", which is the right instruction for exactly one of
    them and confidently wrong for the other two: Full Disk Access will never
    make a write to a read only volume succeed, and it will never clear Finder's
    Locked checkbox.
    """

    #: This account is not allowed. Granting it access is the fix.
    PERMISSION = "permission"
    #: The volume refuses every writer. Remounting or unlocking the medium is.
    READ_ONLY = "read-only"
    #: A per-file immutable flag, which is what Finder's "Locked" checkbox sets.
    LOCKED = "locked"


#: The declared reason slug for each kind. They share an exit code, which is
#: correct and is what the registry's own note describes: the band answers "can
#: this installation proceed", and the slug is where the distinction stays
#: useful.
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

    ``path`` IS NOT OPTIONAL, and that is the type's whole point. The
    classification this replaces answered "yes, a permission" for a
    ``PermissionError`` the kernel raised with no filename at all, which a
    socket bind to a privileged port and ``os.setuid`` both produce, and the
    sentence it then rendered told the user to grant access to "the path named
    below" with no path below it. ``render.access_note``'s own docstring calls
    the path "the entire actionable content"; a type that cannot be built
    without one is how that stops being a docstring and starts being a rule.
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
    """``exc`` and its DECLARED causes, once each.

    THE ``__cause__`` CHAIN IS FOLLOWED AND ``__context__`` IS NOT. An explicit
    ``raise X from exc`` is a statement that this failure IS that failure, so a
    wrapper may not hide a refusal underneath it. An implicit context is merely
    "this happened while handling that", which is exactly what a handler that
    catches a refusal, recovers, and then raises a real defect produces, and
    reading it would classify that defect as a refusal.

    The ``seen`` set is not decoration. ``__cause__`` is assignable, so a pair of
    exceptions can name each other and this walk is then infinite; without it the
    process does not fail, it stops responding, which is the worst shape a defect
    in a classification can take.
    """
    seen: set[int] = set()
    current = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        yield current
        current = current.__cause__


def _immutable(path: str) -> bool:
    """Whether a per-file immutable flag is set on ``path``.

    ``chflags uchg`` is what Finder's "Locked" checkbox writes, and it is the
    commonest way a macOS user meets EPERM on a file they own and can see. The
    flags field only exists on the BSD family, so its absence answers False
    rather than raising.

    ``ValueError`` IS CAUGHT ALONGSIDE ``OSError`` AND IS NOT THE SAME KIND OF
    THING. A path with an embedded null is rejected by ``os.lstat`` before any
    syscall is made, and that is not an ``OSError``: it is the argument being
    unrepresentable. This function is read from inside the dispatcher's own
    ``except CratekitError`` handler, where an escaping exception replaces a
    refusal a user could act on with a traceback, so a question asked about an
    unrepresentable path answers False here for the same reason
    ``os.path.ismount`` answers False for it.
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
    """The path the refusal was about, DESTINATION first.

    ``os.replace`` sets ``filename`` to the source and ``filename2`` to the
    destination, and the guarded writer writes every file by renaming a
    temporary one over it. Reading ``filename`` alone named ``cfg/tmpXXXX.tmp``
    at the user, a path that no longer exists by the time they read about it,
    while the file they actually have to unlock went unmentioned.
    """
    for candidate in (exc.filename2, exc.filename):
        spelled = _spelled(candidate)
        if spelled is not None:
            return spelled
    return None


def _refused_of_two(exc: OSError, fallback: str) -> str:
    """Which of two named paths the operating system ACTUALLY refused.

    POSITION ALONE DOES NOT SAY WHICH SIDE WAS REFUSED, and the destination-first
    rule above is measured right for ``os.replace``, ``os.rename``, ``os.symlink``
    and ``shutil.move`` and measured WRONG for ``os.link``: with a source this
    account cannot reach, ``filename`` is the sealed source and ``filename2`` is
    the destination it can already write, so destination-first names the one path
    there is nothing to do about. The same shape is reachable from ``os.rename``
    whenever the SOURCE side is what the kernel refused.

    So it is measured rather than guessed, the same way ``_probe_readable``
    measures a driver level error instead of assuming one. The destination keeps
    precedence:
    it is asked first, and the source is named only when the destination is not
    itself refused and the source is.

    ONLY FOR A PERMISSION OR A LOCK, never for a read only volume, and that is
    the one caller's job to enforce rather than this function's to explain twice.
    See :func:`_from_os_error`.
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
        # A refusal with no path is not a refusal this program can tell anybody
        # how to fix, so it is not claimed as one. See ``AccessRefusal``.
        return None
    if exc.errno in READ_ONLY_ERRNOS:
        # THE DESTINATION, WITHOUT MEASURING. A read only volume is a property of
        # the MEDIUM rather than of one path on it: a two path call that answers
        # EROFS had both paths on that volume, because a call across two
        # filesystems answers EXDEV instead. There is nothing to choose between
        # them and the destination is the one the user was trying to reach.
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

    ``shutil.copytree`` DOES NOT RAISE THE REFUSAL IT MET. It collects every
    member it could not copy and raises one ``shutil.Error`` at the end whose
    single argument is a list of ``(source, destination, why)`` triples, and
    ``why`` has already been rendered to TEXT. Measured on this platform, that
    exception is an ``OSError`` subclass carrying ``errno``, ``filename`` and
    ``filename2`` all None and no ``__cause__``, so every errno rule in this
    module answers None for it and a sealed member of a declared capture source
    reached the user as "this is a defect; report it".

    The paths survive the rendering even though the errno does not, so the paths
    are what this measures: each named source is asked directly, exactly as
    :func:`_probe_readable` asks for a driver level error. A member that is merely
    gone by now claims nothing.
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


#: WHY THERE ARE TWO OF THESE, AND WHY EXACTLY ONE OF THEM OPENS ANYTHING.
#:
#: This module is admitted to the reports allowlist, because both report modules
#: import ``Scope`` and ``refuse`` from it, and that allowlist's whole argument is
#: that nothing it admits can touch a file. So this module may hold ONE ``os.open``
#: and it has to be a read.
#:
#: The read probe below spells its flags INLINE, and that is not style. The guard
#: decides whether an ``os.open`` is a read by reading THE CALL'S OWN ARGUMENT
#: against a set of reading flags. It cannot resolve a name back to an assignment,
#: so ``os.open(path, flags)`` is reported as an open whose flags it cannot read,
#: whatever the assignment says. Driven 2026-08-14: five different assignments were
#: tried, including a plain ``os.O_RDONLY`` with no conditional in it, and every
#: one was refused. Only the inline expression is readable, and then it is exactly
#: right in both directions: read only passes, write capable fails. The same
#: measurement is why ``os.O_NONBLOCK`` is spelled directly rather than through
#: ``getattr(os, "O_NONBLOCK", 0)``, which was a defensive fallback the guard also
#: could not read. This package targets macOS, where the constant is always
#: present.
#:
#: SO THEY MAY NOT BE FOLDED BACK INTO ONE FUNCTION TAKING ``writing: bool``. That
#: is the obvious spelling and it is the one a tidy up reaches for. It reinstates
#: the unreadable shape, and it reinstates the write capable handle this module is
#: not allowed to hold. See R-80 and R-102.


def _probe_readable(path: str) -> AccessRefusal | None:
    """Ask the operating system whether ``path`` can be READ.

    A driver level error says "unable to open database file" and nothing else,
    so whether that was a permission is not stated anywhere in it. It is
    MEASURED here rather than assumed: the file is opened the same way the driver
    would have, and the ``OSError`` that comes back carries the errno and the
    filename the classification needs. An open that succeeds answers None, and
    the failure keeps its honest "this program did not anticipate it" reading.

    ``ValueError`` is caught for the reason :func:`_immutable` gives: a path with
    an embedded null is rejected by ``os.open`` before any syscall, and this is
    read from inside the dispatcher's own refusal handler, where raising replaces
    an act the user could take with a traceback.

    NOT MEASURED: a mount that has stopped responding. ``O_NONBLOCK`` covers a
    FIFO with no writer, which returns immediately, and does not cover a blocking
    wait inside the virtual filesystem layer, so a hung network mount would still
    block here. No stalled mount was available to drive it.
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
    """Say WHY a write to ``path`` was refused, without opening a write handle.

    THE ONE CALLER IS :func:`_from_database_error`, for a driver error that is not
    ``SQLITE_CANTOPEN``, which leaves ``SQLITE_READONLY`` and ``SQLITE_PERM``.
    Both mean the driver ALREADY tried a write and was refused. So this is not
    predicting an outcome, it is attributing one that has happened, and the three
    attributions this program can act on are all readable from metadata: the
    medium refuses every writer, a per-file lock refuses this write, or this
    account does not hold the permission.

    IT USED TO OPEN ``os.O_RDWR`` AND MAY NOT AGAIN. R-80: this module is on the
    reports allowlist, whose argument is that nothing it admits can touch a file,
    and a write capable handle here made that argument false. The guard that says
    so cannot be widened and the module cannot be relocated, so the handle went.
    The read probe is still real, and is asked first, because a file this account
    cannot even read is a refusal the errno already classifies and that answer
    outranks any metadata reading.

    ORDER IS DELIBERATE. A read only medium is a property of the volume rather
    than of one path on it, so it outranks both per-file answers. The immutable
    flag outranks the mode for the same reason :func:`_from_os_error` checks it
    first: ``chflags uchg`` and a denied mode both arrive as a refusal and they
    route to different acts, and only one of them is something the user can chmod
    away.

    ``effective_ids`` is asked for where the platform has it, because the write
    that was refused was made with the effective identity and ``os.access``
    otherwise answers for the real one.

    DRIVEN, 2026-08-15, against the write capable handle it replaces: 12 real
    arrangements, and every one that this function's ONE producer can actually
    hand it agrees. The two that disagree are both DIRECTORIES, and a directory
    reaches ``sqlite3`` as ``SQLITE_CANTOPEN``, which routes to
    :func:`_probe_readable` and never arrives here. Driven end to end as well,
    through :func:`access_refusal`, on a real read only volume, a real mode
    refusal and a real Finder lock.

    NOT MEASURED: a network mounted volume, where the client can answer from
    cached metadata while the server is what refuses. That class is unmeasured for
    BOTH implementations rather than a known loss, because an open on a client
    that has already cached the attributes does not reach the server either. No
    network share was available.
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
        # The same two guards :func:`_probe_readable` gives, for the same reason:
        # this is read inside the dispatcher's own refusal handler, where an
        # escaping exception replaces an act the user could take with a traceback.
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

    The connection site knows the path; the exception does not carry one and
    never will, because the driver's error is a result code and a sentence. This
    is the whole hand-off: one attribute, set where the knowledge is, read by
    :func:`access_refusal` where the decision is. Returning the SAME exception
    keeps the traceback and the class, so nothing downstream has to learn a new
    type to catch.

    IT RECORDS ALONG THE DECLARED CHAIN, NOT ONLY ON THE EXCEPTION HANDED IN.
    Two of this package's three connection sites catch ``sqlite3.Error`` itself,
    so the chain is one link long and this changes nothing for them. The third
    goes through an object mapper, which catches the driver's error and re-raises
    its OWN type ``from`` it: the exception a handler there can see is a
    ``sqlalchemy.exc.OperationalError``, and the ``sqlite3.OperationalError``
    that actually carries ``sqlite_errorname`` is two links down. Recording only
    on the top of that chain records on the one object the classification cannot
    read, which is a fix landing beside the thing it was meant to land on.
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

    ONE DECISION, MADE ONCE, because making it per call site failed four
    consecutive review rounds. A path the operating system will not let this
    interpreter open, write, or replace is not a defect in this program: it is a
    machine state its user can act on, and every layer that meets one has to say
    so. Rendering it as an internal error sends a person to file a bug report
    about their own filesystem, and on macOS that is the ROUTINE first run rather
    than an exotic state: anything under Documents, Desktop, Downloads or an
    external volume is refused this way for an interpreter without Full Disk
    Access.

    The reason it kept reappearing at ordinary looking call sites is that
    ``Path.exists`` and ``Path.is_dir`` RE RAISE under EPERM rather than
    answering False, so a line that reads like a question is a line that throws.
    A guard per line is a guard the next line will not have, which is why this is
    a classification rather than a handler.

    IT ANSWERS FOR MORE THAN THE ``OSError`` FAMILY. The previous rule was a set
    of two errno values, and this program keeps its own state in SQLite, whose
    refusals are not ``OSError`` at all. It also answers with a KIND, because a
    read only volume and a locked file are refusals that Full Disk Access cannot
    fix, and confidently telling a user to grant access is not a lesser failure
    than telling them to file a bug.
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

    A NARROWER QUESTION THAN :func:`access_refusal`, kept separate on purpose.
    This one answers "is this the CLASS of failure the operating system raises
    when an account is not allowed", and its callers are the ones deciding
    whether to re-raise or to answer False: ``preflight`` will not let a
    permission masquerade as "not a mount point", and ``backup_facts`` will not
    let one masquerade as a corrupt file. None of them tells a user anything, so
    none of them needs a path.

    Anything that RENDERS a refusal asks :func:`access_refusal` instead, because
    a sentence naming no path is a sentence a user can do nothing with.
    """
    for current in _chain(exc):
        if isinstance(current, PermissionError):
            return current
        if isinstance(current, OSError) and current.errno in PERMISSION_ERRNOS:
            return current
    return None


def access_remedy(exc: BaseException | None, *, otherwise: Remedy) -> Remedy:
    """The act for a failure that MIGHT be one the operating system refused.

    The one chooser every site calls instead of writing ``Remedy.REPORT_DEFECT``
    beside a caught ``OSError``. It answers with the act for the KIND that was
    found, so a read only volume is not sent to Full Disk Access and a locked
    file is not either.
    """
    found = access_refusal(exc)
    return found.remedy if found is not None else otherwise


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
        # U56. A public catalogue answered and the page carried no shape this
        # product's parser recognises, which is a defect HERE rather than a fact
        # about the catalogue. It shares ``internal-error``'s code because
        # ``report-defect`` is the right instruction, and it does not share the
        # slug because the two are read by different people: a scraper whose
        # target moved is expected over time and is somebody's afternoon, while
        # ``internal-error`` is a state the program said could not happen.
        # Folding it into ``unavailable-transient`` instead would be worse than
        # either, since a permanent break would then wear "retry later" for ever.
        "catalogue-parse-broken": ExitCode.INTERNAL,
        # U27. The operating system refused this account, anywhere under a verb,
        # at a call nobody guarded. It is deliberately NOT ``internal-error``:
        # that slug carries ``report-defect``, and a permission the user can
        # grant is not a defect in this program. It sits on the installation band
        # rather than on the library's, because the dispatcher meets it without
        # knowing whether the path was the library, the configuration directory
        # or a packaged file. A refusal that DOES know says so under its own
        # slug, which is why ``library-root-unreachable`` still exists.
        "path-permission-denied": ExitCode.PRECONDITION,
        # The same band, and deliberately NOT the same slug. Neither of these is
        # a permission this account can be granted: a read only volume refuses
        # every writer on the machine, and an immutable flag refuses the owner.
        # One slug for all three would put "grant Full Disk Access" beside two
        # states it cannot change, which is the collapse the vocabulary exists to
        # prevent, one level in from where it was last prevented.
        "path-read-only": ExitCode.PRECONDITION,
        "path-locked": ExitCode.PRECONDITION,
        "no-evidence": ExitCode.INTERNAL,
        # R-391. A failed job whose permanent item failures do not share one
        # reason. Beside ``no-evidence`` because it is the same kind of thing, a
        # job level verdict over items that each carry their own cause and their
        # own code, and there is no honest single band for two of them. The
        # cause names every reason and carries the sorted set in its detail, so
        # the item causes are where a person reads the specific codes.
        "mixed-permanent-failures": ExitCode.INTERNAL,
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
        # R-705. The one call at a time lock over the streaming provider was
        # held by another driver for longer than a call can take. A fourth slug
        # on this code, for the reason the third gives: the remedy is still
        # "wait for the holder", and what is held is the account.
        "provider-gate-held": ExitCode.LIBRARY_BUSY,
        "rekordbox-running": ExitCode.REKORDBOX_OPEN,
        "library-volume-unmounted": ExitCode.LIBRARY_UNAVAILABLE,
        # U27. Some directory on the way to the configured library root cannot be
        # opened by this account, so which volume the library sits on was not
        # established. Its own slug rather than one of the three below it,
        # because every one of those is a positive claim this run did NOT make:
        # nothing established that the volume is unmounted, that it is the wrong
        # one, or that the directory is missing. The remedy is a different act
        # too, which is why it carries its own token.
        "library-root-unreachable": ExitCode.LIBRARY_UNAVAILABLE,
        "library-volume-mismatch": ExitCode.LIBRARY_UNAVAILABLE,
        # A volume a PREFIX RULE points at, which is not the library volume. Two
        # slugs of their own rather than the two library ones above, because
        # those carry "mount the configured library volume" as their remedy and
        # that sentence is false here: the library volume is mounted and right,
        # and the act that helps is on a different disk or in one rule.
        "mapped-volume-unmounted": ExitCode.LIBRARY_UNAVAILABLE,
        "mapped-volume-mismatch": ExitCode.LIBRARY_UNAVAILABLE,
        "library-directory-missing": ExitCode.LIBRARY_UNAVAILABLE,
        "library-database-missing": ExitCode.LIBRARY_UNAVAILABLE,
        # R-663. There IS a file at the configured path, and a copy of it is
        # empty or holds none of the tables the canary reads, so it is not a
        # rekordbox library at all. Its own slug rather than the canary's,
        # because the canary's band says the library is damaged and names a
        # snapshot restore, and nothing here is damaged: the path is wrong, and
        # the act that helps is setup with the right one.
        "library-database-not-rekordbox": ExitCode.LIBRARY_UNAVAILABLE,
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
        # U111. ``inbox rotate`` was asked to move a stale batch into a folder
        # this library's taxonomy does not declare, ``[intake_old]``, or the
        # intake root holds that folder twice. The catalog's code and its
        # reason: the remedy is a declaration or a folder, never this
        # installation's configuration.
        "intake-old-undeclared": ExitCode.LIBRARY_PREREQUISITE,
        # U121. A set's playlist was asked for under a folder this library's
        # taxonomy does not declare, ``[inspiration]``, or the playlist root
        # holds that folder twice. The catalog's code and its reason.
        "inspiration-folder-undeclared": ExitCode.LIBRARY_PREREQUISITE,
        # U121. The set's playlist could not be named: the job's page carried
        # no uploader, no title or no upload date, and the flag that stands in
        # for the missing one was not given. PRECONDITION rather than USAGE,
        # since the parser accepted the command line and what is missing is a
        # fact about the recording, which the flag supplies.
        "set-playlist-unnamed": ExitCode.PRECONDITION,
        # U119. The genre Favorites were asked for on a library whose taxonomy
        # declares no sub class derived from a playlist, or the playlist that
        # class mirrors, All Favorites in the shipped template, is not in the
        # library or is there more than once. The catalog's code and its
        # reason: the remedy is a declaration or a playlist, never this
        # installation's configuration. Two slugs because the two acts differ,
        # one in the template and one in rekordbox.
        "favorites-class-undeclared": ExitCode.LIBRARY_PREREQUISITE,
        "favorites-source-missing": ExitCode.LIBRARY_PREREQUISITE,
        # A32. The row probe refuses before its gate: a triple is malformed,
        # names a column the probe may not write or repeats a row and column;
        # the identifier names no live content row; no other live row carries
        # the value asked for; or fewer rows carry it than carry the row's own
        # value, so the write would move the row away from the library's
        # majority. PRECONDITION on all four, since the parser accepted the
        # command line and what is wrong is the choice of probe, which the
        # person changes.
        "link-probe-invalid": ExitCode.PRECONDITION,
        "link-row-unknown": ExitCode.PRECONDITION,
        "link-value-unheld": ExitCode.PRECONDITION,
        "link-value-minority": ExitCode.PRECONDITION,
        # U126. A native landing reads the ContentLink the library's live rows
        # mostly carry and gives it to every row it makes, and no value is
        # held by more than half of them, so there is none to give. The
        # library's state and not the command line: rekordbox's own imports
        # are the remedy.
        "link-majority-unclear": ExitCode.LIBRARY_PREREQUISITE,
        # ── This installation ───────────────────────────────────────────────
        "doctor-check-failed": ExitCode.PRECONDITION,
        # One slug for every way configuration can be unusable, because the
        # thing that differs between them is the REMEDY and the remedy travels
        # on the remediation. ``config.Remedy`` already distinguishes missing
        # from corrupt from too-new from invalid from locked, and a cause built
        # from one of those carries its token through unchanged.
        "config-unusable": ExitCode.PRECONDITION,
        # R-414. A taxonomy rating cut that is neither an export byte (51 to
        # 255 in fifths) nor a database star (1 to 5), so the rating planner
        # cannot say how many stars it means. Refused at plan time because the
        # database stores stars and a value it does not recognise would land in
        # that field as written. A curve mixing the two scales is the same
        # refusal, since it does not say which one it is on.
        "rating-scale-unknown": ExitCode.PRECONDITION,
        "module-extras-missing": ExitCode.MODULE_UNAVAILABLE,
        "credential-missing": ExitCode.PRECONDITION,
        # Item 4 of the residual finding "Five places where "I could not look"
        # is still not said out loud". The presence sidecar ``core.secrets`` keeps so doctor can
        # ask "is this recorded" without retrieving a value could not be read, so
        # this installation cannot say which credentials it holds. DISTINCT FROM
        # ``credential-missing`` on the distinction that entry exists to draw: one
        # is an answer and the other is the absence of one, and a person told a
        # credential is missing records one the keychain may already hold, which
        # is the loop R-116 measured.
        #
        # PRECONDITION rather than INTERNAL because the sidecar is this
        # installation's own state and repairing it is an act the person can
        # take. An OS refusal underneath is reclassified by ``classified`` to
        # ``path-permission-denied``, which is a different act again, so this slug
        # is what is left once nothing granted or mounted explains it.
        "credential-index-unreadable": ExitCode.PRECONDITION,
        # U10. A named job that is not in this installation's queue, and a queue
        # written by a different build of the product. Both are 3x rather than a
        # command-line class because ``USAGE`` belongs to the argument parser and
        # to nothing else, and both carry their remediation as STEPS rather than
        # a token: neither fix is a command, and inventing a token that renders
        # to one would be worse than saying the sentence.
        "job-unknown": ExitCode.PRECONDITION,
        "job-schema-mismatch": ExitCode.PRECONDITION,
        # R-390. A resume of a job whose recorded cause says its failures are
        # permanent. The same band and the same steps shape as its two
        # neighbours: the queue's state is what refuses, and the fix is not a
        # command this product can name, it is reading each item's cause and
        # queueing the work again once the reason is addressed. Deliberately NOT
        # ``job-unknown``, which means the job or the state is not one the queue
        # knows, and this job is known exactly.
        "job-not-retryable": ExitCode.PRECONDITION,
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
        # R-705. The streaming provider rate limited this account past the retry
        # ladder, or a verb started while that cooldown still holds. The same
        # code as the block above, because the account said no, and its own slug
        # because the act differs: a block is checked at the account, and a
        # cooldown lifts at a named time the cause carries. Every provider
        # opener asks the gate before it logs in, so the refusal makes no call.
        "provider-cooldown": ExitCode.UPSTREAM_UNAVAILABLE,
        # U56. No public catalogue could be READ, which is a different fact from
        # no catalogue carrying the track, and the slug is the only place that
        # difference survives. The tagging searcher declines when a source
        # answered and had no match, and raises this when none of them answered,
        # so a tagging job never reports every item done over a network that was
        # never reached. It shares the transient code because that is what it is.
        "catalogue-unreachable": ExitCode.UPSTREAM_UNAVAILABLE,
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
        # U36. The record of which governed trees are converged exists and
        # cannot be understood. LIBRARY_UNREADABLE rather than UNCONVERGED, and
        # the difference is the point: UNCONVERGED means a specific tree is known
        # to be short and names the rebuild that repairs it, while this means
        # nothing at all can be said about any tree, which no rebuild answers.
        # It shares the code and the doctor remedy with the other state
        # documents that can be corrupt, and keeps its own slug because the file
        # to repair is a different file.
        "tree-convergence-unusable": ExitCode.LIBRARY_UNREADABLE,
        # U36. This library's taxonomy declares part of a governed tree that the
        # rebuild has no way to derive, so a rebuild would silently produce a
        # tree missing that whole dimension and then report it converged. A
        # LIBRARY_PREREQUISITE for the same reason the undeclared catalog tree is
        # one: the library declares a structure and the missing half is a fact
        # about the declaration rather than about anything the run did.
        "rebuild-derivation-incomplete": ExitCode.LIBRARY_PREREQUISITE,
        # U36. The derivation ran and placed nothing at all, so there is no
        # declared membership to compare the database against. A separate slug
        # from the one above, because the two are different facts with different
        # answers: that one says the taxonomy declares something this rebuild
        # cannot derive, and this one says the derivation read an empty or absent
        # library. LIBRARY_PREREQUISITE for the same reason: the missing half is
        # a fact about what the library has, not about anything the run did. It
        # is NOT collapsed into "converged", which is the reading that let a
        # rebuild that derived nothing clear the flag saying a tree is short.
        "rebuild-derivation-empty": ExitCode.LIBRARY_PREREQUISITE,
        # U36. The three numbers that say WHICH database this is could not be
        # read, so whether it is the one Cratekit last wrote to cannot be
        # answered either way. LIBRARY_UNREADABLE with the other "the database is
        # there and cannot be trusted to read as expected" slugs, and its own
        # slug because the file to look at is the database rather than one of the
        # state documents.
        "library-fingerprint-unreadable": ExitCode.LIBRARY_UNREADABLE,
        # ── U32's refusals, appended for the reason the block above gives ────
        #
        # The capture store cannot fit one more capture. PRECONDITION rather than
        # a library code, because nothing is wrong with the library: this
        # installation has run out of somewhere to put the undo. It carries STEPS
        # rather than a remedy token for the reason ``job-unknown`` does; freeing
        # disk is not a command this product runs, and inventing a token that
        # rendered to one would be worse than saying the sentence.
        "snapshot-store-full": ExitCode.PRECONDITION,
        # The reconciliation record is present and cannot be understood. ONE SLUG
        # for every way one file can be unusable, exactly as ``config-unusable``
        # and ``routing-ledger-unusable`` already argue: what differs between them
        # is the REMEDY, and the remedy travels on the remediation.
        "restore-record-unusable": ExitCode.PRECONDITION,
        # A bare-metal target that is not one: the library volume turns out to be
        # reachable after all, the target is the empty stub a mount point leaves
        # behind, or it already holds a library nobody named for replacement. One
        # slug, three sentences, because the answer in each case is a different
        # act by the same person and the act rides on the steps.
        "recovery-target-refused": ExitCode.PRECONDITION,
        # Restoring this session would discard a later one that committed. It is
        # a DECISION rather than a failure: the answer is a person naming the
        # sessions they are prepared to lose, and the refusal carries the trees
        # and the counts they would be losing so the naming is informed.
        "restore-discards-committed-work": ExitCode.DECISION_REQUIRED,
        # A restore landed and left markers nobody has dispositioned, or trees
        # nobody has rebuilt. UNCONVERGED because that is precisely what it is:
        # what the library holds and what the record says have come apart, and
        # only a person can close the gap. It shares the code with
        # ``tree-unconverged`` and keeps its own slug because the two name
        # different things to repair, and the detail shapes differ accordingly.
        "restore-reconciliation-outstanding": ExitCode.UNCONVERGED,
        # One step of a restore could not be performed: the volume filled, the
        # directory is not writable by this account, or the drive returned an
        # error. PRECONDITION because every one of those is a condition of the
        # machine that a person puts right and then repeats the restore, and it
        # carries STEPS rather than a remedy token for the reason
        # ``snapshot-store-full`` does. It exists at all because the alternative
        # was a raw OSError escaping mid restore: no reason, no remedy, no
        # reserved exit code, at the moment somebody is already recovering.
        "restore-step-failed": ExitCode.PRECONDITION,
        # A restore's staging directory already holds a companion file under the
        # name this attempt wants, so moving the live one there would overwrite
        # the only surviving copy of transactions that are in no capture. ITS OWN
        # SLUG RATHER THAN ``internal-error``, which is where it used to land,
        # and the difference is what a person is told to do: an internal error
        # says report a defect and stop, and this condition is cleared by running
        # the restore again, because a fresh attempt takes a fresh staging
        # directory. PRECONDITION for the reason ``restore-step-failed`` is one:
        # it is a condition of the machine that a repeat clears.
        "restore-staging-occupied": ExitCode.PRECONDITION,
        # ── U34's refusals, appended for the reason stated just above ───────
        #
        # The first version of this unit filed the export slug beside
        # ``review-file-unusable``, in the middle of the literal, which is the
        # convention this block exists to state. Confirmed with ``git
        # merge-file``: two units appending both conflict textually and get
        # read, while an insertion into a different half of the same mapping
        # auto-merges, so a duplicate key would be resolved silently by
        # whichever line happened to come last.
        #
        # A collection export that is not one, or is one and is truncated, or
        # carries one ``TrackID`` twice. Its own slug rather than the review
        # file's, because that file is something this product WROTE and this one
        # is something rekordbox wrote: the remedy is to export again, and
        # pointing a person at a queue export they never made would be a
        # sentence about the wrong file. Same code, because the class of answer
        # is the same, which is the whole reason a slug exists separately from a
        # code.
        "library-export-unusable": ExitCode.PRECONDITION,
        # The declared intake flow does not appear anywhere in the exported
        # tree. Reported rather than answered with an empty report, because the
        # correct answer for an intake flow with nothing in it is ALSO nothing,
        # so the two are indistinguishable to the person reading the output and
        # only one of them means "you have nothing to do". It sits on the
        # library-prerequisite code beside ``catalog-tree-undeclared`` for the
        # same reason that one exists: the library lacks a structure the
        # operation mirrors, and the remedy is a declaration or a folder rather
        # than anything about this installation's configuration.
        "intake-flow-absent": ExitCode.LIBRARY_PREREQUISITE,
        # ── U24's refusals, appended for the reason the block above gives ────
        #
        # The deletion watermark is present and cannot be understood: not valid
        # JSON, a document that is not this one, a version this build does not
        # know, or a sequence that is not a number. ONE SLUG, exactly as the
        # routing ledger and the tree registry take one each, because what
        # differs between the shapes is the REMEDY and the remedy travels on the
        # remediation. Refusing rather than treating it as unset matters more
        # here than for either sibling: an unreadable watermark read as "never
        # run" presents a whole library's historical removals as if they had
        # just happened, and the answer to that question moves files.
        "deletion-watermark-unusable": ExitCode.PRECONDITION,
        # An active row that will not resolve, or that resolves and will not
        # stat. It contributes no filesystem identity, so the proof that a
        # candidate's file is unreferenced would pass on absence of evidence
        # (R37). Its own slug rather than the doctor's because the pass names
        # exactly which rows are missing from the set and how many, and because
        # this is the one refusal a friend with cloud-backed or online-only
        # files meets while the author's own library never does.
        "deletion-reference-set-incomplete": ExitCode.PRECONDITION,
        # The volume holding a confirmed file has no Trash this account can use,
        # or has one on a different device, which a rename cannot reach. R18
        # permits exactly one destructive act on a music file and it is the move
        # to the system Trash, so there is no fallback to fall back to: an
        # unlink here would be the product doing the one thing it promised never
        # to do, at the one moment nobody could check it afterwards.
        "trash-unavailable": ExitCode.PRECONDITION,
        # A row rekordbox soft-deleted that cannot report the update sequence
        # the removal was stamped with. Its own slug beside
        # ``soft-delete-marker-unreadable`` and on the same code, for the same
        # reason that one exists: the database is present and readable in every
        # other respect, and what cannot be read is one specific fact whose
        # absence has no safe default. Guessing low re-offers every removal in
        # the library on every run; guessing high marks the row handled and
        # nobody is ever asked about it.
        "removal-sequence-unreadable": ExitCode.LIBRARY_UNREADABLE,
        # A walk this pass reads an ANSWER off came back short, so the answer is
        # about the rows that happened to arrive rather than about the library.
        # Two shapes reach it and both are the same fault: the playlist
        # membership walk that could not be shown to have seen every membership
        # row, and an anchor whose existence answer moved while the removals were
        # being categorised. ONE SLUG for the reason the routing ledger and the
        # tree registry each take one: what differs is the REMEDY, and the remedy
        # travels on the remediation. Its own slug rather than the reference
        # set's because that one is about ACTIVE ROWS and names them in its
        # sentence, while neither of these is a statement about any row at all.
        "deletion-evidence-incomplete": ExitCode.PRECONDITION,
        # ── U16's refusal, appended for the reason given above ──────────────
        #
        # The external list a match was asked to resolve is not a list this
        # build reads: the path names nothing, it names a web address rather
        # than a file, it is not the document format this build speaks, or one
        # pasted line carries no artist. ONE SLUG for all of them, the third
        # time this mapping makes that choice, and for the same reason: what
        # differs is the sentence, and the sentence travels on the remediation.
        # PRECONDITION rather than USAGE, because USAGE belongs to the argument
        # parser and to nothing else, and the argument parser accepted this
        # command line perfectly: the path was well formed and what it points at
        # is the problem.
        "intake-list-unusable": ExitCode.PRECONDITION,
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
        # U22. Appended, not filed under an earlier heading: two units writing
        # into different halves of this literal auto-merge and a duplicate key
        # is then resolved by line order. An append conflicts textually.
        #
        # The per-source watermark document is present and cannot be understood.
        # Same shape as the deletion watermark: refusing rather than treating it
        # as unset, because an unreadable audit record read as "never synced"
        # would make the next increment look like a first run.
        "sync-watermark-unusable": ExitCode.PRECONDITION,
        # Every listing call for one source failed. Raising, not returning an
        # empty catalogue, is KTD11: the source system treated that empty list
        # as "nothing new" and advanced a watermark over a playlist that had
        # never been read.
        "sync-source-lookups-failed": ExitCode.UPSTREAM_UNAVAILABLE,
        # An irreversible remote mark was requested before the local importable
        # file existed. Deferred prefixing is the rule; applying the mark first
        # is how a crash leaves the provider believing the run finished.
        "sync-marks-blocked": ExitCode.PRECONDITION,
        # The artifact registry is present and cannot be understood. Treating it
        # as empty would make crash debris look like next-run intake.
        "sync-artifacts-unusable": ExitCode.PRECONDITION,
        # R-838. The record of what sync mark renamed is present and cannot be
        # understood. Read as empty, it would refuse every mark it holds, so
        # the one verb that can take a mark off could take none off.
        "sync-mark-record-unusable": ExitCode.PRECONDITION,
        # ── U20's refusals, appended for the reason given above ─────────────
        #
        # A tree cannot flip while a run is still open, while an intake XML is
        # still sitting there, while nobody took a Fresh Export, or while no
        # snapshot exists to restore from. Four slugs, one code: what differs
        # is the sentence and the step, and those travel on the remediation.
        "cutover-open-run": ExitCode.PRECONDITION,
        "cutover-xml-pending": ExitCode.PRECONDITION,
        "cutover-export-missing": ExitCode.PRECONDITION,
        "cutover-snapshot-missing": ExitCode.PRECONDITION,
        # The rebuild surface needs a named person. An empty actor is the
        # product answering for the user. PRECONDITION rather than USAGE,
        # because USAGE belongs to argparse and the parser accepted the
        # invocation; the missing name is the problem.
        "rebuild-actor-required": ExitCode.PRECONDITION,
        # A rebuild of a tree still on the bridge would write membership the
        # next import would overwrite.
        "rebuild-tree-not-native": ExitCode.PRECONDITION,
        # ── U37's refusals, appended ────────────────────────────────────────
        #
        # APPENDED, same reason as the U20 block above: two units writing into
        # different halves of this literal auto-merge, and a duplicate key is
        # then resolved by line order.
        #
        # A U22 stub listing was handed to the COLLECTION emitter as if it were
        # a Fresh Export. Importing that listing is wrong (R-130). PRECONDITION
        # rather than a defect code, because the file the operator named is the
        # problem, not this build.
        "intake-export-is-stub": ExitCode.PRECONDITION,
        # Recognition spend was about to start without the recorded keys, or
        # without the helper binary that carves the audio. Presence only, never
        # retrieval. SET_CREDENTIAL, not AUTHENTICATE_PROVIDER.
        "intake-recognition-unready": ExitCode.PRECONDITION,
        # Inbox of files still sitting in download staging. Locations stamp from
        # the current path, so importing now would fill the collection with dead
        # staging references (the 2026-06-29 flood).
        "intake-staging-refused": ExitCode.PRECONDITION,
        # ── U26's refusals, appended ────────────────────────────────────────
        #
        # APPENDED, same reason as the U22 and U37 blocks: two units writing
        # into different halves of this literal auto-merge.
        #
        # The curated label list is present and cannot be understood. Treating
        # it as empty would drop the followed labels on the next save.
        "label-intent-unusable": ExitCode.PRECONDITION,
        # A favourite-label name produced no identifier, a rename arrived
        # without the new display name, or a registry verb was handed a field
        # it cannot store: an id: seed that is not digits, a blank seed, a
        # track limit below one, a field on an action that does not set it
        # (U99). PRECONDITION rather than USAGE, because the parser accepted
        # the invocation.
        "label-name-invalid": ExitCode.PRECONDITION,
        # The operator named a label the registry does not hold.
        "label-unknown": ExitCode.PRECONDITION,
        # The per-label last-pulled document is present and cannot be
        # understood. Same shape as sync-watermark-unusable.
        "label-watermark-unusable": ExitCode.PRECONDITION,
        # Harvest could not list the named playlist. An invented label list
        # would be a guess, so the verb refuses rather than offering one.
        "label-playlist-unreadable": ExitCode.UPSTREAM_UNAVAILABLE,
        # ── U33's refusals, appended ────────────────────────────────────────
        #
        # APPENDED, same reason as the U26 block: two units writing into
        # different halves of this literal auto-merge.
        #
        # The outbound write ledger is present and cannot be understood.
        # Treating it as empty would create a second remote playlist for a
        # library playlist this account already exported.
        "outbound-ledger-unusable": ExitCode.PRECONDITION,
        # Export was invoked without a playlist identifier. PRECONDITION
        # rather than USAGE, because the parser accepted the invocation.
        "export-playlist-unknown": ExitCode.PRECONDITION,
        # ── U27's report refusal, appended for the reason the blocks above give ─
        #
        # The declared routing tree does not appear anywhere in the exported
        # tree. It sits beside ``intake-flow-absent`` in meaning and takes the
        # same code for the same reason: the library lacks a structure the
        # report describes, and the remedy is a declaration or a folder rather
        # than anything about this installation's configuration. It is its own
        # slug rather than a second use of the intake one because the two send a
        # person to different places, the routing tree and the intake flow, and
        # a shared slug would make a consumer branch on the message text.
        "governed-tree-absent": ExitCode.LIBRARY_PREREQUISITE,
        # The aging report was given an as-of value that is not a date.
        # PRECONDITION rather than USAGE, for the reason the slug directly above
        # gives: status 2 belongs to the argument parser and to nothing else, and
        # the parser accepted this invocation because any string is a valid
        # argument to a flag that takes one. Refused rather than defaulted to
        # today, because a report that quietly answered for a different day than
        # the one somebody typed would band every grouping against a value this
        # product invented.
        "report-as-of-invalid": ExitCode.PRECONDITION,
        # ── U27's off-machine restore refusals, appended for the reason above ──
        #
        # ``modules.tools.backup`` has always raised its own ``Refusal`` enum,
        # and until a verb surfaced one nothing needed these here: the module was
        # reached only from its own suite, which reads the enum directly.
        # ``restore run --from-backup`` is the first caller that carries one out
        # to a person, and a bare exception at that boundary arrives as an
        # internal error with its remediation discarded, which is the collapse
        # KTD25 exists to stop.
        #
        # EVERY CODE HERE IS THE ONE ``cratekit.cli.exit_codes`` ALREADY RESERVED
        # for the same slug, copied rather than decided again. The two tables
        # answer different questions, the reserved one holding the per-slug
        # remediation and this one holding the status, and for these eight they
        # now answer about the same slugs. ``tests/test_write_session.py`` derives
        # the agreement from ``backup.REFUSALS`` rather than listing it, so a
        # member added to that enum later is covered on the day it appears (P3).
        # ``rekordbox-running`` is deliberately absent from this block: it was
        # already declared above, by the writer that refuses for the same reason.
        #
        # A slug per diagnosis rather than one "the backup refused", because the
        # remedies are eight different acts: install a program, configure a
        # remote, mount a volume, take a backup at all.
        "rclone-missing": ExitCode.PRECONDITION,
        "remote-not-configured": ExitCode.PRECONDITION,
        "destination-not-configured": ExitCode.PRECONDITION,
        "library-root-absent": ExitCode.LIBRARY_UNAVAILABLE,
        "database-absent": ExitCode.LIBRARY_UNAVAILABLE,
        # DECISION_REQUIRED rather than a failure code, which is the reservation
        # table's own judgement: a restore that has not been confirmed is
        # resumable, and the run continues once the decision naming this library
        # and this snapshot is recorded.
        "restore-not-confirmed": ExitCode.DECISION_REQUIRED,
        "restore-target-absent": ExitCode.LIBRARY_UNAVAILABLE,
        "no-snapshot-available": ExitCode.PRECONDITION,
        # R-388. A listing on the remote failed, which is not the absence the
        # slug above names, so it carries its own reserved steps.
        "snapshot-listing-failed": ExitCode.PRECONDITION,
        # ── R-368's two, the rehearsal target the restore verb now takes ───────
        #
        # PRECONDITION rather than USAGE for the reason every block above gives:
        # status 2 belongs to the argument parser and to nothing else, and the
        # parser accepted both of these invocations, because any string is a
        # valid argument to a flag that takes one and a flag combination is not
        # something it is asked about.
        #
        # ``restore-target-is-live-root`` is a fact about a PATH: the directory
        # named is the library, holds it, sits inside it, or would land the
        # restored database on the live one. Not LIBRARY_UNAVAILABLE, which is
        # what the absent target reserves: nothing is unreachable here, and the
        # library being exactly where it should be is the problem.
        "restore-target-is-live-root": ExitCode.PRECONDITION,
        # ``restore-target-invalid`` is a fact about the INVOCATION: a target
        # without the off-machine pull that fills it, or a target beside a
        # capture rollback that cannot be pointed anywhere but the live library.
        # Its own slug rather than a second use of the one above, because a
        # person told their directory is the live library will go looking at the
        # directory, which in these two is not where the mistake is.
        "restore-target-invalid": ExitCode.PRECONDITION,
        # The same shape as the entry above, one flag family over: a flag that
        # describes the off-machine pull, typed without asking for the pull. The
        # parser accepted it, so not USAGE, and it is the verb's own, so it is
        # registered here and not reserved.
        "restore-flag-needs-pull": ExitCode.PRECONDITION,
        # Appended in U27's second fix round rather than with the eight above,
        # because it did not exist when they landed: the review found that
        # ``run_restore`` never read a return code, so this is the slug the
        # reading now raises under.
        "restore-transfer-failed": ExitCode.PRECONDITION,
        # R-154's three, beside the restore refusals they extend. PRECONDITION for
        # each, on the judgement the target slugs above are given: the parser
        # accepted the invocation, because any string is a valid argument to a
        # flag that takes one, and what is wrong is a fact about the value or
        # about the remote. A stamp that is not a stamp, a snapshot whose marker
        # names another volume, and a newest snapshot with no marker at all are
        # three different acts to undo, so they are three slugs.
        "snapshot-name-invalid": ExitCode.PRECONDITION,
        "snapshot-library-mismatch": ExitCode.PRECONDITION,
        "snapshot-identity-unrecorded": ExitCode.PRECONDITION,
        # ── U40's refusal, appended for the reason every block above gives ─────
        #
        # The genre correction verb was invoked with an empty folder. PRECONDITION
        # rather than USAGE for exactly the reason ``export-playlist-unknown``
        # above gives: the parser accepted the invocation, because an empty string
        # is a valid argument to a positional that takes one, and status 2 belongs
        # to the argument parser and to nothing else. Refused rather than defaulted
        # to the working directory, because the verb is destructive and a default
        # here would sweep whatever the person happened to be standing in.
        "tag-retag-folder-unknown": ExitCode.PRECONDITION,
        # ── U43's refusals, appended for the reason every block above gives ────
        #
        # The set builder was invoked with an empty anchor. PRECONDITION rather
        # than USAGE on the same argument ``tag-retag-folder-unknown`` makes: the
        # parser accepted the invocation, because an empty string is a valid
        # argument to a positional that takes one.
        "setbuild-anchor-unknown": ExitCode.PRECONDITION,
        # The anchor resolves outside the configured library root. A separate
        # slug from the one below rather than folded into it, because the two
        # remedies are different acts: this one is "you named a file somewhere
        # else", and that one is "the file is here and the index cannot use it".
        "setbuild-anchor-outside-library": ExitCode.PRECONDITION,
        # The anchor is inside the library and the index does not hold it: it is
        # absent, it is not audio, or it carries no Camelot key from either its
        # tag or its name. One slug for the three, because the index is what
        # decides ownership and a track it does not hold cannot be ranked
        # against, whichever of the three reasons put it outside.
        "setbuild-anchor-not-indexed": ExitCode.PRECONDITION,
        # R-187's one, beside its siblings. A name given with ``--named``
        # reached owned tracks and could not choose between them, or named a
        # longer version than the one the library holds. Its own slug rather
        # than ``not-indexed``, because the remedies are opposite acts: that one
        # says the library does not have it, and this one says the library has
        # it more than once and lists them.
        "setbuild-anchor-ambiguous": ExitCode.PRECONDITION,
        # U98's two, beside their siblings. An unowned anchor named with no
        # Camelot key: the engine answers unresolved rather than guessing, and
        # nothing here looks one up. And a key or tempo supplied beside a PATH
        # anchor, which takes both from the library, so the value would be
        # silently ignored. PRECONDITION for both on the argument above: the
        # parser accepted each flag, and what is wrong is how they combine. Two
        # slugs because the remedies are two acts, add a key, or drop the flags.
        "setbuild-unowned-key-missing": ExitCode.PRECONDITION,
        "setbuild-supplied-needs-unowned": ExitCode.PRECONDITION,
        # ── U44's refusals, appended for the reason every block above gives ────
        #
        # WHY THESE ARRIVE SO LATE, since the mastering engine shipped in U35.
        # ``cli/exit_codes.py`` has reserved all seven since that unit, and this
        # registry never declared one, because U35 landed no CALLER that could
        # raise one. ``Cause.__post_init__`` refuses a slug this mapping does not
        # declare, so until U44 every mastering refusal reaching the dispatcher
        # would have been converted to ``internal-error``, and a person whose
        # recording was not where they said it was would have been told to report
        # a defect. A reserved code with no registry entry is not half a
        # vocabulary; it is a refusal that cannot be raised.
        #
        # ALL SEVEN ARE PRECONDITION, matching the reservation each already
        # carries. Six of the seven share that code for the reason the reserved
        # table states: a recording named on the command line, the container it
        # is in, and the archive slot beside it are all preconditions THIS verb
        # declares, and each is undone by a different act. The slug keeps them
        # apart where that is read, which is the envelope.
        #
        # DO NOT ADD ``restore-transfer-failed`` HERE. It sits interleaved among
        # the mastering reservations in ``cli/exit_codes.py``, between
        # ``archive-verify-failed`` and ``encoder-missing``, and it is already
        # declared above under U27's block. Copying that file's block by line
        # range rather than by slug duplicates the key, and a duplicate is
        # resolved silently by whichever line comes last.
        "source-missing": ExitCode.PRECONDITION,
        "source-unsupported": ExitCode.PRECONDITION,
        "output-exists": ExitCode.PRECONDITION,
        "archive-holds-a-different-recording": ExitCode.PRECONDITION,
        "archive-verify-failed": ExitCode.PRECONDITION,
        "encoder-missing": ExitCode.PRECONDITION,
        "encoder-failed": ExitCode.PRECONDITION,
        # ── U45's refusals, appended for the reason every block above gives ────
        #
        # THE BACKUP SHELL'S TWO, and neither belongs in the engine's ``Refusal``
        # enum. Every member of that enum is a reason ONE PORTION will not run,
        # decided before anything is attempted, and ``run_backup`` reports those
        # per portion rather than raising because a mirror that completed while
        # the database was skipped is a successful mirror. These two are the
        # opposite altitude: they are the WHOLE RUN's verdict over that per
        # portion report, which is a command line's decision rather than an
        # engine's, and the layer that owns an exit code is the layer that owns
        # them. ``cratekit.backup.cli.refusal_for`` is the only raise site.
        #
        # PRECONDITION for both, on the same judgement
        # ``restore-transfer-failed`` above is given: a remote that was reachable
        # enough to plan against and then was not is not a defect in this
        # program, and neither is a machine that has not been set up yet.
        "backup-transfer-failed": ExitCode.PRECONDITION,
        # NOT reserved in ``cli/exit_codes.py``, deliberately, and the same is
        # true of the entry above. The eight backup slugs that ARE reserved there
        # are the engine's enum members, and the reservation table is where a
        # module's own declared vocabulary is pinned to a code. A shell refusal
        # belongs here alone, exactly as ``export-playlist-unknown``,
        # ``tag-retag-folder-unknown`` and the three ``setbuild-anchor`` slugs do.
        "backup-nothing-ran": ExitCode.PRECONDITION,
        # ── U51's four, appended for the reason every block above gives ────────
        #
        # THE THREE DERIVATION REFUSALS. Both outbound verbs decide their items
        # from a rekordbox collection export, and each of these is a distinct way
        # that decision cannot be made. They are separate slugs rather than one
        # because they send a person to three different places: name a file, name
        # a different playlist, put tracks in the one you named.
        #
        # PRECONDITION rather than USAGE for the first, on the judgement
        # ``export-playlist-unknown`` and ``tag-retag-folder-unknown`` already
        # made: status 2 belongs to the argument parser, and the parser accepted
        # an invocation that simply omitted an optional flag.
        "outbound-export-required": ExitCode.PRECONDITION,
        # Several playlists in the exported tree carry the name that was typed.
        # Its own slug rather than a second use of ``export-playlist-unknown``,
        # because "it is not there" and "there are three of them" are undone by
        # different acts, and a consumer that had to tell them apart would have
        # to branch on the message text.
        "export-playlist-ambiguous": ExitCode.PRECONDITION,
        # The playlist resolved and carries no track this build can write. THE
        # ZERO ITEM RULE, at the only place that enforces it: ``core.jobs``
        # reports a job with no items as SUCCEEDED by design, so a verb that
        # queued this would report a clean success over work it never did.
        "export-playlist-empty": ExitCode.PRECONDITION,
        # No adapter in this build can turn a stored provider credential into an
        # account the outbound engines write through. DISTINCT FROM
        # ``credential-missing``, which is the case doctor already diagnoses and
        # already has a remedy for; this one is the product's own gap and no
        # amount of authenticating fixes it.
        #
        # PRECONDITION rather than INTERNAL, because a build that ships without
        # a provider adapter is a stated limitation rather than a defect a person
        # should be told to report.
        "outbound-account-unbound": ExitCode.PRECONDITION,
        # The frozen export no longer carries a track this job already queued as
        # an item. Its own slug rather than a silent skip: an item that reported
        # done having written nothing is the clean-report-over-unreadable-state
        # cost ``docs/METHOD.md`` names, and the person's remedy is to export the
        # collection again and queue a fresh job rather than to resume this one.
        "outbound-item-absent": ExitCode.PRECONDITION,
        # ── U55's two, appended for the reason every block above gives ─────────
        #
        # The collection no longer holds the row this scan job already queued as
        # an item. The sibling of ``outbound-item-absent`` and a separate slug
        # rather than a reuse, because the two send a person to different places:
        # that one says export the collection again, this one says the library
        # itself has moved since the census was queued. PRECONDITION rather than
        # INTERNAL for the same reason its sibling is: a library that changed
        # under a queued job is a thing that happens, not a defect to report.
        "adopt-item-absent": ExitCode.PRECONDITION,
        # One or more of an approved plan's entries could not be applied. The
        # apply worker's whole-run verdict over ``ApplyReport.failed``, which
        # ``apply_plan`` RETURNS rather than raises. Without a slug of its own the
        # worker would return normally, ``jobs.drive`` would flip the item to
        # done, and the job would reach SUCCEEDED over an adoption that placed
        # nothing.
        "adopt-entries-failed": ExitCode.PRECONDITION,
        # ── U52's three, appended for the reason every block above gives ───────
        #
        # No adapter in this build can turn a stored provider credential into a
        # catalogue the label package reads labels and playlists through.
        # DISTINCT FROM ``credential-missing`` on exactly the judgement
        # ``outbound-account-unbound`` above records: the missing credential is
        # the case doctor already diagnoses and already has a remedy for, and
        # this one is the product's own gap that no amount of authenticating
        # moves. Its own slug rather than a second use of the outbound one,
        # because the two are different capabilities and a person told the
        # streaming account is unbound while asking for a label sweep would go
        # looking at the wrong half of the product.
        #
        # PRECONDITION rather than INTERNAL, because a build that ships without
        # a catalogue adapter is a stated limitation rather than a defect a
        # person should be told to report.
        "label-catalogue-unbound": ExitCode.PRECONDITION,
        # A label walk was asked for with no favourite label registered. THE ZERO
        # ITEM RULE, at the second place that enforces it, beside
        # ``export-playlist-empty``: ``core.jobs`` reports a job with no items
        # as SUCCEEDED by design, so a verb that queued this would report a
        # clean success over work it never did. The remedy is a command that
        # adds a label rather than anything about this installation, so the
        # message names that command and the code stays PRECONDITION.
        "label-registry-empty": ExitCode.PRECONDITION,
        # Some of a label's releases could not be offered, so the item FAILED
        # rather than completing. The distinction it protects is the one the
        # ledger keeps recording: a listing nobody could read and a catalogue
        # with nothing new in it look identical in an item that reports done.
        #
        # The raise site carries ``Remedy.RESUME_JOB`` rather than this table
        # deciding it, because this table maps a slug to a STATUS and the
        # remediation is per raise (``refuse`` defaults it from the code only
        # when the site names neither a remedy nor steps). PRECONDITION rather
        # than UPSTREAM_UNAVAILABLE, because the item is resumable state in this
        # product rather than a verdict about the provider: what failed is
        # already carried underneath as the inner cause.
        "label-sweep-incomplete": ExitCode.PRECONDITION,
        # ── U107's refusals, appended for the reason every block above gives ───
        #
        # The guided label sync's record, which labels were asked about what and
        # every answer given, exists and cannot be read or locked. Its own slug,
        # as the per-label watermark and the sync watermark each have one,
        # because reading it as empty would ask every question again and lose
        # every answer. PRECONDITION: the file is this installation's to repair.
        "label-sync-unusable": ExitCode.PRECONDITION,
        # A question was put at the terminal and nothing could answer it: the
        # stream ended, or nothing usable was typed. The answers given before
        # it are saved and the question is waiting, and the remedy is the
        # scriptable path, ``--next`` and ``--answer``, so PRECONDITION rather
        # than a defect.
        "label-sync-unanswerable": ExitCode.PRECONDITION,
        # ── U109's refusal, appended for the reason every block above gives ────
        #
        # A verb whose queueing half was retired in favour of another verb was
        # asked to queue. ``crate sync labels`` is the first: the guided label
        # sync replaced its sweep, and the verb still resumes a job queued
        # before that, so its name stays and only the queueing is refused. The
        # remedy is the replacing command, named in the steps, so PRECONDITION
        # rather than a usage error the parser could have caught.
        "verb-retired": ExitCode.PRECONDITION,
        # ── U58's refusals, appended for the reason every block above gives ────
        #
        # A restamp was asked for over a library that has never been calibrated.
        # A level is where a track sits among its own library, so with no
        # reference there is no level to stamp, and queueing a job whose every
        # item would fail on the same absence is a report over work nothing
        # could do. PRECONDITION because the remedy is a command, the calibrate
        # verb, rather than anything about this installation.
        "energy-calibration-missing": ExitCode.PRECONDITION,
        # The calibration file exists and cannot be read. A DIFFERENT state from
        # missing, refused under its own name so a truncated file is never
        # folded into "never calibrated" and restamped over, and so the
        # remedy, calibrating again, reaches the person instead of a defect
        # report over a JSON error.
        "energy-calibration-unreadable": ExitCode.PRECONDITION,
        # R-342, the same shape for the vocal cut. The file exists and cannot
        # be read, or carries a threshold that is not a finite number, so the
        # My Tags verb refuses rather than tagging from the default cut as if
        # the library had never been calibrated. A MISSING file still means
        # the default, which is honest; only the unreadable one refuses.
        "vocal-calibration-unreadable": ExitCode.PRECONDITION,
        # U90. ``analyze calibrate --vocal-cut`` was given a cut outside the
        # presence score's range, 0 to 100, or one that is not a finite
        # number. A cut above 100 files nothing under with vox and a NaN cut
        # files everything, so neither is written. PRECONDITION rather than
        # USAGE, because the parser accepted a number.
        "vocal-cut-out-of-range": ExitCode.PRECONDITION,
        # R-372. More than half of the collection's active rows record a path
        # that matches neither the library root nor any rule in
        # library.location_prefix_map, which is the shape rekordbox leaves
        # after a drive is renamed and setup wrote no rule. The My Tags plan
        # used to report ok over such a library with every row skipped, and an
        # apply would have written nothing and reported success. The plan, the
        # apply and doctor's library.paths_resolved all refuse under this one
        # slug. PRECONDITION because the remedy is a configuration act, running
        # setup again with the database present, which offers the rule from
        # rekordbox's own recorded drive names.
        "library-paths-majority-unresolved": ExitCode.PRECONDITION,
        # An analysed track could not be finalized: its tag write returned
        # false or its rename could not claim the target. The item FAILS rather
        # than reporting done, because an analysis whose values never reached
        # the file is the clean-report-over-unwritten-state shape the merge bar
        # names. The audio is untouched in every branch that raises this.
        "analysis-write-failed": ExitCode.PRECONDITION,
        # ── U57's refusals, appended for the reason every block above gives ────
        #
        # Recognition would spend more than it is allowed to: the set needs more
        # calls than the per run cap or the month's ledger has left, or the
        # service itself answered that the account's quota is spent. A POLICY
        # refusal and never a miss, because a miss is a fact about the audio and
        # this is a fact about money, and folding the two is the 565 call batch
        # the source system once read as content misses.
        "intake-recognition-spend-bound": ExitCode.REFUSED_BY_POLICY,
        # The recognition service could not be reached, or answered in a shape
        # this build cannot classify. UPSTREAM_UNAVAILABLE because nothing
        # about the set or the account is decided by it, and the chunk that
        # met it is retried on the next run rather than read as silence.
        "intake-recognition-failed": ExitCode.UPSTREAM_UNAVAILABLE,
        # ── U67's refusal, appended for the reason every block above gives ────
        #
        # ``name apply`` could not read the collection it must consult before a
        # rename, so which files rekordbox references was not established. A
        # REFUSAL and never an empty collection, because reading absence as
        # evidence here renames every imported file and strands its row. The
        # raise site carries the inner cause's remedy rather than this code's
        # default, since ``restore-from-snapshot`` is the wrong act for a
        # database that is merely on an unmounted volume.
        "collection-unreadable": ExitCode.LIBRARY_UNREADABLE,
        # ── U75's refusal, appended for the reason every block above gives ────
        #
        # ``label approved`` could not turn the accepted label releases into a
        # list: no accepted release could be read from the provider, none of the
        # missing tracks carries a provider identifier, or the list's own file
        # could not be written. A REFUSAL and never a no-op, because a no-op
        # here reads exactly like a library that already holds every approved
        # release. PRECONDITION on ``intake-list-unusable``'s argument: the
        # command line was fine and what it points at is the problem.
        "label-list-unusable": ExitCode.PRECONDITION,
        # U80. ``acquire fallback`` needed ``yt-dlp`` for a second source search
        # and the binaries module could not resolve it. The same condition as
        # the reserved ``install-binary``, re-raised in this verb's vocabulary
        # exactly as ``rclone-missing`` and ``encoder-missing`` are, because
        # the reserved binary keys are remedy tokens and not declared reasons.
        # The refusal carries the binaries module's own remedy token, so a
        # broken override still says fix the override rather than install.
        "yt-dlp-missing": ExitCode.PRECONDITION,
        # ── R-500's refusal, appended for the reason U19's block gives ───────
        #
        # ``name apply`` read the collection and met a row recorded under a
        # volume no prefix rule names, whose recorded file is not on this
        # machine either, so which file that row references is not known and a
        # rename could strand it. PRECONDITION, the code the deletion pass
        # answers an unmapped row with, because the library read cleanly and
        # the thing to correct is configuration.
        "collection-row-unmapped": ExitCode.PRECONDITION,
        # ── R-172's answer, appended for the reason U19's block gives ────────
        #
        # ``name apply`` could not carry out every rename its plan promised: two
        # files render to one name, a target was taken, a file left while the
        # gate waited, the filesystem refused the rename, or a title tag could
        # not be written. NOT a refusal, because the renames that could happen
        # DID, and the envelope carries the plan so a person can read which ones.
        # It is the same argument ``analysis-write-failed`` above makes, and it
        # answers with the same code: reporting ok over a rename that never
        # happened is the clean-report-over-unwritten-state shape the merge bar
        # names, and every later sweep meets the same collision, so ok would be
        # the answer for ever. PRECONDITION because the library read cleanly and
        # the thing to correct is a file on disk.
        "rename-incomplete": ExitCode.PRECONDITION,
        # ── U105's refusal, appended for the reason U19's block gives ────────
        #
        # ``crate master --lufs`` was given a target outside the range loudnorm
        # accepts, or one that is not a finite number. Refused at queue time so
        # no job is parked whose only outcome is ffmpeg rejecting its filter.
        # PRECONDITION rather than USAGE for the reason ``vocal-cut-out-of-range``
        # gives: the parser accepted a number.
        "target-lufs-out-of-range": ExitCode.PRECONDITION,
        # ── R-229's refusal, appended for the reason U19's block gives ───────
        #
        # A queued export was confirmed against one remote playlist, to update
        # it or to adopt it from the path the crate used to live under, and by
        # drive time the outbound ledger no longer holds that record where the
        # job expects it. Its own slug rather than ``outbound-ledger-unusable``,
        # because the ledger read cleanly and the remedy is to queue again, not
        # to repair a file. Refused rather than created, because the person
        # confirmed an update and a second remote playlist is the cost the
        # finding is named for. PRECONDITION: a ledger that moved under a queued
        # job is a thing that happens, not a defect to report.
        "outbound-record-moved": ExitCode.PRECONDITION,
        # ── R-235's refusals, appended for the reason U19's block gives ──────
        #
        # The cutover verbs' own, beside the four U20 reserved for the precheck.
        # PRECONDITION for all three, for the reason that block gives: the
        # parser accepted the invocation and the state of the library is what
        # is wrong.
        #
        # The tree named is one this library's taxonomy does not declare, so
        # nothing can say where its membership would be rebuilt from.
        "cutover-tree-undeclared": ExitCode.PRECONDITION,
        # The database holds no folder of the tree's display name directly
        # under the playlist root, or holds more than one. ONE SLUG over both
        # counts, because the act is the same, make it exactly one in
        # rekordbox, and the count travels in the detail. Refused rather than
        # created or chosen: creating one is the silent parallel tree, and
        # choosing one of two anchors every later write to a guess.
        "cutover-root-unresolved": ExitCode.PRECONDITION,
        # A revert was asked for a tree the session log says has taken a
        # native write. The database owns the tree from that write on, and
        # putting it back on the bridge would send the next splice at a tree
        # that must not be imported over.
        "cutover-native-write-taken": ExitCode.PRECONDITION,
        # A cutover was asked to record a tree the registry already records as
        # database native. Refused under the registry lock rather than
        # replaced, because the second record would move the anchor or the day
        # under a tree that may have taken writes under the first.
        "cutover-already-recorded": ExitCode.PRECONDITION,
        # ── R-799's refusal, appended for the reason every block above gives ───
        #
        # The correction of genres an older mapping wrote was approved and a file
        # did not take it: it carried something else by the time the write
        # reached it, or the write failed, or it does not read back as written,
        # or its rewrite could not be recorded. PRECONDITION because the cure is
        # the file's, which is named, and a second run plans what is left.
        # Raised after the other files were written, so the message says how
        # many were and names the verb their rows follow by.
        "tag-remap-unwritten": ExitCode.PRECONDITION,
        # ── U114's refusal, appended for the reason every block above gives ────
        #
        # A suggested genre was approved and a file did not take it: it carried
        # a genre by the time the write reached it, the write failed, or it does
        # not read back. Its row is left without one, so file and row agree.
        # PRECONDITION on ``tag-remap-unwritten``'s argument: the cure is the
        # file's, which is named, and a second run offers what is left. Raised
        # after the other rows were written, so the message names their session.
        "tag-suggest-unwritten": ExitCode.PRECONDITION,
        # ── R-835's two, appended for the reason every block above gives ───────
        #
        # A label's folder of year playlists was planned and the label's
        # catalogue was not read in full: a listing of the label went unread, or
        # a release's tracks could not be read. Refused before the gate, so no
        # plan built from part of a catalogue is shown as the whole of one.
        # PRECONDITION on ``label-sweep-incomplete``'s argument: what failed is
        # carried underneath, and another run reads the label again.
        "label-playlists-incomplete": ExitCode.PRECONDITION,
        # The account holds two root folders named as the label, so which one is
        # the label's is not something a name decides. Its own slug rather than
        # ``export-playlist-ambiguous``, since the remedy is on the account and
        # not in the library. Nothing was written.
        "label-playlists-ambiguous": ExitCode.PRECONDITION,
        # A label's dated new releases playlist was to be made and the label's
        # folder is not on the account, since the folder step before it did
        # not build it (U117). Nothing was written; the folder comes first.
        "label-new-playlists-no-folder": ExitCode.PRECONDITION,
        # ── R-837's one, appended for the same reason ──────────────────────────
        #
        # A set playlist's archive was planned and the account holds two root
        # folders named as the year, so which one is the year's is not
        # something a name decides. PRECONDITION on ``label-playlists-
        # ambiguous``'s argument: the remedy is on the account. Nothing was
        # written.
        "export-set-ambiguous": ExitCode.PRECONDITION,
        # ── R-836's one, appended for the same reason ──────────────────────────
        #
        # A removal from a remote playlist was refused with nothing sent: the
        # outbound ledger does not record the playlist as one the product
        # created, or the playlist's positions could not be read in full, so a
        # removal by position might take off the wrong track. PRECONDITION:
        # the remedy is on the account, by hand, and the same ask refuses the
        # same way.
        "outbound-remove-refused": ExitCode.PRECONDITION,
        # ── R-228's one, appended for the same reason ──────────────────────────
        #
        # The favourites sweep looks up the ColourID whose name is Pink inside a
        # read only open, and the colour table has no live row of that name, so
        # the sweep cannot tell which rows are pink. PRECONDITION: restoring the
        # Pink colour in rekordbox is the person's act, and reporting complete
        # over unread colour is the cost this residual named.
        "favorites-pink-colour-missing": ExitCode.PRECONDITION,
        # ── U123's six, appended for the same reason ───────────────────────────
        #
        # ``label heard`` was given a year or a date that is not one.
        # PRECONDITION rather than USAGE, for ``report-as-of-invalid``'s reason:
        # the parser accepted it because any string is a valid argument.
        "label-heard-invalid": ExitCode.PRECONDITION,
        # No go took a release of the label in that year on that day, so no
        # dated playlist by that name is the product's. Nothing was written.
        "label-heard-no-releases": ExitCode.PRECONDITION,
        # A release named with ``--release`` is not one of the dated playlist's,
        # refused by name before the gate. Nothing was marked heard.
        "label-heard-not-in-playlist": ExitCode.PRECONDITION,
        # The label's folder holds two playlists with the dated name, or the
        # year's name, so which one is meant is not something a name decides.
        # The remedy is on the account, ``label-playlists-ambiguous``'s argument.
        "label-heard-ambiguous": ExitCode.PRECONDITION,
        # The outbound ledger does not record the dated playlist as one the
        # product created, so it is not the verb's to take anything off or
        # remove. The person merges it by hand. Nothing was written.
        "label-heard-not-product-made": ExitCode.PRECONDITION,
        # The dated playlist has tracks to put in the year and the folder holds
        # no year playlist. ``label playlists`` builds it first.
        "label-heard-no-year-playlist": ExitCode.PRECONDITION,
        # ── U130's four, appended for the same reason ──────────────────────────
        #
        # The playlist pairs document could not be read or locked, so what each
        # pair held at its last sync is unknown. Nothing was written.
        "sync-pair-store-unusable": ExitCode.PRECONDITION,
        # ``sync pair`` was given an account playlist that is not marked and no
        # rekordbox playlist to pair it with, or a playlist either side does not
        # hold. Nothing was written.
        "sync-pair-unknown": ExitCode.PRECONDITION,
        # The playlist is not one a pair may hold: the hearts, a label's or a
        # set's playlist, a folder, or a playlist under one of Cratekit's own
        # trees. Nothing was written.
        "sync-pair-out-of-scope": ExitCode.PRECONDITION,
        # One of the two playlists is already paired with another. One playlist
        # stays the same list as one other. Nothing was written.
        "sync-pair-conflict": ExitCode.PRECONDITION,
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


def classified(cause: Cause, exc: BaseException | None) -> Cause:
    """``cause``, corrected if the operating system is what actually refused.

    THE CLASSIFICATION LIVES WHERE A REFUSAL IS CONSTRUCTED, NOT ONLY WHERE ONE
    ESCAPES, and that is the whole point of this function. The previous round put
    the decision in two blankets, the dispatcher and doctor's check runner, on
    the stated property that "a site nobody has converted now comes out right".
    That was true and irrelevant: an AST walk over the package finds nineteen
    ``except OSError`` sites that raise a structured refusal, and eighteen of them
    bypassed both blankets by construction, because a blanket only ever sees what
    nobody caught. Three of the eighteen hard coded the wrong answer, and one of
    those rendered a permission as "no session is recorded with that identifier",
    which reads absence out of a refusal that established nothing at all.

    So the correction happens here, at the constructor every structured refusal
    in the package passes through, and the sites need no edit. A site written
    next year is right by default.

    WHAT IT READS IS THE DECLARED CAUSE CHAIN. Every one of those sites writes
    ``raise refuse(...) from exc``, which is the author's own statement that this
    failure IS that one. Nothing is inferred from the call stack and nothing is
    inferred from ``__context__``, so a handler that catches a refusal, recovers,
    and later raises something unrelated is not re-labelled.

    WHAT IT CHANGES IS THE SLUG AND THE ACT, NEVER THE WORDS. This module is
    FOUNDATION and carries tokens, never sentences (D2); ``cli.render`` owns the
    words for the token this chooses. A site whose act is ALREADY the right one
    is left exactly as it is, so a refusal that knows more than this does keeps
    its better slug.
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
            # Kept because the site's own reading is still worth reading, and
            # dropped from the headline because it was not what happened. It is
            # never branched on; ``detail`` is not read for control flow.
            "declared_reason": cause.reason,
        },
    )


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
        self._declared = cause

    @property
    def cause(self) -> Cause:
        """The cause as the reader gets it, classified against what caused it.

        A PROPERTY RATHER THAN AN ATTRIBUTE FOR ONE REASON: ``raise X from exc``
        sets ``__cause__`` AFTER this object is built, so a value computed in
        ``__init__`` cannot see the thing the site just declared this failure to
        be. Reading it here is the first moment the declaration exists, and every
        consumer, the dispatcher, doctor, the job engine and the tests, reaches
        the cause through this one name.
        """
        return classified(self._declared, self.__cause__)

    @property
    def declared_cause(self) -> Cause:
        """The cause exactly as the raising site wrote it, unclassified.

        For the one caller that needs to see the site's own reading rather than
        the corrected one: the test that proves the correction happened.
        """
        return self._declared


class JobBlocked(CratekitError):
    """A queued job PARKED, leaving its verb through the refusal exit as blocked.

    ``jobs.drive`` returns normally when a worker parks the run, because a park is
    not a failure of any item, and the job it returns is ``blocked``, which is an
    OPEN state. Every shell that reported "the job is not closed badly" through a
    normal envelope therefore reported a parked job as ``ok`` and exited 0 over a
    provider that had just walled the account (R-290). This is the type
    ``jobs.raise_for_state`` raises for that job, and the dispatcher reads it as
    ``Outcome.BLOCKED``.

    WHY A TYPE AND NOT A TEST ON THE CAUSE, which is ``jobs.Parked``'s reason
    again. The cause a parked job carries is the adapter's own, ``auth-failed`` or
    ``provider-blocked`` or a missing program, and the same slugs fail single
    items in jobs that were never parked. Nothing on the cause says "the job is
    parked". The job's state says it, and this type carries that one bit across
    the raise without the dispatcher importing the job engine, which imports the
    dispatcher's package for the envelope.

    IT LIVES HERE RATHER THAN IN ``core.jobs`` for that cycle and no other reason.

    A HOP THAT REBUILDS THE REFUSAL MUST REBUILD IT AS THIS TYPE, and
    :func:`rebuilt` is how. The bit rides the exception and not the cause, so
    ``CratekitError(replace(exc.cause, ...))`` in an ``except`` between the shell
    and the dispatcher silently turns blocked into failed.
    ``tagging.retag_cli.with_reload_step`` did exactly that, found by the review
    of the change that introduced this type, and ``backup`` did it again one
    merge later.
    """


class JobCancelled(CratekitError):
    """A queued job somebody STOPPED, leaving its verb as cancelled and not failed.

    ``Outcome.CANCELLED`` was declared from the start and nothing produced it, so
    a run stopped with a signal read ``failed`` in the outcome word while its exit
    code and its job state both said otherwise. ``jobs.raise_for_state`` raises
    this for a cancelled job and the dispatcher reads it as that outcome.

    A TYPE FOR THE SAME REASON ``JobBlocked`` IS ONE, even though this cause does
    carry a reason of its own: one way of carrying a job's ending to the
    dispatcher, so one rule for every hop in between, which is :func:`rebuilt`.
    """


#: The types whose whole meaning is the type. Order is irrelevant, no job is both.
_CARRIED: tuple[type[CratekitError], ...] = (JobBlocked, JobCancelled)


def rebuilt(error: CratekitError, cause: Cause) -> CratekitError:
    """The refusal ``error`` carrying ``cause`` instead, keeping what its type says.

    THE ONE OWNER OF A REWORDED REFUSAL. A shell that adds a sentence to a refusal
    on its way out builds a new exception around an extended cause, and a new
    ``CratekitError`` drops the one bit :class:`JobBlocked` and
    :class:`JobCancelled` exist to carry. Two shells selected the type by hand and
    one of them forgot; a third hop would have had nothing to remind it.
    ``tests/test_job_outcome.py`` refuses a rebuild spelled any other way.

    ONLY THE CARRIED TYPES SURVIVE, deliberately. Every other subclass takes
    constructor arguments of its own, so ``type(error)(cause)`` is not a thing
    this can promise, and no reader downstream of a reworded refusal branches on
    any of them.
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
    "ACCESS_REASONS",
    "ACCESS_REMEDIES",
    "DATABASE_ACCESS_ERRORNAMES",
    "DATABASE_PATH_ATTRIBUTE",
    "PERMISSION_ERRNOS",
    "READ_ONLY_ERRNOS",
    "REASONS",
    "AccessKind",
    "AccessRefusal",
    "Cause",
    "CratekitError",
    "JobBlocked",
    "JobCancelled",
    "Outcome",
    "Remediation",
    "Scope",
    "UnknownReason",
    "access_refusal",
    "access_remedy",
    "classified",
    "name_the_database",
    "permission_denied",
    "rebuilt",
    "refuse",
    "widest_scope",
]
