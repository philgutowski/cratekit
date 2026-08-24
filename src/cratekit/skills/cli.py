"""``crate skills install``: copy the shipped operator skills where an agent reads them.

THE SKILLS ARE OPTIONAL AND THAT IS THE PROPERTY THIS VERB MUST NOT BREAK. R7
says every workflow runs from the CLI without them, so nothing here may become a
step another verb depends on. What the verb buys is that a person who wants the
skills does not have to know where this package keeps them, or which of their
copies is stale.

COPIES, NEVER SYMLINKS. A symlink into the installed package points at a path
that is specific to how this machine installed the package, which is the
author's repository layout on a development checkout and a virtual environment's
internals everywhere else. The moment that path moves, an agent reading the link
gets nothing, and the failure looks like a missing skill rather than a broken
link. A copy is inert and survives the package being upgraded, moved or removed.

EVERY COPY CARRIES THE VERSION THAT WROTE IT, and re-running is how drift is
found. A skill instructs somebody to type a command; a skill written against an
older CLI instructs them to type a command that may no longer exist, and nothing
about reading it says so. The stamp is what lets this verb answer "these copies
were written by a different build" instead of leaving a person to notice.

DRIFT WARNS AND IS THEN REPAIRED, in that order and in one run. Reporting stale
copies without refreshing them would make the warning something a person has to
act on twice, and refreshing without saying so would hide that their agent had
been reading last month's instructions. Both happen and the report names which
skills were which.

Layer: modules. It names ``cratekit.cli.output`` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives at length.
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

#: The file each installed copy carries, naming the build that wrote it. A dot
#: file so an agent listing skills does not read it as one, and TOML because the
#: rest of this product's small state files are TOML and a second format buys
#: nothing.
STAMP_NAME = ".cratekit-skill.toml"

#: Where an agent looks for skills, relative to the user's home directory. NOT a
#: configuration value: this is the agent's own convention rather than something
#: this product gets to choose, and a setting would imply otherwise. A caller who
#: needs a different location passes one.
DEFAULT_TARGET = (".claude", "skills")


def packaged_root():
    """The shipped skills, as a traversable, resolved through the package.

    Through ``importlib.resources`` rather than ``Path(__file__).parent`` because
    the second is a claim about the package being unpacked on a filesystem, which
    is true of every install this product currently sees and is not a property of
    installing a wheel.
    """
    return resources.files("cratekit.skills") / "assets"


def shipped_names() -> tuple[str, ...]:
    """Every skill this build ships, sorted, derived by walking rather than listed.

    A list here would be a second register of the same fact, and the failure mode
    is the one P3 names: the list is right on the day it is written and silently
    misses the next skill added beside it.
    """
    root = packaged_root()
    return tuple(sorted(entry.name for entry in root.iterdir() if entry.is_dir()))


def _files(directory) -> Iterator[Any]:
    """Every regular file in one shipped skill, one level deep.

    One level because a skill is a directory of documents rather than a tree, and
    walking deeper would silently start shipping whatever somebody nests there.
    """
    yield from (entry for entry in directory.iterdir() if entry.is_file())


def installed_version(destination: Path) -> str | None:
    """The version that wrote an installed copy, or None when it is unstamped.

    Unstamped is a real state and not an error: it is what a copy somebody made
    by hand looks like, and it is reported as drift rather than as damage,
    because overwriting it is exactly what the person asked for.
    """
    stamp = destination / STAMP_NAME
    if not stamp.is_file():
        return None
    for line in stamp.read_text().splitlines():
        name, _, value = line.partition("=")
        if name.strip() == "version":
            return value.strip().strip('"')
    return None


def stamped_files(destination: Path) -> tuple[str, ...]:
    """The files a previous install of this skill wrote, per its own stamp.

    Recorded so a refresh can remove exactly what it put there and nothing else.
    An unstamped copy names none, which is correct: nothing in it was written by
    this product, so nothing in it is this product's to delete.
    """
    stamp = destination / STAMP_NAME
    if not stamp.is_file():
        return ()
    for line in stamp.read_text().splitlines():
        name, _, value = line.partition("=")
        if name.strip() == "files":
            body = value.strip().strip("[]")
            return tuple(
                part.strip().strip('"') for part in body.split(",") if part.strip()
            )
    return ()


def install_one(name: str, into: Path) -> str:
    """Copy one shipped skill and stamp it. Returns what happened to it.

    ``installed`` when nothing was there, ``current`` when the copy already came
    from this build, ``refreshed`` when it came from another one or from nowhere.
    Three answers rather than two, because "it was already right" and "it was
    wrong and now is right" are the two facts a person is running this to learn.

    THIS FUNCTION DESTROYED A USER'S OWN FILES AND REPORTED SUCCESS, and the fix
    is the reason it is shaped the way it is now. It used to ``rmtree`` the
    destination whenever the destination existed, INCLUDING on the ``current``
    path where there is nothing to do at all. Driven by an independent review: a
    file written beside the skill between two runs was gone after the second, and
    the second reported ``current``, status ``ok``, "already written by this
    build". That is data lost under a clean report, which is two of the four user
    facing costs ``docs/METHOD.md`` names, and this is the only verb in the
    product that removes a tree at a path the caller supplied.

    SO ``current`` NOW TOUCHES NOTHING, and a refresh removes exactly the files
    the previous stamp says this product wrote. The withdrawn-file property that
    the ``rmtree`` was reaching for survives, because a file this build no longer
    ships is named by the old stamp and by nothing else. A file the product never
    wrote is not the product's to delete, whatever directory it is sitting in.
    """
    source = packaged_root() / name
    destination = into / name
    previous = installed_version(destination) if destination.exists() else None
    if not destination.exists():
        outcome = "installed"
    elif previous == __version__:
        # NOTHING IS WRITTEN ON THIS PATH. Rewriting identical bytes would be
        # harmless and removing anything would not, and the honest report of "it
        # was already right" is a report about a directory nobody touched.
        return "current"
    else:
        outcome = "refreshed"

    for stale in stamped_files(destination):
        # ``name`` only, never a path, so a stamp somebody edited cannot reach
        # outside the directory it describes.
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
    """Declare the verb's arguments. The parameters are unannotated on purpose.

    ``entry`` is a ``cratekit.cli.registry.Entry`` and naming that type here
    would be this layer importing the one above it.
    """
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
    """The agent skills directory, composed rather than spelled.

    Composed from ``Path.home()`` so no home directory appears as a literal
    anywhere in this package, which is what R1 forbids and what the portability
    scanner checks for.
    """
    return Path.home().joinpath(*DEFAULT_TARGET)


def install_skills(ctx) -> Envelope:
    """Install every shipped skill into the target, and report what each one was.

    IT WRITES OUTSIDE THE LIBRARY AND OPENS NO SESSION, deliberately. The
    destructive-session gates exist for the rekordbox database and the files
    coupled to it; this verb touches an agent's configuration directory and
    nothing the library knows about, so requiring a backup acknowledgment to
    install a documentation file would be a gate over the wrong thing.
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
                # REFRESHED IS THE ONE THAT IS NOT "ok", which is the whole of
                # "drift warns". INFO rather than FAIL because nothing is broken
                # now: it was repaired by the run that noticed.
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
                "installed": counts["installed"],
                "refreshed": counts["refreshed"],
                "current": counts["current"],
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


__all__ = [
    "DEFAULT_TARGET",
    "STAMP_NAME",
    "build",
    "default_target",
    "install_one",
    "stamped_files",
    "install_skills",
    "installed_version",
    "packaged_root",
    "shipped_names",
]
