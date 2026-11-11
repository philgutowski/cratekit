"""Catalogue verification. A name match is a heuristic, never an identity.

The crawl finds candidates by copyright text and artist credits. That is
discovery. This module asks an external catalogue whether the claimed label
is actually credited, caches the answer per release, and drops anything that
is not confirmed. Guessing would acquire a compilation, a distributor credit,
or a neighbour imprint.
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

    For a reader that WRITES on the answer (U240): ``tag folder`` gives a file
    its label's genre on it. So it is stricter than :func:`labels_match` twice
    over. The other half, a credit inside a longer needle, is left out, so a
    line reading ``Music`` never names ``Aus Music``. And a letter of any script
    stays a letter, where :func:`fold_label` drops every one outside ASCII, so
    ``Âme`` never shrinks to ``me`` inside ``Give Me Records`` and ``東京
    Records`` never to ``records`` (U240's review, round two).
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


def save_cache(label_id: str, cache: Mapping[str, Mapping[str, Any]]) -> None:
    path = cache_path(label_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(cache), indent=2, ensure_ascii=False) + "\n")


def verify_release(
    claimed_label: str,
    release: Any,
    *,
    search: Callable[[str, Any], Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Verify one release. Does not touch the cache. ``search`` is injectable."""
    if search is not None:
        result = dict(search(claimed_label, release))
        if "verdict" in result:
            return result
        resolved = str(result.get("resolved_label") or result.get("label_name") or "")
        if not resolved:
            return {
                "verdict": "unconfirmed",
                "resolved_label": "",
                "source": str(result.get("source") or ""),
                "notes": "no label credit",
            }
        matched = labels_match(claimed_label, resolved)
        return {
            "verdict": "confirmed" if matched else "mismatch",
            "resolved_label": resolved,
            "source": str(result.get("source") or "search"),
            "notes": "" if matched else f"credited as {resolved!r}",
        }
    return {
        "verdict": "unconfirmed",
        "resolved_label": "",
        "source": "",
        "notes": "no verifier supplied",
    }


def cached_verdict(
    label_id: str,
    claimed_label: str,
    release: Any,
    *,
    search: Callable[[str, Any], Mapping[str, Any]] | None = None,
    cache: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return a cached verdict, or verify and store anything except errors."""
    held = cache if cache is not None else load_cache(label_id)
    release_id = str(getattr(release, "id", "") or "")
    if release_id and release_id in held:
        return held[release_id]
    verdict = verify_release(claimed_label, release, search=search)
    if verdict.get("verdict") != "error" and release_id:
        held[release_id] = verdict
        if cache is None:
            save_cache(label_id, held)
    return verdict
