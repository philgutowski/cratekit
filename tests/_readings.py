"""Fake tag readings for a derivation, served field by field (U250).

The routing suites feed a derivation fake readings from each file's NAME, one
field per fixture: one fixture serves the genre and the energy, another the
vocal level, and a test composes them. They patch the three single field
readers in :mod:`cratekit.core.tags`, because before U250 ``rebuild.read_truth``
called those three.

``read_truth`` now reads all three fields through one container open, so a
patch of a single field reader no longer reaches it. :func:`serve_by_field`
puts it back: it replaces ``read_truth`` with a reader that asks the three
single field readers as they stand when it runs, so whatever each fixture
patched is what the derivation sees, and two fixtures still compose.

What this replaces is a FAKE of the tag read and nothing else. Every test that
uses it fakes the readings by name already; the production ``read_truth``, its
one open and its equality with the three readers are held by
``tests/test_rebuild_one_open.py`` over real containers.
"""

from __future__ import annotations

from pathlib import Path

import pytest


def serve_by_field(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make ``rebuild.read_truth`` answer from the three single field readers."""
    from cratekit.core import tags
    from cratekit.write import rebuild

    def by_field(path: Path) -> rebuild.Truth:
        return rebuild.Truth(
            location=str(path),
            genre=tags.read_genre_from_file(path),
            energy=tags.read_energy_from_file(path),
            voxlevel=tags.read_vox_from_file(path),
        )

    monkeypatch.setattr(rebuild, "read_truth", by_field)
