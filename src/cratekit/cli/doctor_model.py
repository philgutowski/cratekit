"""What doctor's checks answer with and are handed: the finding, the report, the probes.

Split out of ``cli.doctor`` by U303. The names other code reads on
``cratekit.cli.doctor`` stay reachable there; the rest are read here.
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
    """The three answers a check gives.

    ``INFO`` is not a weaker ``FAIL``: it means "worth knowing, nothing to do
    now", and filing such notes under red would train people to ignore red.
    """

    OK = "ok"
    FAIL = "fail"
    INFO = "info"


@dataclass(frozen=True, slots=True)
class Finding:
    """One check's answer: what was asked, what was seen, what fixes it.

    ``remedy`` is a token the CLI renders, never a command line (D2); when no
    token fits it is None and ``detail`` states the act. A finding built from a
    caught exception is classified here, as a raised refusal is, so pass
    ``error`` and the remedy follows the kind of refusal the operating system
    made, without each reporting site having to get it right.
    """

    key: str
    title: str
    status: Status
    detail: str
    remedy: Remedy | None = None
    #: The structured cause when a check refused under a declared reason. It
    #: carries the reason slug and so the reserved exit code, which
    #: ``failure_cause`` uses instead of the report's generic one.
    cause: Cause | None = None
    #: The exception this answer came from catching, read once at construction to
    #: decide whether the operating system refused. Never rendered or serialized,
    #: and outside equality, since two findings saying the same thing are equal.
    error: BaseException | None = field(default=None, compare=False, repr=False)

    def __post_init__(self) -> None:
        """Correct the remedy, and give a failure a cause, when the answer is an OS refusal.

        The remedy follows the kind of refusal, so a read only volume is not sent
        to Full Disk Access, and a failing finding with no cause gains one so a
        machine consumer sees the remedy. The words are left alone, and a finding
        with no exception, or one the OS did not refuse, is left as built.
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

    Read rather than repeated, so KTD19's bound has one copy. None when the
    distribution is not installed or declares no bound, which the check reports
    as its own answer rather than as a pass.
    """
    try:
        return metadata.metadata(registry.DISTRIBUTION)["Requires-Python"]
    except (metadata.PackageNotFoundError, KeyError):
        return None


def _binding_pin_problem(cfg: config.Config | None) -> str | None:
    """The pyrekordbox pin's complaint, or None when it is satisfied.

    Asked through the guarded writer's own assertion, so the check and the
    write can never disagree.
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

    ``config dump`` rather than ``listremotes``, because pruning reclaims space
    only when a remote's own settings say so, and only the dump shows them.
    """
    # An absolute path from ``core/binaries`` and no shell, since a graphical
    # launcher's PATH lacks the package manager's directories.
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

    None for an installed wheel, which has no ``.git`` beside it, so the commit
    hook check says nothing on a user's machine.
    """
    root = Path(cratekit.__file__).resolve().parents[2]
    return root if (root / ".git").exists() else None


def _git_dir(root: Path) -> tuple[Path | None, str | None, Remedy | None]:
    """The git directory that owns ``root``, why it could not be found, and the act that fixes it.

    A worktree's ``.git`` is a file naming its git directory, which names the
    common one where hooks live, so a worktree is not reported unhooked (P7).
    None with no sentence means a marker that parsed and named nothing; anything
    unreadable comes back as a sentence, with a remedy from
    ``cause.access_remedy`` so a permission problem is not called a defect.
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
        # Bytes that read but will not decode are never a permission problem.
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
            # Both members are reachable: a commondir that is not text is a
            # damaged checkout, and a refused read is a permission.
            return (
                None,
                f"the commondir at {common} could not be read ({exc})",
                access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
            )
    return pointed, None, None


def _survey_paths(cfg: config.Config) -> metadata_cli.ResolutionTotals | None:
    """How the collection's rows resolve here, read off a copy of the database.

    The live path is never opened, not even read only (R-372). None when there
    is no database file; a database that cannot be opened raises its own
    refusal instead. The binding and schema pins still apply to the copy.
    """
    source = rb_writer.live_db_path(cfg)
    if not source.is_file():
        return None
    with rb_writer.read_only_copy(source, cfg=cfg) as db:
        return metadata_cli.resolution_totals(cfg, db)


def _probe_trash(path: Path) -> TrashStatus:
    """Whether a file at ``path`` could be trashed, without making it possible.

    ``create=False`` is bound here because :func:`trash.probe` creates the
    per-volume Trash by default, and a check that did so would pass on a
    directory it made itself.
    """
    from cratekit.deletion import trash

    return trash.probe(path, create=False)


#: Where a release install comes from when a check has to say how to move to one.
RELEASE_REPOSITORY = "https://github.com/philgutowski/cratekit"


#: How long the release read may take before it is reported as unread, short
#: because doctor runs before every gated verb.
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

    Neither pipx nor PEP 610 records the extras an install named, so they are
    read back from what is present. An extra naming this package itself
    (``all``) is an alias and is left out.
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

    Doctor's one network read, behind this function so no test reaches the
    network. ``GIT_TERMINAL_PROMPT=0`` makes a missing credential a refusal
    rather than a prompt that hangs the report.
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

    A bound loader is taken as able, the rule the vocals verb queues by.
    """
    from cratekit.analysis import vocals as vocal_scoring

    return None if vocal_scoring.loader_bound() else vocal_scoring.requirement()


def _vocals_scored(cfg: config.Config | None) -> bool:
    """Whether this library has ever scored a track for vocals (U181).

    Read as a recorded vocal calibration, since reading every file for a
    voxlevel costs more than doctor may spend.
    """
    if cfg is None:
        return False
    return config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, cfg).is_file()


def _deadca7_home() -> Path | None:
    """DEADCA7's support folder under this account, where its push backups land.

    The app makes it only on a push (U224), so its absence says nothing about
    whether the app is installed; :func:`_deadca7_installed` says that.
    """
    try:
        return Path.home() / "Library" / "Application Support" / "deadca7"
    except RuntimeError:  # no home directory to resolve
        return None


#: DEADCA7's app bundle, as its disk image installs it (U224).
DEADCA7_BUNDLE = "DEADCA7.app"


#: The folder DEADCA7 keeps its state in under Application Support (U224).
DEADCA7_STATE = "deadcatalog"


def _deadca7_installed() -> tuple[Path, ...]:
    """The places whose presence says DEADCA7 is installed on this machine (U224).

    Its app bundle in either Applications folder, or its state folder; any one
    present is an install.
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

    One value, so a test describes a whole machine and drives the real checks
    against it, and a new platform is a different probe rather than a branch.
    """

    now: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    python_version: tuple[int, ...] = field(default_factory=lambda: sys.version_info[:3])
    requires_python: str | None = field(default_factory=_declared_python_bound)
    find_binary: Callable[[str], str | None] = binaries.find
    #: Why a binary was not found, when the reason is an override the user set.
    #: A second seam because ``find``'s contract is a path or nothing.
    binary_override_problem: Callable[[str], str | None] = binaries.override_problem
    identity_provider: preflight.IdentityProvider | None = None
    mount_enumerator: preflight.MountEnumerator | None = None
    process_lister: processes.ProcessLister | None = None
    keychain_available: Callable[[], bool] = secrets.backend_available
    credential_recorded: Callable[[str], bool] = secrets.exists
    #: Whether the opted-in environment fallback is supplying a credential, asked
    #: through the module that owns the rule.
    environment_credential: Callable[[str], str | None] = secrets.environment_value
    installed_app_version: Callable[[config.Config | None], str | None] = (
        lambda cfg: rb_writer.read_installed_app_version(cfg=cfg)
    )
    binding_pin_problem: Callable[[config.Config | None], str | None] = _binding_pin_problem
    rclone_remotes: Callable[[str], Mapping[str, Mapping[str, Any]] | None] = _rclone_remotes
    checkout_root: Callable[[], Path | None] = _checkout_root
    #: Whether this account could move a file into the library volume's Trash.
    trash_probe: Callable[[Path], TrashStatus] = _probe_trash
    #: How the collection's active rows resolve on this machine, or None when
    #: there is no database file. The default opens a copy, never the live path,
    #: and is asked only once rekordbox is known closed, so the copy is whole.
    path_survey: Callable[[config.Config], metadata_cli.ResolutionTotals | None] = (
        _survey_paths
    )
    #: How this copy was installed, read off its PEP 610 record (U159).
    install_origin: Callable[[], InstallOrigin] = _install_origin
    #: The tags a repository publishes, or None when they could not be read.
    #: The one network read doctor makes, so every test replaces it.
    release_tags: Callable[[str], tuple[str, ...] | None] = _release_tags
    #: Why the vocal model cannot score here, a kind and a sentence, or None (U181).
    vocal_requirement: Callable[[], tuple[str, str] | None] = _vocal_requirement
    #: Whether this library has ever scored a track for vocals (U181), which
    #: decides whether an upgrade command keeps the vocals extra.
    vocals_scored: Callable[[config.Config | None], bool] = _vocals_scored
    #: Where DEADCA7's push backups land on this machine, or None (U185).
    deadca7_home: Callable[[], Path | None] = _deadca7_home
    #: The places whose presence says DEADCA7 is installed here (U224), a
    #: separate question from where its push backups land.
    deadca7_installed: Callable[[], tuple[Path, ...]] = _deadca7_installed
    #: Every call the provider gate has counted, per identity, or None when its
    #: state file could not be read (U205).
    provider_spend: Callable[[], provider_gate.Spend | None] = provider_gate.read_spend
    #: The hour's spend per identity and any cooldown, off the one gate, at the
    #: moment given, or None when its file could not be read (U278).
    provider_standing: Callable[[float], provider_gate.Standing | None] = (
        provider_gate.read_standing
    )


def requires_check(key: str, membership: profiles.Membership) -> bool:
    """Whether any verb this profile switches on declares ``key``.

    Derived from the registry, so enabling a module makes its checks required
    with no edit here. Taken over every entry, landed or not, so what a profile
    needs does not shift as later units land.
    """
    return bool(verbs_requiring(key, membership))


def verbs_requiring(key: str, membership: profiles.Membership) -> tuple[str, ...]:
    """The verbs this profile switches on that declare ``key``, as a person types them.

    So a failing row names what it stops (U263).
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

    The mount probe is memoized so ``library.mounted`` and ``library.identity``
    report one observation and cannot disagree (U18).
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

    INFO, since ``config.present`` already reports the failure once.
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

    A small parser rather than a version library the slim core does not declare
    (R5). Anything unrecognised, or a specifier that compares nothing, returns
    None, which the caller reports as unchecked rather than as a pass.
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
