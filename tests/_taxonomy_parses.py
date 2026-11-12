"""Counting the taxonomy module's parses by their text (U247).

ONE COUNTER FOR EVERY SUITE THAT ASKS how often a taxonomy was parsed, so the
memo's tests and the verbs' tests count the same thing. It replaces the
``tomllib`` the taxonomy module reads at call time, and only that module's, so
a configuration or an artifact parsed elsewhere is not counted.

COUNT A TEXT THE TEST MADE UNIQUE. The memo lives for the process, so a text
another test already parsed can be answered from it with no parse at all, and
a count of zero there proves nothing. :func:`unique` appends a comment no other
test writes, which changes no declaration and makes the text a key of its own.
"""

from __future__ import annotations

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
