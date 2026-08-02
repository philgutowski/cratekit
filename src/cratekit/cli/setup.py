"""``crate setup``: clone to first write, without help.

THE ONE INTERACTIVE VERB, and the registry says so: ``interactive=True`` on this
entry and on no other, asserted by ``tests/test_cli_contract.py`` in both
directions. Even here, the standard-input READ happens in ``cli/prompt.py`` and
nowhere else, so this module passes the same no-standard-input guard every other
module passes. The exemption is one file and this is not it.

WHAT THE WIZARD IS FOR. Six configuration keys have no default, deliberately: a
short required list is a short first-run wizard, and every other key is a
decision the product can make on the user's behalf. Those six plus the taxonomy
choice, the profile, and the credentials are what stands between a fresh clone
and a first successful write, and before this verb existed the only way to
produce them was to hand-write a TOML file against a validation error message.

FOUR PROPERTIES, EACH ANSWERING A WAY A WIZARD GOES WRONG.

**Every answer has the same four sources, in one order: a flag, the existing
configuration, a derived probe, then a question.** So a re-run changes nothing it
was not asked to change, and a scripted invocation with every flag supplied never
reaches a prompt at all. The alternative, asking everything every time, is how a
second run silently re-answers a question the user answered carefully once.

**An existing configuration that cannot be understood REFUSES rather than being
replaced.** Only a genuinely absent file starts from empty. A file that fails
validation is read for its answers and completed, because that is what setup is
for; a file that is corrupt, or was written by a newer build, stops the wizard.
Treating an unreadable document as an empty one and then writing over it is how a
user loses the answers they gave, and it is the same shape as a reader that
cannot tell a wrong document from an empty one.

**The volume identity is DERIVED and never re-derived.** R38 identifies the
library by the volume's own identity so that a restored clone mounted in its
place fails the assertion instead of passing it. A wizard that re-read the
identity on every run would quietly re-record whatever disk happened to be
mounted, which is the clone case arriving through the thing meant to catch it. An
identity already recorded is kept unless the user names a new one explicitly.

**The rekordbox pin is PROPOSED and never adopted.** S2: a pin the software
copies from whatever is installed refuses nothing, forever. The wizard reads the
installed version and asks; an answer that is not a deliberate yes leaves the pin
unset, and doctor keeps saying so. The date the pin was confirmed against a real
write is never written here, because this verb has not made one.

IT ENDS BY RUNNING DOCTOR, and it exits on doctor's verdict rather than on its
own. Writing a valid configuration onto a machine with no ffmpeg, no credential
and no keychain is not "setup succeeded"; the user still cannot reach a write.
The configuration is saved either way, so the fix is one more run rather than
starting over.
"""

from __future__ import annotations

import argparse
import tomllib
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from importlib import resources
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import doctor, output, prompt, registry
from cratekit.cli.output import Envelope
from cratekit.core import config, preflight, profiles, rb_writer, secrets
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope
from cratekit.core.exit_codes import ExitCode, Remedy

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

#: Where downloads land when the user has no opinion. On the library volume on
#: purpose: staging and the destination then share a filesystem, so the move into
#: the library is a rename rather than a copy, and a half-finished download
#: cannot fill a boot disk the user needs for other things.
STAGING_DIRNAME = "Downloads"


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    """Every answer is also a flag, so the whole wizard is scriptable.

    Not a convenience. A verb that can only be driven by typing at it cannot be
    exercised end to end by anything except a person, which is how the source
    system's three unguarded prompts survived a non-interactive contract that
    claimed to be complete.
    """
    parser.add_argument("--library-root", help="the directory holding the music library")
    parser.add_argument("--db-path", help="the rekordbox database this library uses")
    parser.add_argument(
        "--volume-id",
        help="the library volume's own identity, a UUID or serial and never a mount path",
    )
    parser.add_argument("--staging", help="where fresh downloads land before they are moved")
    parser.add_argument("--profile", choices=profiles.PROFILE_NAMES, help="the module preset")
    parser.add_argument("--taxonomy", help="which shipped taxonomy template to adopt")
    parser.set_defaults(_handler=setup)


# ---------------------------------------------------------------------------
# The shipped taxonomy templates
# ---------------------------------------------------------------------------


def template_names() -> tuple[str, ...]:
    """Every taxonomy template that ships in the wheel, by its short name.

    Derived by walking the packaged directory rather than listed, so a second
    template is offered on the day it is added and no edit is needed here (P3).
    The short name is the stable identifier configuration records; the display
    names inside the template belong to the template (R19).
    """
    found = []
    for item in (resources.files("cratekit") / "templates").iterdir():
        name = item.name
        if name.startswith("taxonomy.") and name.endswith(".toml"):
            found.append(name[len("taxonomy.") : -len(".toml")])
    return tuple(sorted(found))


def template_text(name: str) -> str:
    """The packaged text of one template. Raises when the name is not shipped."""
    source = resources.files("cratekit") / "templates" / f"taxonomy.{name}.toml"
    return source.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Reading what is already there
# ---------------------------------------------------------------------------


def _refuse(
    message: str, *, remedy: Remedy, detail: Mapping[str, Any] | None = None
) -> CratekitError:
    return CratekitError(
        Cause(
            reason="config-unusable",
            message=message,
            remediation=Remediation(remedy=remedy),
            scope=Scope.RUN,
            origin=("cli.setup",),
            detail=dict(detail or {}),
        )
    )


def existing_document() -> tuple[dict[str, Any], str]:
    """The configuration this run is completing, and one word for where it came from.

    Three outcomes and they are not interchangeable:

    * a config that loads is returned in its EFFECTIVE, migrated form, so the
      wizard completes the values the running system actually reads rather than
      the ones the file happens to spell (P2);
    * a config that is merely INCOMPLETE is read raw and completed, because
      completing it is what this verb is for;
    * anything else refuses. A corrupt file and a file from a newer build both
      mean a person has to look, and overwriting either destroys answers.
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

    # Incomplete, so the file parsed and carried an integer schema version;
    # anything else would have raised ConfigCorrupt above. Read it for the
    # answers it does hold rather than discarding them.
    path = config.config_path()
    try:
        with path.open("rb") as handle:
            raw = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:  # pragma: no cover - see above
        raise _refuse(
            f"setup will not overwrite a configuration it cannot read: {exc}",
            remedy=Remedy.REPAIR_CONFIG_FILE,
        ) from exc
    if not isinstance(raw, dict):  # pragma: no cover - tomllib always yields a table
        raise _refuse(
            f"{path} does not hold a table at its top level",
            remedy=Remedy.REPAIR_CONFIG_FILE,
        )
    # MIGRATED before it is completed. The loaded branch above returns an already
    # migrated document, and this one must too, or an older file that happens to
    # be incomplete gets the current schema version stamped onto data no
    # migration ever touched. Nothing exercises that today because the ladder is
    # empty at version 1, which is exactly why it has to be written now: the
    # first migration would land in a unit that has no reason to look here.
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
    """Set a dotted key, creating the tables above it.

    A key with no dot in it is a TOP-LEVEL key and gets no table at all. Splitting
    an empty head on "." yields one empty segment, which quietly builds a table
    named "" and files ``schema_version`` inside it, and the only symptom is
    validation reporting the key missing on a document that plainly contains it.
    """
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

    The record of HOW each value was reached is kept rather than discarded,
    because "setup changed nothing" and "setup re-answered everything" look
    identical in a config file and completely different to a user.
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
    ) -> None:
        self.notes.append(
            doctor.Finding(key=key, title=title, status=status, detail=detail, remedy=remedy)
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

        An unanswerable question falls back to the derived default when there is
        one and refuses when there is not. That is the rule that makes this verb
        honest in a pipe: a value nobody supplied and nothing could derive is a
        refusal naming the flag, not a guess written into a config file.

        ``probe`` is a CALLABLE rather than a value because probing costs
        something: one of them reads another application's settings files. Passing
        the result would run every probe on every run, including the runs where
        the answer was recorded months ago and nothing needed asking.
        """
        if flag:
            self.asked.append(f"{dotted} (from the command line)")
            return flag
        recorded = _get(self.document, dotted)
        if isinstance(recorded, str) and recorded.strip():
            return recorded
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
        """A yes or no that may go unanswered, in which case it is a no.

        Every caller of this is proposing something the product may not do on the
        user's behalf: recording a version pin, storing a credential. "Nobody
        answered" and "no" have the same consequence for all of them, which is
        precisely why they are the questions allowed to go unanswered.
        """
        try:
            return self.prompter.confirm(question, default=default)
        except prompt.PromptUnavailable:
            return False


# ---------------------------------------------------------------------------
# The steps
# ---------------------------------------------------------------------------


def _probe_db_path() -> str | None:
    """Where rekordbox itself says its database is, when it will say.

    Asked of rekordbox's own recorded settings rather than assembled from a
    hardcoded vendor layout, because a layout written into this file is one
    person's install shape shipped to everybody (R1). The answer is only a
    PROPOSAL: it becomes the default of a question, never a value written without
    one. Nothing here opens the database. The path is stat-ed to see whether the
    proposal is worth making and its contents are never read.

    Anything the settings reader raises means the same thing here, which is that
    rekordbox's own files could not be read. It is a third-party reader over
    another application's private format, so its failure modes are not a closed
    set this module gets to enumerate, and a wizard that died because a settings
    file was in an unexpected shape would be refusing over a value it was only
    ever going to offer.
    """
    try:
        settings = rb_writer.read_rekordbox_settings()
    except Exception:  # noqa: BLE001 - see the docstring
        return None
    recorded = settings.get("db_path") if isinstance(settings, Mapping) else None
    if isinstance(recorded, str) and recorded.strip() and Path(recorded).exists():
        return recorded
    return None


def _resolve_volume_id(wizard: _Wizard, root: str, flag: str | None) -> str:
    recorded = _get(wizard.document, "library.volume_id")
    if not flag and isinstance(recorded, str) and recorded.strip():
        # NEVER re-derived. See the module docstring: re-reading the identity on
        # every run is how a restored clone gets recorded as the library.
        return recorded
    if flag:
        wizard.asked.append("library.volume_id (from the command line)")
        return flag
    provider = preflight.default_identity_provider()
    observed = provider(preflight.containing_mount(Path(root)))
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


def _seed_taxonomy(wizard: _Wizard, cfg: config.Config) -> None:
    """Copy the chosen template beside the database, once (S6).

    The shipped template is read-only packaged data; the ACTIVE one is a copy,
    which is what makes a library self-describing: a reinstall or a second
    machine resolves the same tree without re-answering the wizard, and a
    snapshot rolls the taxonomy back with the database it describes.
    """
    name = cfg.taxonomy.template
    path = config.state_path("taxonomy_active", cfg)
    try:
        text = template_text(name)
    except (FileNotFoundError, OSError):
        wizard.note(
            "setup.taxonomy",
            "active taxonomy template",
            doctor.Status.FAIL,
            f"no shipped template is named {name!r}; shipped: {', '.join(template_names())}",
            Remedy.FIX_CONFIG_VALUES,
        )
        return
    if path.exists():
        wizard.note(
            "setup.taxonomy",
            "active taxonomy template",
            doctor.Status.INFO,
            f"{path} already exists and was left alone; the library's own copy wins",
        )
        return
    config.atomic_write_bytes(text.encode("utf-8"), path)
    wizard.note(
        "setup.taxonomy",
        "active taxonomy template",
        doctor.Status.OK,
        f"template {name!r} copied to {path}",
    )


def _propose_pin(wizard: _Wizard, document: dict[str, Any], cfg: config.Config) -> bool:
    """Read the installed rekordbox version and OFFER it. Return whether it was taken.

    S2 in one function. The version is read, the user is asked, and nothing is
    recorded unless they say yes. ``rekordbox.validated_on`` is never written
    here: it means "the date this pin was confirmed against a real write", and
    this verb has not made one, so writing it would turn a pin that has never
    been tested into one that claims it has.
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


def _capture_credentials(wizard: _Wizard, cfg: config.Config) -> None:
    """Offer to record each credential this profile's verbs will spend.

    Read through ``cli/prompt``'s secret reader, so the value is never echoed,
    never reaches a command line, and never reaches a shell history. What is
    offered is derived from the same registry question doctor asks, so a module
    switched on above is a credential offered here with no edit.
    """
    membership = profiles.resolve(cfg.profile.name, dict(cfg.modules.explicit))
    for key in sorted(doctor.CREDENTIALS_BY_CHECK):
        if not doctor.requires_check(key, membership):
            continue
        # Keyed by the CREDENTIAL rather than by the check that groups it. One
        # check covers two credentials, so a note keyed on the check would emit
        # the same key twice in one report and any consumer keying on it would
        # keep whichever arrived last.
        for name in doctor.CREDENTIALS_BY_CHECK[key]:
            if secrets.exists(str(name)):
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
                secrets.set(str(name), value)
            except prompt.PromptUnavailable as exc:
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.FAIL,
                    f"{name} was offered and nothing could be read: {exc}",
                    Remedy.SET_CREDENTIAL,
                )
                continue
            except secrets.CredentialError as exc:
                # The remedy travels ON the exception and the three subclasses
                # carry three different ones: no backend, no entry, and a rejected
                # entry need opposite acts. Substituting one here would be the
                # collapse the secrets module declares three types to avoid.
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.FAIL,
                    f"{name} could not be recorded: {exc}",
                    Remedy(str(exc.remedy)),
                )
                continue
            wizard.note(
                f"setup.credential.{name}",
                f"credential {name}",
                doctor.Status.OK,
                f"{name} recorded in the OS keychain",
            )


# ---------------------------------------------------------------------------
# The verb
# ---------------------------------------------------------------------------


def setup(ctx: "Context") -> Envelope:
    document, provenance = existing_document()
    wizard = _Wizard(document, prompt.Prompter())
    args = ctx.args

    # Only when there is none. A document that arrived with a version has already
    # been through the migration ladder above, and stamping the current number
    # over it a second time would be the one write that could claim a migration
    # nobody ran.
    if _get(document, "schema_version") is None:
        _put(document, "schema_version", config.CURRENT_SCHEMA_VERSION)

    root = wizard.resolve(
        "library.root",
        flag=args.library_root,
        question="Where is the music library",
    )
    _put(document, "library.root", root)
    _put(document, "library.volume_id", _resolve_volume_id(wizard, root, args.volume_id))
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

    problems = config.validate(document)
    if problems:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message="the answers do not make a usable configuration yet",
                remediation=Remediation(remedy=Remedy.RUN_SETUP, steps=tuple(problems)),
                scope=Scope.RUN,
                origin=("cli.setup",),
                detail={"problems": list(problems)},
            )
        )

    cfg = config.from_dict(document)
    # The pin is proposed against the configuration the answers describe and is
    # written back through the same document, so the file is saved once. Saving
    # twice would leave a window in which a config exists with the pin missing
    # and a reader could act on it.
    if _propose_pin(wizard, document, cfg):
        cfg = config.from_dict(document)
    written = config.save(cfg)
    wizard.note(
        "setup.config",
        "configuration",
        doctor.Status.OK,
        f"{provenance} configuration written to {written}",
    )

    _seed_taxonomy(wizard, cfg)
    _capture_credentials(wizard, cfg)

    report = doctor.run(cfg)
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
    return output.build(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        schema=ctx.entry.output_schema or output.current_schema("diagnostic"),
        started=ctx.started,
        outcome=Outcome.FAILED,
        code=ExitCode.PRECONDITION,
        data=payload,
        cause=doctor.failure_cause(
            doctor.Report(findings), origin="cli.setup"
        ),
    )


__all__ = [
    "STAGING_DIRNAME",
    "build",
    "existing_document",
    "setup",
    "template_names",
    "template_text",
]
