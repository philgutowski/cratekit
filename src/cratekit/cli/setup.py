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

SIX PROPERTIES, EACH ANSWERING A WAY A WIZARD GOES WRONG. The last two arrived
from a review that found the first four were not enough on their own.

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

**And it is derived from a volume that actually HOLDS the configured root.**
Guarding the re-derive alone was not enough, and the gap cost the whole
assertion. ``preflight.containing_mount`` walks up to the deepest EXISTING
ancestor, which is what makes it right for a library root that is a subdirectory
of a mount and lethal here: with the drive unplugged the configured root does not
exist, the walk climbs past the empty mount point to the boot disk, and the boot
disk's identity is recorded as the library's. Every destructive verb's identity
precondition then passes against the boot disk, and doctor reports four greens
over it.

What is refused is AN EMPTY MOUNT SLOT, which took three corrections to get
right. The first two refused a disk that was attached and readable: requiring the
root to exist refuses every first run, and allowing a gap of one directory
refuses every library nested deeper than one, which is the ordinary layout. The
third refused the gap where a volume would appear, which is the right subject and
the wrong evidence, because an ejected volume leaves its mount point behind as an
empty directory and then there is no gap to refuse. Neither absence nor depth was
ever the hazard: the hazard is that nothing is MOUNTED at the place the path goes
through, so that is the question ``preflight.identity_source`` asks, against a
declared table of where this platform mounts one.

**NOTHING LIBRARY-SCOPED IS WRITTEN UNTIL THE VOLUME IS ASSERTED.** The active
taxonomy is the one thing this verb writes beside the library, and it used to be
written before anything checked which disk was there. Two consequences, both
real: on macOS an occupied ``/Volumes/NAME`` makes the real volume mount at
``/Volumes/NAME 1`` on its next attach, so a directory created there is
permanently the wrong mount point; and the copied template is coupled state
landing on a filesystem no snapshot of that library captures and no rollback
reverts. The mount is resolved first now, through the same seams doctor answers
with, and a volume the product cannot recognise as this library's is a refusal to
write rather than a write somewhere else.

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
import copy
import tomllib
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import doctor, output, prompt, registry, render
from cratekit.cli.output import Envelope
from cratekit.core import config, preflight, profiles, rb_writer, secrets, taxonomy
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope
from cratekit.core.exit_codes import Remedy

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
    # A CLOSED SET, exactly like the profile beside it. Without the choices, a
    # typed name reached validation, was written to the configuration file, and
    # was then RETURNED by the next run before any guard looked at it, so the
    # only escape from one transposed letter was to hand-edit the TOML this verb
    # exists to abolish.
    #
    # ``or None`` IS LOAD BEARING, and so is the fact that the walk behind it
    # cannot raise. THIS FUNCTION RUNS ON EVERY INVOCATION OF EVERY VERB: the
    # command tree builds each landed entry's parser before anything dispatches,
    # so a packaged directory that is missing or unreadable would take
    # ``crate doctor`` and ``crate --help`` down with it, on exactly the machine
    # doctor exists to report on. An install with no readable templates offers no
    # closed set rather than an empty one, since an empty ``choices`` rejects
    # every value including the correct one, and the wizard then reports the
    # missing template as a finding.
    parser.add_argument(
        "--taxonomy",
        choices=taxonomy.shipped_template_names() or None,
        help="which shipped taxonomy template to adopt",
    )
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

    The walk itself moved DOWN to ``core/taxonomy`` and this is now one line over
    it. Doctor asks the same question, to refuse a configuration naming a
    template nothing ships, and it cannot import this module: the wizard imports
    doctor, so the arrow only runs one way. Two walks would let the wizard offer
    a name the check rejects.
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
    """A refusal from the wizard, under a declared reason.

    ``reason`` is a parameter because not everything this verb refuses is a
    problem with the configuration document. Recording a volume identity for a
    root that is not there is a fact about the LIBRARY, and it carries the slug
    and therefore the exit code that already means exactly that, rather than
    being filed under the config's.
    """
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
    """The closing clause of a wizard sentence, chosen by the KIND of refusal.

    ONE FUNCTION SO THE SENTENCE CANNOT DRIFT FROM THE TOKEN. Every one of these
    branches used to close with "grant this interpreter access", written into the
    prose, beside a remedy token the classification now chooses. Those two can
    disagree, and on a read only volume they did: the sentence named the read only
    case and then gave the advice for the other one, over a volume no permission
    grant can change. ``render.access_note`` holds one sentence per kind and is
    the same wording every other caller in the package gets, so this is a lookup
    rather than a fourth wording.

    ``otherwise`` is for the failure the operating system did not refuse at all,
    where there is no kind to follow, and it says what the wizard can offer
    without claiming to know what happened.
    """
    note = render.access_note(exc)
    return f" {note}" if note is not None else f" {otherwise}"


def _unreachable_root(root: str, exc: OSError) -> str:
    """The sentence for a library root behind a directory nobody can open.

    ONE SENTENCE, TWO CALLERS, because the wizard meets this in two places and
    they must not describe it two ways. ``Path.exists`` re-raises a permission
    error rather than answering False, so an ancestor this account cannot
    traverse comes back from ``core/preflight`` as an exception rather than as a
    verdict, and both of the wizard's mount questions go through that module.

    IT IS A ROUTINE FIRST-RUN STATE ON THE PLATFORM THIS SHIPS FOR FIRST, which
    is why it earns a sentence rather than a traceback. On macOS a library root
    under Documents, Desktop, Downloads or an external volume raises EPERM from
    ``stat`` for any interpreter without Full Disk Access. Before this, the
    dispatcher's blanket caught it and rendered "internal-error ... this is a
    defect; report it", so the product classified the user's own filesystem
    permission as a Cratekit bug and sent them to file a report, in the one verb
    whose whole job is getting a fresh clone to a first write. Doctor already
    answers it as a failed check; the wizard now refuses in the same words.

    THE ACT COMES FROM THE KIND, NOT FROM THIS FUNCTION. The closing clause used
    to be "Grant this interpreter access to the path", hard coded, beside a
    remedy token the classification is free to change: under a read only volume
    or a locked file the token flips and the sentence would then contradict it,
    which is the same collapse one level in. ``render.access_note`` owns one
    sentence per kind and every other caller in the package already uses it, so
    the sentence follows the token by construction. A failure the operating
    system did not refuse keeps the generic close, because there is no kind to
    follow.
    """
    return (
        f"{root} could not be examined: {exc}. A directory on the way to it "
        f"cannot be opened by this account, so which volume the library would "
        f"sit on was not established and nothing was recorded. This is not a "
        f"defect and it is not a missing drive."
    ) + _act(exc, "Choose a library root this account can already reach")


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
    #
    # THIS IS THE SECOND READ OF ONE FILE, so the two can disagree, and the
    # handler below is what happens when they do: a file removed, a permission
    # taken away, or a truncation between the load above and this open. It used
    # to carry a "see above" pragma arguing the load had already classified it,
    # which is true of the file as it was and says nothing about the file as it
    # is now. The one thing this may not do is read the document as empty and
    # write over it, so it refuses.
    path = config.config_path()
    try:
        with path.open("rb") as handle:
            raw = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        # "REPAIR OR RECREATE IT" IS FOR A DOCUMENT THAT IS ACTUALLY DAMAGED.
        # A configuration file with mode 0o000 is byte for byte intact, and
        # telling its owner to repair or recreate it sends them to rewrite work
        # they still have over a chmod. The ``from exc`` is what lets the refusal
        # constructor overrule the token when the operating system is what
        # refused; the token stands for a document that really will not parse.
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
        *,
        error: BaseException | None = None,
    ) -> None:
        """Record one answer. ``error`` is the exception this answer is ABOUT.

        A NOTE IS NOT A LESSER REFUSAL, and until this it was the unclassified
        one. Everything the wizard RAISES goes through ``CratekitError``, whose
        constructor classifies against its declared cause. Everything the wizard
        REPORTS came through here instead, which builds a ``doctor.Finding`` and
        returns, so the remedy was whatever the branch hard coded, forever. Hand
        the exception over and the finding decides; see ``doctor.Finding``.
        """
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

        An unanswerable question falls back to the derived default when there is
        one and refuses when there is not. That is the rule that makes this verb
        honest in a pipe: a value nobody supplied and nothing could derive is a
        refusal naming the flag, not a guess written into a config file.

        ``probe`` is a CALLABLE rather than a value because probing costs
        something: one of them reads another application's settings files. Passing
        the result would run every probe on every run, including the runs where
        the answer was recorded months ago and nothing needed asking.

        A CLOSED SET IS CHECKED AGAINST EVERY SOURCE, not only against the
        derived default. A recorded value outside the set was returned ahead of
        the guard, so one transposed letter in a taxonomy name was written to the
        file and then handed back by every later run: setup refused, its remedy
        was to run setup, and the only way out was to hand-edit the document this
        verb exists to abolish. A recorded value the set does not contain is
        therefore treated as UNANSWERED, which is what makes a re-run repair it.
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

    THE STAT WAS OUTSIDE THAT HANDLER AND IT KILLED THE WHOLE VERB. The clause
    above covers the reader and nothing else, and ``Path.exists`` re raises under
    EPERM rather than answering False, so a machine where rekordbox's OWN
    settings name a database this interpreter cannot stat, which is a library on
    an external drive or under Documents, took ``crate setup`` down before it
    asked its first question. Worse than every other instance of that defect on
    this branch: the path is not one the user supplied, so there was nothing for
    them to route around, and setup could not complete on that machine at all.

    AND AN UNSTATTABLE PATH IS STILL PROPOSED. "Could not look" is not "is not
    there", which is this branch's first recurring defect, and dropping the
    proposal would apply it to the one machine where the proposal is most likely
    to be exactly right: rekordbox is using that database, and only this
    interpreter is refused. It remains a default to a question, so a user who
    disagrees answers differently and nothing is written unasked.
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

    Two guards rather than one, and the second is the one that was missing.

    NEVER RE-DERIVED, because re-reading the identity on every run records
    whatever disk is mounted, which is the restored clone arriving through the
    check meant to catch it.

    AND NEVER DERIVED FROM A VOLUME THAT DOES NOT HOLD THE ROOT.
    ``containing_mount`` climbs to the deepest EXISTING ancestor, so an absent
    library root does not fail the read, it succeeds against whatever is mounted
    further up, which on every platform this ships for is the boot disk. Recorded
    once, that identity is what every destructive verb then asserts, against the
    disk holding the user's operating system.

    WHAT IS REFUSED IS AN EMPTY MOUNT SLOT, and getting there took three
    corrections. The first two refused a volume that was attached and readable:
    "the root must already exist" refused every first run, and "the gap may be at
    most one level" refused every library nested two or more directories down,
    which is the ordinary layout. The third refused too little rather than too
    much. It asked whether the first MISSING directory was a mount location,
    which reads absence as the hazard, and an ejected volume routinely leaves its
    mount point behind as an empty directory: nothing was missing, nothing was
    refused, and the boot disk was recorded exactly as before.

    ``preflight.identity_source`` asks of the SLOT rather than of the gap. For
    every place on the way down where this platform mounts a volume, is a volume
    mounted there right now. Depth is not consulted and absence is not consulted.

    The identity provider comes from the run's ``Probes`` rather than from the
    platform default here, so the volume this wizard reads is the volume doctor
    reports on three lines later. Two probes for one disk is how one run says two
    things about it.
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
        # See ``_unreachable_root``. A refusal naming the path, under a slug of
        # its own, rather than a traceback the dispatcher files as a defect.
        #
        # ``path`` as well as ``root``, spelled the way every other refusal in
        # the package spells it, because a consumer reading the actionable path
        # out of a cause should not have to know which slug it arrived under.
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


def _seed_taxonomy(wizard: _Wizard, cfg: config.Config, machine: doctor.Probes) -> None:
    """Copy the chosen template beside the database, once (S6).

    The shipped template is read-only packaged data; the ACTIVE one is a copy,
    which is what makes a library self-describing: a reinstall or a second
    machine resolves the same tree without re-answering the wizard, and a
    snapshot rolls the taxonomy back with the database it describes.

    THE VOLUME IS ASSERTED BEFORE THE WRITE, and this is the only place in this
    verb where that matters, because this is the only thing it writes beside the
    library. Writing first and checking last put a ``.cratekit`` directory and a
    coupled state file onto whatever filesystem happened to be at the configured
    path, and then reported the copy green. Two costs, both permanent: the
    directory becomes a leftover mount point, which is the first of the three
    states ``core/preflight`` exists to tell apart and which makes the real
    volume mount somewhere else on its next attach; and the template is coupled
    state on a disk no snapshot of this library captures and no rollback reverts.

    ``resolve_mount_state`` rather than ``assert_library_mounted``: this wants
    the diagnosis rather than an exception, and the suite neutralizes the
    asserting entry point everywhere, so a guard written on top of that one would
    be a guard no test could see.

    What the diagnosis MEANS is ``preflight.library_state_may_be_written``, and
    that is a DIFFERENT question from the one doctor asks before reporting on
    this same file. The two differ in exactly one mount outcome: a matching
    identity with an absent root is nothing to READ and is precisely when
    creating the directory and copying the template into it is correct, which is
    a first run on the right volume, or a library folder somebody renamed. One
    rule serving both questions refused that write and explained the refusal with
    a sentence its own parenthetical contradicted.

    It is also why the rule is not "the state must be OK". A platform with no
    identity adapter answers "identity unavailable" for every volume it will ever
    see, so that rule would lock every such platform out of its own library
    state, permanently, which is a guard firing on a correct setup (P7).
    """
    try:
        status = preflight.resolve_mount_state(
            cfg.library.root,
            cfg.library.volume_id,
            identity_provider=machine.identity_provider,
            mount_enumerator=machine.mount_enumerator,
        )
    except OSError as exc:
        # A NOTE RATHER THAN A RAISE, because this function's contract is that it
        # reports and never aborts the run: the configuration is already saved by
        # the time it is called, and the report is what the user reads. The
        # derive above raises for the same condition because it has no value to
        # return, and it runs first unless ``--volume-id`` supplied one, which is
        # the only way this branch is reached.
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
    # "NOT PRESENT" AND "COULD NOT LOOK" ARE DIFFERENT ANSWERS, and one handler
    # over both said the wrong one in the verb this unit is named for.
    # ``except (FileNotFoundError, OSError)`` is one clause over both conditions,
    # and the redundancy is the fingerprint: ``FileNotFoundError`` IS an
    # ``OSError``, so the tuple is the trace of a split that was never made. With
    # the packaged directory unreadable, ONE ``crate setup`` envelope carried
    # "no shipped template is named 'default'; shipped: " from here and "the
    # packaged template directory could not be listed ... a damaged or partial
    # install rather than a configuration error" from doctor, in the same report.
    # The first contradicted the second, sent the user to change a configuration
    # value that was correct, and printed an empty shipped set as a fact.
    #
    # So the shipped set is asked for in BOTH halves, exactly as doctor asks, and
    # the three conditions answer separately: the directory could not be listed,
    # the name is not in a set that WAS listed, or the named template ships and
    # its own text could not be read.
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
        # It IS in the listed set, so this is packaged data that lists and does
        # not open. Same diagnosis as an unlistable directory and the same
        # remedy; re-running setup cannot repair a wheel.
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
    # THE SAME COLLAPSE, ONE SCREEN LOWER, and handling it at the top of this
    # function while leaving it here would have MOVED the hole rather than closed
    # it. Both of the two calls below reach the filesystem and both raise:
    # ``Path.exists`` re-raises a permission error rather than answering False,
    # and ``atomic_write_bytes`` raises for a state directory this account may
    # not write and for a library volume mounted read only. Neither was handled,
    # so both escaped into the dispatcher's blanket and were rendered
    # "internal-error ... this is a defect; report it", which is verbatim the
    # support failure item 3 of the residual finding "Five places where "I could
    # not look" is still not said out loud" records.
    #
    # TWO HANDLERS RATHER THAN ONE, because they are two different acts with two
    # different remedies in the same sentence family: one is a path this account
    # could not look at, the other is a path it reached and was refused a write
    # on. One handler over both would be the collapse the whole round is about.
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

    A REFUSAL HERE IS A NOTE AND NEVER A RAISE, which is the rule ``_seed_taxonomy``
    already follows one screen up and for the same reason: this runs AFTER
    ``config.save``, so a wizard that dies here loses the whole report over a
    configuration that is already on disk. Item 4 of the residual finding this
    file already cites at ``_seed_taxonomy`` gave the presence question
    a refusal of its own, for an index this account cannot read, and that refusal
    reaches the line below with nothing between it and the verb. The note carries
    the refusal's own remedy, so a person is told to repair the sidecar rather
    than to record a credential the keychain may already hold.
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
                secrets.set(str(name), value)
            except prompt.NothingEntered:
                # An offer accepted and then left empty is the same fact as a
                # no: nothing recorded, doctor reports it. A FAIL here failed the
                # whole wizard over a session blob only login can produce (R-347).
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
            except CratekitError as exc:
                # THE SAME REFUSAL AS THE PROBE ABOVE, REACHED THROUGH THE WRITE.
                # ``secrets.set`` notes the name in the presence index after the
                # keychain write, through the same reader, so an index it cannot
                # use refuses here too. A leg of its own because the three above
                # cannot see it: ``CredentialError`` is not a ``CratekitError``,
                # so catching one does not catch the other, and the window is a
                # person typing a secret, which is as wide as windows get.
                cause = exc.cause
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.FAIL,
                    f"{name} could not be recorded, {cause.message}",
                    cause.remediation.remedy,
                    error=exc,
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
    # The document AS IT WAS READ, kept apart from the one the answers go into.
    # The difference between the two is what this run actually answered, and that
    # difference is all the write below is entitled to put on disk (R-116).
    as_read = copy.deepcopy(document)
    wizard = _Wizard(document, prompt.Prompter())
    args = ctx.args
    # ONE description of this machine for the whole run. The wizard reads the
    # volume identity through it, refuses to write library state through it, and
    # hands it to doctor at the end, so the disk setup recorded, the disk it
    # wrote to, and the disk doctor reports on are one disk observed once. Two
    # probes over one run is how a report and the act it describes come apart.
    machine = doctor.Probes()

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
    _propose_pin(wizard, document, cfg)
    # READ, ASK, WRITE, AND THE WRITE RE-DECIDES UNDER THE LOCK. Everything above
    # ran unlocked, because a lock held across a question blocks every other
    # command on somebody typing. So another command may have written since the
    # read at the top, and writing ``document`` whole would erase its answers
    # while this run reported success. ``merge_changes`` lays only what this run
    # changed over what is on disk now, and refuses, writing nothing, when both
    # changed one value. ``cfg`` is rebound to what was WRITTEN, because the
    # taxonomy, the credentials and doctor below must describe the file that
    # exists rather than the one this run had in mind.
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
        # From the cause, for the reason doctor's own envelope reads it there: a
        # check that refused under a declared reason has reserved a code, and
        # PRECONDITION written in here would overwrite it.
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
