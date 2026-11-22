"""Catalogue verification. A name match is a heuristic, never an identity.

The crawl finds candidates by copyright text and artist credits, which is
discovery. This module asks a catalogue whether the claimed label is actually
credited and drops anything not confirmed, since a guess would acquire a
compilation, a distributor credit or a neighbour imprint.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from cratekit.core import config

CACHE_NAME = "verify.json"

_NORM = re.compile(r"[^a-z0-9]+")


def fold_label(value: str) -> str:
    return _NORM.sub(" ", (value or "").lower()).strip()


def _words_within(needle: str, credit: str) -> bool:
    """Whether the folded ``needle`` is a run of whole words inside ``credit``."""
    return f" {needle} " in f" {credit} "


_WORD_BREAK = re.compile(r"[\W_]+")


def _fold_words(value: str) -> str:
    """Case folded, every run of non word characters one space, letters of any script kept."""
    return _WORD_BREAK.sub(" ", (value or "").casefold()).strip()


def credit_names(needle: str, credit: str) -> bool:
    """Whether ``credit`` carries the whole of ``needle``, as whole words. One way only.

    For a reader that writes on the answer (U240), so stricter than
    :func:`labels_match` twice over: a credit inside a longer needle does not
    count (``Music`` never names ``Aus Music``), and a letter of any script
    stays a letter, so ``Âme`` never shrinks to ``me``.
    """
    left, right = _fold_words(needle), _fold_words(credit)
    return bool(left) and bool(right) and _words_within(left, right)


def labels_match(claimed: str, resolved: str) -> bool:
    """Whole words either way. Discovery heuristic, used only after a web hit.

    Both sides are folded first, so case and punctuation never decide it. Then
    one side must appear in the other as whole words (U237): ``Rawax`` matches
    ``RAWAX`` and ``Rawax Records``, and never ``RAWAXXX``, another act.
    """
    left, right = fold_label(claimed), fold_label(resolved)
    return bool(left) and bool(right) and (_words_within(left, right) or _words_within(right, left))


def cache_path(label_id: str) -> Path:
    return config.state_path("label_crawl_cache") / label_id / CACHE_NAME


def load_cache(label_id: str) -> dict[str, dict[str, Any]]:
    path = cache_path(label_id)
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return raw if isinstance(raw, dict) else {}


def _verdict(verdict: str, resolved: str, source: str, notes: str) -> dict[str, Any]:
    return {"verdict": verdict, "resolved_label": resolved, "source": source, "notes": notes}


def verify_release(
    claimed_label: str,
    release: Any,
    *,
    search: Callable[[str, Any], Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Verify one release. Does not touch the cache. ``search`` is injectable."""
    if search is None:
        return _verdict("unconfirmed", "", "", "no verifier supplied")
    result = dict(search(claimed_label, release))
    if "verdict" in result:
        return result
    resolved = str(result.get("resolved_label") or result.get("label_name") or "")
    if not resolved:
        return _verdict("unconfirmed", "", str(result.get("source") or ""), "no label credit")
    matched = labels_match(claimed_label, resolved)
    return _verdict(
        "confirmed" if matched else "mismatch",
        resolved,
        str(result.get("source") or "search"),
        "" if matched else f"credited as {resolved!r}",
    )
