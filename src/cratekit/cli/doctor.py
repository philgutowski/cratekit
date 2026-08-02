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
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
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
    tree_registry,
)
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope
from cratekit.core.exit_codes import ExitCode, Remedy

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
    """

    key: str
    title: str
    status: Status
    detail: str
    remedy: Remedy | None = None

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
    is imported straight from a checkout. That is reported as its own answer
    rather than as a pass, because a check that cannot fail is not a check.
    """
    try:
        return metadata.metadata(registry.DISTRIBUTION)["Requires-Python"]
    except (metadata.PackageNotFoundError, KeyError):  # pragma: no cover - needs no install
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
    is not only whether a remote exists but how it is configured: R-7 records
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
    beside it and the answer is None, which is what makes R-1's check a
    developer check that says nothing on a user's machine.
    """
    root = Path(cratekit.__file__).resolve().parents[2]
    return root if (root / ".git").exists() else None


def _git_dir(root: Path) -> Path | None:
    """The git directory that owns ``root``, following a worktree pointer.

    A worktree's ``.git`` is a FILE naming its own git directory, and that
    directory names the COMMON one, which is where hooks actually live. Looking
    only for ``.git/hooks`` would therefore report every worktree as unhooked
    while the hook was installed and running, which is a guard that fires on
    correct setups, and those get worked around rather than fixed (P7).
    """
    marker = root / ".git"
    if marker.is_dir():
        return marker
    try:
        text = marker.read_text().strip()
    except OSError:
        return None
    if not text.startswith("gitdir:"):
        return None
    pointed = Path(text.split(":", 1)[1].strip())
    if not pointed.is_absolute():
        pointed = (root / pointed).resolve()
    common = pointed / "commondir"
    if common.is_file():
        try:
            return (pointed / common.read_text().strip()).resolve()
        except OSError:  # pragma: no cover - a commondir that vanished mid-read
            return None
    return pointed


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
    identity_provider: preflight.IdentityProvider | None = None
    mount_enumerator: preflight.MountEnumerator | None = None
    process_lister: processes.ProcessLister | None = None
    keychain_available: Callable[[], bool] = secrets.backend_available
    credential_recorded: Callable[[str], bool] = secrets.exists
    installed_app_version: Callable[[config.Config | None], str | None] = (
        lambda cfg: rb_writer.read_installed_app_version(cfg=cfg)
    )
    binding_pin_problem: Callable[[config.Config | None], str | None] = _binding_pin_problem
    rclone_remotes: Callable[[str], Mapping[str, Mapping[str, Any]] | None] = _rclone_remotes
    checkout_root: Callable[[], Path | None] = _checkout_root


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
    """
    running = tuple(version)
    verdict = True
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
                verdict = verdict and _COMPARATORS[symbol](left, right)
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
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=str(error),
        remedy=Remedy(str(error.remedy)),
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
        detail = (
            f"nothing at the configured root to compare: {_MOUNT_DETAIL[status.state]}. "
            f"The recorded identity {status.recorded_identity} is intact"
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


def _check_taxonomy(inputs: _Inputs) -> Finding:
    key, title = "taxonomy.active", "active taxonomy template"
    if inputs.cfg is None:
        return _unchecked(key, title)
    path = config.state_path("taxonomy_active", inputs.cfg)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        # UnicodeDecodeError is a ValueError, not an OSError, so a template that
        # is present and is not text would otherwise escape this check as an
        # internal defect rather than as the unusable template it is.
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
    return Finding(
        key=key,
        title=title,
        status=Status.OK,
        detail=(
            f"template {inputs.cfg.taxonomy.template!r} is active with "
            f"{len(declared.buckets)} declared buckets"
        ),
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


def _check_keychain(inputs: _Inputs) -> Finding:
    key, title = "keychain.reachable", "OS keychain"
    if inputs.probes.keychain_available():
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail="a keychain backend that can store a credential is available",
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            "no keychain backend resolves on this machine. Credentials are never "
            "written to a plain file, so this installation cannot hold one until a "
            "backend is installed or the environment fallback is opted into by name"
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


def _check_backup_portion(key: str, inputs: _Inputs) -> Finding:
    portion = backup_facts.PORTIONS[key.split(".")[-1]]
    title = f"backup age, {portion} portion"
    if inputs.cfg is None:
        return _unchecked(key, title)
    try:
        ages = backup_facts.ages(inputs.cfg, now=inputs.probes.now)
    except backup_facts.BackupFactsUnreadable as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=str(exc),
            remedy=Remedy(str(exc.remedy)),
        )
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
    days = answer.age.days if answer.age is not None else 0
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=f"last completed {days} days ago, to {answer.destination or 'an unnamed destination'}",
    )


#: rclone remote types whose provider moves a deleted object to a trash that keeps
#: counting against the quota. R-7: pruning a backup archive on one of these
#: reclaims nothing for the trash retention period unless the remote's own
#: no-trash option is set, and the source system solved it by passing a provider
#: flag from inside the prune, which is the one-provider assumption this port
#: removed.
_TRASHING_REMOTE_TYPES: Mapping[str, str] = MappingProxyType({"drive": "use_trash"})


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
                "the backup module is on and backup.remote names no destination, "
                "so the backup verb has nowhere to write until one is configured"
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
    settings = remotes.get(remote.rstrip(":"))
    if settings is None:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"backup.remote names {remote!r} and rclone has no remote by that "
                f"name; it knows {', '.join(sorted(remotes)) or 'none'}"
            ),
            remedy=Remedy.RUN_SETUP,
        )
    kind = str(settings.get("type", ""))
    option = _TRASHING_REMOTE_TYPES.get(kind)
    if option is None:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"{remote!r} is configured as a {kind or 'typeless'} remote",
        )
    if str(settings.get(option, "")).lower() == "false":
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"{remote!r} is a {kind} remote with {option} disabled, so a prune reclaims space",
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"{remote!r} is a {kind} remote and its {option} option is not disabled. "
            f"A pruned archive folder goes to the provider's trash and keeps "
            f"counting against the quota for the retention period, which is the "
            f"whole point of pruning. Set {option} to false on that remote in "
            f"rclone's own configuration"
        ),
    )


def _check_unresolved_session(inputs: _Inputs) -> Finding:
    key, title = "session.unresolved", "destructive sessions"
    if inputs.cfg is None:
        return _unchecked(key, title)
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
            detail=f"{len(parsed)} recorded session(s), none of them open",
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
            f"{', '.join(f'{r.session_id} ({r.state})' for r in open_records)}"
        ),
    )


def _check_commit_hook(inputs: _Inputs) -> Finding:
    """R-1: the repository's own guard is off by default on a fresh clone.

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
    git_dir = _git_dir(root)
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
    except OSError:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"no pre-commit hook at {hook}, so the repository scan does not run "
                f"before a commit and a personal path or a credential reaches the "
                f"history unchallenged. Run `pre-commit install` in {root}"
            ),
        )
    if "pre-commit" not in body:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the hook at {hook} does not dispatch to this repository's "
                f"pre-commit configuration, so the scan it is supposed to run does "
                f"not run. Run `pre-commit install` in {root}"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.OK,
        detail=f"{hook} dispatches to the repository's pre-commit configuration",
    )


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
    Check("taxonomy.active", _check_taxonomy),
    Check("rekordbox.closed", _check_rekordbox_closed),
    Check("rekordbox.pins", _check_rekordbox_pins),
    Check("keychain.reachable", _check_keychain),
    *(_bound(key, _check_credential) for key in sorted(CREDENTIALS_BY_CHECK)),
    *(_bound(f"binary.{name}", _check_binary) for name in BINARY_NAMES),
    Check("adapter.contract", _check_adapter),
    *(
        _bound(f"backup.age.{portion}", _check_backup_portion)
        for portion in backup_facts.PORTIONS
    ),
    Check("backup.remote", _check_backup_remote),
    Check("session.unresolved", _check_unresolved_session),
    Check("repo.commit_hook", _check_commit_hook),
)

#: The keys this doctor can answer, in run order. ``tests/test_cli_contract.py``
#: asserts every key any verb declares appears here, so a verb declaring a check
#: nobody wrote fails the build rather than silently depending on nothing.
CHECK_KEYS: tuple[str, ...] = tuple(check.key for check in CHECKS)


def run(cfg: config.Config | None = None, *, probes: Probes | None = None) -> Report:
    """Answer every check, always, and never raise.

    Every check answers on every run, including the ones that cannot be evaluated,
    because a report whose length depends on the machine is a report a consumer
    cannot diff. A check that cannot run says so as INFO and names why.

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
    return Report(tuple(check.run(inputs) for check in CHECKS))


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
    """
    steps = []
    for finding in report.failures:
        fix = render.remedy_text(finding.remedy) if finding.remedy is not None else None
        steps.append(f"{finding.key}: {finding.detail}" + (f" -> {fix}" if fix else ""))
    return Cause(
        reason="doctor-check-failed",
        message=(
            f"{len(report.failures)} of {len(report.findings)} checks are failing"
        ),
        remediation=Remediation(steps=tuple(steps)),
        scope=Scope.RUN,
        retryable=True,
        origin=(origin,),
        detail={"failing": [finding.key for finding in report.failures]},
    )


def doctor(ctx: "Context") -> Envelope:
    report = run()
    schema = ctx.entry.output_schema or output.current_schema("diagnostic")
    if report.ok:
        return ctx.envelope(data=report.payload())
    return output.build(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        schema=schema,
        started=ctx.started,
        outcome=Outcome.FAILED,
        code=ExitCode.PRECONDITION,
        data=report.payload(),
        cause=failure_cause(report),
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
    except OSError:  # pragma: no cover - an unreadable state directory
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
    """Per-source sync state, from the one landed producer of it.

    R29 makes the destructive boundary one source per run, committed and captured
    independently, and the session record carries a state per source for exactly
    that reason: without it a resume either redoes committed work or skips
    uncommitted work and nothing outside can tell which. That record is what this
    reports. The per-source WATERMARKS the sweeps will keep are a different store
    and land with the units that write them; reporting a watermark this build
    cannot read would be guessing at a shape.
    """
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
