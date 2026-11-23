"""``crate setup``: clone to first write, without help.

The one interactive verb (``interactive=True`` in the registry, asserted by
``tests/test_cli_contract.py``); even so, standard input is read only in
``cli/prompt.py``. It produces the six required configuration keys, the
taxonomy, the profile and the credentials.

Every answer comes from a flag, the existing configuration, a derived probe,
then a question, in that order, so a re-run changes only what it was asked to
and a fully flagged run never prompts. A configuration that cannot be
understood refuses rather than being replaced. The volume identity is derived
once, from a volume actually mounted where the root goes (an empty mount slot
is refused, since the walk would otherwise record the boot disk), and kept
unless the user names a new one. Nothing library scoped is written before the
volume is asserted. The rekordbox pin is proposed, never adopted. The verb ends
by running doctor and exits on its verdict, with the configuration saved
either way.
"""

from __future__ import annotations

import argparse
import copy
import tomllib
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import doctor, output, prompt, registry, render
from cratekit.cli.output import Envelope
from cratekit.core import (
    config,
    preflight,
    processes,
    profiles,
    rb_writer,
    secrets,
    taxonomy,
    taxonomy_upgrade,
)
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import searchers

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

#: Default staging folder, on the library volume so the move into the library
#: is a rename and a half finished download cannot fill the boot disk.
STAGING_DIRNAME = "Downloads"


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    """Every answer is also a flag, so the whole wizard is scriptable and testable."""
    parser.add_argument("--library-root", help="the directory holding the music library")
    parser.add_argument("--db-path", help="the rekordbox database this library uses")
    parser.add_argument(
        "--volume-id",
        help="the library volume's own identity, a UUID or serial and never a mount path",
    )
    parser.add_argument("--staging", help="where fresh downloads land before they are moved")
    parser.add_argument(
        "--processed-dir",
        help=(
            "the folder under the music folder where intake shelve files an imported "
            f"batch, by year and date (default: {config.DEFAULT_PROCESSED_DIR})"
        ),
    )
    parser.add_argument("--profile", choices=profiles.PROFILE_NAMES, help="the module preset")
    # A closed set, so a mistyped name never reaches the file. ``or None`` is
    # load bearing: this runs for every verb, and an install with no readable
    # templates must offer no closed set rather than an empty one that rejects
    # every value; the wizard then reports the missing template.
    parser.add_argument(
        "--taxonomy",
        choices=taxonomy.shipped_template_names() or None,
        help="which shipped taxonomy template to adopt",
    )
    # The rclone targets, spelled remote:path; a bare folder name is refused
    # rather than handed to rclone as a local path (R-345).
    parser.add_argument(
        "--backup-dest",
        help="where the library mirror goes, as an rclone remote:path",
    )
    parser.add_argument(
        "--backup-archive-root",
        help="where dated archives of changed files go, as an rclone remote:path",
    )
    parser.add_argument(
        "--backup-db-dest-root",
        help="where database snapshots go, as an rclone remote:path",
    )
    # Derived from the three above and never asked, but a file can spell one
    # that disagrees, so this flag replaces it (R-662).
    parser.add_argument(
        "--backup-remote",
        help="the rclone remote the three destinations name, replacing a recorded one",
    )
    # A recorded Discogs token is left alone unless this is passed; a
    # replacement Discogs does not accept keeps the recorded one (U283).
    parser.add_argument(
        RELINK_FLAG,
        dest="relink_discogs",
        action="store_true",
        help="offer to replace the recorded Discogs token, checking the new one first",
    )
    parser.set_defaults(_handler=setup)


# ---------------------------------------------------------------------------
# The shipped taxonomy templates
# ---------------------------------------------------------------------------


def template_names() -> tuple[str, ...]:
    """Every taxonomy template that ships in the wheel, by its short name.

    The walk lives in ``core/taxonomy`` so doctor, which this module imports,
    checks against the same list the wizard offers (P3, R19).
    """
    return taxonomy.shipped_template_names()


def template_text(name: str) -> str:
    """The packaged text of one template. Raises when the name is not shipped."""
    return taxonomy.shipped_template_text(name)


# ---------------------------------------------------------------------------
# Reading what is already there
# ---------------------------------------------------------------------------


def _refuse(
    message: str,
    *,
    remedy: Remedy,
    detail: Mapping[str, Any] | None = None,
    reason: str = "config-unusable",
) -> CratekitError:
    """A refusal from the wizard; ``reason`` lets a library fact carry its own slug."""
    return CratekitError(
        Cause(
            reason=reason,
            message=message,
            remediation=Remediation(remedy=remedy),
            scope=Scope.RUN,
            origin=("cli.setup",),
            detail=dict(detail or {}),
        )
    )


def _act(exc: BaseException, otherwise: str) -> str:
    """The closing clause by kind of refusal, from ``render.access_note``, else ``otherwise``."""
    note = render.access_note(exc)
    return f" {note}" if note is not None else f" {otherwise}"


def _unreachable_root(root: str, exc: OSError) -> str:
    """The sentence for a library root behind a directory this account cannot open.

    Shared by both mount questions so they say it one way. On macOS this is a
    routine first run state (EPERM without Full Disk Access), so it is a
    refusal in plain words, never an internal error.
    """
    return (
        f"{root} could not be examined: {exc}. A directory on the way to it "
        f"cannot be opened by this account, so which volume the library would "
        f"sit on was not established and nothing was recorded. This is not a "
        f"defect and it is not a missing drive."
    ) + _act(exc, "Choose a library root this account can already reach")


def existing_document() -> tuple[dict[str, Any], str]:
    """The configuration this run is completing, and one word for where it came from.

    A config that loads is returned in its effective, migrated form (P2); one
    that is merely incomplete is read raw and completed; anything else, corrupt
    or from a newer build, refuses, since overwriting it destroys answers.
    """
    try:
        return dict(config.load().to_toml_dict()), "existing"
    except config.ConfigMissing:
        return {}, "new"
    except config.ConfigInvalid:
        pass
    except config.ConfigError as exc:
        raise _refuse(
            f"setup will not overwrite this configuration: {exc}",
            remedy=Remedy(str(exc.remedy)),
        ) from exc

    # Incomplete: read it for the answers it holds. This second read can
    # disagree with the first if the file changed between them, and it must
    # then refuse rather than treat the document as empty.
    path = config.config_path()
    try:
        with path.open("rb") as handle:
            raw = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        # ``from exc`` lets the refusal overrule the repair token when the
        # system refused access, since an unreadable file is still intact.
        raise _refuse(
            f"setup will not overwrite a configuration it cannot read: {exc}",
            remedy=Remedy.REPAIR_CONFIG_FILE,
        ) from exc
    if not isinstance(raw, dict):  # pragma: no cover - tomllib always yields a table
        raise _refuse(
            f"{path} does not hold a table at its top level",
            remedy=Remedy.REPAIR_CONFIG_FILE,
        )
    # Migrated before it is completed, like the loaded branch, or an older
    # incomplete file gets the current version stamped on unmigrated data.
    try:
        return dict(config.migrate(raw)), "incomplete"
    except config.ConfigError as exc:
        raise _refuse(
            f"setup will not overwrite this configuration: {exc}",
            remedy=Remedy(str(exc.remedy)),
        ) from exc


def _get(document: Mapping[str, Any], dotted: str) -> Any:
    node: Any = document
    for part in dotted.split("."):
        if not isinstance(node, Mapping) or part not in node:
            return None
        node = node[part]
    return node


def _put(document: dict[str, Any], dotted: str, value: Any) -> None:
    """Set a dotted key, creating the tables above it; an undotted key is top level."""
    head, _, tail = dotted.rpartition(".")
    node = document
    for part in head.split(".") if head else ():
        child = node.get(part)
        if not isinstance(child, dict):
            child = {}
            node[part] = child
        node = child
    node[tail] = value


# ---------------------------------------------------------------------------
# Resolving one answer
# ---------------------------------------------------------------------------


class _Wizard:
    """One run of the wizard: what it asked, what it kept, what it derived.

    How each value was reached is kept, because "changed nothing" and
    "re-answered everything" look identical in the file.
    """

    def __init__(self, document: dict[str, Any], prompter: prompt.Prompter) -> None:
        self.document = document
        self.prompter = prompter
        self.notes: list[doctor.Finding] = []
        self.asked: list[str] = []

    def note(
        self,
        key: str,
        title: str,
        status: doctor.Status,
        detail: str,
        remedy: Remedy | None = None,
        *,
        error: BaseException | None = None,
    ) -> None:
        """Record one answer; ``error``, when given, lets the finding classify its remedy."""
        self.notes.append(
            doctor.Finding(
                key=key,
                title=title,
                status=status,
                detail=detail,
                remedy=remedy,
                error=error,
            )
        )

    def resolve(
        self,
        dotted: str,
        *,
        flag: str | None,
        question: str,
        default: str | None = None,
        probe: Callable[[], str | None] | None = None,
        choices: Sequence[str] | None = None,
    ) -> str:
        """A flag, then what is recorded, then a probe's default, then a question.

        An unanswerable question falls back to the default, or refuses naming
        the flag when there is none, never guessing. ``probe`` is a callable so
        it runs only when needed. A closed set is checked against every source;
        a recorded value outside it is treated as unanswered so a re-run repairs
        it.
        """
        if flag:
            if choices is not None and flag not in choices:
                raise _refuse(
                    f"{dotted} was given as {flag!r}, which is not one of "
                    f"{', '.join(choices)}",
                    remedy=Remedy.FIX_COMMAND_LINE,
                    detail={"key": dotted, "given": flag, "choices": list(choices)},
                )
            self.asked.append(f"{dotted} (from the command line)")
            return flag
        recorded = _get(self.document, dotted)
        if isinstance(recorded, str) and recorded.strip():
            if choices is None or recorded in choices:
                return recorded
            self.note(
                f"setup.{dotted}",
                f"recorded {dotted}",
                doctor.Status.INFO,
                (
                    f"the recorded value {recorded!r} is not one of "
                    f"{', '.join(choices)} and was replaced rather than kept; a "
                    f"value outside the set cannot be corrected by any flag this "
                    f"verb offers"
                ),
            )
        if default is None and probe is not None:
            default = probe()
        if choices is not None and default not in choices:
            raise ValueError(
                f"{dotted} offers a closed set of answers and {default!r} is not "
                f"one of them; a default outside the set cannot be accepted by "
                f"pressing return, which is the only thing a default is for"
            )
        try:
            if choices is not None:
                answer = self.prompter.choose(question, list(choices), default=str(default))
            else:
                answer = self.prompter.ask(question, default=default)
        except prompt.PromptUnavailable as exc:
            if default is None:
                raise _refuse(
                    f"{dotted} has no recorded value and no question could be asked "
                    f"({exc}). Supply it on the command line and re-run",
                    remedy=Remedy.RUN_SETUP,
                    detail={"key": dotted},
                ) from exc
            self.asked.append(f"{dotted} (derived, nothing could be asked)")
            return default
        self.asked.append(f"{dotted} (answered)")
        return answer

    def optional(self, question: str, *, default: bool = False) -> bool:
        """A yes or no where silence is a no, for proposals the product may not make alone."""
        try:
            return self.prompter.confirm(question, default=default)
        except prompt.PromptUnavailable:
            return False


# ---------------------------------------------------------------------------
# The steps
# ---------------------------------------------------------------------------


def _probe_db_path() -> str | None:
    """Where rekordbox's own settings say its database is, as a proposed default.

    Read from rekordbox rather than a hardcoded layout (R1), and only offered
    as a default; the database is never opened. Any reader failure means no
    proposal, since this is a third party reader over a private format. A path
    that cannot be stat'ed is still proposed, since could not look is not absent.
    """
    try:
        settings = rb_writer.read_rekordbox_settings()
    except Exception:  # noqa: BLE001 - see the docstring
        return None
    recorded = settings.get("db_path") if isinstance(settings, Mapping) else None
    if not (isinstance(recorded, str) and recorded.strip()):
        return None
    try:
        present = Path(recorded).exists()
    except OSError:
        return recorded
    return recorded if present else None


def _resolve_volume_id(
    wizard: _Wizard, root: str, flag: str | None, machine: doctor.Probes
) -> str:
    """The library's identity: named, kept, or read off the volume holding it.

    Never re-derived, since that would record whatever disk is mounted, a
    restored clone included. Never derived through an empty mount slot, since
    the walk would then read the boot disk: ``preflight.identity_source`` asks
    whether a volume is mounted at each mount location on the way down. The
    provider comes from the run's ``Probes`` so doctor reads the same volume.
    """
    recorded = _get(wizard.document, "library.volume_id")
    if not flag and isinstance(recorded, str) and recorded.strip():
        return recorded
    if flag:
        wizard.asked.append("library.volume_id (from the command line)")
        return flag
    provider = machine.identity_provider or preflight.default_identity_provider()
    try:
        slots = preflight.mount_location_ancestors(Path(root))
        source = preflight.identity_source(Path(root))
    except OSError as exc:
        # A refusal under its own slug, not a traceback; ``path`` as well as
        # ``root`` so consumers read the path the same way under any slug.
        raise _refuse(
            _unreachable_root(root, exc),
            remedy=Remedy.GRANT_PATH_ACCESS,
            detail={"key": "library.volume_id", "root": root, "path": root},
            reason="library-root-unreachable",
        ) from exc
    if source is None:
        empty = ", ".join(str(slot) for slot in slots)
        raise _refuse(
            f"{root} sits under {empty}, which is where this platform mounts a "
            f"volume, and no volume is mounted there right now. The identity a "
            f"read would find belongs to the filesystem ABOVE that point rather "
            f"than to the disk this library will sit on, and recording it would "
            f"make every destructive refusal pass against the wrong disk. Attach "
            f"the library volume and run setup again, or supply the identity "
            f"with --volume-id",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            detail={
                "key": "library.volume_id",
                "root": root,
                "empty_mount_points": [str(slot) for slot in slots],
            },
            reason="library-volume-unmounted",
        )
    observed = provider(source)
    if observed:
        wizard.asked.append("library.volume_id (read from the mounted volume)")
        return observed
    return wizard.resolve(
        "library.volume_id",
        flag=None,
        question=(
            "This platform reports no volume identity. Enter one for this library "
            "(a UUID or serial, never a mount path)"
        ),
    )


#: The question per destination, keyed as the validator keys them.
_BACKUP_QUESTIONS: Mapping[str, str] = {
    "backup.dest": "Where should the library mirror go (rclone remote:path)",
    "backup.archive_root": (
        "Where should dated archives of changed files go (rclone remote:path)"
    ),
    "backup.db_dest_root": "Where should database snapshots go (rclone remote:path)",
}


def _backup_flags(args: argparse.Namespace) -> dict[str, str | None]:
    """The three destination flags, keyed like the configuration keys."""
    return {
        "backup.dest": args.backup_dest,
        "backup.archive_root": args.backup_archive_root,
        "backup.db_dest_root": args.backup_db_dest_root,
    }


def _resolve_backup(
    wizard: _Wizard,
    document: dict[str, Any],
    args: argparse.Namespace,
    machine: doctor.Probes,
) -> None:
    """Ask for the three rclone destinations when the backup module is on (R-345).

    Flags are recorded first whatever the profile says. What is still missing
    is offered as one yes or no rather than demanded, so a scripted run on a
    full profile does not refuse; a no records nothing and doctor reports it.
    ``backup.remote`` is derived from the destinations, never asked, unless
    ``--backup-remote`` replaces a disagreeing one (R-662). Membership is read
    off the raw document, filtered to known modules so a misspelled module is
    left for ``validate`` to report.
    """
    flags = _backup_flags(args)
    for key, flag in flags.items():
        if flag:
            _put(document, key, wizard.resolve(key, flag=flag, question=""))
    if args.backup_remote:
        _put(
            document,
            "backup.remote",
            wizard.resolve("backup.remote", flag=args.backup_remote, question=""),
        )

    def recorded(key: str) -> bool:
        value = _get(document, key)
        return isinstance(value, str) and bool(value.strip())

    missing = [key for key in config.BACKUP_DESTINATION_KEYS if not recorded(key)]
    modules = document.get("modules") or {}
    membership = profiles.resolve(
        str(_get(document, "profile.name")),
        {k: bool(v) for k, v in modules.items() if k in profiles.MODULES}
        if isinstance(modules, Mapping)
        else {},
    )
    if "backup" not in membership.modules:
        wizard.note(
            "setup.backup",
            "backup destinations",
            doctor.Status.INFO,
            "the backup module is off in this profile, so no destination was asked for",
        )
    elif missing and not wizard.optional(
        f"The backup module is on and {len(missing)} destination"
        f"{'s are' if len(missing) != 1 else ' is'} not recorded "
        f"({', '.join(missing)}). Record {'them' if len(missing) != 1 else 'it'} now?"
    ):
        wizard.note(
            "setup.backup",
            "backup destinations",
            doctor.Status.INFO,
            (
                f"{', '.join(missing)} not recorded and not entered; the backup verb "
                f"refuses until every destination names an rclone remote as "
                f"remote:path, and doctor reports the unset remote. Re-run setup, "
                f"or supply --backup-dest, --backup-archive-root and "
                f"--backup-db-dest-root"
            ),
        )
    else:
        for key in missing:
            _put(document, key, wizard.resolve(key, flag=None, question=_BACKUP_QUESTIONS[key]))

    if not args.backup_remote:
        _replace_a_remote_rclone_lacks(wizard, document, machine)
    derived = config.derived_backup_remote(document)
    if derived is not None:
        _put(document, "backup.remote", derived)


def _replace_a_remote_rclone_lacks(
    wizard: _Wizard, document: dict[str, Any], machine: doctor.Probes
) -> None:
    """Replace a spelled remote the destinations disagree with, when rclone lacks it.

    Only when rclone's configuration was read, lacks the spelled name and has
    the destinations' name, so a replacement never guesses between unknowns;
    otherwise validation refuses naming the flag. Same lookup as doctor's.
    """
    disagreement = config.backup_remote_disagreement(document)
    if disagreement is None:
        return
    spelled, expected = disagreement
    rclone = machine.find_binary("rclone")
    remotes = machine.rclone_remotes(rclone) if rclone is not None else None
    if remotes is None or spelled.split(":", 1)[0] in remotes or expected not in remotes:
        return
    _put(document, "backup.remote", expected)
    wizard.note(
        "setup.backup.remote",
        "backup remote",
        doctor.Status.INFO,
        (
            f"backup.remote was {spelled!r}, which rclone has no remote by, and "
            f"every backup destination names {expected!r}, so it was replaced "
            f"with {expected!r}"
        ),
    )


def _answers_remediation(document: Mapping[str, Any], problems: Sequence[str]) -> Remediation:
    """What a refusal of this run's answers tells a person to do.

    ``crate setup`` for most problems. A disagreeing spelled remote (R-662)
    leads with the replacing flag instead, since a bare re-run would refuse
    again, and drops the token when it is the only problem, because the fix
    line prefers the token's words.
    """
    disagreement = config.backup_remote_disagreement(document)
    if disagreement is None:
        return Remediation(remedy=Remedy.RUN_SETUP, steps=tuple(problems))
    spelled, expected = disagreement
    steps = (
        f"re-run crate setup with --backup-remote {expected} to record the remote "
        f"the destinations name, or give --backup-dest, --backup-archive-root "
        f"and --backup-db-dest-root under {spelled.split(':', 1)[0]!r} if that "
        f"is the remote meant",
        *problems,
    )
    if len(problems) > 1:
        return Remediation(remedy=Remedy.RUN_SETUP, steps=steps)
    return Remediation(steps=steps)


def _seed_taxonomy(wizard: _Wizard, cfg: config.Config, machine: doctor.Probes) -> None:
    """Copy the chosen template beside the database, once (S6).

    The active copy makes the library self describing and rolls back with its
    snapshot. The volume is asserted before the write, since a write onto the
    wrong filesystem leaves a stray mount point and unsnapshotted state.
    ``resolve_mount_state`` gives a diagnosis the suite can see, judged by
    ``preflight.library_state_may_be_written``, which unlike doctor's read rule
    allows a matching identity with an absent root and an unavailable identity
    (P7). Every failure is a note, never an abort.
    """
    try:
        status = preflight.resolve_mount_state(
            cfg.library.root,
            cfg.library.volume_id,
            identity_provider=machine.identity_provider,
            mount_enumerator=machine.mount_enumerator,
        )
    except OSError as exc:
        # A note, not a raise: the configuration is already saved. Reached only
        # when ``--volume-id`` skipped the derive that raises for this.
        wizard.note(
            "setup.taxonomy",
            "active taxonomy template",
            doctor.Status.FAIL,
            f"nothing was written under {cfg.library.root}: "
            + _unreachable_root(str(cfg.library.root), exc),
            Remedy.GRANT_PATH_ACCESS,
            error=exc,
        )
        return
    if not preflight.library_state_may_be_written(status):
        wizard.note(
            "setup.taxonomy",
            "active taxonomy template",
            doctor.Status.FAIL,
            (
                f"nothing was written under {cfg.library.root}: this run could not "
                f"establish that the volume there is the one recorded for this "
                f"library ({status.state.value}, recorded "
                f"{status.recorded_identity}, observed "
                f"{status.observed_identity or 'no identity'}). The active "
                f"template is state that belongs to the library, and writing it "
                f"anyway would put it on whichever filesystem is at that path"
            ),
            Remedy.MOUNT_LIBRARY_VOLUME,
        )
        return
    name = cfg.taxonomy.template
    path = config.state_path("taxonomy_active", cfg)
    # Not present and could not look are different answers, asked as doctor
    # asks: the directory could not be listed, the name is not in a listed set,
    # or the named template ships and its text could not be read.
    shipped, unlistable = taxonomy.shipped_templates()
    if unlistable is not None:
        wizard.note(
            "setup.taxonomy",
            "active taxonomy template",
            doctor.Status.FAIL,
            (
                f"{unlistable}. Whether a template named {name!r} ships was "
                f"therefore not established and nothing was copied beside the "
                f"database. This is a damaged or partial install rather than a "
                f"configuration error, so re-running setup would not repair it"
            ),
            Remedy.REPORT_DEFECT,
        )
        return
    if name not in shipped:
        wizard.note(
            "setup.taxonomy",
            "active taxonomy template",
            doctor.Status.FAIL,
            f"no shipped template is named {name!r}; shipped: {', '.join(shipped)}",
            Remedy.FIX_CONFIG_VALUES,
        )
        return
    try:
        text = template_text(name)
    except (OSError, UnicodeDecodeError) as exc:
        # Listed but unreadable packaged data; re-running setup cannot repair it.
        wizard.note(
            "setup.taxonomy",
            "active taxonomy template",
            doctor.Status.FAIL,
            (
                f"the template {name!r} ships and its packaged text could not be "
                f"read ({exc}), so nothing was copied beside the database. This "
                f"is a damaged or partial install rather than a configuration "
                f"error, so re-running setup would not repair it"
            ),
            Remedy.REPORT_DEFECT,
        )
        return
    # Both calls below can raise, and each gets its own handler: a path this
    # account could not look at differs from one it reached and could not write.
    try:
        already_there = path.exists()
    except OSError as exc:
        wizard.note(
            "setup.taxonomy",
            "active taxonomy template",
            doctor.Status.FAIL,
            (
                f"nothing was copied beside the database: {path} could not be "
                f"examined ({exc}). A directory on the way to it cannot be opened "
                f"by this account, so whether the library already carries its own "
                f"template was not established and nothing was written. This is "
                f"not a defect."
            )
            + _act(exc, "Choose a library root this account can already reach"),
            Remedy.GRANT_PATH_ACCESS,
            error=exc,
        )
        return
    if already_there:
        wizard.note(
            "setup.taxonomy",
            "active taxonomy template",
            doctor.Status.INFO,
            f"{path} already exists and was left alone; the library's own copy wins",
        )
        return
    try:
        config.atomic_write_bytes(text.encode("utf-8"), path)
    except OSError as exc:
        wizard.note(
            "setup.taxonomy",
            "active taxonomy template",
            doctor.Status.FAIL,
            (
                f"the template {name!r} could not be written to {path} ({exc}), so "
                f"nothing was copied beside the database and this library does not "
                f"describe its own tree. The location WAS reached and the write "
                f"was refused, which is a state of this machine rather than a "
                f"defect, and it is not something a second run of setup repairs."
            )
            + _act(exc, "Choose a library root this account can already write"),
            Remedy.GRANT_PATH_ACCESS,
            error=exc,
        )
        return
    # The origin record goes with a fresh copy only, so doctor can tell a stale
    # copy from an edited one (R-689). A failed record leaves the copy in place.
    origin = config.state_path("taxonomy_origin", cfg)
    try:
        config.atomic_write_bytes(taxonomy.origin_record_text(name, text).encode("utf-8"), origin)
    except OSError as exc:
        wizard.note(
            "setup.taxonomy",
            "active taxonomy template",
            doctor.Status.INFO,
            (
                f"template {name!r} copied to {path}, and the record of which "
                f"shipped text it was copied from could not be written to "
                f"{origin} ({exc}), so doctor will not be able to tell this copy "
                f"falling behind the shipped template from an edit. No remedy is "
                f"named: a second run of setup leaves the copy alone and writes "
                f"no record for it"
            ),
        )
        return
    wizard.note(
        "setup.taxonomy",
        "active taxonomy template",
        doctor.Status.OK,
        f"template {name!r} copied to {path}, its origin recorded at {origin}",
    )


def _refuse_a_database_that_is_not_one(cfg: config.Config) -> None:
    """Refuse, writing nothing, a database path whose copy is not a library (R-663).

    The judgement is ``rb_writer.read_only_copy``'s, on a copy. Only its "not a
    library" refusal stops the verb; a missing file, rekordbox running or any
    other failure is left to the notes and to doctor.
    """
    source = Path(cfg.library.db_path)
    try:
        if not source.is_file():
            return
    except OSError:
        return
    try:
        if rb_writer.rekordbox_processes_running():
            return
    except processes.AbsenceUnconfirmed:
        # No whole copy over an unconfirmed absence either (U211).
        return
    try:
        with rb_writer.read_only_copy(source, cfg=cfg):
            pass
    except CratekitError as exc:
        if exc.cause.reason == "library-database-not-rekordbox":
            raise
    except OSError:
        pass


def _propose_pin(wizard: _Wizard, document: dict[str, Any], cfg: config.Config) -> bool:
    """Offer the installed rekordbox version as the pin. Return whether it was taken.

    Recorded only on a yes (S2). ``rekordbox.validated_on`` is never written,
    since this verb has made no real write to confirm the pin against.
    """
    if cfg.rekordbox.pinned_app_version:
        wizard.note(
            "setup.pin",
            "rekordbox application pin",
            doctor.Status.INFO,
            f"already pinned at {cfg.rekordbox.pinned_app_version}; left alone",
        )
        return False
    installed = rb_writer.read_installed_app_version(cfg=cfg)
    if not installed:
        wizard.note(
            "setup.pin",
            "rekordbox application pin",
            doctor.Status.INFO,
            (
                "no installed rekordbox application could be located, so there is "
                "nothing to propose. Every database write refuses until a pin is "
                "recorded, which is the point of an unset pin"
            ),
        )
        return False
    if not wizard.optional(
        f"rekordbox {installed} is installed. Record it as the version pin?"
    ):
        wizard.note(
            "setup.pin",
            "rekordbox application pin",
            doctor.Status.INFO,
            (
                f"rekordbox {installed} is installed and was NOT recorded as the "
                f"pin. A pin copied from whatever happens to be installed refuses "
                f"nothing, forever, so it is only ever recorded on a deliberate yes"
            ),
        )
        return False
    _put(document, "rekordbox.pinned_app_version", installed)
    wizard.note(
        "setup.pin",
        "rekordbox application pin",
        doctor.Status.OK,
        (
            f"pinned at {installed} by an explicit answer. The date it was "
            f"confirmed against a real write is still unset, and doctor reports it"
        ),
    )
    return True


def _propose_prefix_map(wizard: _Wizard, document: dict[str, Any], cfg: config.Config) -> bool:
    """Read rekordbox's recorded drive names off a copy and offer the rule (R-372).

    rekordbox keeps rows under the drive they were imported with and remaps
    through ``BaseDBDrive`` and ``CurrentDBDrive``; the live database is never
    opened. ``from`` is the base drive; ``to`` is the current drive when it
    differs, else the library root, written as the ``{library.root}`` token. A
    root already under the base drive needs no rule. A recorded map, a missing
    file, rekordbox running, or a copy that fails each offers nothing with a
    note. Adopted only on a deliberate yes.
    """
    recorded = _get(document, "library.location_prefix_map")
    if isinstance(recorded, list) and recorded:
        wizard.note(
            "setup.prefix_map",
            "location prefix map",
            doctor.Status.INFO,
            f"library.location_prefix_map already records {len(recorded)} rule"
            f"{'s' if len(recorded) != 1 else ''}; left alone",
        )
        return False
    source = Path(cfg.library.db_path)
    try:
        present = source.is_file()
    except OSError as exc:
        wizard.note(
            "setup.prefix_map",
            "location prefix map",
            doctor.Status.INFO,
            (
                f"{source} could not be examined ({exc}), so no drive rule was "
                f"read from it and none was offered; doctor reports whether the "
                f"collection's rows resolve"
            ),
            error=exc,
        )
        return False
    if not present:
        wizard.note(
            "setup.prefix_map",
            "location prefix map",
            doctor.Status.INFO,
            (
                f"no database file at {source}, so no drive rule was read and none "
                f"was offered; run setup again once the database is there, and "
                f"doctor reports whether the collection's rows resolve"
            ),
        )
        return False
    try:
        running = rb_writer.rekordbox_processes_running()
    except processes.AbsenceUnconfirmed as exc:
        # Treated as rekordbox running, said as unknown (U211).
        wizard.note(
            "setup.prefix_map",
            "location prefix map",
            doctor.Status.INFO,
            (
                f"{exc.cause.message}, so no copy of the database was taken and no "
                f"drive rule was offered; run setup again once it clears"
            ),
        )
        return False
    if running:
        wizard.note(
            "setup.prefix_map",
            "location prefix map",
            doctor.Status.INFO,
            (
                f"{running} running, and a copy of the database taken under a live "
                f"application is incomplete, so none was taken and no drive rule "
                f"was offered; quit it and run setup again"
            ),
        )
        return False
    try:
        with rb_writer.read_only_copy(source, cfg=cfg) as db:
            base, current = rb_writer.recorded_db_drives(db)
    except CratekitError as exc:
        cause = exc.cause
        wizard.note(
            "setup.prefix_map",
            "location prefix map",
            doctor.Status.INFO,
            (
                f"the database could not be read from a copy, {cause.message}, so "
                f"no drive rule was read and none was offered; doctor reports the "
                f"condition under its own cause and whether the collection's rows "
                f"resolve"
            ),
            error=exc,
        )
        return False
    except OSError as exc:
        # The copy itself failed; a note, since the answers are not yet saved.
        wizard.note(
            "setup.prefix_map",
            "location prefix map",
            doctor.Status.INFO,
            (
                f"{source} could not be copied for a read only look ({exc}), so no "
                f"drive rule was read and none was offered; doctor reports whether "
                f"the collection's rows resolve."
            )
            + _act(exc, "Nothing was written and the live database was not opened"),
            error=exc,
        )
        return False
    root = str(cfg.library.root).rstrip("/") or str(cfg.library.root)
    if base is None:
        wizard.note(
            "setup.prefix_map",
            "location prefix map",
            doctor.Status.INFO,
            (
                f"the database records no drive it was made on (current drive "
                f"{current or 'not recorded'}), so no rule can be read from it"
            ),
        )
        return False
    if root == base or root.startswith(base + "/"):
        wizard.note(
            "setup.prefix_map",
            "location prefix map",
            doctor.Status.INFO,
            (
                f"the database records its rows under {base} and the configured "
                f"library root {root} sits under it, so no prefix rule is needed"
            ),
        )
        return False
    # The current drive when it differs from the base, else the configured root,
    # spelled as the token so the rule follows the root.
    target = current if current is not None and current != base else root
    spelled = config.LIBRARY_ROOT_TOKEN if target == root else target
    if not wizard.optional(
        f"rekordbox records this library's paths under {base}, and the library is "
        f"at {target} today. Record the rule mapping {base} to {spelled} in "
        f"library.location_prefix_map?"
    ):
        wizard.note(
            "setup.prefix_map",
            "location prefix map",
            doctor.Status.INFO,
            (
                f"the rule mapping {base} to {spelled} was offered and NOT recorded. "
                f"Every row rekordbox recorded under {base} stays unresolved until "
                f"it is, and the My Tags plan and doctor refuse over a majority of "
                f"them"
            ),
        )
        return False
    _put(document, "library.location_prefix_map", [{"from": base, "to": spelled}])
    wizard.asked.append("library.location_prefix_map (answered)")
    wizard.note(
        "setup.prefix_map",
        "location prefix map",
        doctor.Status.OK,
        (
            f"rule recorded by an explicit answer: paths under {base} resolve under "
            f"{spelled}, read from the database's own BaseDBDrive and CurrentDBDrive"
        ),
    )
    return True


def _capture_credentials(wizard: _Wizard, cfg: config.Config) -> None:
    """Offer to record each credential this profile's verbs may spend, Discogs aside.

    Values are read unechoed through ``cli/prompt``; what is offered follows
    doctor's own registry question. A refusal is a note carrying its own remedy,
    never a raise, since this runs after ``config.save``.
    """
    membership = profiles.resolve(cfg.profile.name, dict(cfg.modules.explicit))
    for key in sorted(doctor.CREDENTIALS_BY_CHECK):
        # Discogs is its own step, :func:`_link_discogs` (U283).
        if key == DISCOGS_CHECK:
            continue
        if not doctor.offered(key, membership):
            continue
        # Keyed by credential, since one check covers two and keys must be unique.
        for name in doctor.CREDENTIALS_BY_CHECK[key]:
            try:
                already = secrets.exists(str(name))
            except CratekitError as exc:
                cause = exc.cause
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.FAIL,
                    f"whether {name} is recorded could not be answered, {cause.message}",
                    cause.remediation.remedy,
                    error=exc,
                )
                continue
            if already:
                continue
            if not wizard.optional(f"Record the credential {name} now?"):
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.INFO,
                    f"{name} is not recorded and was not entered; doctor reports it",
                )
                continue
            try:
                value = wizard.prompter.secret(f"Value for {name}")
            except prompt.NothingEntered:
                # Accepted then left empty is the same as a no (R-347).
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.INFO,
                    f"{name} is not recorded and was not entered; doctor reports it",
                )
                continue
            except prompt.PromptUnavailable as exc:
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.FAIL,
                    f"{name} was offered and nothing could be read: {exc}",
                    Remedy.SET_CREDENTIAL,
                )
                continue
            if _store(wizard, f"setup.credential.{name}", f"credential {name}", str(name), value):
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.OK,
                    f"{name} recorded in the OS keychain",
                )


def _store(wizard: _Wizard, key: str, title: str, name: str, value: str) -> bool:
    """Record ``value`` under ``name``, or note why not, never quoting it. True when stored."""
    try:
        secrets.set(name, value)
    except secrets.CredentialError as exc:
        # The remedy travels on the exception; the subclasses need different acts.
        wizard.note(
            key,
            title,
            doctor.Status.FAIL,
            f"{name} could not be recorded: {exc}",
            Remedy(str(exc.remedy)),
        )
        return False
    except CratekitError as exc:
        # The presence index refusal, reached through the write; a separate leg
        # since ``CredentialError`` is not a ``CratekitError``.
        cause = exc.cause
        wizard.note(
            key,
            title,
            doctor.Status.FAIL,
            f"{name} could not be recorded, {cause.message}",
            cause.remediation.remedy,
            error=exc,
        )
        return False
    return True


# ---------------------------------------------------------------------------
# Discogs, its own step (U283)
# ---------------------------------------------------------------------------

#: The doctor check that groups the Discogs token, skipped by the credential loop.
DISCOGS_CHECK = "credential.discogs"

#: How many tokens a person may type before the step gives up for this run.
DISCOGS_TRIES = prompt.MAX_ATTEMPTS

#: What the step says before it asks: what the token buys and where it comes from.
DISCOGS_INTRO = (
    "\n"
    "Discogs\n"
    "  Genre tagging asks Discogs first for a track's genre and style, and\n"
    "  Beatport only when Discogs has none. Without Discogs, a track Beatport\n"
    "  does not carry stays untagged.\n"
    "  Linking it is free. It needs a Discogs account and a personal access token:\n"
    "  sign in at discogs.com, open discogs.com/settings/developers and press\n"
    "  Generate new token. Setup checks the token with Discogs and keeps it in\n"
    "  this computer's keychain. It is not shown as you type or paste it.\n"
)

#: What leaving Discogs unlinked costs and how to link it later.
DISCOGS_UNLINKED = (
    "Discogs is not linked, so genre tagging asks Beatport alone: a track "
    "Beatport does not carry stays untagged, and a later run asks it again. To "
    f"link it later, run crate setup again, or {searchers.DISCOGS_LOGIN_STEPS}"
)

#: The flag that offers to replace a token already recorded.
RELINK_FLAG = "--relink-discogs"


def _link_discogs(
    wizard: _Wizard,
    cfg: config.Config,
    *,
    relink: bool = False,
    fetch: searchers.Fetch | None = None,
    sleep: Callable[[float], None] | None = None,
) -> None:
    """Link Discogs: say why, take the token, check it, and only then store it (U283).

    The token is read unechoed, checked by ``searchers.check_discogs_token``
    and stored by :func:`_store`; it appears in no note. A rejected token is
    never stored and is asked again up to :data:`DISCOGS_TRIES` times. One that
    could not be checked is stored with a note, except on a relink, where only
    an accepted token replaces the recorded one. Refusals are notes, since the
    configuration is already saved, and unlinked is INFO, never FAIL.
    ``fetch`` and ``sleep`` are the client's test seams.
    """
    membership = profiles.resolve(cfg.profile.name, dict(cfg.modules.explicit))
    if not doctor.offered(DISCOGS_CHECK, membership):
        return
    name = str(secrets.Credential.DISCOGS_TOKEN)
    key, title = f"setup.credential.{name}", "Discogs"
    try:
        already = secrets.exists(name)
    except CratekitError as exc:
        cause = exc.cause
        wizard.note(
            key,
            title,
            doctor.Status.FAIL,
            f"whether {name} is recorded could not be answered, {cause.message}",
            cause.remediation.remedy,
            error=exc,
        )
        return
    if already and not relink:
        wizard.note(
            key,
            title,
            doctor.Status.OK,
            (
                f"linked: a Discogs token is recorded as {name}, and setup left it "
                f"as it is; crate setup {RELINK_FLAG} offers to replace it"
            ),
        )
        _discogs_vocabulary(wizard, cfg)
        return
    # What stays true whatever this run does: on a relink, the recorded token.
    unlinked = (
        f"the Discogs token already recorded as {name} was kept"
        if already
        else DISCOGS_UNLINKED
    )
    wizard.prompter.write(DISCOGS_INTRO)
    question = "Replace the recorded Discogs token now?" if already else "Link Discogs now?"
    if not wizard.optional(question, default=True):
        wizard.note(key, title, doctor.Status.INFO, unlinked)
        return
    refused: list[str] = []
    for _ in range(DISCOGS_TRIES):
        try:
            token = wizard.prompter.secret("Discogs personal access token")
        except prompt.NothingEntered:
            wizard.note(key, title, doctor.Status.INFO, f"nothing was entered; {unlinked}")
            return
        except prompt.PromptUnavailable as exc:
            wizard.note(
                key,
                title,
                doctor.Status.FAIL,
                f"{name} was offered and nothing could be read: {exc}; {unlinked}",
                Remedy.SET_CREDENTIAL,
            )
            return
        # Said first, since a rate limited check can wait a minute and a half.
        wizard.prompter.write("  Checking the token with Discogs...\n")
        try:
            check = searchers.check_discogs_token(token, fetch=fetch, sleep=sleep)
        except CratekitError as exc:
            cause = exc.cause
            wizard.note(
                key,
                title,
                doctor.Status.FAIL,
                f"the token could not be checked, so it was not recorded: "
                f"{cause.message}; {unlinked}",
                cause.remediation.remedy,
                error=exc,
            )
            return
        # Broad on purpose: the configuration is saved, and a hostile server must
        # not lose the report. No verdict, no store.
        except Exception as exc:  # noqa: BLE001
            wizard.note(
                key,
                title,
                doctor.Status.FAIL,
                f"the token could not be checked ({type(exc).__name__}), so it was "
                f"not recorded; {unlinked}",
                Remedy.REPORT_DEFECT,
            )
            return
        if check.verdict is searchers.TokenVerdict.REJECTED:
            refused.append(check.note)
            wizard.prompter.write(f"  Not linked: {check.note}. Nothing was recorded.\n")
            continue
        if already and check.verdict is not searchers.TokenVerdict.ACCEPTED:
            # A replacement must be accepted, or it could overwrite a working token.
            wizard.note(
                key,
                title,
                doctor.Status.INFO,
                (
                    f"the new token was not recorded, because it could not be "
                    f"checked: {check.note}; {unlinked}. Run crate setup "
                    f"{RELINK_FLAG} again once Discogs answers, or record it "
                    f"unchecked: {searchers.DISCOGS_LOGIN_STEPS}"
                ),
                Remedy.SET_CREDENTIAL,
            )
            return
        if not _store(wizard, key, title, name, token):
            return
        if check.verdict is searchers.TokenVerdict.ACCEPTED:
            wizard.note(
                key,
                title,
                doctor.Status.OK,
                f"linked: Discogs accepted the token, recorded in the OS keychain as {name}",
            )
        else:
            wizard.note(
                key,
                title,
                doctor.Status.INFO,
                (
                    f"recorded in the OS keychain as {name} without being checked, "
                    f"because {check.note}. A tag run asks Discogs with it and says "
                    f"so if Discogs refuses it"
                ),
            )
        _discogs_vocabulary(wizard, cfg)
        return
    wizard.note(
        key,
        title,
        doctor.Status.INFO,
        (
            f"Discogs refused all {len(refused)} tokens entered, the last because "
            f"{refused[-1]}, so none was recorded; {unlinked}"
        ),
        Remedy.SET_CREDENTIAL,
    )


def _discogs_vocabulary(wizard: _Wizard, cfg: config.Config) -> None:
    """Note a linked Discogs whose styles this library's copy has nowhere to file.

    A copy made before U244 lacks ``[vocabulary.discogs]``; read through the
    upgrade's own planner. Silent when it could not look, since doctor's
    taxonomy lines in the same report say why.
    """
    try:
        _, found = taxonomy_upgrade.planned(cfg)
    except CratekitError:
        return
    if searchers.DISCOGS not in found.missing_vocabularies:
        return
    wizard.note(
        "setup.discogs.vocabulary",
        "Discogs styles",
        doctor.Status.INFO,
        (
            f"this library's taxonomy copy has no [vocabulary.discogs] table, so a "
            f"Discogs style files only where an alias or a rule already names it. "
            f"{taxonomy_upgrade.remedy(found)}"
        ),
    )


# ---------------------------------------------------------------------------
# The verb
# ---------------------------------------------------------------------------


def setup(ctx: "Context") -> Envelope:
    document, provenance = existing_document()
    # The document as read; only the difference from it is written (R-116).
    as_read = copy.deepcopy(document)
    wizard = _Wizard(document, prompt.Prompter())
    args = ctx.args
    # One description of this machine for the whole run, so the disk recorded,
    # written to and reported on by doctor is one disk observed once.
    machine = doctor.Probes()

    # Only when absent, since a versioned document was already migrated.
    if _get(document, "schema_version") is None:
        _put(document, "schema_version", config.CURRENT_SCHEMA_VERSION)

    root = wizard.resolve(
        "library.root",
        flag=args.library_root,
        question="Where is the music library",
    )
    _put(document, "library.root", root)
    _put(
        document,
        "library.volume_id",
        _resolve_volume_id(wizard, root, args.volume_id, machine),
    )
    _put(
        document,
        "library.db_path",
        wizard.resolve(
            "library.db_path",
            flag=args.db_path,
            question="Where is the rekordbox database",
            probe=_probe_db_path,
        ),
    )
    _put(
        document,
        "paths.download_staging",
        wizard.resolve(
            "paths.download_staging",
            flag=args.staging,
            question="Where should fresh downloads land before they are moved",
            default=str(Path(root) / STAGING_DIRNAME),
        ),
    )
    # A name under the music folder, not a path, so a moved library keeps its
    # processed tree (U154).
    _put(
        document,
        "library.processed_dir",
        wizard.resolve(
            "library.processed_dir",
            flag=args.processed_dir,
            question="Which folder under the music folder holds filed batches",
            default=config.DEFAULT_PROCESSED_DIR,
        ),
    )
    _put(
        document,
        "profile.name",
        wizard.resolve(
            "profile.name",
            flag=args.profile,
            question="Which module preset",
            default="full",
            choices=profiles.PROFILE_NAMES,
        ),
    )
    shipped = template_names()
    _put(
        document,
        "taxonomy.template",
        wizard.resolve(
            "taxonomy.template",
            flag=args.taxonomy,
            question="Which taxonomy template",
            default=shipped[0] if shipped else None,
            choices=shipped or None,
        ),
    )
    _resolve_backup(wizard, document, args, machine)

    problems = config.validate(document)
    if problems:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message="the answers do not make a usable configuration yet",
                remediation=_answers_remediation(document, problems),
                scope=Scope.RUN,
                origin=("cli.setup",),
                detail={"problems": list(problems)},
            )
        )

    cfg = config.from_dict(document)
    # Before anything is proposed or saved (R-663).
    _refuse_a_database_that_is_not_one(cfg)
    # The pin and the drive rule go into the same document so the file is saved
    # once, leaving no window with them missing (R-372).
    _propose_pin(wizard, document, cfg)
    _propose_prefix_map(wizard, document, cfg)
    # The questions ran unlocked, so the write re-decides under the lock:
    # ``merge_changes`` lays only this run's changes over the file as it is now
    # and refuses when both changed one value. ``cfg`` is what was written.
    cfg, written = config.update(
        lambda current: config.merge_changes(as_read, document, current)
    )
    wizard.note(
        "setup.config",
        "configuration",
        doctor.Status.OK,
        f"{provenance} configuration written to {written}",
    )

    _seed_taxonomy(wizard, cfg, machine)
    _capture_credentials(wizard, cfg)
    _link_discogs(wizard, cfg, relink=bool(args.relink_discogs))

    report = doctor.run(cfg, probes=machine)
    findings = tuple(wizard.notes) + report.findings
    payload = {
        "checks": [finding.to_json() for finding in findings],
        "summary": {
            "config": str(written),
            "provenance": provenance,
            "answered": wizard.asked,
            "checked": len(report.findings),
            "failing": len(report.failures),
            "completed": datetime.now(timezone.utc).isoformat(),
        },
    }
    refused = tuple(f for f in findings if f.status is doctor.Status.FAIL)
    if not refused:
        return ctx.envelope(data=payload)
    cause = doctor.failure_cause(doctor.Report(findings), origin="cli.setup")
    return output.build(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        schema=ctx.entry.output_schema or output.current_schema("diagnostic"),
        started=ctx.started,
        outcome=Outcome.FAILED,
        # From the cause, so a declared reason keeps its reserved code.
        code=cause.code,
        data=payload,
        cause=cause,
    )


__all__ = [
    "STAGING_DIRNAME",
    "build",
    "existing_document",
    "setup",
    "template_names",
    "template_text",
]
