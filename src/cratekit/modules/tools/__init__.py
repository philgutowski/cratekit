"""The standalone utilities, and the verb declarations the CLI registry consumes.

Three Feature Inventory rows land here, and they are grouped because of what
they have in common rather than what they do: none of them touches the rekordbox
database, the acquisition adapter, the job engine, or the review queue. That is
why the plan schedules them early instead of behind the heaviest unit, and it is
the property to preserve. A change here that reaches for the writer has put a
utility inside the safety spine.

    row 29  set builder   pure read over the library's own analyzed tags
    row 30  mastering     one recording at a time, source never modified
    row 31  backup        the volume mirror, the gated database snapshot, restore

WHY THE VERBS ARE DATA HERE INSTEAD OF FUNCTIONS SOMEWHERE ELSE. KTD7 puts every
module in a static table with a LAZY import, so that ``--help`` on a slim install
lists a verb whose dependencies are absent rather than crashing on the way to
printing it. A table can only stay lazy if the entries are inert: the moment an
entry holds a function object, building the table imports the module that
defines it, and the laziness is gone while still looking present. So each entry
below names its implementation as a dotted string, and the CLI resolves that
string only when the verb actually runs.

THE EXTRAS GROUP IS DERIVED, NEVER RESTATED. ``profiles.install_command`` already
answers "which extras group carries this module's heavy dependencies", and a
second copy of that answer beside this table is a copy that drifts. What these
three need is not a Python extra at all but an external BINARY, which pip cannot
install; :data:`VerbSpec.binaries` records that separately so doctor can check
for it, because a module whose extras are satisfied and whose binary is missing
fails at the first subprocess with a message naming none of this.
"""

from __future__ import annotations

from dataclasses import dataclass

from cratekit.core import profiles


@dataclass(frozen=True, slots=True)
class VerbSpec:
    """One subcommand, described well enough for the registry to build it lazily.

    ``feature`` is the ``profiles.MODULES`` name whose toggle governs the verb.
    It is separate from ``name`` on purpose: a module can grow a second verb, and
    tying the toggle to the verb name would then make half a module switchable.
    """

    name: str
    feature: str
    module: str
    summary: str
    #: Sub-actions the verb dispatches on, empty when the verb takes none. The
    #: registry renders these; they are declared here because which actions exist
    #: is a property of the implementation, not of the CLI.
    actions: tuple[str, ...] = ()
    #: External executables the verb shells out to. Not a Python dependency and
    #: therefore not expressible as an extras group, which is exactly why it is
    #: recorded rather than left to fail at the first subprocess call.
    binaries: tuple[str, ...] = ()
    #: True when the verb can destroy user data and must therefore bind to the
    #: library lock, the backup acknowledgment, and the volume identity assertion
    #: (KTD24). Restore replaces a live database, so the backup verb qualifies
    #: even though nothing here writes a database row.
    destructive: bool = False

    @property
    def extras(self) -> str | None:
        """The extras group carrying this module's heavy Python dependencies.

        Derived from the profile layer rather than restated, so the two cannot
        disagree. None is the answer for all three utilities here, not a gap.
        """
        return profiles.install_command(self.feature)


VERBS: tuple[VerbSpec, ...] = (
    VerbSpec(
        name="setbuild",
        feature="setbuilder",
        module="cratekit.modules.tools.setbuilder",
        summary=(
            "Rank owned tracks that mix with an anchor and sequence them, using "
            "only the library's own analyzed tags"
        ),
    ),
    VerbSpec(
        name="master",
        feature="mastering",
        module="cratekit.modules.tools.mastering",
        summary=(
            "Level, normalize, and encode a live set recording to lossless FLAC, "
            "archiving the untouched source first"
        ),
        binaries=("ffmpeg", "ffprobe"),
    ),
    VerbSpec(
        name="backup.run",
        feature="backup",
        module="cratekit.modules.tools.backup",
        summary=(
            "Mirror the library to the configured remote, snapshot the database "
            "when no rekordbox process holds it, and restore either"
        ),
        # Four actions, and no "setup". Checking that rclone is installed and
        # that the remote is configured is a health check, and this product has
        # one place for those: the doctor verb, which already knows where rclone
        # comes from on each platform. A second, module-local setup path would
        # be a second answer to a question doctor already answers.
        actions=("check", "run", "restore", "restore-database"),
        binaries=("rclone",),
        # Restore overwrites a live database and its sidecars. Binding it to the
        # destructive-session gates is KTD24's whole point: the gates attach to
        # anything that can destroy user data, not only to database writes.
        destructive=True,
    ),
)

#: The verb names, for the registry's parity check and for the layering guard's
#: verb list. Derived, so a verb added above cannot be missing from it.
VERB_NAMES: tuple[str, ...] = tuple(v.name for v in VERBS)

#: The feature toggles these verbs answer to, derived the same way.
FEATURES: tuple[str, ...] = tuple(v.feature for v in VERBS)


def verb(name: str) -> VerbSpec:
    """Look up one verb, or raise naming the ones that exist."""
    for spec in VERBS:
        if spec.name == name:
            return spec
    raise KeyError(f"{name!r} is not a verb declared here; declared: {', '.join(VERB_NAMES)}")


__all__ = ["FEATURES", "VERBS", "VERB_NAMES", "VerbSpec", "verb"]
