"""``crate doctor`` and ``crate status``: the environment, checked before it is spent.

WHAT WAS WRONG. The source system has health checks, and they have exactly one
caller: an HTML template in a local web dashboard. No workflow consults them, so
nothing is ever a precondition to anything. A missing ``ffmpeg`` is discovered
part way through a download, after the identification calls have been paid for.
A dead provider session is discovered as "these tracks are missing". An unset
version pin is discovered by the writer refusing, one step before the write the
user was trying to make. Every one of those is knowable in advance, cheaply, and
none of it is asked.

So R3 is met here in two halves that have to arrive together:

* this module answers a named check and reports a fix per failure;
* ``cli/registry.py`` lets every verb DECLARE the checks it depends on, and
  ``tests/test_cli_contract.py`` asserts that anything which writes declares at
  least one, and that every declared key exists here.

The second half is the one the source system has no shape for at all.

THE CHECK SHAPE IS PORTED, WITH ONE SUBSTITUTION. The source returns
``{key, title, status, detail, fix}`` per check, with three statuses: ok, fail
and info. That shape is good and is kept, because it is already the ancestor of
this product's structured cause: it is the one place in that codebase that pairs
a failure with its exact remedy. The substitution is ``fix``, a sentence, for
``remedy``, a token the CLI renders (D2). A sentence is still allowed in
``detail`` for a fix that is not a command at all, because this IS the CLI layer
and rendering is what it is for.

WHAT IS ADDED, AND WHY EACH ONE.

* **The interpreter, before anything else.** KTD19 bounds the supported Python at
  both ends and the bound is declared once, in packaging metadata. It is READ
  from there rather than repeated here: a second copy is a copy that drifts, and
  the drift would be a check reporting green against a bound nobody enforces.
  It runs first because every other answer in this file is worthless if the
  interpreter is one the vendored tree has never run on.
* **The library volume, with unmounted told apart from moved.** ``core/preflight``
  already distinguishes five outcomes, and the whole reason it does is that a
  guard saying "the volume is wrong" sends the user to unplug a drive that was
  never the problem. Doctor reports which of the five it is, and both findings
  come from ONE probe rather than from two, so the mount and the identity can
  never disagree about the state they are describing.
* **External binaries, resolved before any spend.** Every installable binary is
  probed on every run, derived from ``core/binaries``' own table rather than
  listed here, so a binary added there is checked here the day it is added (P3).
* **The acquisition adapter, against the contract.** R9 says the point of the
  adapter boundary is that the downloader is replaceable. A configured
  alternative that does not satisfy the protocol is a substitution that fails at
  the first download rather than at configuration time, so the members are
  derived from the Protocol itself and checked on the configured class.
* **Credentials, per enabled module.** Presence only, never retrieval: reading a
  value on macOS raises an interactive authorization prompt, which in an
  unattended check means a hang rather than a report.
* **Backup age, per portion.** ``core/backup_facts`` answers per portion because
  the normal state of a library backed up without quitting rekordbox is "files
  current, database stale", and one aggregate number hides exactly that.

WHETHER A CHECK IS REQUIRED IS DERIVED, NOT DECIDED HERE. A check key is
required when some verb declaring it is available under the active profile.
That is what makes "a module enabled without its credential is reported" true by
construction: enabling ``identify`` makes ``intake.identify`` available, that
verb declares ``credential.recognition``, and the check turns from a note into a
failure with no edit to this file. The set is taken over EVERY registry entry
rather than only the landed ones, so the report does not change its mind about
what a profile needs as later units land.

WHY A FAILING DOCTOR DOES NOT DISCARD ITS REPORT. Every other refusal in the
product raises, and the dispatcher turns the cause into an envelope carrying an
empty diagnostic payload. That is right everywhere else and wrong here: the
checks ARE the answer, and a doctor that fails by throwing them away is useless
in exactly the case it exists for. So this module builds its own envelope, with
the full report in ``data`` and a structured cause beside it, and exits
``PRECONDITION``.

Layer note: CLI. It imports downward only, and it is the layer allowed to turn a
remediation token into words.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from importlib import metadata
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

import cratekit
from cratekit import acquire
from cratekit.acquire import adapter as adapter_contract
from cratekit.cli import gates, output, registry, render
from cratekit.cli.output import Envelope
from cratekit.core import (
    active_taxonomy,
    backup_facts,
    binaries,
    config,
    preflight,
    processes,
    profiles,
    rb_writer,
    secrets,
    session,
    taxonomy,
    taxonomy_upgrade,
    tree_registry,
)
from cratekit.core.cause import (
    Cause,
    CratekitError,
    Outcome,
    Remediation,
    Scope,
    access_refusal,
    access_remedy,
)
from cratekit.core.exit_codes import Remedy
from cratekit.deletion import trash
from cratekit.write import metadata_cli

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context


class Status(StrEnum):
    """The three answers a check gives, ported unchanged.

    ``INFO`` is not a weaker ``FAIL``. It means "worth knowing, nothing to do
    now", and the distinction is load-bearing in both directions: a report where
    everything is either green or red has nowhere to put "the backup module is
    off, so no backup has been recorded", and a report that files that under red
    trains people to ignore red.
    """

    OK = "ok"
    FAIL = "fail"
    INFO = "info"


@dataclass(frozen=True, slots=True)
class Finding:
    """One check's answer: what was asked, what was seen, what fixes it.

    ``remedy`` is a token the CLI renders, never a command line (D2). It is None
    when the fix is not expressible as a token at all, and in that case
    ``detail`` states the act, which is legal here and only here: this is the
    layer that renders.

    A FINDING IS THE SECOND CHANNEL A REFUSAL TRAVELS, AND UNTIL THIS IT WAS THE
    UNCLASSIFIED ONE. Round seven put the operating system's own refusal at the
    constructor every ``CratekitError`` passes through, which covers every site
    that RAISES. It does not cover the sites that REPORT: a check, and every
    branch of the wizard, answers by building one of these and returning, so the
    exception is caught and never re-raised and ``cause.classified`` is never
    reached. That gap is not theoretical or evenly spread. It sits exactly on the
    one site in the wizard that WRITES to the library volume, which is where
    EROFS actually arises, and that site hard coded "grant this interpreter
    access" for a volume no grant can change.

    So the classification happens HERE, where a finding is built, for the same
    reason it happens at the refusal constructor: a site written next year is
    right without being edited. Pass ``error`` and the act follows the kind.
    """

    key: str
    title: str
    status: Status
    detail: str
    remedy: Remedy | None = None
    #: The structured cause when the answer IS one, which is a check that refused
    #: under a declared reason rather than a check that observed something. It
    #: carries the reason slug and therefore the RESERVED EXIT CODE, neither of
    #: which a finding has anywhere else to put. ``failure_cause`` reads it, so a
    #: refusal that names its own code leaves the process under that code instead
    #: of under the report's generic one.
    cause: Cause | None = None
    #: The exception this answer is ABOUT, when the answer came from catching one.
    #: Never rendered and never serialized: it is read once, at construction, to
    #: decide whether the operating system is what refused. Excluded from equality
    #: and from the repr because two findings that say the same thing are the same
    #: finding whether or not they carry the same exception object.
    error: BaseException | None = field(default=None, compare=False, repr=False)

    def __post_init__(self) -> None:
        """Correct the act, and give the report a cause, when the answer is a refusal.

        THREE THINGS AND NO MORE. The remedy token follows the KIND the operating
        system actually made, so a read only volume is not sent to Full Disk
        Access. A failing finding with no cause of its own gains one, because a
        refusal that reaches the envelope as "N checks are failing" with a null
        remedy has lost the one field a machine consumer reads. The words are not
        touched: this layer renders them from the token, and a site that writes an
        act into its own sentence is the defect this closes rather than a second
        place to fix it.

        A finding that carries no exception, or one the operating system did not
        refuse, is left exactly as it was built.
        """
        if self.error is None:
            return
        refusal = access_refusal(self.error)
        if refusal is None:
            return
        if self.remedy is not refusal.remedy:
            object.__setattr__(self, "remedy", refusal.remedy)
        if self.cause is None and self.status is Status.FAIL:
            object.__setattr__(
                self,
                "cause",
                Cause(
                    reason=refusal.reason,
                    message=self.detail,
                    remediation=Remediation(remedy=refusal.remedy),
                    scope=Scope.RUN,
                    origin=("cli.doctor",),
                    detail={
                        "path": refusal.path,
                        "access": str(refusal.kind),
                        "check": self.key,
                    },
                ),
            )

    @property
    def failed(self) -> bool:
        return self.status is Status.FAIL

    def to_json(self) -> dict[str, Any]:
        """The ported check shape, with ``fix`` replaced by a remediation token."""
        return {
            "key": self.key,
            "title": self.title,
            "status": str(self.status),
            "detail": self.detail,
            "remedy": str(self.remedy) if self.remedy is not None else None,
        }


@dataclass(frozen=True, slots=True)
class Report:
    """Every check's answer from one run, in the declared order."""

    findings: tuple[Finding, ...] = ()

    @property
    def failures(self) -> tuple[Finding, ...]:
        return tuple(f for f in self.findings if f.failed)

    @property
    def ok(self) -> bool:
        return not self.failures

    def payload(self) -> dict[str, Any]:
        """The ``diagnostic`` surface: the checks, plus counts for a consumer."""
        counted = {
            str(status): sum(1 for f in self.findings if f.status is status)
            for status in Status
        }
        return {
            "checks": [f.to_json() for f in self.findings],
            "summary": {
                "checked": len(self.findings),
                "failing": len(self.failures),
                "counts": counted,
            },
        }


# ---------------------------------------------------------------------------
# The seams
# ---------------------------------------------------------------------------


def _declared_python_bound() -> str | None:
    """The supported interpreter range, read from packaging metadata.

    Read rather than repeated. KTD19's bound lives in ``pyproject.toml`` and is
    already asserted there by ``tests/test_packaging.py``; a constant here would
    be a second copy of one decision, and the copy that drifts is always the one
    nobody is looking at.

    None when the distribution is not installed, which happens when the package
    is imported straight from a checkout, and None again when it is installed
    with no declared bound. Both are reported as their own answer rather than as
    a pass, because a check that cannot fail is not a check. Both legs are driven
    in ``tests/test_doctor.py``; the handler used to carry a "needs no install"
    pragma and nothing exercised either of them.
    """
    try:
        return metadata.metadata(registry.DISTRIBUTION)["Requires-Python"]
    except (metadata.PackageNotFoundError, KeyError):
        return None


def _binding_pin_problem(cfg: config.Config | None) -> str | None:
    """The pyrekordbox pin's complaint, or None when it is satisfied.

    Asked through the guarded writer's OWN assertion rather than by comparing
    version strings here. Two ways of asking one question is how two guards come
    apart, and the writer's is the one that decides whether a write happens.
    """
    try:
        rb_writer.assert_binding_version(cfg)
    except CratekitError as exc:
        return exc.cause.message
    except ImportError as exc:
        return f"the rekordbox binding could not be imported: {exc}"
    return None


def _rclone_remotes(rclone: str) -> Mapping[str, Mapping[str, Any]] | None:
    """Every configured rclone remote and its settings, or None if unreadable.

    ``config dump`` is asked for rather than ``listremotes`` because the question
    is not only whether a remote exists but how it is configured: the residual
    finding "Backup pruning reclaims space only if the remote is configured to"
    records
    that a provider which trashes on delete reclaims nothing when a backup is
    pruned unless its per-remote option says otherwise, and ``listremotes``
    cannot answer that.
    """
    # The executable is an absolute path resolved through ``core/binaries``, never
    # a bare name, and there is no shell: a graphical launcher's PATH does not
    # contain the directories a package manager installs into, which is the whole
    # reason that module exists.
    try:
        finished = subprocess.run(
            [rclone, "config", "dump"],
            capture_output=True,
            text=True,
            timeout=10,
            env=binaries.subprocess_env(),
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if finished.returncode != 0:
        return None
    try:
        parsed = json.loads(finished.stdout or "{}")
    except ValueError:
        return None
    if not isinstance(parsed, dict):
        return None
    return {
        str(name): dict(body)
        for name, body in parsed.items()
        if isinstance(body, Mapping)
    }


def _checkout_root() -> Path | None:
    """The repository root when this package is imported from a checkout.

    ``src/cratekit/__init__.py`` sits two directories below the root, so the
    walk is arithmetic rather than a search. An installed wheel has no ``.git``
    beside it and the answer is None, which is what makes the check asked for by
    the residual finding "The commit hook is off by default on a fresh clone" a
    developer check that says nothing on a user's machine.
    """
    root = Path(cratekit.__file__).resolve().parents[2]
    return root if (root / ".git").exists() else None


def _git_dir(root: Path) -> tuple[Path | None, str | None, Remedy | None]:
    """The git directory that owns ``root``, why it could not be found, and the act that fixes it.

    A worktree's ``.git`` is a FILE naming its own git directory, and that
    directory names the COMMON one, which is where hooks actually live. Looking
    only for ``.git/hooks`` would therefore report every worktree as unhooked
    while the hook was installed and running, which is a guard that fires on
    correct setups, and those get worked around rather than fixed (P7).

    TWO RETURNS RATHER THAN ONE, for the reason ``taxonomy.shipped_templates``
    has two: a bare None was standing for three different things, and the caller
    rendered all three as the mildest of them. A ``.git`` marker this account
    cannot open came back as None and was reported as "carries a .git marker that
    names no git directory", at INFO, with no remedy, so ``crate doctor`` exited
    0 over a repository whose commit scan may or may not be running. That is the
    same split the same check already makes one screen below for the hook FILE,
    left unmade for the MARKER that leads to it.

    None with no sentence is the one honest quiet answer: a marker that parsed
    and named nothing. Anything this could not look at comes back as a sentence.

    THREE RETURNS RATHER THAN TWO, and the third is the ACT. Every sentence here
    is produced by an exception, and only the exception knows whether the file
    was refused by the operating system or was unreadable for some other reason;
    the caller sees a string and cannot tell. It returned report-defect for both,
    so a ``.git`` directory belonging to another account was reported to its
    owner as a Cratekit bug. ``cause.access_remedy`` makes that one decision, the
    same one the dispatcher and the check runner make.
    """
    marker = root / ".git"
    if marker.is_dir():
        return marker, None, None
    try:
        text = marker.read_text().strip()
    except OSError as exc:
        return (
            None,
            f"the .git marker at {marker} could not be read ({exc})",
            access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
        )
    except UnicodeDecodeError as exc:
        # A ``ValueError`` rather than an ``OSError``, so a marker that is
        # present and is not text would otherwise escape as an internal defect.
        # It is never a permission: the bytes were read and then would not
        # decode, so this leg keeps report-defect outright rather than asking.
        return (
            None,
            f"the .git marker at {marker} is not readable text ({exc})",
            Remedy.REPORT_DEFECT,
        )
    if not text.startswith("gitdir:"):
        return None, None, None
    pointed = Path(text.split(":", 1)[1].strip())
    if not pointed.is_absolute():
        pointed = (root / pointed).resolve()
    common = pointed / "commondir"
    if common.is_file():
        try:
            return (pointed / common.read_text().strip()).resolve(), None, None
        except (OSError, UnicodeDecodeError) as exc:
            # BOTH MEMBERS OF THE TUPLE ARE REACHABLE and only one was driven: a
            # commondir that is present and is not text is a ``ValueError``, so
            # dropping that member from this clause killed no test while leaving
            # the whole check open to escaping as an internal defect. The
            # decoding half can only be a damaged checkout, and the permission
            # half is a permission, which is exactly what the chooser decides.
            return (
                None,
                f"the commondir at {common} could not be read ({exc})",
                access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
            )
    return pointed, None, None


def _survey_paths(cfg: config.Config) -> metadata_cli.ResolutionTotals | None:
    """How the collection's rows resolve here, read off a COPY of the database.

    THE LIVE PATH IS NEVER OPENED, not even read only (R-372). The file is
    copied into a private temporary directory by ``rb_writer.disposable_copy``
    and the copy is what the binding opens; the directory is gone before this
    returns. None when there is no database file at the configured path, which
    is a different answer from a database that could not be opened: the second
    raises the open's own refusal and the check reports it as such.

    ``check_app_version=False`` for the reason ``integrity_ok`` gives: a copy is
    a file, and whether an application is installed says nothing about whether
    its rows resolve. The binding pin and the schema pin still apply on the way
    in, because a copy opened by a binding the pin refuses is a reading nobody
    can trust.
    """
    source = rb_writer.live_db_path(cfg)
    if not source.is_file():
        return None
    with rb_writer.read_only_copy(source, cfg=cfg) as db:
        return metadata_cli.resolution_totals(cfg, db)


def _probe_trash(path: Path) -> trash.TrashStatus:
    """Whether a file at ``path`` could be trashed, WITHOUT making it possible.

    ``create=False`` is bound here rather than left to the check, and it is the
    whole reason this seam exists as its own function. :func:`trash.probe`
    creates the per-volume Trash by default, because the desktop does too and a
    volume nobody has trashed anything on legitimately has no directory yet. A
    health check that took that default would make the directory it is asking
    about exist, and would then report a pass it had itself produced, which is
    the same defect as a test that asserts its own fixture.
    """
    return trash.probe(path, create=False)


@dataclass(frozen=True, slots=True)
class Probes:
    """Every seam a check reaches the outside world through.

    Injected as one value rather than as a dozen keyword arguments, so a test
    describes a whole machine and drives the real checks against it. The seams
    are the reason this file has no ``if sys.platform`` in it: adding a platform
    is a different probe, not a different decision.
    """

    now: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    python_version: tuple[int, ...] = field(default_factory=lambda: sys.version_info[:3])
    requires_python: str | None = field(default_factory=_declared_python_bound)
    find_binary: Callable[[str], str | None] = binaries.find
    #: Why a binary was not found, when the reason is an override the user set.
    #: A SECOND seam over the same subject rather than a richer return from the
    #: first, because ``find`` is used by everything that runs a binary and its
    #: contract is a path or nothing. What differs here is the REMEDY, and the
    #: two answers are produced by one rule in the module that owns it.
    binary_override_problem: Callable[[str], str | None] = binaries.override_problem
    identity_provider: preflight.IdentityProvider | None = None
    mount_enumerator: preflight.MountEnumerator | None = None
    process_lister: processes.ProcessLister | None = None
    keychain_available: Callable[[], bool] = secrets.backend_available
    credential_recorded: Callable[[str], bool] = secrets.exists
    #: Whether the opted-in environment fallback is SUPPLYING a credential.
    #: Asked through the module that owns the rule rather than by re-reading the
    #: two variables here, so there is one answer to "may the environment supply
    #: this" rather than one per reader.
    environment_credential: Callable[[str], str | None] = secrets.environment_value
    installed_app_version: Callable[[config.Config | None], str | None] = (
        lambda cfg: rb_writer.read_installed_app_version(cfg=cfg)
    )
    binding_pin_problem: Callable[[config.Config | None], str | None] = _binding_pin_problem
    rclone_remotes: Callable[[str], Mapping[str, Mapping[str, Any]] | None] = _rclone_remotes
    checkout_root: Callable[[], Path | None] = _checkout_root
    #: Whether this account could move a file into the library volume's Trash.
    #: A seam like every other here, so a test describes a volume whose Trash is
    #: missing, unwritable, or on another filesystem without needing three real
    #: volumes to describe them on.
    trash_probe: Callable[[Path], trash.TrashStatus] = _probe_trash
    #: How the collection's active rows resolve on this machine, or None when
    #: there is no database file to read. A seam so a test describes a library
    #: whose rows record a renamed drive without building one, and so the two
    #: synthetic machines can answer it opposite ways. The default copies the
    #: database and opens the copy, and never the live path. It is asked only
    #: once the check has established that rekordbox is closed, through the
    #: process seam above, so the copy it takes is whole.
    path_survey: Callable[[config.Config], metadata_cli.ResolutionTotals | None] = (
        _survey_paths
    )


# ---------------------------------------------------------------------------
# What a check is handed
# ---------------------------------------------------------------------------


def requires_check(key: str, membership: profiles.Membership) -> bool:
    """Whether any verb this profile switches on declares ``key``.

    DERIVED from the registry rather than decided in this module, which is what
    makes "a module enabled without its credential is reported" true without an
    edit here: switching on a module makes its verbs available, and the checks
    they declare become required by arithmetic.

    Taken over EVERY entry rather than only the landed ones. A verb that has not
    shipped cannot spend anything yet, so the narrower reading is defensible, but
    it would make the report change its mind about what a profile needs as later
    units land, and "doctor said this was optional last month" is exactly the
    kind of moving target a precondition must not be.
    """
    return any(
        key in entry.doctor_checks and entry.available_to(membership)
        for entry in registry.entries()
    )


class _Inputs:
    """One run's shared state: the configuration, the seams, and one mount probe.

    The mount probe is memoized deliberately. ``library.mounted`` and
    ``library.identity`` are two findings about ONE observation, and asking twice
    is how two answers about one disk come apart, which is the shape U18 paid for
    when an enumeration and a write resolved the same name differently.
    """

    def __init__(
        self,
        cfg: config.Config | None,
        config_error: config.ConfigError | None,
        probes: Probes,
    ) -> None:
        self.cfg = cfg
        self.config_error = config_error
        self.probes = probes
        self._mount: preflight.MountStatus | None = None
        self.membership = (
            profiles.resolve(cfg.profile.name, dict(cfg.modules.explicit))
            if cfg is not None
            else profiles.resolve("full")
        )

    def mount(self) -> preflight.MountStatus | None:
        if self.cfg is None:
            return None
        if self._mount is None:
            self._mount = preflight.resolve_mount_state(
                self.cfg.library.root,
                self.cfg.library.volume_id,
                identity_provider=self.probes.identity_provider,
                mount_enumerator=self.probes.mount_enumerator,
            )
        return self._mount

    def required(self, key: str) -> bool:
        """Whether some verb this profile switches on depends on ``key``."""
        return requires_check(key, self.membership)


def _unchecked(key: str, title: str) -> Finding:
    """The answer for a check that cannot run because configuration cannot load.

    INFO rather than FAIL, because the failure is already reported once by
    ``config.present`` and reporting it a dozen more times buries it.
    """
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail="not checked: this installation has no usable configuration yet",
    )


# ---------------------------------------------------------------------------
# The checks
# ---------------------------------------------------------------------------


def _parse_release(text: str) -> tuple[int, ...] | None:
    parts = text.strip().split(".")
    if not parts or not all(part.isdigit() for part in parts):
        return None
    return tuple(int(part) for part in parts)


_COMPARATORS: Mapping[str, Callable[[tuple[int, ...], tuple[int, ...]], bool]] = (
    MappingProxyType(
        {
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
        }
    )
)


def satisfies(version: Sequence[int], specifier: str) -> bool | None:
    """Whether ``version`` satisfies a comma separated specifier. None if unknown.

    A deliberately small parser over the operators packaging metadata actually
    uses for an interpreter bound, rather than a dependency on a full version
    library that the slim core does not declare (R5). Anything it does not
    recognise returns None, which the caller reports as "could not be checked"
    rather than as a pass: guessing at a specifier shape is how a bound stops
    being a bound.

    THE VERDICT STARTS AT "NOTHING WAS COMPARED" rather than at True, which is
    the same rule one level down. Initialised True, a specifier that produced no
    clause at all, an empty string or a run of separators, returned True having
    compared nothing, so the answer for "this bound says nothing" was
    indistinguishable from the answer for "this version satisfies it". Only a
    clause that actually ran a comparison may make this anything but None.
    """
    running = tuple(version)
    verdict: bool | None = None
    for clause in specifier.split(","):
        clause = clause.strip()
        if not clause:
            continue
        for symbol in (">=", "<=", "==", "!=", ">", "<"):
            if clause.startswith(symbol):
                bound = _parse_release(clause[len(symbol) :])
                if bound is None:
                    return None
                width = max(len(running), len(bound))
                left = running + (0,) * (width - len(running))
                right = bound + (0,) * (width - len(bound))
                outcome = _COMPARATORS[symbol](left, right)
                verdict = outcome if verdict is None else (verdict and outcome)
                break
        else:
            return None
    return verdict


def _check_interpreter(inputs: _Inputs) -> Finding:
    running = ".".join(str(part) for part in inputs.probes.python_version)
    declared = inputs.probes.requires_python
    key, title = "interpreter.version", "supported Python"
    if not declared:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"running Python {running}; the supported range could not be read "
                f"from this installation's packaging metadata, so nothing was "
                f"asserted about it"
            ),
        )
    verdict = satisfies(inputs.probes.python_version, declared)
    if verdict is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"running Python {running}; the declared range {declared!r} is not "
                f"in a shape this check understands, so nothing was asserted"
            ),
        )
    if verdict:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"Python {running} is inside the supported range {declared}",
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"Python {running} is outside the supported range {declared}. The "
            f"vendored downloader has never run on it, and the failure that "
            f"follows names a dependency rather than the interpreter"
        ),
        # UNSUPPORTED_PLATFORM is reused rather than joined by a near synonym.
        # The exit-code vocabulary's own docstring records three re-authentication
        # tokens it will not collapse because each is already a persisted slug,
        # and the lesson runs the other way too: a new token whose meaning is
        # inside an existing one is a second name for one idea. The running
        # interpreter is part of the platform this install is on, and the token
        # already means "this environment cannot run the operation".
        remedy=Remedy.UNSUPPORTED_PLATFORM,
    )


def _check_config(inputs: _Inputs) -> Finding:
    key, title = "config.present", "configuration"
    if inputs.cfg is not None:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"loaded from {config.config_path()}",
        )
    error = inputs.config_error
    if error is None:  # pragma: no cover - run() sets one whenever cfg is None
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail="no configuration was supplied and none could be loaded",
            remedy=Remedy.RUN_SETUP,
        )
    # ``ConfigError.remedy`` is a declared class attribute on every member of the
    # hierarchy, so it is read directly. A ``getattr`` with a default here would
    # hand back a permissive answer for a field whose whole purpose is that the
    # five failures do NOT share one remediation.
    #
    # AND THEN THE CLASSIFICATION OVERRULES IT WHEN THE OPERATING SYSTEM IS WHAT
    # REFUSED. A config file with mode 0o000 is byte for byte intact, and this
    # check reported "repair or recreate it" over it, which is a report telling
    # its reader to rewrite a file that is perfectly good. The declared remedy
    # stands for every other way a config can be unusable.
    note = render.access_note(error)
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=str(error) + (f". {note}" if note else ""),
        remedy=access_remedy(error, otherwise=Remedy(str(error.remedy))),
    )


#: One sentence per mount outcome, and the whole reason there are six of them.
#: "Not mounted" and "mounted somewhere else" have different fixes, and a report
#: that says only "the volume is wrong" sends the user to unplug a drive that was
#: never the problem.
_MOUNT_DETAIL: Mapping[preflight.MountState, str] = MappingProxyType(
    {
        preflight.MountState.OK: "the recorded volume is mounted at the configured root",
        preflight.MountState.NOT_MOUNTED: (
            "the recorded volume is not mounted anywhere and the configured root "
            "does not exist. Attach it"
        ),
        preflight.MountState.MOUNTED_ELSEWHERE: (
            "the recorded volume IS attached, at a different mount point than the "
            "configured root. Nothing needs plugging in; the configured root is "
            "pointing at the wrong place"
        ),
        preflight.MountState.FOREIGN_VOLUME: (
            "a DIFFERENT volume occupies the configured root. A restored clone "
            "looks healthy from the outside and is the case this check exists for"
        ),
        preflight.MountState.LIBRARY_PATH_MISSING: (
            "the recorded volume is mounted and the configured root is not a "
            "directory on it, so the library was moved within the volume"
        ),
        preflight.MountState.IDENTITY_UNAVAILABLE: (
            "the filesystem at the configured root reports no volume identity, so "
            "a clone mounted in its place could not be told apart from it"
        ),
        preflight.MountState.IDENTITY_NOT_RECORDED: (
            "no volume identity was recorded for this library, so nothing can be "
            "asserted before a destructive write"
        ),
    }
)


def _check_library_mounted(inputs: _Inputs) -> Finding:
    key, title = "library.mounted", "library volume"
    status = inputs.mount()
    if status is None:
        return _unchecked(key, title)
    described = _MOUNT_DETAIL[status.state]
    where = f" (configured root {status.configured_root})"
    if status.state is preflight.MountState.MOUNTED_ELSEWHERE:
        where = f" (configured root {status.configured_root}, found at {status.found_at})"
    if status.state is preflight.MountState.OK:
        return Finding(key=key, title=title, status=Status.OK, detail=described + where)
    if status.state in (
        preflight.MountState.IDENTITY_UNAVAILABLE,
        preflight.MountState.IDENTITY_NOT_RECORDED,
    ):
        # Both are the IDENTITY question and are answered by the next check.
        # Repeating them here as a failure would report one problem twice and
        # attach the wrong fix to one of the copies.
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=f"the identity question is answered by its own check{where}",
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=described + where,
        remedy=Remedy.MOUNT_LIBRARY_VOLUME,
    )


#: What the IDENTITY question answers for each mount outcome, as a TOTAL mapping
#: over the enum rather than as a chain of branches with a fall-through at the end.
#:
#: The fall-through is what makes the branch shape wrong here, and it was wrong
#: for two states before this table existed. ``resolve_mount_state`` populates
#: ``observed_identity`` for NOT_MOUNTED and MOUNTED_ELSEWHERE alike, because it
#: observed SOMETHING at the configured path in both cases, so a final "and
#: otherwise the identity matched" reported a green identity beside a red mount
#: for a volume that is somewhere else entirely, and for one that is not attached
#: at all. Only two states mean the observed identity equalled the recorded one,
#: and they are named here rather than inferred.
_IDENTITY_VERDICT: Mapping[preflight.MountState, tuple[Status, Remedy | None]] = (
    MappingProxyType(
        {
            preflight.MountState.OK: (Status.OK, None),
            # The volume matched; what is missing is a directory ON it, which is
            # the mount check's answer rather than this one's.
            preflight.MountState.LIBRARY_PATH_MISSING: (Status.OK, None),
            preflight.MountState.IDENTITY_NOT_RECORDED: (Status.FAIL, Remedy.RUN_SETUP),
            preflight.MountState.IDENTITY_UNAVAILABLE: (
                Status.FAIL,
                Remedy.UNSUPPORTED_PLATFORM,
            ),
            preflight.MountState.FOREIGN_VOLUME: (Status.FAIL, Remedy.MOUNT_LIBRARY_VOLUME),
            # Both of these are the MOUNT question. The recorded identity is
            # intact and reporting it as a second failure would attach a fix to a
            # problem that is not this one.
            preflight.MountState.NOT_MOUNTED: (Status.INFO, None),
            preflight.MountState.MOUNTED_ELSEWHERE: (Status.INFO, None),
        }
    )
)


def _check_library_identity(inputs: _Inputs) -> Finding:
    key, title = "library.identity", "library volume identity"
    status = inputs.mount()
    if status is None:
        return _unchecked(key, title)
    verdict, remedy = _IDENTITY_VERDICT[status.state]
    if verdict is Status.OK:
        detail = f"the observed identity matches the recorded {status.recorded_identity}"
    elif status.state is preflight.MountState.FOREIGN_VOLUME:
        detail = (
            f"recorded identity {status.recorded_identity}, observed "
            f"{status.observed_identity}: {_MOUNT_DETAIL[status.state]}"
        )
    elif verdict is Status.INFO:
        # The OBSERVED identity is named even here, where it is not the answer.
        # ``--volume-id`` is the only way to replace a recorded identity, by
        # design, and a user whose configuration carries the wrong one has no
        # other way to learn what the right one is: nothing else in the product
        # prints a volume's identity. A refusal that cannot be acted on is a
        # refusal people work around.
        detail = (
            f"nothing at the configured root to compare: {_MOUNT_DETAIL[status.state]}. "
            f"The recorded identity {status.recorded_identity} is intact; the "
            f"filesystem at {status.mount_point} reports "
            f"{status.observed_identity or 'no identity'}"
        )
    else:
        detail = _MOUNT_DETAIL[status.state]
    return Finding(key=key, title=title, status=verdict, detail=detail, remedy=remedy)


def _check_db_containment(inputs: _Inputs) -> Finding:
    """An accepted database outside the library root is reported on EVERY run.

    ``tests/_pending.py`` held this against U27 rather than leaving it in a
    docstring, and the reason is in ``core/config``: refusing at load makes the
    consequence visible at setup, when the user can still move the database, and
    does nothing at all about the install where somebody accepted it eighteen
    months ago and has since forgotten that their snapshots are copies across two
    filesystems rather than one atomic commit. This is the run that keeps saying
    so.
    """
    key, title = "library.db_containment", "database and library on one filesystem"
    if inputs.cfg is None:
        return _unchecked(key, title)
    cfg = inputs.cfg
    if cfg.db_is_inside_library_root():
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                "library.db_path sits under library.root, so a snapshot commits "
                "atomically with a rename"
            ),
        )
    accepted = cfg.library.db_outside_root_acknowledged_on
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"library.db_path ({cfg.library.db_path}) is outside library.root "
            f"({cfg.library.root}), accepted on {accepted}. A snapshot of the "
            f"database and its coupled state therefore spans two filesystems and "
            f"is a copy rather than one atomic commit, so a crash mid-capture can "
            f"leave the two halves describing different moments"
        ),
    )


def _check_trash(inputs: _Inputs) -> Finding:
    """Whether the library volume has a Trash this account can move a file into.

    R35 sends a confirmed deletion to the system Trash and never to an unlink, so
    a volume with no usable Trash is a volume on which the deletion pass refuses.
    Without this check a person meets that refusal in the middle of a deletion,
    after the review, after the confirm gate, with a plan already digested. This
    is the run that says so beforehand.

    IT DOES NOT DEFER TO THE MOUNT CHECKS, unlike the two library-scoped state
    readers below, and the difference is real rather than an oversight. Those two
    read a file this product WROTE under the library root, so an absent volume
    means there is nothing to read and the volume is one problem reported once.
    This asks whether a specific directory on that volume will accept a move, and
    the two questions come apart in the direction that matters: a mounted volume
    with the recorded identity and a read-only mount answers both mount checks
    green and has no usable Trash at all. A foreign volume failing both is not one
    answer twice, it is two preconditions of one destructive act.

    ASKED WITH ``create=False``, through the seam that binds it, so the check
    cannot pass by having run.
    """
    key, title = "library.trash", "system Trash on the library volume"
    if inputs.cfg is None:
        return _unchecked(key, title)
    root = inputs.cfg.library.root
    try:
        status = inputs.probes.trash_probe(root)
    except OSError as exc:
        # GATED ON ``required`` LIKE EVERY NEIGHBOURING CHECK. An unanswerable
        # question is still not a pass, but on a profile where nothing trashes a
        # file it is not a red either, and a report that paints red for a
        # capability nothing uses is how people learn to ignore red.
        needed = inputs.required(key)
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL if needed else Status.INFO,
            detail=(
                f"whether {root} has a usable Trash could not be established "
                f"({exc}), so whether a confirmed deletion would land in the "
                f"Trash or refuse is unknown"
            ),
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT) if needed else None,
            error=exc if needed else None,
        )
    if status.usable:
        where = status.layout.files if status.layout is not None else root
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"{where} exists on the same filesystem as {root} and accepts a move",
        )
    if status.absent:
        # NOT A FAILURE, and getting this wrong made the check worse than absent.
        # ``trash.probe`` creates the per-volume Trash on first use because the
        # desktop does, and the deletion pass takes that default. Doctor asks with
        # ``create=False`` so its answer cannot be produced by its own asking,
        # which means a volume nobody has trashed anything on answers "not a
        # directory" here and works perfectly when a deletion actually runs.
        # Driven: probe(create=False) says unusable and probe(create=True) says
        # usable on the same fresh volume. Reporting that as red tells a person
        # deletion will refuse when it will not, which is the one thing a
        # precondition must never do.
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                f"{root} has no Trash directory yet, which is the state of a "
                f"volume nobody has deleted from; the deletion pass creates it on "
                f"first use exactly as the desktop does"
            ),
        )
    if not inputs.required(key):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{status.problem}, and no verb this profile switches on moves a "
                f"file to the Trash, so nothing depends on it today"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"{status.problem}. A confirmed deletion moves the file to the "
            f"volume's own Trash and never unlinks it, so this profile switches "
            f"on a verb that would refuse partway through a deletion rather than "
            f"before one"
        ),
        # NOT ``RUN_DOCTOR``, which is what ``trash.assert_usable`` refuses with:
        # that token sends a person here, and here answering with it again is a
        # loop. The three shapes this probe reports are a directory that is not
        # there, one this account cannot write, and one on another filesystem,
        # and the first two are a path to grant access to. The third is named in
        # the sentence, because no token in the vocabulary means "your Trash is
        # on the wrong disk" and inventing one for a case a person meets once
        # would be a token nobody ever reads.
        remedy=Remedy.GRANT_PATH_ACCESS,
    )


def _library_state_unreadable(inputs: _Inputs, what: str) -> str | None:
    """Why library-scoped state may not be read here, or None when it may.

    Both callers below report on a file that sits under the library root by
    construction, and for both of them "the file is not there" and "the disk the
    file lives on is not there" produce the same bytes: none. The rule for
    telling those apart is ``core/preflight``'s, because that is the module that
    owns what a mount outcome means.

    The wizard asks a NEIGHBOURING question before it writes one of these files,
    and the two are deliberately separate functions over separate tables: a
    matching identity with an absent root is nothing to read here and exactly the
    right moment to write there.

    The caller reports it as INFO, for the reason the mount check gives when it
    defers to the identity check: the volume is one problem and it is reported
    once, by the checks that own it. Reporting a missing template here would also
    attach the wrong remedy, since running setup against an absent volume is the
    write this unit had to be stopped from making.
    """
    status = inputs.mount()
    if status is None or preflight.library_state_is_readable(status):
        return None
    return (
        f"not asserted: {what} lives on the library volume, and this run could "
        f"not establish that the volume is there ({status.state.value}), so "
        f"nothing at the configured root was read. The volume is reported by its "
        f"own checks"
    )


def _volume_clause(inputs: _Inputs) -> str:
    """What an OK detail may CLAIM about the disk it just read from.

    Derived from ``_IDENTITY_VERDICT``, the same total mapping the identity check
    itself answers with, so the two can never disagree about whether a comparison
    happened. Only the two outcomes that mean "observed equals recorded" earn the
    strong sentence.

    It exists because the OK details asserted the strong one unconditionally. A
    machine with no identity adapter reaches these checks through the leg of the
    reachability rule whose entire meaning is that the identity could not be
    ASKED, and it then read "on the recorded library volume" on the same report
    as ``library.identity`` failing with "the filesystem at the configured root
    reports no volume identity". That is a positive claim about a disk nobody
    looked at, which is the class of defect this whole pass exists to remove, so
    it may not be reintroduced by the pass itself.
    """
    status = inputs.mount()
    if status is not None and _IDENTITY_VERDICT[status.state][0] is Status.OK:
        return "on the recorded library volume"
    return (
        "at the configured root, on a volume whose identity could not be "
        "compared here, so which disk it is was not established"
    )


def _check_taxonomy(inputs: _Inputs) -> Finding:
    key, title = "taxonomy.active", "active taxonomy template"
    if inputs.cfg is None:
        return _unchecked(key, title)
    unreadable = _library_state_unreadable(inputs, "the active template")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    shipped, unlistable = taxonomy.shipped_templates()
    named = inputs.cfg.taxonomy.template
    if unlistable is not None:
        # "NOT PRESENT" AND "COULD NOT LOOK" ARE DIFFERENT ANSWERS, and the empty
        # tuple was serving as both. The walk swallows an unreadable packaged
        # directory so that building the command tree cannot die on a partial
        # install, which is right; what was wrong is reading the resulting
        # emptiness as a fact about the shipped set. A user with a damaged
        # install was told their configuration named a template nothing ships and
        # sent to re-run setup, which cannot repair packaged data.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{unlistable}. Whether a template named {named!r} ships was "
                f"therefore not established, and neither was the active copy "
                f"beside the database. This is a damaged or partial install "
                f"rather than a configuration error, so re-running setup would "
                f"not repair it"
            ),
            remedy=Remedy.REPORT_DEFECT,
        )
    if named not in shipped:
        # ASSERTED rather than assumed, and it was assumed. The OK branch below
        # claimed the configured template "is active" while comparing nothing to
        # that name, so a configuration naming a template that does not ship read
        # green: nothing rejected the name, and the file beside the database is
        # whatever was copied there once, under whatever name.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"taxonomy.template names {named!r} and no template ships under "
                f"that name; shipped: {', '.join(shipped)}. A re-run of setup "
                f"replaces a recorded name the shipped set does not contain"
            ),
            remedy=Remedy.RUN_SETUP,
        )
    path = config.state_path("taxonomy_active", inputs.cfg)
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, NotADirectoryError):
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"no active taxonomy template at {path}. S6 makes the library "
                f"self-describing by copying the chosen template beside the "
                f"database, and routing has no declared tree without it"
            ),
            remedy=Remedy.RUN_SETUP,
        )
    except (OSError, UnicodeDecodeError) as exc:
        # UnicodeDecodeError is a ValueError, not an OSError, so a template that
        # is present and is not text would otherwise escape this check as an
        # internal defect rather than as the unusable template it is.
        #
        # AND IT IS A SEPARATE ANSWER FROM "IT IS NOT THERE". One handler over
        # both said "no active taxonomy template at X" for a file that is at X
        # and cannot be read by this account, and then attached run-setup, which
        # takes the branch below that leaves an existing file alone. The user
        # re-runs setup forever.
        #
        # AND IT DOES NOT CLAIM THE FILE EXISTS. It said "exists and could not be
        # read", and the exception that lands here does not establish existence:
        # a permission error raised by an untraversable PARENT arrives on this
        # branch, and nothing under such a parent has been observed at all.
        # Asserting a file is at a path nobody could look at is the same defect,
        # one line further on, as the one this handler was split out to fix.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the active taxonomy template at {path} could not be read "
                f"({exc}), so whether the library declares a usable tree was not "
                f"established. Whether the file is even there is unknown too: a "
                f"directory on the way to it that this account cannot open fails "
                f"the same way. Setup leaves an existing copy alone, so this is a "
                f"permission or a corruption to repair rather than an answer to "
                f"give again"
            ),
            # The sentence already names a permission as one of the two shapes,
            # and the remedy has to name the same two. A corruption is a defect
            # to report and a permission is one to grant, so the token follows
            # the classification rather than assuming the worse of the user.
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
        )
    try:
        declared = taxonomy.load_taxonomy(text)
    except taxonomy.TaxonomyError as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=f"the active taxonomy template at {path} is not usable: {exc}",
            remedy=Remedy.RUN_SETUP,
        )
    status, origin = _origin_verdict(inputs.cfg, text, named)
    return Finding(
        key=key,
        title=title,
        status=status,
        detail=(
            f"an active template at {path}, {_volume_clause(inputs)}, parses and "
            f"declares {len(declared.buckets)} buckets; taxonomy.template names "
            f"the shipped {named!r}; {origin}"
        ),
    )


def _check_taxonomy_schema(inputs: _Inputs) -> Finding:
    """The active copy's schema version against the shipped one, and each entry it lacks (U132).

    THE CHECK THE LIVE LIBRARY NEEDED. Its copy stated ``schema_version = 2``
    with no genre Favorites class long after one shipped, and every Favorites
    step refused or skipped over it while doctor read the copy as parsing and
    said nothing more. This names both versions, every shipped class and bucket
    the copy lacks, what ``crate taxonomy upgrade`` would add, and the hand edit
    each entry it holds needs.

    INFO, NEVER FAIL. A copy without a bucket the shipped template has may be a
    person's decision, and a red line over it trains people to ignore red. A
    copy that does not load or cannot be read is ``taxonomy.active``'s failure
    and is not reported a second time here.

    THE SHIPPED TEXT STAYS OUT OF THIS MODULE. The planner reads it and answers
    in names and sentences, so doctor still holds no parsed shipped taxonomy.
    """
    key, title = "taxonomy.schema", "active taxonomy against the shipped schema"
    if inputs.cfg is None:
        return _unchecked(key, title)
    unreadable = _library_state_unreadable(inputs, "the active template")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    try:
        _, found = taxonomy_upgrade.planned(inputs.cfg)
    except CratekitError as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"not compared: {exc.cause.message}. taxonomy.active reports the copy "
                f"itself"
            ),
        )
    except ValueError as exc:
        # The shipped text could not be cut, which is packaged data this
        # repository wrote, so it is a defect to report and not the person's.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the shipped {inputs.cfg.taxonomy.template!r} template could not be "
                f"compared with the copy ({exc})"
            ),
            remedy=Remedy.REPORT_DEFECT,
        )
    if not found.behind:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                f"the active copy states schema_version {found.from_version}, as the "
                f"shipped {found.template!r} template does, and declares every class and "
                f"bucket it ships"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=f"{taxonomy_upgrade.gap(found)}. {taxonomy_upgrade.remedy(found)}",
    )


def _origin_verdict(cfg: config.Config, active_text: str, named: str) -> tuple[Status, str]:
    """Whether the active copy fell behind the shipped template, or was edited (R-689).

    Three digests answer it: the one setup RECORDED beside the copy, the copy as
    it is now, and the shipped text as it ships now. A copy that still matches
    the record is the copy setup made, so if the shipped text has moved on the
    library is missing what it gained, and that is the INFO this exists for. A
    copy that differs from the record is the person's, and what the shipped text
    did since is not this check's to raise. With no record, which is every
    library set up before the record existed, the two cannot be told apart and
    the detail says so rather than guessing either way. A record naming a
    template other than the configured one is the other INFO, since the copy
    and the configuration then disagree about which tree this library means.

    IT REPORTS AND NEVER WRITES. The copy is the person's declaration, and a
    section the shipped template gained is theirs to take or leave. It reads
    the shipped template only as a fingerprint the definer computes, never as
    text, so it cannot come to route by it.
    """
    origin_path = config.state_path("taxonomy_origin", cfg)
    record: taxonomy.Origin | None
    try:
        record_text = origin_path.read_text(encoding="utf-8")
    except (FileNotFoundError, NotADirectoryError):
        record = None
    except (OSError, UnicodeDecodeError) as exc:
        return Status.INFO, (
            f"the record of which shipped text the copy was made from, at "
            f"{origin_path}, could not be read ({exc}), so a copy that fell "
            f"behind the shipped template cannot be told from one a person edited"
        )
    else:
        try:
            record = taxonomy.parse_origin_record(record_text)
        except ValueError as exc:
            return Status.INFO, (
                f"the record of which shipped text the copy was made from, at "
                f"{origin_path}, is not usable ({exc}), so a copy that fell "
                f"behind the shipped template cannot be told from one a person "
                f"edited"
            )
    if record is not None and record.template != named:
        # The record carries the one fact that shows the configured name and
        # the copy disagree, and the check above only asserted the name ships.
        # Every verb reads the copy, so the library declares the recorded
        # template's tree whatever the configuration says, and a re-run of
        # setup leaves the copy alone rather than replacing it.
        return Status.INFO, (
            f"the copy was made from the shipped {record.template!r} and "
            f"taxonomy.template now names {named!r}; every verb reads the copy, "
            f"so this library declares the tree of {record.template!r}, and a "
            f"re-run of setup leaves an existing copy alone"
        )
    active = taxonomy.template_fingerprint(active_text)
    # ``named`` is in the shipped set, the check above refused otherwise, so the
    # only way not to read it is packaged data that lists and does not open,
    # which is the damaged install setup reports the same way.
    try:
        current = taxonomy.shipped_template_fingerprint(named)
    except (OSError, UnicodeDecodeError) as exc:
        return Status.INFO, (
            f"the packaged text of {named!r} could not be read ({exc}), so the "
            f"copy was compared with nothing and whether it fell behind the "
            f"shipped template was not established. This is a damaged or partial "
            f"install"
        )
    if record is None:
        if active.digest == current.digest:
            return Status.OK, (
                f"nothing records which shipped text the copy was made from, "
                f"and it matches the shipped {named!r} as it ships now"
            )
        return Status.OK, (
            f"nothing records which shipped text the copy was made from, and it "
            f"differs from the shipped {named!r} as it ships now, so whether it "
            f"was edited or fell behind the shipped template cannot be told. "
            f"Setup records the origin only for a copy it makes"
        )
    if active.digest != record.digest:
        return Status.OK, f"edited since setup copied the shipped {record.template!r}"
    if current.digest == record.digest:
        return Status.OK, (
            f"unedited since setup copied the shipped {record.template!r}, which "
            f"has not changed since"
        )
    gained = sorted(current.sections - active.sections)
    dropped = sorted(active.sections - current.sections)
    changes = []
    if gained:
        changes.append(
            f"it now declares {', '.join(f'[{name}]' for name in gained)}, which "
            f"the copy does not"
        )
    if dropped:
        changes.append(
            f"it no longer declares {', '.join(f'[{name}]' for name in dropped)}, "
            f"which the copy still does"
        )
    change = "; ".join(changes) or "the difference is inside sections both declare"
    return Status.INFO, (
        f"the copy is the one setup made from the shipped {record.template!r}, "
        f"unedited, and that template has changed since: {change}. Every verb "
        f"reads the copy, so nothing the shipped template changed applies to this "
        f"library until it is copied in, by hand or, for a class or a bucket, by "
        f"{taxonomy_upgrade.VERB}; doctor does not rewrite the copy"
    )


def _check_rekordbox_closed(inputs: _Inputs) -> Finding:
    key, title = "rekordbox.closed", "rekordbox not running"
    running = processes.rekordbox_processes_running(lister=inputs.probes.process_lister)
    if not running:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail="neither the application nor its background agent is running",
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"{', '.join(running)} running. The agent is the one that surprises "
            f"people: it holds the database and mutates it through Cloud Library "
            f"Sync with the window closed"
        ),
        remedy=Remedy.QUIT_REKORDBOX,
    )


def _check_rekordbox_pins(inputs: _Inputs) -> Finding:
    key, title = "rekordbox.pins", "rekordbox version pins"
    if inputs.cfg is None:
        return _unchecked(key, title)
    cfg = inputs.cfg
    binding = inputs.probes.binding_pin_problem(cfg)
    if binding is not None:
        return Finding(
            key=key, title=title, status=Status.FAIL, detail=binding,
            remedy=Remedy.REVALIDATE_PINS,
        )
    pinned = cfg.rekordbox.pinned_app_version
    installed = inputs.probes.installed_app_version(cfg)
    if not pinned:
        # S2. An unset pin refuses every database write, and it is never adopted
        # from whatever happens to be installed: a pin the software copies from
        # its own machine refuses nothing, forever.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"no rekordbox application version is pinned, so every database "
                f"write refuses. The installed version is "
                f"{installed or 'not locatable from here'}, and recording a pin is "
                f"a deliberate act rather than a value this reads off the machine"
            ),
            remedy=Remedy.RECORD_REKORDBOX_PIN,
        )
    if installed is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"pinned at {pinned}; the installed application could not be "
                f"located, so the schema pin is the only one still asserting"
            ),
        )
    if installed != pinned:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"installed rekordbox {installed} does not match the recorded pin "
                f"{pinned}, so database writes are frozen by design rather than "
                f"broken"
            ),
            remedy=Remedy.REVALIDATE_PINS,
        )
    validated = cfg.rekordbox.validated_on
    if not validated:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"pinned at {pinned} and matching, with no recorded date on which "
                f"the pin was confirmed against a real write. Without that date a "
                f"pin is a number somebody typed"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.OK,
        detail=f"pinned at {pinned}, matching, confirmed against a write on {validated}",
    )


def _check_paths_resolved(inputs: _Inputs) -> Finding:
    """Whether the collection's recorded paths can be read from this machine.

    THE CHECK R-372 ASKED FOR, AND THE FIRST ONE TO READ THE PREFIX MAP. The
    first real My Tags plan reported ok with count 0 over 9937 active rows it
    had skipped, because rekordbox records nearly every row under the drive's
    old name and setup had written no rule, and this report was green beside
    it. Doctor now reads the same ratio the plan refuses on, off a disposable
    copy of the database, so a person is told before the plan rather than by
    reading a zero.

    THE ORDER OF THE QUESTIONS IS WHAT KEEPS THE COPY HONEST. Whether rekordbox
    is running is asked FIRST, through the same seam ``rekordbox.closed``
    answers with, because a copy taken under the live application is torn the
    way a backup taken under it is: it opens, and is missing whatever was mid
    write, and a torn copy's open failure would then be forwarded as a refusal
    naming a snapshot restore against a library that is fine. Whether the
    volume is there is asked SECOND, before anything at the configured path is
    read, for the reason
    the taxonomy check asks it: a leftover mount point holding a stale database
    is the first of the three states ``core/preflight`` exists to tell apart,
    and a survey over it is a report on a disk nobody is using. It is not gated
    on ``required`` the way the trash check is, and the gate was written and
    removed: the routing passes, the rebuild and the convergence report resolve
    recorded paths and are core verbs on every profile, so the question is
    required everywhere and a branch for "nobody asks it" was a branch nothing
    could reach.

    THEN THE ANSWERS, AND "COULD NOT LOOK" IS NOT ONE OF THE GOOD ONES. No file
    at the configured path is INFO, because a fresh library has nothing to
    resolve yet. A copy that would not open is FAIL carrying the open's own
    cause and remedy, since an unanswered question is not a pass. A majority of
    rows under no rule is FAIL under the same slug the plan refuses with, so
    doctor exits under that code and the two surfaces cannot disagree. A
    minority is INFO with the count, which is the state the sitting was left in
    after the rule was typed by hand, 167 of 9937, and a person should see the
    number rather than an unqualified green.
    """
    key, title = "library.paths_resolved", "recorded paths resolve on this machine"
    if inputs.cfg is None:
        return _unchecked(key, title)
    cfg = inputs.cfg
    running = processes.rekordbox_processes_running(lister=inputs.probes.process_lister)
    if running:
        # FAIL and not INFO, with the act that unblocks it. The condition is
        # reported by rekordbox.closed as well, and this is not that report
        # repeated: it says this question is unanswered until that one is
        # fixed, which is a different sentence from "the application is open".
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"whether the collection's rows resolve could not be established: "
                f"{', '.join(running)} running, and a copy of the database taken "
                f"under a live application is incomplete, so none was taken. The "
                f"answer is unknown rather than good"
            ),
            remedy=Remedy.QUIT_REKORDBOX,
        )
    unreadable = _library_state_unreadable(inputs, "the database")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    try:
        totals = inputs.probes.path_survey(cfg)
    except CratekitError as exc:
        cause = exc.cause
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"whether the collection's rows resolve could not be established: "
                f"a copy of the database could not be opened, {cause.message}. The "
                f"answer is unknown rather than good, and the live file was not "
                f"touched"
            ),
            remedy=cause.remediation.remedy,
            cause=cause,
        )
    if totals is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"no database file at {cfg.library.db_path}, so no row was read and "
                f"nothing was asserted about how the collection resolves"
            ),
        )
    rules = len(cfg.library.location_prefix_map)
    if totals.majority_unmapped:
        cause = metadata_cli.majority_unmapped_cause(cfg, totals)
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{cause.message}. The My Tags plan reads ok over such a library "
                f"with every one of those rows skipped, and an apply writes nothing"
            ),
            remedy=cause.remediation.remedy,
            cause=cause,
        )
    if totals.unmapped:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{totals.unmapped} of {totals.active} active rows record a path "
                f"under no library.location_prefix_map rule, a minority, with "
                f"{rules} rule{'s' if rules != 1 else ''} recorded; those rows are "
                f"skipped by every pass that resolves paths, and {totals.unresolved} "
                f"rows in all resolve to no file here"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.OK,
        detail=(
            f"every one of {totals.active} active rows records a path under the "
            f"library root or a recorded rule ({rules} rule"
            f"{'s' if rules != 1 else ''}), read off a disposable copy of the "
            f"database; {totals.unresolved} resolve to no file here"
        ),
    )


def _check_keychain(inputs: _Inputs) -> Finding:
    key, title = "keychain.reachable", "OS keychain"
    if inputs.probes.keychain_available():
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail="a keychain backend that can store a credential is available",
        )
    # THE FALLBACK THIS CHECK'S OWN MESSAGE NAMES IS ASKED ABOUT, rather than
    # named and then ignored. A headless machine that opted in by name and set
    # every variable is the documented shape for exactly this case, and it was
    # painted red: the credential checks read green through the same fallback
    # while this one failed the whole run on PRECONDITION. A check that refuses a
    # configuration the product documents is one people learn to work around.
    needed = _required_credentials(inputs)
    supplied = [name for name in needed if inputs.probes.environment_credential(name)]
    if needed and len(supplied) == len(needed):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"no keychain backend resolves here and every credential this "
                f"profile needs is supplied by the opted-in environment fallback "
                f"({', '.join(needed)}). Nothing can be RECORDED until a backend "
                f"is installed, which is what {secrets.ENV_ALLOW_ENV_CREDENTIALS} "
                f"is for"
            ),
        )
    outstanding = [name for name in needed if name not in supplied]
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            "no keychain backend resolves on this machine. Credentials are never "
            "written to a plain file, so this installation cannot hold one until a "
            "backend is installed or the environment fallback is opted into by name"
            + (
                f". The fallback is supplying {', '.join(supplied)} and not "
                f"{', '.join(outstanding)}"
                if supplied
                else ""
            )
        ),
        remedy=Remedy.INSTALL_KEYCHAIN_BACKEND,
    )


#: Which stored credentials each declared check key is asking about. Declared
#: rather than derived from the names, because the correspondence is a decision:
#: the recognition service needs TWO values and a workflow with one of them is
#: not half working, it is not working. ``tests/test_doctor.py`` asserts every
#: member of ``secrets.Credential`` appears here exactly once, so a credential
#: added there cannot be silently unchecked (P3, P4).
CREDENTIALS_BY_CHECK: Mapping[str, tuple[secrets.Credential, ...]] = MappingProxyType(
    {
        "credential.provider": (secrets.Credential.PROVIDER_SESSION,),
        "credential.recognition": (
            secrets.Credential.IDENTIFY_KEY,
            secrets.Credential.IDENTIFY_SIGNING_KEY,
        ),
    }
)

#: The remediation for each credential group. The provider session is obtained by
#: authorising, the recognition keys are copied from an account page, and telling
#: a user to do one when they need the other is the collapse ``core/secrets``
#: names three separate failure types to avoid.
_CREDENTIAL_REMEDY: Mapping[str, Remedy] = MappingProxyType(
    {
        "credential.provider": Remedy.AUTHENTICATE_PROVIDER,
        "credential.recognition": Remedy.SET_CREDENTIAL,
    }
)


def _required_credentials(inputs: _Inputs) -> tuple[str, ...]:
    """Every credential name some verb this profile switches on will spend.

    Derived from the same table and the same registry question the per-credential
    checks use, so the keychain check and the credential checks cannot disagree
    about what this installation actually needs.
    """
    return tuple(
        str(name)
        for check, names in sorted(CREDENTIALS_BY_CHECK.items())
        if inputs.required(check)
        for name in names
    )


def _check_credential(key: str, inputs: _Inputs) -> Finding:
    names = CREDENTIALS_BY_CHECK[key]
    title = f"credentials for {key.split('.', 1)[1]}"
    missing = [str(n) for n in names if not inputs.probes.credential_recorded(str(n))]
    if not missing:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"recorded: {', '.join(str(n) for n in names)}",
        )
    if not inputs.required(key):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"not recorded ({', '.join(missing)}), and no verb this profile "
                f"switches on needs it"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"not recorded ({', '.join(missing)}), and this profile switches on a "
            f"verb that spends it. Recording it before the run is the difference "
            f"between a refusal now and a refusal after the first paid call"
        ),
        remedy=_CREDENTIAL_REMEDY[key],
    )


#: Every external binary this product shells out to, DERIVED from the binaries
#: module's own tables rather than listed. A binary added there is probed here on
#: the day it is added, which is the failure the source system's hand-written
#: list has already had once (P3).
BINARY_NAMES: tuple[str, ...] = (
    *binaries.INSTALLABLE_BINARIES,
    *sorted(binaries.PLATFORM_BINARIES),
)


def _check_binary(key: str, inputs: _Inputs) -> Finding:
    name = key.split(".", 1)[1]
    title = f"external binary {name}"
    found = inputs.probes.find_binary(name)
    if found:
        return Finding(key=key, title=title, status=Status.OK, detail=found)
    override = binaries.env_var(name)
    broken = inputs.probes.binary_override_problem(name)
    if broken is not None:
        # A SET override that does not point at an executable is its own failure
        # and has its own remediation, which existed in the vocabulary and in the
        # rendered advice and was emitted by nothing. Reported as "not found on
        # PATH, install it", a user installs a binary they already have and the
        # override keeps winning over it, because ``find`` deliberately does not
        # fall through to PATH once an override is set.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL if inputs.required(key) else Status.INFO,
            detail=(
                f"{override} is set to {broken!r}, which is not an executable "
                f"file. Nothing falls through to PATH while it is set, because "
                f"silently running a different binary than the one you named is "
                f"worse than finding none"
            ),
            remedy=Remedy.FIX_BINARY_OVERRIDE,
        )
    if name in binaries.PLATFORM_BINARIES:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL if inputs.required(key) else Status.INFO,
            detail=(
                f"{name} is provided by the operating system and was not found. "
                f"There is nothing to install; its absence means this is not the "
                f"platform it ships with"
            ),
            remedy=Remedy.UNSUPPORTED_PLATFORM if inputs.required(key) else None,
        )
    hint = binaries.install_hint(name)
    source = (
        f"{hint.manager} package {', '.join(hint.packages)}"
        if hint is not None
        else "no packaged source is known for this platform"
    )
    if not inputs.required(key):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"not found, and no verb this profile switches on declares it "
                f"({source}; override with {override})"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"not found on PATH or in the launcher fallback directories, and this "
            f"profile switches on a verb that shells out to it ({source}; override "
            f"with {override})"
        ),
        remedy=(
            Remedy.INSTALL_BINARY if hint is not None
            else Remedy.INSTALL_BINARY_SOURCE_UNKNOWN
        ),
    )


def contract_members(protocol: type = adapter_contract.AcquisitionAdapter) -> tuple[str, ...]:
    """The public members the acquisition protocol declares, derived from it.

    Derived rather than listed, because a listed copy is a copy that stops
    covering the protocol the moment somebody adds a member to it, and the whole
    value of the check is that a substitute adapter is measured against the WHOLE
    contract rather than against the part somebody remembered (P4).
    """
    annotated = set(protocol.__annotations__)
    methods = {
        name
        for name, value in vars(protocol).items()
        if not name.startswith("_") and callable(value)
    }
    return tuple(sorted(annotated | methods))


def _check_adapter(inputs: _Inputs) -> Finding:
    key, title = "adapter.contract", "acquisition adapter"
    if inputs.cfg is None:
        return _unchecked(key, title)
    name = inputs.cfg.acquisition.adapter
    try:
        loaded = acquire.load(name)
    except adapter_contract.UnknownAdapter as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=str(exc),
            remedy=Remedy.CHOOSE_KNOWN_ADAPTER,
        )
    except ImportError as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the adapter {name!r} is registered and its tool is not installed "
                f"here: {exc}. R9's whole point is that acquisition survives one "
                f"tool breaking, and the alternatives are "
                f"{', '.join(acquire.alternatives_to(name)) or 'none'}"
            ),
            remedy=Remedy.INSTALL_ADAPTER,
        )
    required = contract_members()
    absent = [member for member in required if not hasattr(loaded, member)]
    if absent:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the adapter {name!r} resolves to {loaded.__qualname__}, which does "
                f"not satisfy the acquisition contract: missing {', '.join(absent)}"
            ),
            remedy=Remedy.SWITCH_ADAPTER,
        )
    # Read only after the membership check above proved it is there, rather than
    # through a defaulting accessor: a default here would invent an empty name
    # for a class that declares none and then report the mismatch as the class's
    # fault instead of as the missing member it is.
    declared = loaded.name
    if declared != name:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"acquisition.adapter names {name!r} and the resolved class calls "
                f"itself {declared!r}. The name is the identifier configuration "
                f"records and every result is reported under, so the two "
                f"disagreeing means a run reports work against an adapter nobody "
                f"selected"
            ),
            remedy=Remedy.SWITCH_ADAPTER,
        )
    return Finding(
        key=key,
        title=title,
        status=Status.OK,
        detail=(
            f"{name!r} resolves to {loaded.__qualname__} and satisfies the "
            f"contract ({', '.join(required)})"
        ),
    )


def _whole_days(age: timedelta | None) -> int:
    """An age in whole days, never below zero.

    A record from a clock a few minutes ahead is inside the tolerance and is a
    known age, and ``timedelta.days`` of minus ten minutes is minus one.
    """
    return max(age.days, 0) if age is not None else 0


def _unreadable_facts(key: str, title: str, exc) -> Finding:
    """The one finding every check reading the backup fact file gives for that."""
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=str(exc),
        remedy=Remedy(str(exc.remedy)),
    )


def _check_backup_portion(key: str, inputs: _Inputs) -> Finding:
    portion = backup_facts.PORTIONS[key.split(".")[-1]]
    title = f"backup age, {portion} portion"
    if inputs.cfg is None:
        return _unchecked(key, title)
    try:
        ages = backup_facts.ages(inputs.cfg, now=inputs.probes.now)
    except backup_facts.BackupFactsUnreadable as exc:
        return _unreadable_facts(key, title, exc)
    answer = next(entry for entry in ages if entry.portion is portion)
    if answer.state is backup_facts.AgeState.NEVER_RECORDED:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                "no completion has been recorded for this portion here, which is "
                "the state of every library before a backup has run once"
            ),
        )
    if answer.state is backup_facts.AgeState.RECORDED_IN_THE_FUTURE:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the recorded completion at {answer.completed_at} is ahead of now. "
                f"Any check comparing an age against a maximum reads a negative age "
                f"as the freshest possible value, so this record silently satisfies "
                f"every freshness test it was written to fail"
            ),
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )
    days = _whole_days(answer.age)
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=f"last completed {days} days ago, to {answer.destination or 'an unnamed destination'}",
    )


#: How old the last full comparison may be before the check says to run one.
#: Not a failure at any age: both modes compare every file, so what ages is
#: only the proof that the recursive listing and the folder by folder one agree.
FULL_COMPARISON_DUE_DAYS = 30


def _check_full_comparison(inputs: _Inputs) -> Finding:
    """How long ago the file mirror last compared folder by folder (R-757).

    INFO AT EVERY AGE, and FAIL only where the record itself cannot be trusted.
    The ordinary backup compares every file through one recursive listing, and
    this is the date of the last run that did not depend on that listing, so a
    fast mode cannot go unchecked for ever without the report saying so.
    """
    key, title = "backup.full_comparison", "backup, last full comparison"
    if inputs.cfg is None:
        return _unchecked(key, title)
    try:
        answer = backup_facts.full_comparison_age(inputs.cfg, now=inputs.probes.now)
    except backup_facts.BackupFactsUnreadable as exc:
        return _unreadable_facts(key, title, exc)
    run_one = "Run one with: crate backup run --full"
    if answer.state is backup_facts.AgeState.NEVER_RECORDED:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                "no backup here has compared the library with the remote folder "
                "by folder. Every backup compares every file, through one "
                f"recursive listing of the remote. {run_one}"
            ),
        )
    if answer.state is backup_facts.AgeState.RECORDED_IN_THE_FUTURE:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the recorded full comparison at {answer.completed_at} is ahead "
                f"of now, so its age cannot be stated"
            ),
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )
    days = _whole_days(answer.age)
    due = f". {run_one}" if days >= FULL_COMPARISON_DUE_DAYS else ""
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"last ran {days} days ago, against "
            f"{answer.destination or 'an unnamed destination'}{due}"
        ),
    )


@dataclass(frozen=True, slots=True)
class TrashPolicy:
    """What one rclone remote type does with a deleted object, as a declaration.

    ``option`` is the per-remote setting that turns trashing off, and ``disabled``
    is the value of that setting which MEANS off. Both are needed because the
    providers disagree about the sense: Drive's ``use_trash`` has to be false,
    while OneDrive's ``hard_delete`` has to be true. One shared "is it false" test
    read the two backwards, which would have
    reported a correctly configured remote as trashing and a trashing one as
    correct.

    ``option`` is None for a provider that trashes and offers no per-remote escape
    at all. That is a real state and it is not a failure: there is nothing for the
    user to set, so reporting red every run would train them past it (P7). It is a
    note naming the consequence.

    ``applies_when`` is the remote setting that names an account kind and the
    values of it on which ``option`` does anything at all. OneDrive's
    ``hard_delete`` is honoured on business drives and document libraries and
    ignored on a personal drive, so reading the option alone reported a personal
    remote green on a setting that changes nothing. Outside those values, an
    unset setting included, the answer is a note: nothing can be set there.
    """

    option: str | None
    disabled: str = "false"
    applies_when: tuple[str, frozenset[str]] | None = None


#: What each rclone remote type does on delete. The residual finding "Backup pruning
#: reclaims space only if the remote is configured to": pruning a backup archive on a
#: provider that trashes reclaims nothing for the retention period unless the
#: remote's own option says otherwise, and the source system solved it by passing
#: a Drive flag from inside the prune, which is the one-provider assumption this
#: port removed.
#:
#: DECLARED IN BOTH DIRECTIONS, and that is the fix. The table used to hold one
#: row and the check reported OK for every type that was not in it, so every
#: provider with a recycle bin that nobody had gotten around to adding, OneDrive,
#: Box, pCloud and Dropbox among them, read green over the exact condition this
#: check exists to find. A type with no row here is now "not asserted" rather than
#: "fine", and the only way to reach OK is a row that says so.
_REMOTE_TRASH_POLICY: Mapping[str, TrashPolicy] = MappingProxyType(
    {
        "drive": TrashPolicy(option="use_trash", disabled="false"),
        "onedrive": TrashPolicy(
            option="hard_delete",
            disabled="true",
            applies_when=("drive_type", frozenset({"business", "documentLibrary"})),
        ),
        # All three keep deleted files and none exposes a per-remote way out.
        # Dropbox's row used to name a permanent_delete option, and rclone's
        # Dropbox backend has no such option, measured against rclone 1.74.3's
        # own backend help: every run failed with a fix nothing could apply.
        "dropbox": TrashPolicy(option=None),
        "box": TrashPolicy(option=None),
        "pcloud": TrashPolicy(option=None),
    }
)

#: Remote types where a delete is an unlink and a prune therefore reclaims space
#: immediately. Named rather than assumed, because "assumed" is what the single
#: row above was doing for everything else.
_NON_TRASHING_REMOTE_TYPES: frozenset[str] = frozenset({"local", "sftp", "ftp"})


def _check_backup_remote(inputs: _Inputs) -> Finding:
    key, title = "backup.remote", "backup remote"
    if inputs.cfg is None:
        return _unchecked(key, title)
    if "backup" not in inputs.membership.modules:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail="the backup module is off in this profile",
        )
    remote = inputs.cfg.backup.remote
    if not remote:
        # INFO rather than FAIL, deliberately. The full preset switches the backup
        # module on for everybody, so failing here would paint a correctly
        # configured install red on the day it is set up and keep it red for
        # anybody who never intends to back up remotely. A guard that fires on
        # correct setups is one people learn to ignore, and then it protects
        # nothing (P7). The backup verb refuses on its own missing destination,
        # which is where that refusal belongs.
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                "the backup module is on and no backup destination is recorded, "
                "so the backup verb has nowhere to write. Run setup and take the "
                "offer, or pass --backup-dest, --backup-archive-root and "
                "--backup-db-dest-root, each an rclone remote:path"
            ),
        )
    rclone = inputs.probes.find_binary("rclone")
    if rclone is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"backup.remote is {remote!r}; rclone is not installed here, so its "
                f"configuration could not be read. The missing binary is reported "
                f"under its own check"
            ),
        )
    remotes = inputs.probes.rclone_remotes(rclone)
    if remotes is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=f"backup.remote is {remote!r}; rclone's configuration could not be read",
        )
    # ``remote:path`` is rclone's own spelling and is what a user writes for an
    # archive under a remote. Trimming the trailing colon alone left the path
    # attached, so a perfectly configured destination looked up as a remote name
    # nobody had, and the check reported the one FAIL in this function against a
    # correct configuration.
    named = remote.split(":", 1)[0]
    settings = remotes.get(named)
    if settings is None:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            # "The backup remote" rather than "backup.remote names", because
            # the value may be derived from the destinations and absent from
            # the file, and a person sent to a key they cannot find stops
            # looking.
            detail=(
                f"the backup remote is {remote!r}, from backup.remote or derived "
                f"from the destinations, and rclone has no remote called "
                f"{named!r}; it knows {', '.join(sorted(remotes)) or 'none'}"
            ),
            # NOT run-setup. The wizard asks for the three destinations and
            # derives the remote from them (R-345), and it keeps every value it
            # finds recorded, so a re-run would hand this same name back
            # unchanged. The remote is named in the configuration file and
            # created in rclone's own configuration, and this token is the one
            # that says so.
            remedy=Remedy.FIX_CONFIG_VALUES,
        )
    kind = str(settings.get("type", ""))
    if kind in _NON_TRASHING_REMOTE_TYPES:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                f"{named!r} is a {kind} remote, where a delete is a delete, so a "
                f"prune reclaims its space immediately"
            ),
        )
    policy = _REMOTE_TRASH_POLICY.get(kind)
    if policy is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{named!r} is a {kind or 'typeless'} remote, which this check has "
                f"no row for, so nothing was asserted about whether a pruned "
                f"archive keeps counting against the quota. Providers that trash "
                f"on delete are named one by one here rather than assumed absent"
            ),
        )
    if policy.option is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{named!r} is a {kind} remote. That provider moves a deleted "
                f"object to a recycle bin and offers no per-remote option to stop "
                f"it, so a pruned archive keeps counting against the quota until "
                f"the provider's own retention expires. There is nothing to set; "
                f"emptying it is done at the provider"
            ),
        )
    if policy.applies_when is not None:
        setting, honoured = policy.applies_when
        value = str(settings.get(setting, ""))
        if value not in honoured:
            return Finding(
                key=key,
                title=title,
                status=Status.INFO,
                detail=(
                    f"{named!r} is a {kind} remote whose {setting} is "
                    f"{value or 'unset'}. rclone honours {policy.option} only where "
                    f"{setting} is {' or '.join(sorted(honoured))}, so on this remote "
                    f"it cannot stop a pruned archive going to the recycle bin, and "
                    f"whatever it is set to says nothing about the quota. Emptying it "
                    f"is done at the provider"
                ),
            )
    if str(settings.get(policy.option, "")).lower() == policy.disabled:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                f"{named!r} is a {kind} remote with {policy.option} set to "
                f"{policy.disabled}, so a prune reclaims space"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"{named!r} is a {kind} remote and its {policy.option} option is not "
            f"{policy.disabled}. A pruned archive folder goes to the provider's "
            f"trash and keeps counting against the quota for the retention period, "
            f"which is the whole point of pruning. Set {policy.option} to "
            f"{policy.disabled} on that remote in rclone's own configuration"
        ),
    )


def _log_directory_unreadable(cfg: config.Config) -> Path | None:
    """The session log directory when it exists and cannot be listed, else None.

    The mount question answers "is the disk there". This answers the other half,
    which no mount state can: a directory that IS on the right volume and that
    this account cannot open. ``scan_log`` swallows that into the same empty pair
    it returns for a library that has simply never opened a session, and the
    difference between those two is the difference between "nothing to resolve"
    and "cannot tell".
    """
    directory = session.log_dir(cfg)
    try:
        if not directory.exists():
            return None
    except OSError:
        # ``Path.exists`` re-raises anything that is not "it is not there", so a
        # state directory this account cannot TRAVERSE arrived here as an
        # exception rather than as False. Doctor lost the whole report to it.
        # Unreadable is the honest answer and it is the one the caller renders.
        return directory
    try:
        # Listed rather than stat-ed. A directory with no execute bit stats fine
        # and cannot be read, which is exactly the state that produced an empty
        # scan and a green report.
        next(iter(directory.iterdir()), None)
    except OSError:
        return directory
    return None


def _check_unresolved_session(inputs: _Inputs) -> Finding:
    key, title = "session.unresolved", "destructive sessions"
    if inputs.cfg is None:
        return _unchecked(key, title)
    unreadable = _library_state_unreadable(inputs, "the session log")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    unreadable_directory = _log_directory_unreadable(inputs.cfg)
    if unreadable_directory is not None:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the session log directory {unreadable_directory} exists and "
                f"cannot be listed by this account, so whether a destructive "
                f"session is still open is unknown. An unreadable log is not an "
                f"empty one, and the next destructive run refuses on what is in it"
            ),
            remedy=Remedy.REPORT_DEFECT,
        )
    parsed, unreadable = session.scan_log(inputs.cfg)
    if unreadable:
        # A gate reading its own state through a tolerant reader fails OPEN, which
        # is why the scan returns both halves. Doctor reports the half the gate
        # will refuse on rather than the half it can read.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{len(unreadable)} session record(s) in the log cannot be read: "
                f"{', '.join(path.name for path in unreadable)}. An unreadable "
                f"record is a record that has not been cleared, so the next "
                f"destructive session refuses on it"
            ),
            remedy=Remedy.REPORT_DEFECT,
        )
    open_records = [record for record in parsed if not record.terminal]
    if not open_records:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                f"the session log {_volume_clause(inputs)} was read: "
                f"{len(parsed)} recorded session(s), none of them open"
            ),
        )
    condemning = [
        record
        for record in open_records
        if record.state is session.SessionState.COMMITTED_UNVERIFIED
    ]
    if condemning:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"session {condemning[0].session_id} committed and its read-back "
                f"disagreed, so what the library holds cannot be vouched for and "
                f"every further destructive write refuses until it is resolved"
            ),
            remedy=Remedy.RESTORE_FROM_SNAPSHOT,
        )
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"{len(open_records)} session(s) still open: "
            f"{', '.join(f'{r.session_id} ({_open_state(r)})' for r in open_records)}"
        ),
    )


def _open_state(record: session.SessionRecord) -> str:
    """An open run's state, as a person should read it.

    A landing whose import was proven stays ``open`` until a tree cuts over,
    because the placement it still owes needs one (R-501). Listed bare, a
    library with fifty finished landings reads as fifty runs in progress.
    """
    if session.owes_only_deferred_routing(record):
        return f"{record.state}, import proven, placement waits for a cutover"
    # A RUN WHOSE HOLDER IS GONE WILL NEVER END ITSELF (R-598), and listed bare it
    # reads as a run in progress. This layer names verbs, so it names the one.
    if session.orphaned(record):
        return f"{record.state}, its process is gone, crate session release abandons it"
    return str(record.state)


#: The configuration file pre-commit reads when the hook names none.
_HOOK_CONFIG_DEFAULT = ".pre-commit-config.yaml"

#: What a generated pre-commit hook actually contains: a call into the tool's own
#: hook implementation, bound to the stage it was installed for.
_HOOK_DISPATCH = "hook-impl"

#: Every git hook type pre-commit can install. Copied from its own constants
#: rather than imported, because this check runs in checkouts that never
#: installed the dev extra, and it must not need the tool in order to report that
#: the tool's hooks are missing.
_HOOK_TYPES = frozenset(
    {
        "commit-msg",
        "post-checkout",
        "post-commit",
        "post-merge",
        "post-rewrite",
        "pre-commit",
        "pre-merge-commit",
        "pre-push",
        "pre-rebase",
        "prepare-commit-msg",
    }
)

#: The legacy stage spellings pre-commit still accepts, and the hook each one names.
_STAGE_ALIASES = {"commit": "pre-commit", "merge-commit": "pre-merge-commit", "push": "pre-push"}


def _config_path(named: str, root: Path) -> Path:
    """Where a configuration name from a hook's dispatch line points.

    Relative names are resolved by pre-commit against the repository it runs in,
    which is this one.
    """
    configured = Path(named)
    return configured if configured.is_absolute() else root / configured


def _configured_hook_types(
    config_file: Path,
) -> tuple[tuple[str, ...], str | None, Remedy | None]:
    """Every hook type ``config_file`` needs installed, pre-commit first, or why that is unknown.

    THE WIDENED HALF OF THE RESIDUAL FINDING "The commit hook is off by default on
    a fresh clone". ``pre-commit install`` on its own writes the pre-commit hook
    and nothing else, and this repository also runs a check on the commit-msg
    stage. A clone with a perfectly good pre-commit hook and no commit-msg hook
    reported green here while that check never ran. So the answer is read from
    the configuration rather than assumed to be the one type the check happened
    to know when it was written.

    A type is needed when the configuration NAMES it: a hook's ``stages``, the
    ``default_stages``, or ``default_install_hook_types``. A hook that names no
    stage runs on every stage that is installed, which makes no further type
    necessary, so pre-commit itself is the floor and is always first.

    UNKNOWN IS NOT ONE. A configuration this cannot read, parse, or understand
    comes back as a sentence rather than as ``("pre-commit",)``, because that
    tuple is the answer that reports green over exactly the gap this exists to
    close.
    """
    try:
        text = config_file.read_text()
    except (OSError, UnicodeDecodeError) as exc:
        return (
            (),
            f"{config_file} could not be read ({exc})",
            access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
        )
    try:
        # The dev extra's, through pre-commit. Not a runtime dependency, and not
        # worth making one for a check that only speaks in a checkout.
        import yaml
    except ImportError:
        return (
            (),
            (
                f"PyYAML is not importable from this interpreter, so the hook types "
                f"{config_file.name} configures could not be read. Install the dev "
                f"extra, `pip install -e '.[dev]'`"
            ),
            None,
        )
    try:
        document = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return (), f"{config_file} is not valid YAML ({exc})", None
    if not isinstance(document, dict):
        return (), f"{config_file} is not a pre-commit configuration", None

    named: list[object] = []
    named.extend(document.get("default_install_hook_types") or [])
    named.extend(document.get("default_stages") or [])
    for repo in document.get("repos") or []:
        hooks = repo.get("hooks") if isinstance(repo, dict) else None
        for hook in hooks or []:
            if isinstance(hook, dict):
                named.extend(hook.get("stages") or [])

    types = ["pre-commit"]
    for stage in named:
        hook_type = _STAGE_ALIASES.get(stage, stage) if isinstance(stage, str) else None
        if hook_type == "manual":  # run by hand, never by git
            continue
        if hook_type not in _HOOK_TYPES:
            return (
                (),
                f"{config_file} names a stage pre-commit installs no hook for, {stage!r}",
                None,
            )
        if hook_type not in types:
            types.append(hook_type)
    return tuple(types), None, None


def _install_command(types: Sequence[str], config_name: str = _HOOK_CONFIG_DEFAULT) -> str:
    """The one line that installs every hook type in ``types`` against ``config_name``.

    The configuration is named whenever it is not the default, because the
    installer rewrites every hook it writes to dispatch to whichever one it was
    given. Without it that is the default, which may not exist, so following the
    advice would break a pre-commit hook that was working.
    """
    words = ["pre-commit", "install"]
    if config_name != _HOOK_CONFIG_DEFAULT:
        words += ["--config", config_name]
    for kind in types:
        words += ["--hook-type", kind]
    # ``shlex.join``, as pre-commit builds its own argument vector, so a name
    # needing quotes comes out quoted.
    return shlex.join(words)


def _remedy_command(root: Path) -> str:
    """The install line for this checkout, naming every type its configuration needs.

    ``pre-commit install`` writes its hooks against the default configuration,
    so that is the one read. When it cannot be read the line falls back to the
    floor, and the check reports the configuration itself once that hook exists.
    """
    types, problem, _remedy = _configured_hook_types(root / _HOOK_CONFIG_DEFAULT)
    return _install_command(types if problem is None else ("pre-commit",))


def _hook_config_name(body: str) -> str:
    """Which configuration file the hook's dispatch line names.

    READ WITH ``shlex``, BECAUSE IT WAS WRITTEN WITH ``shlex``. ``pre_commit``
    builds that argument vector with ``shlex.join``, which quotes any path
    carrying a character a shell would treat specially, so a regular expression
    matching non-space characters stops at the space in ``my config.yaml`` and
    reports that a file called ``my`` does not exist. That is a refusal aimed at
    a developer whose hook is installed and working, and doctor exits 30 over it.

    Absence is not a defect: pre-commit's own default is what it means, and the
    default is named here once so the answer this returns is always a real
    filename rather than sometimes None.
    """
    for line in body.splitlines():
        if _HOOK_DISPATCH not in line:
            continue
        try:
            tokens = shlex.split(line)
        except ValueError:  # an unbalanced quote: not a line we can read
            continue
        for index, token in enumerate(tokens):
            if token.startswith("--config="):
                return token[len("--config=") :]
            if token == "--config" and index + 1 < len(tokens):
                return tokens[index + 1]
    return _HOOK_CONFIG_DEFAULT


def _hook_dispatch_problem(body: str, root: Path, hook_type: str = "pre-commit") -> str | None:
    """Why this hook does not run THIS repository's pre-commit for ``hook_type``, or None.

    Substring-matching ``pre-commit`` was the whole test before, and it is
    satisfied by a hook whose entire content is the comment ``# pre-commit``, and
    by a hook that dispatches to a completely different repository's
    configuration. Both report green while nothing scans the commit, which is the
    state the residual finding "The commit hook is off by default on a fresh
    clone" exists to end, and the check's own message already CLAIMED it
    refused when the hook "does not dispatch to this repository's pre-commit
    configuration". This makes the claim and the code agree.

    Three positive requirements, each killing one of those:

    * the body calls pre-commit's own hook implementation;
    * it was installed for ``hook_type``'s STAGE, not for some other hook type
      that happens to have been copied into this file;
    * the configuration it names resolves INSIDE this checkout and exists. A hook
      pointing at another repository's configuration runs that repository's
      checks over these commits.
    """
    stage = f"--hook-type={hook_type}"
    if _HOOK_DISPATCH not in body:
        return f"it never invokes pre-commit's {_HOOK_DISPATCH}"
    if stage not in body:
        return f"it does not carry {stage}"
    named = _hook_config_name(body)
    try:
        resolved = _config_path(named, root).resolve()
    except (OSError, RuntimeError) as exc:
        # ``RuntimeError`` IS THE ONE THAT HAPPENS. ``Path.resolve`` does not
        # raise for an absent path, so an ``OSError`` alone was a handler for a
        # shape a hook file cannot produce, while the shape it CAN produce, a
        # symlink loop on the way to the named configuration, arrives as
        # ``RuntimeError("Symlink loop from ...")`` and escaped this handler
        # entirely to be reported as a check that did not complete.
        return f"the configuration it names, {named}, cannot be resolved ({exc})"
    if root.resolve() not in resolved.parents and resolved != root.resolve():
        return f"the configuration it names, {named}, is outside {root}"
    if not resolved.is_file():
        return f"the configuration it names, {named}, does not exist"
    return None


def _check_commit_hook(inputs: _Inputs) -> Finding:
    """The residual finding "The commit hook is off by default on a fresh clone".

    A personal path or a credential that reaches a commit is already in the
    history, and removing it is a rewrite every clone has to follow. The scan is
    wired as a pre-commit hook, and the hook only exists once somebody has run
    the installer; on a machine where the tool was not on PATH, a planted literal
    committed cleanly with no hook and no warning.

    It says nothing at all on a user's machine, because an installed wheel has no
    checkout beside it. A check that reported on the absence of a developer tool
    to somebody who is not a developer would be noise, and noise is what teaches
    people to stop reading the report.
    """
    key, title = "repo.commit_hook", "repository commit hook"
    root = inputs.probes.checkout_root()
    if root is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail="this is an installed package rather than a checkout; nothing to hook",
        )
    git_dir, unreadable, unreadable_remedy = _git_dir(root)
    if unreadable is not None:
        # AN UNREADABLE MARKER IS NOT A MARKER THAT NAMES NOTHING. Both arrived
        # here as None and both read as the second, at INFO with no remedy, so
        # the whole report stayed green and doctor exited 0 over a repository
        # whose commit scan was never established to run. Git reads the marker
        # with different privileges than this process may have, so whether the
        # hook fires is genuinely unknown, and unknown is a FAIL here for the
        # reason ``answer`` gives: INFO means "nothing to do now", and nothing
        # established that.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{unreadable}, so which git directory owns {root} was not "
                f"established and neither was whether a pre-commit hook is "
                f"installed in it. Git resolves the same marker on every commit "
                f"regardless of what this check can open, so the answer is "
                f"unknown rather than no"
            ),
            remedy=unreadable_remedy,
        )
    if git_dir is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=f"{root} carries a .git marker that names no git directory",
        )
    hook = git_dir / "hooks" / "pre-commit"
    try:
        body = hook.read_text()
    except (FileNotFoundError, NotADirectoryError):
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"no pre-commit hook at {hook}, so the repository scan does not run "
                f"before a commit and a personal path or a credential reaches the "
                f"history unchallenged. Run `{_remedy_command(root)}` in {root}"
            ),
        )
    except (OSError, UnicodeDecodeError) as exc:
        # A HOOK THAT IS THERE AND CANNOT BE READ IS NOT A MISSING HOOK. One
        # handler over both reported "no pre-commit hook at X" for a file sitting
        # at X, and sent the user to `pre-commit install`, which rewrites a file
        # it may not be able to open either. Git will still try to RUN it, so
        # whether the scan happens is genuinely unknown here, which is the answer.
        #
        # It no longer says the hook EXISTS, for the reason the taxonomy check
        # gives one screen up: an untraversable hooks directory raises the same
        # permission error, and nothing beneath it has been observed.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the pre-commit hook at {hook} could not be read ({exc}), so "
                f"whether the repository scan runs before a commit was not "
                f"established, and neither was whether the file is there: a "
                f"directory on the way to it that this account cannot open fails "
                f"the same way. Git runs the file regardless of whether this "
                f"check can open it, so the answer is unknown rather than no"
            ),
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
        )
    problem = _hook_dispatch_problem(body, root)
    if problem is not None:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the hook at {hook} does not dispatch to this repository's "
                f"pre-commit configuration ({problem}), so the scan it is supposed "
                f"to run does not run. Run `{_remedy_command(root)}` in {root}"
            ),
        )

    # EVERY OTHER TYPE THE CONFIGURATION NEEDS, read from the configuration this
    # hook actually dispatches to. A pre-commit hook alone was reported green
    # while the commit-msg stage, and the closing check on it, never ran.
    config_name = _hook_config_name(body)
    config_file = _config_path(config_name, root)
    types, unknown, unknown_remedy = _configured_hook_types(config_file)
    if unknown is not None:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{hook} runs the pre-commit stage, and which other hook types "
                f"{config_name} needs was not established: {unknown}. A stage it "
                f"configures with no hook installed does not run, so the answer is "
                f"unknown rather than no"
            ),
            remedy=unknown_remedy,
        )
    command = _install_command(types, config_name)
    absent: list[str] = []
    for hook_type in types[1:]:
        other = git_dir / "hooks" / hook_type
        try:
            other_body = other.read_text()
        except (FileNotFoundError, NotADirectoryError):
            absent.append(f"no {hook_type} hook at {other}")
            continue
        except (OSError, UnicodeDecodeError) as exc:
            # The same split the pre-commit hook makes above: a file this account
            # cannot open is not a file that is missing, and git runs it anyway.
            return Finding(
                key=key,
                title=title,
                status=Status.FAIL,
                detail=(
                    f"the {hook_type} hook at {other} could not be read ({exc}), so "
                    f"whether the checks {config_name} configures for that stage run "
                    f"was not established. Git runs the file regardless of whether "
                    f"this check can open it, so the answer is unknown rather than no"
                ),
                remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
            )
        other_problem = _hook_dispatch_problem(other_body, root, hook_type)
        if other_problem is not None:
            absent.append(
                f"the hook at {other} does not dispatch to this repository's "
                f"pre-commit configuration ({other_problem})"
            )
            continue
        # THE SAME configuration, not merely one inside the checkout. The types
        # were read from the pre-commit hook's configuration, so a hook for one of
        # them that dispatches anywhere else runs a stage that configuration does
        # not describe, and the check it configures there never runs. Both paths
        # already resolved once, in the dispatch checks above.
        other_name = _hook_config_name(other_body)
        if _config_path(other_name, root).resolve() != config_file.resolve():
            absent.append(f"the hook at {other} dispatches to {other_name}, not {config_name}")
    if absent:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{hook} runs the pre-commit stage, and {config_name} also configures "
                f"{', '.join(types[1:])}, where {'; '.join(absent)}. The checks on "
                f"those stages do not run before the commit they judge. Run "
                f"`{command}` in {root}"
            ),
        )
    others = (
        f", and so does the hook for every other stage it configures, {', '.join(types[1:])}"
        if len(types) > 1
        else ""
    )
    return Finding(
        key=key,
        title=title,
        status=Status.OK,
        detail=(
            f"{hook} invokes pre-commit's hook implementation for the pre-commit "
            f"stage against this repository's own {config_name}{others}"
        ),
    )


def _declared_trees(
    cfg: config.Config,
) -> tuple[tuple[str, ...], frozenset[str], str | None]:
    """The trees this taxonomy declares, the ones that may cut over, and why not.

    The routing tree, the intake tree, and the catalogue tree when one is
    declared, by stable identifier. The second answer is the subset a cutover
    may record, and it is ``tree_registry.cutover_trees``, the set the cutover
    verb accepts, read from the one place both ask. A list kept here said the
    routing tree alone after #224 taught the verb the intake tree, so doctor
    failed every library that had cut its inbox over (R-787). An unusable
    template is ``taxonomy.active``'s failure and is reported there, so here it
    costs the declared half of the list and a clause saying so, never the check.
    """
    try:
        declared = active_taxonomy.load(cfg)
    except CratekitError as exc:
        return (), frozenset(), exc.cause.message
    named = [declared.tree.id, declared.intake.id]
    if declared.catalog is not None:
        named.append(declared.catalog.id)
    return tuple(named), tree_registry.cutover_trees(declared), None


def _check_tree_registry(inputs: _Inputs) -> Finding:
    """Each tree's medium and anchored root, read off the registry (R-235).

    EVERY DECLARED TREE IS LISTED, recorded or not. A tree with no record is on
    the XML bridge, and a report listing only the records would answer "which
    trees have cut over" with silence on the library where the answer is none,
    which is the library a person is about to cut over.

    A RECORD FOR A TREE THE TAXONOMY DOES NOT DECLARE IS LISTED TOO, after the
    declared ones, because the registry is what decides which writer runs and a
    record nobody can see still decides it.

    A NATIVE RECORD THE PRODUCT WOULD REFUSE TO CREATE IS NOT GREEN. The cutover
    verb records the routing tree and the intake tree and nothing else, so a
    native record for the catalogue tree or a tree nobody declares arrived by a
    hand edit or by a template that changed after the cutover. So did a native
    record for either of those two that names a source no rebuild reproduces,
    since ``assert_rebuildable`` refuses that before anything is recorded. It
    is a FAIL, since it routes a writer today. A native intake tree from a
    rebuildable source is a record the verb makes and reads ok, in the same
    sentence as the routing tree. The sentence
    names the act, because no remedy token means "revert this tree" and this is
    the layer that may name a verb.

    AN UNREADABLE REGISTRY IS NOT ANSWERED HERE. ``tree_registry.read`` refuses
    with its own cause and remedy, and :func:`answer` reports that refusal
    whole. Collapsing it into "no record" would read as every tree still being
    on the bridge.

    WHAT IS REPORTED IS THE RECORD. Whether the anchored root is still in the
    database, and whether the tree's membership matches its declaration, need
    the database open and are the convergence report's to answer.
    """
    key, title = "tree.registry", "tree registry"
    if inputs.cfg is None:
        return _unchecked(key, title)
    unreadable = _library_state_unreadable(inputs, "the tree registry")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    found = tree_registry.read(inputs.cfg)
    declared, may_cut_over, undeclared_reason = _declared_trees(inputs.cfg)
    listed = [*declared, *(t for t in found.tree_ids() if t not in declared)]
    described: list[str] = []
    refused: list[str] = []
    for tree_id in listed:
        record = found.record(tree_id)
        if record is None or record.mode != tree_registry.Mode.DATABASE:
            described.append(f"{tree_id} is on the XML bridge, no cutover recorded")
            continue
        described.append(
            f"{tree_id} is database native, anchored to root {record.root_id} "
            f"since {record.cutover_on}, rebuilt from {record.source}"
        )
        if undeclared_reason is None and (
            tree_id not in may_cut_over or record.source not in tree_registry.REBUILDABLE
        ):
            refused.append(tree_id)
    detail = "; ".join(described) if described else "no tree is declared or recorded"
    if undeclared_reason is not None:
        detail += (
            f". The declared trees could not be listed ({undeclared_reason}), so "
            f"only recorded trees are shown and none was judged"
        )
    where = tree_registry.path_for(inputs.cfg)
    if refused:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{where}: {detail}. The database native record for "
                f"{', '.join(refused)} is one a cutover never makes, since a "
                f"cutover records only {', '.join(sorted(may_cut_over))} and "
                f"only from a source a rebuild can reproduce, so a writer is "
                f"being routed by a record this product would refuse to create. "
                f"Run `crate tree revert <tree>` for each, which refuses if the "
                f"tree has taken a native write"
            ),
        )
    return Finding(key=key, title=title, status=Status.OK, detail=f"{where}: {detail}")


# ---------------------------------------------------------------------------
# The check table
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Check:
    """One named question and the function that answers it."""

    key: str
    run: Callable[[_Inputs], Finding]


def _bound(key: str, function: Callable[[str, _Inputs], Finding]) -> Check:
    """A check whose answer function serves a whole family of keys."""
    return Check(key=key, run=lambda inputs, _key=key: function(_key, inputs))


#: Every check, in the order they run, and the order IS part of the contract.
#: The interpreter comes first because every answer below it is worthless on an
#: interpreter the vendored tree has never run on. The three families are
#: expanded from their own declarations rather than typed out, so a credential, a
#: binary, or a backup portion added elsewhere is checked here without an edit.
CHECKS: tuple[Check, ...] = (
    Check("interpreter.version", _check_interpreter),
    Check("config.present", _check_config),
    Check("library.mounted", _check_library_mounted),
    Check("library.identity", _check_library_identity),
    Check("library.db_containment", _check_db_containment),
    Check("library.trash", _check_trash),
    Check("taxonomy.active", _check_taxonomy),
    # U132. After the copy is known to parse, which it reports on.
    Check("taxonomy.schema", _check_taxonomy_schema),
    Check("rekordbox.closed", _check_rekordbox_closed),
    Check("rekordbox.pins", _check_rekordbox_pins),
    # After the pins rather than beside the other library checks, because its
    # answer comes off an open the binding pin governs: a reader meets the pin
    # refusal first and this check's "could not be opened" second.
    Check("library.paths_resolved", _check_paths_resolved),
    Check("keychain.reachable", _check_keychain),
    *(_bound(key, _check_credential) for key in sorted(CREDENTIALS_BY_CHECK)),
    *(_bound(f"binary.{name}", _check_binary) for name in BINARY_NAMES),
    Check("adapter.contract", _check_adapter),
    *(
        _bound(f"backup.age.{portion}", _check_backup_portion)
        for portion in backup_facts.PORTIONS
    ),
    # R-757. After the ages it qualifies and before the remote they all name.
    Check("backup.full_comparison", _check_full_comparison),
    Check("backup.remote", _check_backup_remote),
    Check("session.unresolved", _check_unresolved_session),
    # R-235. Beside the session check because both report this product's own
    # library state, and after the taxonomy check, which it lists trees from.
    Check("tree.registry", _check_tree_registry),
    Check("repo.commit_hook", _check_commit_hook),
)

#: The keys this doctor can answer, in run order. ``tests/test_cli_contract.py``
#: asserts every key any verb declares appears here, so a verb declaring a check
#: nobody wrote fails the build rather than silently depending on nothing.
CHECK_KEYS: tuple[str, ...] = tuple(check.key for check in CHECKS)


def answer(check: Check, inputs: _Inputs) -> Finding:
    """One check's answer, and a THIRD outcome for the check that cannot give one.

    "Never raises" was a sentence in :func:`run`'s docstring and nothing made it
    true. Every check here reaches the outside world, and three of those reaches
    raise on an ordinary broken machine rather than returning a value:
    ``psutil`` refusing to enumerate processes, and ``Path.exists`` and
    ``Path.is_dir`` re-raising a permission error instead of answering False,
    which is what a library root under a directory this account cannot traverse
    produces. One of those took the ENTIRE report down, on precisely the machine
    the module's own opening argument says the report exists for: "a doctor that
    fails by throwing them away is useless in exactly the case it exists for".

    It is a FAIL rather than an INFO, and that is the load-bearing half. INFO is
    "worth knowing, nothing to do now", and a check that did not complete has not
    established that there is nothing to do. Green over an unanswered question is
    the defect this whole unit keeps being sent back for, and a rescue that
    reported one would be that defect wearing a handler.

    It is deliberately NOT per check. A handler inside each one is a handler that
    the next check written here will not have, and the property wanted is about
    every check rather than about the ones somebody remembered.

    AND IT ONLY RESCUES THE UNSTRUCTURED ONES. A ``CratekitError`` is not a check
    that broke, it is a check that REFUSED, and it already carries everything the
    rescue below invents: a declared reason, the reserved exit code that reason
    maps to, a remediation token and its steps. Flattening one produced a FAIL
    whose remedy was report-defect and whose detail read "this check did not
    complete", and the process left under PRECONDITION rather than under the
    reserved code, so a user with an unmounted drive was told to file a defect
    about it. Being not-per-check is exactly why that mattered: it is the shape
    every check written here inherits.

    AND THE UNSTRUCTURED LEG CLASSIFIES BEFORE IT BLAMES. This is the CHECKING
    path, and rescuing the structured refusals out of it left the remaining leg
    attaching report-defect to the exact condition the paragraph above names: a
    library root under a directory this account cannot traverse. One ``crate
    setup`` report then said "this is not a defect, grant this interpreter
    access" from the wizard's own note and "this is a defect; report it" three
    lines below from four checks at once, over one path and one permission.
    ``cause.access_remedy`` is the single decision, shared with the dispatcher,
    so a check nobody has guarded comes out right without a handler of its own.
    """
    try:
        return check.run(inputs)
    except CratekitError as exc:
        cause = exc.cause
        steps = "; ".join(cause.remediation.steps)
        return Finding(
            key=check.key,
            title=check.key,
            status=Status.FAIL,
            detail=cause.message + (f" ({steps})" if steps else ""),
            remedy=cause.remediation.remedy,
            cause=cause,
        )
    except Exception as exc:  # noqa: BLE001 - see the docstring
        note = render.access_note(exc)
        return Finding(
            key=check.key,
            title=check.key,
            status=Status.FAIL,
            detail=(
                f"this check did not complete: {type(exc).__name__}: {exc}. The "
                f"answer is unknown rather than good, and the rest of the report "
                f"is below rather than discarded with it"
                + (f". {note}" if note else "")
            ),
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
        )


def run(cfg: config.Config | None = None, *, probes: Probes | None = None) -> Report:
    """Answer every check, always, and never raise.

    Every check answers on every run, including the ones that cannot be evaluated,
    because a report whose length depends on the machine is a report a consumer
    cannot diff. A check that cannot run says so as INFO and names why, and a
    check that BREAKS trying says so as FAIL through :func:`answer`.

    ``cfg`` is loaded here rather than required from the caller, because doctor's
    first job on a broken install is to report that there is no configuration,
    and a signature that demanded one could not do it.
    """
    error: Exception | None = None
    if cfg is None:
        try:
            cfg = config.load()
        except config.ConfigError as exc:
            cfg, error = None, exc
    inputs = _Inputs(cfg, error, probes or Probes())
    return Report(tuple(answer(check, inputs) for check in CHECKS))


# ---------------------------------------------------------------------------
# crate doctor
# ---------------------------------------------------------------------------


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.set_defaults(_handler=doctor)


def failure_cause(report: Report, *, origin: str = "cli.doctor") -> Cause:
    """One cause carrying every failing check and its rendered fix.

    The steps exist so a consumer that reads only the cause, which is every
    consumer that got the failure across a process boundary, still learns which
    checks failed and what answers each of them. Turning a token into words
    happens here rather than lower down, which is the one place D2 allows it.

    Public because the wizard raises the same refusal for the same reason: a
    setup that wrote a valid config onto a machine that still cannot reach a
    write has not achieved what it was run for, and reporting OK would be a lie
    with the evidence sitting in the same envelope.

    A CHECK THAT REFUSED UNDER ITS OWN REASON KEEPS IT. ``doctor-check-failed``
    maps to PRECONDITION, which is the right answer for "some things this machine
    needs are not here" and the wrong one for a structured refusal that already
    reserved a code of its own: rewriting an unmounted library volume as "N
    checks are failing" drops the reserved 22 and the reason slug a caller
    branches on. The whole report still travels, as steps and in the envelope's
    data, so nothing is lost by leading with the refusal that named itself.
    """
    steps = []
    for finding in report.failures:
        fix = render.remedy_text(finding.remedy) if finding.remedy is not None else None
        steps.append(f"{finding.key}: {finding.detail}" + (f" -> {fix}" if fix else ""))
    failing = [finding.key for finding in report.failures]
    refusal = next((f.cause for f in report.failures if f.cause is not None), None)
    if refusal is not None:
        return Cause(
            reason=refusal.reason,
            message=refusal.message,
            remediation=Remediation(
                remedy=refusal.remediation.remedy,
                steps=tuple(refusal.remediation.steps) + tuple(steps),
            ),
            scope=refusal.scope,
            retryable=refusal.retryable,
            origin=(origin,),
            detail={**dict(refusal.detail), "failing": failing},
        )
    return Cause(
        reason="doctor-check-failed",
        message=(
            f"{len(report.failures)} of {len(report.findings)} checks are failing"
        ),
        remediation=Remediation(steps=tuple(steps)),
        scope=Scope.RUN,
        retryable=True,
        origin=(origin,),
        detail={"failing": failing},
    )


def doctor(ctx: "Context") -> Envelope:
    report = run()
    schema = ctx.entry.output_schema or output.current_schema("diagnostic")
    if report.ok:
        return ctx.envelope(data=report.payload())
    cause = failure_cause(report)
    return output.build(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        schema=schema,
        started=ctx.started,
        outcome=Outcome.FAILED,
        # READ OFF THE CAUSE rather than written here. It is PRECONDITION for
        # every ordinary failing report, because that is what
        # ``doctor-check-failed`` maps to, and a check that refused under its own
        # reason leaves under the code that reason reserves.
        code=cause.code,
        data=report.payload(),
        cause=cause,
    )


# ---------------------------------------------------------------------------
# crate status
# ---------------------------------------------------------------------------


def build_status(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.set_defaults(_handler=status)


def _run_findings() -> list[Finding]:
    """Runs that stopped at a gate or are waiting on a person.

    Read from the run records the dispatcher already persists, so this reports
    the same state ``crate run show`` addresses rather than a second notion of
    what an open run is.
    """
    found: list[Finding] = []
    try:
        records = sorted(gates.run_dir().glob("*.json"))
    except OSError:
        # THE TRIGGER IS UNOBSERVABLE AND THE CONTRACT IS NOT. Measured on this
        # interpreter, ``Path.glob`` swallows ``PermissionError`` inside its own
        # scandir walk and answers with an empty result for a directory that is a
        # plain file, so neither an unreadable state root nor a run directory
        # somebody replaced with a file reaches here through a real filesystem.
        # It is kept because the swallowing is an implementation detail of the
        # standard library rather than a documented promise, and losing the whole
        # status verb to a future change of mind would be worse than a handler
        # that never fires.
        #
        # What that argument does NOT excuse is leaving the promise unwritten,
        # which is how it sat as a rescue nothing exercised. The promise is that
        # a walk which refuses costs the report its run records rather than the
        # verb, and ``tests/test_doctor.py`` states it at the seam by handing
        # this a run directory that raises.
        records = []
    for path in records:
        try:
            state = gates.load(path.stem)
        except CratekitError as exc:
            found.append(
                Finding(
                    key=f"run.{path.stem}",
                    title="run record",
                    status=Status.FAIL,
                    detail=exc.cause.message,
                    remedy=Remedy.REPORT_DEFECT,
                )
            )
            continue
        if state.open_gate is None and state.pending is None:
            continue
        waiting = (
            f"open gate {state.open_gate}"
            if state.open_gate is not None
            else f"awaiting {state.pending.kind}"
        )
        found.append(
            Finding(
                key=f"run.{state.run_id}",
                title=state.verb,
                status=Status.INFO,
                detail=f"{waiting}, started {state.created}",
                remedy=Remedy.ANSWER_DECISION
                if state.open_gate is not None
                else Remedy.COMPLETE_PENDING_ACTION,
            )
        )
    return found


def _source_findings(cfg: config.Config) -> list[Finding]:
    """Per-source sync state, from the session log and the watermark store.

    R29 makes the destructive boundary one source per run, committed and captured
    independently, and the session record carries a state per source for exactly
    that reason: without it a resume either redoes committed work or skips
    uncommitted work and nothing outside can tell which. U22's watermark store
    is the other half: each source's last clean completion, reported rather than
    guessed. The rows come from ``cratekit.sync.watermarks.status_rows``, which
    derives the source set, so a source added there cannot go unreported (P3).
    """
    from cratekit.sync import watermarks as sync_watermarks

    found: list[Finding] = []
    for record in session.records(cfg):
        if record.terminal:
            continue
        for source, state in sorted(record.sources.items()):
            found.append(
                Finding(
                    key=f"source.{source}",
                    title=f"{source} in session {record.session_id}",
                    status=Status.FAIL
                    if state == str(session.SourceState.REFUSED)
                    else Status.INFO,
                    detail=f"{state} in workflow {record.workflow}",
                    remedy=Remedy.RESUME_JOB
                    if state == str(session.SourceState.REFUSED)
                    else None,
                )
            )
    try:
        rows = sync_watermarks.status_rows(cfg)
    except CratekitError as exc:
        found.append(
            Finding(
                key="source.watermarks",
                title="source watermarks",
                status=Status.FAIL,
                detail=exc.cause.message,
                remedy=exc.cause.remediation.remedy,
            )
        )
        return found
    for row in rows:
        found.append(
            Finding(
                key=f"source.{row['source_id']}.watermark",
                title=f"{row['source_id']} watermark",
                status=Status.INFO,
                detail=row["detail"],
            )
        )
    return found


def _tree_findings(cfg: config.Config) -> list[Finding]:
    """What medium owns each tree, and whether the registry can be read at all.

    An unreadable registry is its own answer and is never collapsed into "no
    record": no record reads as "every tree is still on the bridge", which would
    send a byte write at a tree the database already owns.

    Whether a tree's declared membership actually MATCHES the database is a
    different question, it needs the database open, and the verb that answers it
    lands with the convergence check. What is reported here is the record.
    """
    try:
        found_registry = tree_registry.read(cfg)
    except CratekitError as exc:
        return [
            Finding(
                key="tree.registry",
                title="tree registry",
                status=Status.FAIL,
                detail=exc.cause.message,
                remedy=exc.cause.remediation.remedy,
            )
        ]
    return [
        Finding(
            key=f"tree.{record.tree_id}",
            title=f"tree {record.tree_id}",
            status=Status.INFO,
            detail=(
                f"{record.mode}, cutover {record.cutover_on or 'not recorded'}, "
                f"adopted root {record.root_id or 'none'}"
            ),
        )
        for record in found_registry.trees
    ]


def status(ctx: "Context") -> Envelope:
    cfg = config.load()
    findings = _run_findings() + _source_findings(cfg) + _tree_findings(cfg)
    data = {
        "checks": [finding.to_json() for finding in findings],
        "summary": {
            "open_runs": sum(1 for f in findings if f.key.startswith("run.")),
            "sources": sum(1 for f in findings if f.key.startswith("source.")),
            "trees": sum(1 for f in findings if f.key.startswith("tree.")),
            "library": str(cfg.library.root),
        },
    }
    return ctx.envelope(data=data, outcome=Outcome.OK if findings else Outcome.NO_OP)


__all__ = [
    "BINARY_NAMES",
    "CHECKS",
    "CHECK_KEYS",
    "CREDENTIALS_BY_CHECK",
    "Check",
    "Finding",
    "Probes",
    "Report",
    "Status",
    "answer",
    "build",
    "build_status",
    "contract_members",
    "doctor",
    "failure_cause",
    "requires_check",
    "run",
    "satisfies",
    "status",
]
