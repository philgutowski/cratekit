"""Fake tag readings for a derivation, served per field at ``tags.read_tags`` (U250).

The routing suites compose per field fakes keyed on each file's NAME, served
at :func:`cratekit.core.tags.read_tags`, so the production ``read_truth``
still runs with its one open, field keys and number conversion. A served
field answers stored text (numbers as digits) or None; an unserved field
reads the real file. :func:`read_tag` and the single field readers see the
fake; the strict readers (``read_tags_checked``, the energy reader) do not.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

Lookup = Callable[[Path], object]


def serve_field(monkeypatch: pytest.MonkeyPatch, field: str, lookup: Lookup) -> None:
    """Serve ``field`` from ``lookup(path)`` to every ``tags.read_tags`` call.

    One wrapper per test, added to, so fixtures compose and the later wins a
    shared field. Undone with the test's monkeypatch.
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
    """Serve the routing readings by lookup, at ``read_tags`` and the single readers."""
    from cratekit.core import tags

    for field, lookup in (("genre", genre), ("energylevel", energy), ("voxlevel", vox)):
        if lookup is None:
            continue
        serve_field(monkeypatch, field, lookup)
        monkeypatch.setattr(
            tags, _READERS[field], lambda path, lookup=lookup: lookup(Path(path))
        )
