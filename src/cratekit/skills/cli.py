"""``crate skills install``: copy the shipped operator skills where an agent reads them.

The skills are OPTIONAL (R7): every workflow runs from the CLI without them, so
nothing here may become a step another verb depends on.

COPIES, NEVER SYMLINKS: a link into the installed package breaks when the
package moves, while a copy survives upgrades and removal. EVERY COPY CARRIES
THE VERSION THAT WROTE IT, so a rerun finds copies written by another build,
warns of them as drift and repairs them in the same run.

Layer: modules. It names ``cratekit.cli.output`` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from collections.abc import Iterator
from importlib import resources
from pathlib import Path
from typing import Any

from cratekit import __version__
from cratekit.cli.output import Envelope
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy

#: The file each installed copy carries, naming the build that wrote it: a dot
#: file so an agent does not read it as a skill, and TOML like the other state.
STAMP_NAME = ".cratekit-skill.toml"

#: Where an agent looks for skills, under the home directory. The agent's own
#: convention, not a setting; a caller wanting elsewhere passes ``--into``.
DEFAULT_TARGET = (".claude", "skills")


def packaged_root():
    """The shipped skills, resolved through ``importlib.resources`` rather than
    ``__file__``, since a wheel need not be unpacked on a filesystem.
    """
    return resources.files("cratekit.skills") / "assets"


def shipped_names() -> tuple[str, ...]:
    """Every skill this build ships, sorted, derived by walking rather than listed."""
    root = packaged_root()
    return tuple(sorted(entry.name for entry in root.iterdir() if entry.is_dir()))


def _files(directory) -> Iterator[Any]:
    """Every regular file in one shipped skill, one level deep and no deeper."""
    yield from (entry for entry in directory.iterdir() if entry.is_file())


def _stamp_fields(destination: Path) -> Iterator[tuple[str, str]]:
    """Each ``name = value`` line of a copy's stamp, none when it is unstamped."""
    stamp = destination / STAMP_NAME
    if stamp.is_file():
        for line in stamp.read_text().splitlines():
            name, _, value = line.partition("=")
            yield name.strip(), value


def installed_version(destination: Path) -> str | None:
    """The version that wrote an installed copy, or None when it is unstamped.

    Unstamped is what a hand made copy looks like, reported as drift.
    """
    for name, value in _stamp_fields(destination):
        if name == "version":
            return value.strip().strip('"')
    return None


def stamped_files(destination: Path) -> tuple[str, ...]:
    """The files a previous install of this skill wrote, per its own stamp.

    A refresh removes exactly these; an unstamped copy names none, since nothing
    in it is this product's to delete.
    """
    for name, value in _stamp_fields(destination):
        if name == "files":
            body = value.strip().strip("[]")
            return tuple(part.strip().strip('"') for part in body.split(",") if part.strip())
    return ()


def install_one(name: str, into: Path) -> str:
    """Copy one shipped skill and stamp it. Returns what happened to it.

    ``installed`` when nothing was there, ``current`` when this build wrote it,
    ``refreshed`` when another build or a person did. ``current`` TOUCHES
    NOTHING, and a refresh removes only the files the previous stamp names, so
    a file the product never wrote is never deleted.
    """
    source = packaged_root() / name
    destination = into / name
    previous = installed_version(destination) if destination.exists() else None
    if not destination.exists():
        outcome = "installed"
    elif previous == __version__:
        # NOTHING IS WRITTEN ON THIS PATH.
        return "current"
    else:
        outcome = "refreshed"

    for stale in stamped_files(destination):
        # ``name`` only, never a path, so an edited stamp cannot reach outside.
        (destination / Path(stale).name).unlink(missing_ok=True)
    (destination / STAMP_NAME).unlink(missing_ok=True)

    destination.mkdir(parents=True, exist_ok=True)
    written = []
    for entry in _files(source):
        (destination / entry.name).write_bytes(entry.read_bytes())
        written.append(entry.name)
    listed = ", ".join(f'"{n}"' for n in sorted(written))
    (destination / STAMP_NAME).write_text(
        f'version = "{__version__}"\nskill = "{name}"\nfiles = [{listed}]\n'
    )
    return outcome


def build(parser, entry) -> None:
    """Declare the verb's arguments; unannotated so this layer names no CLI type."""
    del entry
    parser.add_argument(
        "--into",
        default=None,
        metavar="DIR",
        help=(
            "where to write the copies; defaults to the agent skills directory "
            "under your home directory"
        ),
    )
    parser.set_defaults(_handler=install_skills)


def default_target() -> Path:
    """The agent skills directory, composed from ``Path.home()`` so no home
    directory is a literal here (R1).
    """
    return Path.home().joinpath(*DEFAULT_TARGET)


def install_skills(ctx) -> Envelope:
    """Install every shipped skill into the target, and report what each one was.

    It writes outside the library and opens no session: the destructive session
    gates guard the rekordbox database, not an agent's configuration directory.
    """
    into = Path(ctx.args.into).expanduser() if ctx.args.into else default_target()
    try:
        into.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise CratekitError(
            Cause(
                reason="path-permission-denied",
                message=f"the skills directory {into} could not be created: {exc}",
                remediation=Remediation(remedy=Remedy.GRANT_PATH_ACCESS),
                origin=("skills.cli",),
                detail={"path": str(into)},
            )
        ) from exc

    checks = []
    counts = {"installed": 0, "refreshed": 0, "current": 0}
    for name in shipped_names():
        was = install_one(name, into)
        counts[was] += 1
        checks.append(
            {
                "key": f"skill.{name}",
                "title": name,
                # Drift warns as INFO: nothing is broken, the run repaired it.
                "status": "ok" if was in {"installed", "current"} else "info",
                "detail": _detail(was, name, into),
                "remedy": None,
            }
        )
    return ctx.envelope(
        data={
            "checks": checks,
            "summary": {
                "target": str(into),
                "version": __version__,
                **counts,
            },
        },
        outcome=Outcome.OK if checks else Outcome.NO_OP,
    )


def _detail(was: str, name: str, into: Path) -> str:
    """One sentence per skill, saying what a person now has."""
    where = into / name
    if was == "installed":
        return f"written to {where}"
    if was == "current":
        return f"already written by this build at {where}"
    return (
        f"the copy at {where} was written by a different build and has been "
        f"replaced; anything reading it was following older instructions"
    )
