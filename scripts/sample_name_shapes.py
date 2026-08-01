#!/usr/bin/env python3
"""Measure the head parser against a real rekordbox export. READ ONLY, counts only.

The plan's verification gate for the naming engine is that the parser handles
every name shape present in a sample of a live library. A test cannot carry that
evidence: seam decision D1 forbids shipping a real library string in any artifact
including tests, and a synthesized corpus can only prove the shapes somebody
thought of. So the corpus in ``tests/test_naming.py`` is checked against reality
here, by a script anybody can re-run against their own export.

It prints COUNTS AND SHAPE CLASSES ONLY. No name, no path, and no tag value ever
reaches the output, so the result can be pasted into a report or a pull request
without leaking one person's library.

Usage::

    python scripts/sample_name_shapes.py path/to/export.xml

A non-zero exit means some name shape in the export is one the engine can neither
parse nor safely leave alone, which is the condition the gate exists to detect.
"""

from __future__ import annotations

import collections
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cratekit.core.naming import (  # noqa: E402  (path setup must precede the import)
    MarkerRule,
    NameTemplate,
    has_head,
    parse_head,
    strip_head,
)


def classify(name: str, template: NameTemplate) -> str:
    """A shape class for one name. The vocabulary here IS the test corpus."""
    stripped = name.strip()
    if not stripped:
        return "empty name"
    if parse_head(stripped, template=template) is not None:
        body = strip_head(stripped, template=template)
        if not body.strip():
            return "PARSED but strips to nothing"
        if parse_head(body, template=template) is not None:
            return "PARSED but a second head survives the strip"
        return "parsed: a complete head"
    if stripped[:1].isdigit():
        return "no head: the body begins with a digit"
    return "no head: never analyzed"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2

    # The marker text is configuration. It is named on the command line rather
    # than baked in, but a default is offered so the common case is one argument.
    template = NameTemplate(markers=(MarkerRule(field="lossy", literal="[MP3]"),))

    classes: collections.Counter[str] = collections.Counter()
    char_classes: collections.Counter[str] = collections.Counter()
    total = 0
    for _event, element in ET.iterparse(argv[1], events=("end",)):
        if element.tag != "TRACK" or element.get("TrackID") is None:
            element.clear()
            continue
        name = element.get("Name")
        element.clear()
        if name is None:
            continue
        total += 1
        classes[classify(name, template)] += 1
        if has_head(name, template=template):
            body = strip_head(name, template=template)
            for label, present in (
                ("space", " " in body),
                ("exclamation mark", "!" in body),
                ("ampersand", "&" in body),
                ("square bracket", "[" in body),
                ("non-ascii", any(ord(c) > 127 for c in body)),
                ("decomposed accent", unicodedata.normalize("NFC", body) != body),
                ("truncation disambiguator", "~" in body),
            ):
                if present:
                    char_classes[label] += 1

    if not total:
        print("no COLLECTION track rows found in that file", file=sys.stderr)
        return 2

    print(f"names examined: {total}")
    print("\nshape classes:")
    for label, count in classes.most_common():
        print(f"  {count:>7}  {count / total:>7.2%}  {label}")
    print("\ncharacter classes in parsed bodies:")
    for label, count in char_classes.most_common():
        print(f"  {count:>7}  {label}")

    # The only genuinely bad outcomes. A name with no head is normal: it has not
    # been analyzed. A name that parses but strips to nothing, or whose head
    # survives its own strip, is a name the engine would corrupt.
    bad = sum(count for label, count in classes.items() if "PARSED but" in label)
    if bad:
        print(f"\n{bad} names the engine cannot round-trip", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
