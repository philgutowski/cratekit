"""The names the rest of configuration builds on: the schema version, the
keys and environment variables, the failure types and the directory
resolvers.

Split from :mod:`cratekit.core.config` (U299), which re-exports every name
here. Nothing here touches the filesystem at import (Rule 1 of config).
"""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING

import platformdirs

if TYPE_CHECKING:
    pass


#: The schema this build writes. Bumped only with a ``MIGRATIONS`` entry;
#: ``test_config_migration.py`` fails on a gap.
CURRENT_SCHEMA_VERSION = 1


#: The on-disk shape of the library state directory, separate from
#: ``CURRENT_SCHEMA_VERSION`` because ``MIGRATIONS`` is dict to dict and cannot
#: move a file. Nothing migrates a library state directory yet, as no build ever
#: wrote another shape. The unit that bumps this owns a one-time reconciliation
#: under the migration lock, idempotent and refusing rather than half-moving;
#: ``tests/test_config.py`` fails a bump without one.
LIBRARY_STATE_LAYOUT_VERSION = 1


CONFIG_FILENAME = "config.toml"


#: The key U31's destructive-operation assertion reads (R38), named here so a
#: guard never hardcodes the name of what it guards.
VOLUME_IDENTITY_KEY = "library.volume_id"


#: The key naming which shipped taxonomy template a library adopted (S6).
#: Only its shape is validated here; membership belongs to the taxonomy module
#: a layer above, so the wizard and doctor enforce it. A path-shaped value is
#: refused because the reader composes it into a packaged resource name.
TAXONOMY_TEMPLATE_KEY = "taxonomy.template"


#: A shipped template's short name: a bare token, never a path fragment.
_TEMPLATE_NAME_SHAPE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def template_name_is_usable(value: object) -> bool:
    """Whether ``value`` is a shape this configuration can carry as a template name.

    Public so the packaged template walker applies the same rule and never
    offers a name configuration would reject.
    """
    return isinstance(value, str) and bool(_TEMPLATE_NAME_SHAPE.match(value))


# Environment overrides. Each relocates a configured value and none supplies
# one, so a machine with no setup can never resolve a library root from the
# environment and write to the wrong volume (R38). They are applied in one
# place, ``_apply_env_overrides``, before any rule is decided, so validation and
# the builder see the same root. Relocating the root also re-bases a db_path
# under it, which is what keeps tests off the real rekordbox database.
ENV_CONFIG_DIR = "CRATEKIT_CONFIG_DIR"


ENV_STATE_DIR = "CRATEKIT_STATE_DIR"


ENV_LIBRARY_ROOT = "CRATEKIT_LIBRARY_ROOT"


#: The directory the ISRC cache and its lock live in, when set (U206). A copy
#: run points it at the live state directory so catalogue answers are not paid
#: for twice; ``core.rehearsal`` does that for every rehearsal.
ENV_ISRC_CACHE_DIR = "CRATEKIT_ISRC_CACHE_DIR"


#: The directory the provider gate's state file and its lock live in, when set
#: (U278). Unset, they live under the platform's installation state directory,
#: never under ``CRATEKIT_STATE_DIR``, so a copy run spends from the one
#: allowance the live run reads. The suite sets this to each test's own state.
ENV_PROVIDER_GATE_DIR = "CRATEKIT_PROVIDER_GATE_DIR"


ENV_DOWNLOAD_STAGING = "CRATEKIT_DOWNLOAD_STAGING"


_APP_NAME = "cratekit"


def config_dir() -> Path:
    """The installation-scoped configuration directory (KTD6, R1). Creates nothing."""
    override = os.environ.get(ENV_CONFIG_DIR)
    if override:
        return Path(override)
    return Path(platformdirs.user_config_dir(_APP_NAME))


def installation_state_dir() -> Path:
    """The installation-scoped state directory, distinct from the config directory.

    Kept apart so syncing a config directory between machines never syncs one
    machine's job queue and caches.
    """
    override = os.environ.get(ENV_STATE_DIR)
    if override:
        return Path(override)
    return Path(platformdirs.user_state_dir(_APP_NAME))


def _dig(data: Mapping, dotted: str):
    """Fetch a dotted key from nested mappings, or return None when absent."""
    node: object = data
    for part in dotted.split("."):
        if not isinstance(node, Mapping) or part not in node:
            return None
        node = node[part]
    return node


def is_inside(child: Path, parent: Path) -> bool:
    """True when ``child`` is ``parent`` or sits under it. Purely textual.

    No ``resolve()`` or ``exists()`` (Rule 1); ``normpath`` collapses ``..`` so
    a typed path cannot escape by spelling.
    """
    child_parts = Path(os.path.normpath(str(child))).parts
    parent_parts = Path(os.path.normpath(str(parent))).parts
    return child_parts[: len(parent_parts)] == parent_parts
