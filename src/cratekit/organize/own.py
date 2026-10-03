"""What the author made himself, and where it might live (U112).

``crate organize`` never moves, renames or removes a playlist the product did
not make. It LISTS each one and, where a home is obvious, names it, and the
plan says plainly that nothing moves. Obvious means one of two things and no
third:

* a FOLLOWED LABEL'S NAME is the playlist's whole name, or its first words:
  the label's folder on the account, ``Record Labels / <Label>`` in rekordbox;
* a YEAR, a standalone four digit number from 1980 to 2099 in the name, on the
  account only, where the year folders ``export archive`` files sets in live.

A label wins over a year, since ``Lobster Theremin 2021`` is that label's year.
Anything else gets no suggestion rather than a guess.

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

#: A year in a name: four digits from 1980 to 2099 with no digit either side.
_YEAR = re.compile(r"(?<!\d)(19[89]\d|20\d\d)(?!\d)")


def _fold(text: str) -> str:
    return " ".join(str(text).casefold().split())


def label_of(name: str, labels: Iterable[str]) -> str | None:
    """The followed label a name is, or starts with as whole words, else ``None``.

    The LONGEST matching label wins, so ``Kompakt Extra`` is not filed under a
    followed ``Kompakt`` when both are followed.
    """
    folded = _fold(name)
    best: str | None = None
    for label in labels:
        key = _fold(label)
        if not key:
            continue
        if folded == key or folded.startswith(key + " "):
            if best is None or len(key) > len(_fold(best)):
                best = label
    return best


def year_of(name: str) -> str | None:
    """The one year a name carries, or ``None`` when it carries none or several."""
    found = set(_YEAR.findall(str(name)))
    return found.pop() if len(found) == 1 else None


def account_home(name: str, labels: Iterable[str]) -> str | None:
    """Where an account playlist of the author's would obviously live, if anywhere."""
    label = label_of(name, labels)
    if label is not None:
        return f"the {label} label folder"
    year = year_of(name)
    if year is not None:
        return f"the {year} year folder"
    return None


def rekordbox_home(name: str, labels: Iterable[str], catalog: str | None) -> str | None:
    """Where a rekordbox playlist of the author's would obviously live, if anywhere.

    Only a label's folder, and only when the taxonomy declares the tree a label
    lands in, since a home named from a default nobody declared is a guess.
    """
    if catalog is None:
        return None
    label = label_of(name, labels)
    return f"{catalog} / {label}" if label is not None else None


__all__ = ["account_home", "label_of", "rekordbox_home", "year_of"]
