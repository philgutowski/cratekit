"""Doctor's checks of this installation's own state: sessions, the commit hook, trees, the install and its notes.
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
    active_taxonomy,
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
    # ONE SCAN, BRANCHED ON WHAT IT COULD NOT READ (R-1255, review round one):
    # the log itself, unlisted, or records in it. A probe of its own asked the
    # listing a second time, and a window between the two let the record
    # branch name the log directory as a record nobody could read.
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


def _release_version(tag: str) -> tuple[int, ...] | None:
    """A ``vX.Y.Z`` tag as a tuple; any tag that is not one is None and ignored."""
    if not tag.startswith("v"):
        return None
    release = _parse_release(tag[1:])
    return release if release is not None and len(release) == 3 else None


def _kept(inputs: _Inputs, origin: InstallOrigin) -> tuple[str, ...]:
    """The extras an upgrade keeps: this copy's, plus ``vocals`` once the library scored (U181).

    An upgrade from a copy that lost the vocals extra would otherwise install
    without it again, and the next pass would land rows with no score.
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

    Sitting 51 landed a pass from a pipx copy installed with the analysis
    extra and not the vocals one: ``analyze run`` finished every file with a
    key and an energy and no voxlevel, the files took the Camelot head that
    is its resume marker, and the landing plan said so in one line. This row
    says it before the pass does.

    THE ONE TEST IS THE VOCALS MODULE'S OWN, through its probe, so this row
    and the refusal ``crate sync land`` gives agree by construction. A missing
    extra prints the reinstall command with the extras this copy carries plus
    ``vocals``; missing model files print the sentence that names them, since
    a reinstall does not place them.

    NEVER A FAIL, for the reason ``install.release`` gives: this runs inside
    ``crate setup``, and a copy without the vocals extra still runs every verb
    but the score. The pass that would land rows with no score refuses on its
    own, in its preflight.
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

    A release install is reinstalled at its own tag with the extras it carries
    plus ``vocals``, in the form ``install.release`` prints. Any other install
    is the vocals module's own command, which reads pipx's record or names this
    interpreter's pip. A git install whose version is not ``X.Y.Z``, a branch
    head, has no tag of its own to name, so it takes that command too.
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

    NEVER A FAIL. A copy behind the latest release still works, and this check
    runs inside ``crate setup``, which must not refuse a person over it. A newer
    release is INFO carrying the one command that upgrades. A read that fails is
    INFO saying the releases could not be read, and never OK, because a check
    that could not look has not established that the copy is current.
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
        # A version this parser cannot read is not behind every release, and
        # telling it to "upgrade" to an older tag would be a downgrade.
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


#: The key of doctor's note on runs left at a gate (U186), and the age past
#: which a run counts as left there. A day, because a plan answered within
#: a sitting is answered within hours, and sitting 51 left two runs blocked
#: that nobody went back to.
OPEN_GATES_CHECK = "runs.open-gates"


#: The key of doctor's note on the ISRC cache (U206).
ISRC_CACHE_CHECK = "provider.isrc-cache"


#: The key of doctor's note on the hour's budget (U278).
BUDGET_CHECK = "provider.budget"


#: The key of doctor's note on the last night pass (U293).
NIGHT_CHECK = "sync.night"


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

    A NOTE AND NEVER A FAILURE: a run left at a gate costs nothing until
    somebody answers a plan the library has moved past, and that answer is
    refused stale on the write handle. Doctor says it so a person finds the
    run before a second session plans over the same rows.

    The age is :func:`gates.idle_since`, the one ``crate status`` and ``crate
    run retire`` read through :func:`gates.old_gate`, so the three never
    disagree about which run is old. A record that cannot be read is named in
    the note rather than skipped, since an unread record is not a record
    without a gate.
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

    A NOTE AND NEVER A FAILURE: the cache is a saving, and a file it could not
    parse costs calls and no data. Doctor names a set aside file so a person
    knows why the provider was asked again, and may remove it. The module is
    imported here, so a doctor run loads the matcher it keys by only to answer
    this note.
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

    A NOTE AND NEVER A FAILURE, in every state: a night that waits at the
    landing's gate is the pass working as meant, and one that stopped or was
    refused says why in its own line. A record that cannot be read is said,
    never shown as no night pass having run.
    """
    from cratekit.cli import sync_night  # noqa: PLC0415 - the verb's own record

    title = "the last night pass"
    try:
        # AS THINGS STAND NOW (review round one): a wait answered or landed
        # since its firing reads as settled, never as still waiting.
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
        # THE LATEST FIRING'S TIME (review round two): a record kept over a
        # refusal carries the refusal's own under ``firing``.
        firing = record.get("firing") if isinstance(record.get("firing"), dict) else {}
        detail = f"{record['line']} (ended {firing.get('ended') or record.get('ended')})"
    return Finding(key=NIGHT_CHECK, title=title, status=Status.INFO, detail=detail)


def _check_provider_budget(inputs: _Inputs) -> Finding:
    """Where the account stands in the hour, off the one gate (U278).

    Each identity's calls in the last sixty minutes against the hour's budget,
    the line a read stops at and what is kept for writes and downloads, an
    identity at its read line with the time it frees, and any cooldown with the
    time it lifts. Read from the gate every installation state pointed at the
    account shares, and its file named, so a copy run's doctor shows the live
    hour. A NOTE AND NEVER A FAILURE: the gate itself refuses each call past a
    line, and doctor's job is to say so before a person starts one. A file
    that could not be read is said, never shown as an hour with nothing spent.
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
