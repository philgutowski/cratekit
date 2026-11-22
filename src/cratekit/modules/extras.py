"""The command that installs a missing extras group, for the environment running.

ONE SOURCE, in the modules layer: the parser stub in ``cli/render.py`` and the
analysis workers both print it, the workers may not import the CLI (KTD23), and
nothing below this layer may spell a package manager line (D2).

The command depends on how Cratekit was installed, read from the running
interpreter (R-395):

- A pipx environment holds ``pipx_metadata.json`` at its root and gets
  ``pipx install --force`` against the source pipx recorded, with the extras
  already chosen kept, since ``--force`` reinstalls exactly the spec given. A
  release install recorded as a direct reference, ``cratekit[analysis] @
  git+...``, is reinstalled from that same reference.
- Anything else gets ``<this interpreter> -m pip``, which installs into the
  environment ``crate`` runs from whether or not it is activated.
"""

from __future__ import annotations

import json
import re
import shlex
import sys
from pathlib import Path

#: The distribution name. ``cli.registry`` re-exports it, so the doctor's
#: metadata lookups and this command cannot name two different packages.
DISTRIBUTION = "cratekit"

PIPX_METADATA = "pipx_metadata.json"

# A recorded source with an optional extras suffix, ``/path/to/clone[analysis]``.
_SPEC = re.compile(r"^(?P<source>[^\[\]]+)(?:\[(?P<extras>[^\[\]]*)\])?$")

# A PEP 508 direct reference to this distribution as pipx records one,
# ``cratekit[analysis] @ git+url``; a reference to anything else is not this install.
_REFERENCE = re.compile(
    rf"^(?P<name>{re.escape(DISTRIBUTION)})\s*(?:\[(?P<extras>[^\[\]]*)\])?\s*@\s*(?P<url>\S+)$",
    re.IGNORECASE,
)


def install_command(extras: str) -> str:
    """The exact command that installs ``extras`` where this process runs.

    Quoted with ``shlex`` because several shells read square brackets as a glob,
    and a clone path may hold a space.
    """
    prefix = Path(sys.prefix)
    if (prefix / PIPX_METADATA).is_file():
        reference = _pipx_reference(prefix / PIPX_METADATA)
        if reference is not None:
            name, chosen, url = reference
            wanted = ",".join(sorted({*chosen, extras}))
            return shlex.join(["pipx", "install", "--force", f"{name}[{wanted}] @ {url}"])
        source, chosen = _pipx_source(prefix / PIPX_METADATA)
        wanted = ",".join(sorted({*chosen, extras}))
        return shlex.join(["pipx", "install", "--force", f"{source}[{wanted}]"])
    return shlex.join([sys.executable, "-m", "pip", "install", f"{DISTRIBUTION}[{extras}]"])


def _recorded_spec(metadata: Path) -> str | None:
    try:
        recorded = json.loads(metadata.read_text(encoding="utf-8"))
        spec = recorded["main_package"]["package_or_url"]
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return spec if isinstance(spec, str) else None


def _extras(match: re.Match[str]) -> tuple[str, ...]:
    return tuple(e.strip() for e in (match["extras"] or "").split(",") if e.strip())


def _pipx_reference(metadata: Path) -> tuple[str, tuple[str, ...], str] | None:
    """The name, extras and url of a release install pipx recorded, or None.

    Reinstalling from that same reference, at the same tag, keeps the extras;
    the clone form below would fall back to ``.`` and drop them.
    """
    spec = _recorded_spec(metadata)
    match = _REFERENCE.match(spec) if spec is not None else None
    if match is None:
        return None
    return match["name"], _extras(match), match["url"]


def _pipx_source(metadata: Path) -> tuple[str, tuple[str, ...]]:
    """The clone pipx installed from and the extras it recorded.

    The source falls back to ``.``, the README's form run from inside the clone,
    whenever the record names no directory that still exists. The recorded
    extras are kept whenever they can be read, even then, because dropping them
    is the failure the pipx form exists to prevent.
    """
    spec = _recorded_spec(metadata)
    match = _SPEC.match(spec) if spec is not None else None
    if match is None:
        return ".", ()
    chosen = _extras(match)
    source = match["source"] if Path(match["source"]).is_dir() else "."
    return source, chosen
