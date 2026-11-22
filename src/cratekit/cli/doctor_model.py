"""What doctor's checks answer with and are handed: the finding, the report, the probes.

Split out of ``cli.doctor`` by U303; every name here is also reachable as
``cratekit.cli.doctor.NAME``.
"""

from __future__ import annotations

import json
import os
import re
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
from cratekit.cli import registry
from cratekit.core import (
    binaries,
    config,
    preflight,
    processes,
    profiles,
    provider_gate,
    rb_writer,
    secrets,
)
from cratekit.core.cause import (
    Cause,
    CratekitError,
    Remediation,
    Scope,
    access_refusal,
    access_remedy,
)
from cratekit.core.exit_codes import Remedy
from cratekit.write import metadata_cli

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.deletion.trash import TrashStatus


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


def _probe_trash(path: Path) -> TrashStatus:
    """Whether a file at ``path`` could be trashed, WITHOUT making it possible.

    ``create=False`` is bound here rather than left to the check, and it is the
    whole reason this seam exists as its own function. :func:`trash.probe`
    creates the per-volume Trash by default, because the desktop does too and a
    volume nobody has trashed anything on legitimately has no directory yet. A
    health check that took that default would make the directory it is asking
    about exist, and would then report a pass it had itself produced, which is
    the same defect as a test that asserts its own fixture.
    """
    from cratekit.deletion import trash

    return trash.probe(path, create=False)


#: Where a release install comes from when a check has to say how to move to one.
RELEASE_REPOSITORY = "https://github.com/philgutowski/cratekit"


#: How long the release read may take before it is reported as unread. Short,
#: because doctor runs before every gated verb and a hung remote is not a
#: reason to hold one up.
RELEASE_READ_TIMEOUT = 10.0


@dataclass(frozen=True, slots=True)
class InstallOrigin:
    """How this copy was installed, read off its PEP 610 record (U159).

    ``kind`` is one of ``vcs`` (installed from a git repository, the release
    install), ``editable`` (a checkout installed in place), ``folder`` (a
    directory or an archive installed as a copy), ``index`` (no
    ``direct_url.json`` at all, so from a package index) or ``unknown`` (no
    distribution, or a record that does not parse).
    """

    kind: str
    version: str | None = None
    url: str | None = None
    extras: tuple[str, ...] = ()


_REQUIREMENT_NAME_RE = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")


_EXTRA_MARKER_RE = re.compile(r"""extra\s*==\s*["']([^"']+)["']""")


def _canonical(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _installed_extras(dist: metadata.Distribution) -> tuple[str, ...]:
    """The extras whose every requirement is installed beside this copy.

    pipx keeps no record of the extras an install named, and PEP 610 does not
    either, so they are read back from what is present: an extra counts when
    each distribution it requires can be found. An extra that names this
    package itself (``all``) is an alias for others and is left out, since the
    others it names are listed in their own right.
    """
    own = _canonical(dist.metadata["Name"] or "cratekit")
    wanted: dict[str, list[str]] = {}
    for requirement in dist.requires or ():
        marker = _EXTRA_MARKER_RE.search(requirement)
        name = _REQUIREMENT_NAME_RE.match(requirement)
        if marker is None or name is None:
            continue
        wanted.setdefault(marker.group(1), []).append(_canonical(name.group(1)))
    present = []
    for extra, names in sorted(wanted.items()):
        if own in names:
            continue
        try:
            for name in names:
                metadata.distribution(name)
        except metadata.PackageNotFoundError:
            continue
        present.append(extra)
    return tuple(present)


def _install_origin() -> InstallOrigin:
    try:
        dist = metadata.distribution("cratekit")
    except metadata.PackageNotFoundError:
        return InstallOrigin(kind="unknown")
    version = dist.version
    text = dist.read_text("direct_url.json")
    if text is None:
        return InstallOrigin(kind="index", version=version)
    try:
        record = json.loads(text)
    except json.JSONDecodeError:
        return InstallOrigin(kind="unknown", version=version)
    if not isinstance(record, dict):
        return InstallOrigin(kind="unknown", version=version)
    url = record.get("url")
    if isinstance(record.get("vcs_info"), dict):
        return InstallOrigin(
            kind="vcs", version=version, url=url, extras=_installed_extras(dist)
        )
    dir_info = record.get("dir_info")
    if isinstance(dir_info, dict) and dir_info.get("editable"):
        return InstallOrigin(kind="editable", version=version, url=url)
    return InstallOrigin(kind="folder", version=version, url=url)


def _release_tags(url: str) -> tuple[str, ...] | None:
    """The tag names the repository at ``url`` publishes, or None if unread.

    The one network read doctor makes, and it is behind this one function so no
    test reaches the network. The person's own git credentials answer it, and
    ``GIT_TERMINAL_PROMPT=0`` makes a missing credential a refusal rather than a
    prompt that hangs the report.
    """
    try:
        done = subprocess.run(
            ["git", "ls-remote", "--tags", "--refs", url],
            capture_output=True,
            text=True,
            timeout=RELEASE_READ_TIMEOUT,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if done.returncode != 0:
        return None
    tags = []
    for line in done.stdout.splitlines():
        _sha, _tab, ref = line.partition("\t")
        if ref.startswith("refs/tags/"):
            tags.append(ref.removeprefix("refs/tags/"))
    return tuple(tags)


def _vocal_requirement() -> tuple[str, str] | None:
    """Why the vocal model cannot score here, as a kind and a sentence, or None (U181).

    The vocals module's own probe. A bound loader is taken as able, the rule
    the vocals verb queues by.
    """
    from cratekit.analysis import vocals as vocal_scoring

    return None if vocal_scoring.loader_bound() else vocal_scoring.requirement()


def _vocals_scored(cfg: config.Config | None) -> bool:
    """Whether this library has ever scored a track for vocals (U181).

    Read as a vocal calibration recorded for it, which is fitted only from
    files carrying a voxlevel, or set by hand to tag them. Reading every file
    or every row for a voxlevel is not a cost doctor may spend, so a library
    scored and never calibrated reads as never scored here.
    """
    if cfg is None:
        return False
    return config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, cfg).is_file()


def _deadca7_home() -> Path | None:
    """DEADCA7's support folder under this account, where its push backups land.

    Read from the app's source (the 2026-10-26 assessment), not from a push:
    DEADCA7 0.2.3 as shipped makes no such folder on launch (U224), so this is
    the folder a push would make, and its absence alone says nothing about
    whether the app is installed. :func:`_deadca7_installed` says that.
    """
    try:
        return Path.home() / "Library" / "Application Support" / "deadca7"
    except RuntimeError:  # no home directory to resolve
        return None


#: DEADCA7's app bundle, as its disk image installs it (U224).
DEADCA7_BUNDLE = "DEADCA7.app"


#: The folder DEADCA7 keeps its state in under Application Support, as shipped:
#: version 0.2.3 (build 0345c1db) holds its engine in a ``runtime`` folder
#: there and logs to ``Library/Logs/deadca7`` (U224, read at sitting 68).
DEADCA7_STATE = "deadcatalog"


def _deadca7_installed() -> tuple[Path, ...]:
    """The places whose presence says DEADCA7 is installed on this machine (U224).

    Its app bundle in the system's Applications folder and in this account's,
    and the state folder the app keeps once it has run. Any one present is an
    install; a machine with no home to resolve is asked about the system's
    folder only.
    """
    system = Path("/Applications") / DEADCA7_BUNDLE
    try:
        home = Path.home()
    except RuntimeError:  # no home directory to resolve
        return (system,)
    return (
        system,
        home / "Applications" / DEADCA7_BUNDLE,
        home / "Library" / "Application Support" / DEADCA7_STATE,
    )


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
    trash_probe: Callable[[Path], TrashStatus] = _probe_trash
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
    #: How this copy was installed, read off its PEP 610 record (U159).
    install_origin: Callable[[], InstallOrigin] = _install_origin
    #: The tags a repository publishes, or None when they could not be read.
    #: The one network read doctor makes, so every test replaces it.
    release_tags: Callable[[str], tuple[str, ...] | None] = _release_tags
    #: Why the vocal model cannot score here, a kind and a sentence, or None
    #: (U181). A seam so a test describes a copy with and without the extra.
    vocal_requirement: Callable[[], tuple[str, str] | None] = _vocal_requirement
    #: Whether this library has ever scored a track for vocals (U181), which
    #: decides whether an upgrade command keeps the vocals extra.
    vocals_scored: Callable[[config.Config | None], bool] = _vocals_scored
    #: Where DEADCA7 keeps its own state on this machine, or None for a machine
    #: with no such place (U185). A seam so a test describes an install, a push
    #: and its age without the app.
    deadca7_home: Callable[[], Path | None] = _deadca7_home
    #: The places whose presence says DEADCA7 is installed here, its bundle and
    #: its state folder (U224). A second seam rather than a richer first one,
    #: because the shipped app makes the state folder and never the support
    #: folder the push backups land in, so the two answer different questions.
    deadca7_installed: Callable[[], tuple[Path, ...]] = _deadca7_installed
    #: Every call the provider gate has counted, per identity, off its state
    #: file, or None when the file could not be read (U205). A seam so a test
    #: describes an installation's history without writing the real file.
    provider_spend: Callable[[], provider_gate.Spend | None] = provider_gate.read_spend
    #: The hour's spend per identity and any cooldown, off the one gate, at the
    #: moment given, or None when its file could not be read (U278).
    provider_standing: Callable[[float], provider_gate.Standing | None] = (
        provider_gate.read_standing
    )


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
    return bool(verbs_requiring(key, membership))


def verbs_requiring(key: str, membership: profiles.Membership) -> tuple[str, ...]:
    """The verbs this profile switches on that declare ``key``, as a person types them.

    So a failing row says what it stops, rather than that something does: a
    missing ffmpeg names ``analyze run``, whose decode of an M4A goes through
    it (U263), beside the download verbs that extract through it.
    """
    return tuple(
        sorted(
            entry.name.replace(".", " ")
            for entry in registry.entries()
            if key in entry.doctor_checks and entry.available_to(membership)
        )
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

    def requiring(self, key: str) -> tuple[str, ...]:
        """The verbs this profile switches on that depend on ``key``."""
        return verbs_requiring(key, self.membership)


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
