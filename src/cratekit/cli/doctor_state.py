"""Doctor's checks of this installation's own state: sessions, the commit hook, trees, the install and its notes.

What could not be read is said as unknown, never as absent or empty, and the
notes at the end are INFO in every state.
"""

from __future__ import annotations

import os
import shlex
from collections.abc import Sequence
from datetime import datetime, timedelta
from pathlib import Path

from cratekit.cli import gates
from cratekit.cli.doctor_library import _library_state_unreadable, _volume_clause
from cratekit.cli.doctor_model import (
    RELEASE_REPOSITORY,
    Finding,
    InstallOrigin,
    Status,
    _git_dir,
    _Inputs,
    _parse_release,
    _unchecked,
)
from cratekit.core import (
    config,
    provider_gate,
    session,
    tree_registry,
)
from cratekit.core.cause import (
    CratekitError,
    access_remedy,
)
from cratekit.core.exit_codes import Remedy


def _check_unresolved_session(inputs: _Inputs) -> Finding:
    key, title = "session.unresolved", "destructive sessions"
    if inputs.cfg is None:
        return _unchecked(key, title)
    unreadable = _library_state_unreadable(inputs, "the session log")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    # One scan, branched on what it could not read, so no second listing can
    # race the first (R-1255).
    parsed, unreadable = session.scan_log(inputs.cfg)
    if session.log_unlisted(unreadable, inputs.cfg):
        unreadable_directory = session.log_dir(inputs.cfg)
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
    if unreadable:
        # Report the unreadable records the gate will refuse on, not only the
        # ones it can read.
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

    Names a proven landing waiting for a cutover (R-501) and an orphaned run
    (R-598), which listed bare would read as runs in progress.
    """
    if session.owes_only_deferred_routing(record):
        return f"{record.state}, import proven, placement waits for a cutover"
    if session.orphaned(record):
        return f"{record.state}, its process is gone, crate session release abandons it"
    return str(record.state)


#: The configuration file pre-commit reads when the hook names none.
_HOOK_CONFIG_DEFAULT = ".pre-commit-config.yaml"


#: What a generated pre-commit hook actually contains: a call into the tool's own
#: hook implementation, bound to the stage it was installed for.
_HOOK_DISPATCH = "hook-impl"


#: Every git hook type pre-commit can install, copied rather than imported so
#: the check works without the dev extra.
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
    """Where a configuration name from a hook's dispatch line points, relative to ``root``."""
    configured = Path(named)
    return configured if configured.is_absolute() else root / configured


def _configured_hook_types(
    config_file: Path,
) -> tuple[tuple[str, ...], str | None, Remedy | None]:
    """Every hook type ``config_file`` needs installed, pre-commit first, or why that is unknown.

    Read from the configuration, since ``pre-commit install`` alone writes only
    the pre-commit hook. A type is needed when a hook's ``stages``,
    ``default_stages`` or ``default_install_hook_types`` names it. A
    configuration that cannot be understood returns a sentence, never
    ``("pre-commit",)``, which would read green over the gap.
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
        # From the dev extra, not a runtime dependency.
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

    A configuration other than the default is named, since the installer points
    every hook it writes at the one it is given.
    """
    words = ["pre-commit", "install"]
    if config_name != _HOOK_CONFIG_DEFAULT:
        words += ["--config", config_name]
    for kind in types:
        words += ["--hook-type", kind]
    # ``shlex.join``, so a name needing quotes comes out quoted.
    return shlex.join(words)


def _remedy_command(root: Path) -> str:
    """The install line for this checkout, naming every type its configuration needs.

    Reads the default configuration, falling back to the pre-commit hook alone
    when it cannot be read.
    """
    types, problem, _remedy = _configured_hook_types(root / _HOOK_CONFIG_DEFAULT)
    return _install_command(types if problem is None else ("pre-commit",))


def _hook_config_name(body: str) -> str:
    """Which configuration file the hook's dispatch line names, or the default.

    Read with ``shlex``, since pre-commit writes the line with ``shlex.join``
    and a quoted path may hold spaces.
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

    It must call pre-commit's hook implementation, for ``hook_type``'s stage,
    against a configuration that exists inside this checkout, since a hook
    pointing elsewhere runs another repository's checks.
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
        # A symlink loop arrives as ``RuntimeError`` from ``Path.resolve``.
        return f"the configuration it names, {named}, cannot be resolved ({exc})"
    if root.resolve() not in resolved.parents and resolved != root.resolve():
        return f"the configuration it names, {named}, is outside {root}"
    if not resolved.is_file():
        return f"the configuration it names, {named}, does not exist"
    return None


def _check_commit_hook(inputs: _Inputs) -> Finding:
    """Whether the repository scan runs as a commit hook in this checkout.

    A secret that reaches a commit needs a history rewrite to remove, and the
    hook exists only once the installer has run. An installed package has no
    checkout, so it gets an INFO note.
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
        # An unreadable marker is not one that names nothing: whether the hook
        # fires is unknown, and unknown is a FAIL.
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
        # An unreadable hook is not a missing one, and not proven present
        # either, since an untraversable directory fails the same way.
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

    # Every other type the configuration this hook dispatches to needs.
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
            # Unreadable is not missing, as for the pre-commit hook above.
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
        # The same configuration as the pre-commit hook, since the types were
        # read from it.
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

    The cutover set is ``tree_registry.cutover_trees``, the one the verb accepts
    (R-787). An unusable template is reported by ``taxonomy.active``, so here it
    costs only the declared list. The loader is imported here, where it is
    read, since it answers for the foreign tree too (U331) and the doctor's
    help would otherwise load that module.
    """
    from cratekit.core import active_taxonomy

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

    Every declared tree is listed, recorded or not, then any undeclared record,
    since a record still routes a writer. A native record a cutover would never
    make (a tree outside the cutover set, or a source no rebuild reproduces) is
    a FAIL naming ``crate tree revert``. An unreadable registry raises, so it is
    never read as every tree on the bridge. Only the record is reported; the
    database itself is the convergence report's.
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


def _release_version(tag: str) -> tuple[int, ...] | None:
    """A ``vX.Y.Z`` tag as a tuple; any tag that is not one is None and ignored."""
    if not tag.startswith("v"):
        return None
    release = _parse_release(tag[1:])
    return release if release is not None and len(release) == 3 else None


def _kept(inputs: _Inputs, origin: InstallOrigin) -> tuple[str, ...]:
    """The extras an upgrade keeps: this copy's, plus ``vocals`` once the library scored (U181).

    So an upgrade does not drop the vocals extra and land rows with no score.
    """
    if VOCALS_EXTRA in origin.extras or not inputs.probes.vocals_scored(inputs.cfg):
        return origin.extras
    return tuple(sorted({*origin.extras, VOCALS_EXTRA}))


def release_upgrade_command(url: str, tag: str, extras: Sequence[str]) -> str:
    """The one pipx command that moves this install to ``tag``, keeping its extras."""
    named = f"cratekit[{','.join(extras)}]" if extras else "cratekit"
    return f'pipx install --force "{named} @ git+{url}@{tag}"'


def _check_install_extras(inputs: _Inputs) -> Finding:
    """Whether the vocal model can score in this copy, and the command if not (U181).

    Uses the vocals module's own probe, so it agrees with ``crate sync land``.
    Never a FAIL, since it runs inside ``crate setup`` and the pass refuses on
    its own in its preflight.
    """
    key, title = "install.extras", "installed extras"
    missing = inputs.probes.vocal_requirement()
    if missing is None:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail="the vocal model can score here, so analysed tracks carry a voxlevel",
        )
    from cratekit.analysis import vocals as vocal_scoring

    kind, said = missing
    if kind != vocal_scoring.MISSING_EXTRA:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"the vocals extra is installed and its model cannot load: {said}. "
                f"Until it can, analysed tracks carry no voxlevel and landed rows "
                f"get no vox My Tag"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"the vocals extra is absent from this copy ({said}), so analysed "
            f"tracks carry no voxlevel and landed rows get no vox My Tag. "
            f"Reinstall with: {vocals_install_command(inputs.probes.install_origin())}"
        ),
    )


def vocals_install_command(origin: InstallOrigin) -> str:
    """The command that adds the vocals extra to this copy, keeping the rest (U181).

    A release install is reinstalled at its own tag; any other install, a
    branch head included, takes the vocals module's own command.
    """
    if origin.kind == "vcs" and origin.url and origin.version and _is_release(origin.version):
        extras = sorted({*origin.extras, VOCALS_EXTRA})
        return release_upgrade_command(origin.url, f"v{origin.version}", extras)
    from cratekit.analysis import vocals as vocal_scoring

    return vocal_scoring.install()


def _is_release(version: str) -> bool:
    """Whether ``version`` is a plain ``X.Y.Z``, the one shape a release tag names."""
    return _release_version(f"v{version}") is not None


#: The extra that carries the vocal model, as ``pyproject.toml`` names it.
VOCALS_EXTRA = "vocals"


def _check_release(inputs: _Inputs) -> Finding:
    """Whether a newer release than this copy is published (U159).

    Never a FAIL, since an older copy still works and this runs inside
    ``crate setup``. A failed read is INFO, never OK, since it did not look.
    """
    key, title = "install.release", "installed release"
    origin = inputs.probes.install_origin()
    move = release_upgrade_command(RELEASE_REPOSITORY, "<tag>", ())
    if origin.kind in ("editable", "folder"):
        what = "an editable checkout" if origin.kind == "editable" else "a folder"
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"this copy was installed from {what}, so the release check does "
                f"not apply. To move to a release install, name the latest tag: {move}"
            ),
        )
    if origin.kind != "vcs" or not origin.url or not origin.version:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                "this copy was not installed from the GitHub repository, so the "
                f"release check does not apply. A release install is: {move}"
            ),
        )
    installed = _parse_release(origin.version)
    tags = inputs.probes.release_tags(origin.url)
    if tags is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"the releases at {origin.url} could not be read (offline, no git "
                f"credentials, or the read timed out), so whether {origin.version} "
                f"is current is unknown"
            ),
        )
    releases = sorted(
        (version, tag) for tag in tags if (version := _release_version(tag)) is not None
    )
    if not releases:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"no release has been published yet; this copy is {origin.version}",
        )
    newest, tag = releases[-1]
    if installed is None:
        # An unparsed version is not behind every release; advising one could
        # be a downgrade.
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"this copy's version {origin.version!r} is not X.Y.Z, so whether "
                f"the latest release, {tag}, is newer is unknown"
            ),
        )
    if installed >= newest:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"this copy is {origin.version}, and the latest release is {tag}",
        )
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"a newer release, {tag}, is published; this copy is {origin.version}. "
            f"Upgrade with: {release_upgrade_command(origin.url, tag, _kept(inputs, origin))}"
        ),
    )


#: The key of doctor's note on runs left at a gate (U186).
OPEN_GATES_CHECK = "runs.open-gates"


#: The key of doctor's note on the ISRC cache (U206).
ISRC_CACHE_CHECK = "provider.isrc-cache"


#: The key of doctor's note on the hour's budget (U278).
BUDGET_CHECK = "provider.budget"


#: The key of doctor's note on the last night pass (U293).
NIGHT_CHECK = "sync.night"


#: The age past which a run counts as left at a gate, since a plan is
#: answered within hours in a sitting.
OPEN_GATE_NOTE_AGE = timedelta(days=1)


def _age_words(age: timedelta) -> str:
    """A whole number of days, or of hours under two days, in words."""
    days = age.days
    if days >= 2:
        return f"{days} days"
    hours = int(age.total_seconds() // 3600)
    return f"{hours} hours"


def _check_open_gates(inputs: _Inputs) -> Finding:
    """Runs blocked at a gate for more than a day, with their verb, gate and age (U186).

    A note, since a stale answer is refused on the write handle. The age is
    read through :func:`gates.old_gate`, as ``crate status`` and ``crate run
    retire`` read it, and an unreadable record is named, never skipped.
    """
    moment = inputs.probes.now
    try:
        records = sorted(gates.run_dir().glob("*.json"))
    except OSError:
        records = []
    blocked: list[gates.OldGate] = []
    unreadable: list[str] = []
    for path in records:
        try:
            state = gates.load(path.stem)
        except Exception:  # noqa: BLE001 - a note never fails; an unread record is named
            unreadable.append(path.stem)
            continue
        aged = gates.old_gate(state, path, older_than=OPEN_GATE_NOTE_AGE, now=moment)
        if aged is not None:
            blocked.append(aged)
    if blocked:
        listed = "; ".join(
            f"{one.run_id} ({one.verb} at {one.gate}, "
            f"{_age_words(moment - datetime.fromisoformat(one.idle_since))})"
            for one in sorted(blocked, key=lambda one: (one.idle_since, one.run_id))
        )
        runs_word = "run has" if len(blocked) == 1 else "runs have"
        detail = (
            f"{len(blocked)} {runs_word} sat at a gate for more than a day: {listed}. "
            f"crate run show describes one, and crate run decide answers it"
        )
    else:
        detail = "no run has sat at a gate for more than a day"
    if unreadable:
        records_word = "record" if len(unreadable) == 1 else "records"
        detail += (
            f"; {len(unreadable)} run {records_word} could not be read "
            f"({', '.join(unreadable)}), so a gate among them is not listed"
        )
    return Finding(key=OPEN_GATES_CHECK, title="runs at a gate", status=Status.INFO, detail=detail)


def _check_isrc_cache(inputs: _Inputs) -> Finding:
    """What the ISRC cache holds, and every file it set aside (U206).

    A note, since the cache only saves calls. The module is imported here so
    doctor loads its matcher only for this note.
    """
    from cratekit.acquire import isrc_cache  # noqa: PLC0415 - see the docstring

    cache = isrc_cache.Cache.from_config(inputs.cfg)
    if not cache.enabled:
        detail = "off: [provider] isrc_cache_days is 0, so every ISRC lookup asks the provider"
    else:
        held = cache.count()
        if held == isrc_cache.UNREADABLE:
            detail = (
                f"{cache.path} could not be read, so every ISRC lookup asks the provider "
                f"until it can be"
            )
        elif held == isrc_cache.UNPARSED:
            detail = (
                f"{cache.path} does not parse; the next ISRC lookup sets it aside and "
                f"starts a fresh one, so there is nothing to do"
            )
        else:
            answers = "answer" if held == 1 else "answers"
            detail = f"{held} ISRC {answers} kept for up to {cache.days} days in {cache.path}"
    aside = cache.set_aside()
    if aside:
        files = "file" if len(aside) == 1 else "files"
        detail += (
            f"; {len(aside)} {files} that could not be parsed were set aside and the "
            f"cache rebuilt: {', '.join(str(one) for one in aside)}. Nothing reads them; "
            f"they may be removed"
        )
    return Finding(key=ISRC_CACHE_CHECK, title="ISRC answers kept", status=Status.INFO, detail=detail)


def _check_night_pass(inputs: _Inputs) -> Finding:
    """The last night pass's one line (U293), what ``crate sync night`` left.

    A note in every state; an unreadable record is said, never shown as no pass.
    """
    from cratekit.cli import sync_night  # noqa: PLC0415 - the verb's own record

    title = "the last night pass"
    try:
        # As things stand now: a wait answered since its firing reads settled.
        record = sync_night.settle(sync_night.read_status(), inputs.cfg)
    except ValueError as exc:
        return Finding(
            key=NIGHT_CHECK,
            title=title,
            status=Status.INFO,
            detail=(
                f"the last night pass's record could not be read: {exc}; the next "
                f"crate sync night writes a new one"
            ),
        )
    if record is None:
        detail = "no night pass has run on this installation; crate sync night runs one"
    else:
        # The latest firing's time, kept under ``firing`` after a refusal.
        firing = record.get("firing") if isinstance(record.get("firing"), dict) else {}
        detail = f"{record['line']} (ended {firing.get('ended') or record.get('ended')})"
    return Finding(key=NIGHT_CHECK, title=title, status=Status.INFO, detail=detail)


def _check_provider_budget(inputs: _Inputs) -> Finding:
    """Where the account stands in the hour, off the one gate (U278).

    Each identity's calls against the budget, the read line, any identity at it
    and any cooldown, from the shared gate file it names. A note, since the gate
    refuses each call itself; an unreadable file is said, never shown as empty.
    """
    settings = (
        provider_gate.GateSettings.from_config(inputs.cfg)
        if inputs.cfg is not None
        else provider_gate.GateSettings()
    )
    budget = settings.calls_per_hour
    read = provider_gate.line_for(settings, reserve=False)
    kept = budget - read
    lines = f"reads stop at {read} and {kept} kept for writes and downloads"
    standing = inputs.probes.provider_standing(inputs.probes.now.timestamp())
    if standing is None:
        detail = (
            f"the provider gate's state file could not be read, so what each identity "
            f"spent in the last hour is not known; each may make {budget} calls an "
            f"hour, {lines}"
        )
        return Finding(key=BUDGET_CHECK, title="the hour's provider budget", status=Status.INFO,
                       detail=detail)
    account = standing.spent(provider_gate.ACCOUNT)
    app = standing.spent(provider_gate.APP)
    said = [
        f"in the last hour {account} of {budget} calls on the account and {app} of "
        f"{budget} under Cratekit's app credentials; {lines}"
    ]
    for identity, spent in ((provider_gate.ACCOUNT, account), (provider_gate.APP, app)):
        if spent >= read:
            who = "the account" if identity == provider_gate.ACCOUNT else "the app credentials"
            frees = provider_gate.iso(standing.frees_at(identity, read))
            said.append(f"{who} is at its read line until {frees}")
    if standing.cooling():
        said.append(
            f"cooling down until {provider_gate.iso(float(standing.lifts_at or 0))}, every "
            f"provider call refused until then"
        )
    else:
        said.append("no cooldown")
    pointer = os.environ.get(config.ENV_PROVIDER_GATE_DIR)
    where = f"read from {standing.path}"
    if pointer:
        where += f", where {config.ENV_PROVIDER_GATE_DIR} points"
    said.append(where)
    return Finding(
        key=BUDGET_CHECK,
        title="the hour's provider budget",
        status=Status.INFO,
        detail="; ".join(said),
    )
