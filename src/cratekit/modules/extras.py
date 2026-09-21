"""The command that installs a missing extras group, for the environment running.

ONE SOURCE, AND IT LIVES IN THE MODULES LAYER ON PURPOSE. The parser stub renders
this command in ``cli/render.py``, and two workers put the same command in a
refusal from inside the analysis module. The workers may not import the CLI
(KTD23), and nothing below the modules layer may spell a package manager line
(D2), so this is the lowest place both can reach and the highest place allowed to
write the words. A second copy anywhere else is the copy that drifts.

THE COMMAND DEPENDS ON HOW CRATEKIT WAS INSTALLED (R-395). The README installs
with pipx, which keeps Cratekit in a private environment, and a bare ``pip`` runs
against whichever Python the shell finds first. So the answer is read from the
running interpreter:

- A pipx environment holds ``pipx_metadata.json`` at its root. It gets
  ``pipx install --force`` against the source pipx recorded, with the extras
  already chosen kept, because ``--force`` reinstalls from exactly the spec given
  and naming only the missing extra would drop the one already there. Extras
  added with pip directly are not in pipx's record, so ``pipx reinstall`` would
  drop them too, which is why this is not simply the pip form below.
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


def install_command(extras: str) -> str:
    """The exact command that installs ``extras`` where this process runs.

    Quoted with ``shlex`` because several shells read square brackets as a glob,
    and a clone path may hold a space.
    """
    prefix = Path(sys.prefix)
    if (prefix / PIPX_METADATA).is_file():
        source, chosen = _pipx_source(prefix / PIPX_METADATA)
        wanted = ",".join(sorted({*chosen, extras}))
        return shlex.join(["pipx", "install", "--force", f"{source}[{wanted}]"])
    return shlex.join(
        [sys.executable, "-m", "pip", "install", f"{DISTRIBUTION}[{extras}]"]
    )


def _pipx_source(metadata: Path) -> tuple[str, tuple[str, ...]]:
    """The clone pipx installed from and the extras it recorded.

    The source falls back to ``.``, the README's form, which is run from inside
    the clone, whenever the record cannot name a directory that still exists:
    an unreadable file, a moved clone, a source that is not a folder at all.
    The recorded extras are kept whenever they can be read, even when the
    source cannot be used, because dropping them is the failure the pipx form
    exists to prevent.
    """
    try:
        recorded = json.loads(metadata.read_text(encoding="utf-8"))
        spec = recorded["main_package"]["package_or_url"]
    except (OSError, ValueError, KeyError, TypeError):
        return ".", ()
    match = _SPEC.match(spec) if isinstance(spec, str) else None
    if match is None:
        return ".", ()
    chosen = tuple(e.strip() for e in (match["extras"] or "").split(",") if e.strip())
    source = match["source"] if Path(match["source"]).is_dir() else "."
    return source, chosen


__all__ = ["DISTRIBUTION", "PIPX_METADATA", "install_command"]
