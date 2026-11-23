"""Counting the taxonomy module's parses by their text (U247).

One counter for every suite, replacing the ``tomllib`` the taxonomy module
reads at call time, and only that module's. The memo lives for the process,
so count a text the test made unique: :func:`unique` appends a comment no
other test writes.
"""

from __future__ import annotations

import os
import tomllib
import uuid

from cratekit.core import taxonomy


class Parses:
    """``tomllib`` as the taxonomy module sees it, recording every text it parses."""

    TOMLDecodeError = tomllib.TOMLDecodeError

    def __init__(self) -> None:
        self.texts: list[str] = []

    def loads(self, text: str, /, **kwargs):
        self.texts.append(text)
        return tomllib.loads(text, **kwargs)

    def of(self, text: str) -> int:
        """How many times ``text`` itself was parsed."""
        return sum(1 for seen in self.texts if seen == text)


def counted(monkeypatch) -> Parses:
    """Count every parse the taxonomy module makes for the rest of the test."""
    parses = Parses()
    monkeypatch.setattr(taxonomy, "tomllib", parses)
    return parses


def unique(text: str) -> str:
    """``text`` with a comment no other test writes, so it is a key of its own."""
    return f"{text}\n# a text of this test's own, {uuid.uuid4().hex}\n"


def renamed_in_place(text: str, display: str) -> tuple[str, str]:
    """``text`` with one display name replaced by another of the SAME LENGTH, and the new name.

    A memo keyed on a size, or a size and a time, would miss an edit that keeps
    the length, so only this kind of edit tells such a memo from the right one.
    """
    renamed = "X" * len(display)
    edited = text.replace(f'display = "{display}"', f'display = "{renamed}"', 1)
    assert edited != text and len(edited) == len(text), "the edit did not keep the length"
    return edited, renamed


def rewrite_keeping_time(path, text: str) -> None:
    """Write ``text`` over ``path`` in place, keeping its modification time and inode."""
    before = path.stat()
    path.write_text(text, encoding="utf-8")
    os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
    assert path.stat().st_mtime_ns == before.st_mtime_ns
