"""The standalone utilities, and the verb declarations the CLI registry consumes.

    row 29  set builder   pure read over the library's own analyzed tags
    row 30  mastering     one recording at a time, source never modified
    row 31  backup        the volume mirror, the gated database snapshot, restore

None of them touches the rekordbox database, the acquisition adapter, the job
engine or the review queue; a change here that reaches for the writer has put a
utility inside the safety spine. Each verb names its implementation as a dotted
string, so the table stays inert and ``--help`` works on a slim install (KTD7).
The extras group is derived from ``profiles``, never restated; an external
binary, which pip cannot install, is recorded separately for doctor to check.
"""

from __future__ import annotations

from dataclasses import dataclass

from cratekit.core import profiles


@dataclass(frozen=True, slots=True)
class VerbSpec:
    """One subcommand, described well enough for the registry to build it lazily.

    ``feature`` is the ``profiles.MODULES`` toggle governing the verb, separate
    from ``name`` so a module's second verb cannot make half a module switchable.
    """

    name: str
    feature: str
    module: str
    summary: str
    #: Sub-actions the verb dispatches on, empty when it takes none.
    actions: tuple[str, ...] = ()
    #: External executables the verb shells out to, which no extras group can express.
    binaries: tuple[str, ...] = ()
    #: True when the verb can destroy user data, binding it to the library lock,
    #: the backup acknowledgment and the volume identity assertion (KTD24).
    destructive: bool = False

    @property
    def extras(self) -> str | None:
        """The extras group carrying this module's heavy Python dependencies, derived."""
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
        # No "setup": checking rclone and the remote is doctor's health check.
        actions=("check", "run", "restore", "restore-database"),
        binaries=("rclone",),
        # Restore overwrites a live database and its sidecars (KTD24).
        destructive=True,
    ),
)

#: The verb names, for the registry's parity check and the layering guard, derived.
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
