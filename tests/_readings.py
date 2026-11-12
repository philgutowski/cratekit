"""Fake tag readings for a derivation, served per field at ``tags.read_tags`` (U250).

The routing suites feed a derivation fake readings from each file's NAME, one
field per fixture: one fixture serves the genre and the energy, another the
vocal level, and a test composes them. Before U250 they patched the three
single field readers in :mod:`cratekit.core.tags`, because ``rebuild.read_truth``
called those three. It now reads all three fields through one
:func:`cratekit.core.tags.read_tags` open, so the readings are served there.

THE PRODUCTION ``read_truth`` STILL RUNS, which is the point of serving the
fake one layer down: its one open, its field keys and its number conversion
are all exercised by every routing test, so a crossed key or a dropped field
in it fails those suites and not only ``tests/test_rebuild_one_open.py``.

A served field answers what its lookup gives, as stored text (a number is
served as its digits, so ``tags.whole_number`` converts it back), and None as
absent. A field nobody served, and every call that asks for no served field,
reads the real file. :func:`read_tag` and the single field readers built on
it go through ``read_tags`` too, so they see the same fake; the strict
readers (``read_tags_checked``, and the energy reader through it) do not, and
a fixture that needs those keeps its own patch of them.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

Lookup = Callable[[Path], object]


def serve_field(monkeypatch: pytest.MonkeyPatch, field: str, lookup: Lookup) -> None:
    """Serve ``field`` from ``lookup(path)`` to every ``tags.read_tags`` call.

    Installs one wrapper per test and adds to it, so two fixtures serving
    different fields compose, and the later one wins for a field both serve,
    as a later monkeypatch always has. Undone with the test's monkeypatch.
    """
    from cratekit.core import tags

    served: dict[str, Lookup] | None = getattr(tags.read_tags, "_served", None)
    if served is None:
        real = tags.read_tags
        served = {}

        def read_tags(path: Path, fields) -> dict[str, str | None]:
            values = real(path, fields)
            for name in fields:
                if name in served:
                    value = served[name](Path(path))
                    values[name] = None if value is None else str(value)
            return values

        read_tags._served = served  # type: ignore[attr-defined]
        monkeypatch.setattr(tags, "read_tags", read_tags)
    if field not in tags.FIELDS:
        raise ValueError(f"unknown tag field: {field!r}")
    served[field] = lookup


#: The single field reader each served field also answers through, patched
#: alongside so a path that reads one field alone sees the same fake.
_READERS = {
    "genre": "read_genre_from_file",
    "energylevel": "read_energy_from_file",
    "voxlevel": "read_vox_from_file",
}


def serve_readings(
    monkeypatch: pytest.MonkeyPatch,
    *,
    genre: Lookup | None = None,
    energy: Lookup | None = None,
    vox: Lookup | None = None,
) -> None:
    """Serve the routing readings by lookup, at ``read_tags`` and the single readers.

    Each lookup takes the file's path and answers its value or None. A field
    left out is not served, and a later call serving it adds to this one.
    """
    from cratekit.core import tags

    for field, lookup in (("genre", genre), ("energylevel", energy), ("voxlevel", vox)):
        if lookup is None:
            continue
        serve_field(monkeypatch, field, lookup)
        monkeypatch.setattr(
            tags, _READERS[field], lambda path, lookup=lookup: lookup(Path(path))
        )
