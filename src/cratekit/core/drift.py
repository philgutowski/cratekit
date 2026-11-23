"""How far a track's tempo moves, so a landing can mark rows for Dynamic analysis (U157).

THE DRIFT IS NOT A TEMPO, only a percent spread; no field carries a tempo (R17).
Shared here so the intake and analysis modules need not import each other.
"""

from __future__ import annotations

import math

#: ``unknown`` is too little rhythm to judge, never a guess; a landing treats it as steady.
STEADY = "steady"
VARIABLE = "variable"
UNKNOWN = "unknown"
VERDICTS = (STEADY, VARIABLE, UNKNOWN)

#: A file with no drift reading at all. Never written to a file.
UNSCORED = "unscored"

#: Phillip's Analyze Tracks standard, named once so every sentence agrees.
NORMAL_SETTINGS = "Analysis Mode Normal, high precision off, BPM/Grid, Phrase and KEY on"
DYNAMIC_SETTINGS = "Analysis Mode Dynamic, every other setting the same"


def verdict(drift: float | None, cut: float) -> str:
    """The verdict of ``drift`` against ``cut``; at the cut is variable, as for vocal scores."""
    if drift is None or not math.isfinite(drift):
        return UNKNOWN
    return VARIABLE if drift >= cut else STEADY


def shown(drift: float) -> str:
    """A drift as its file tag spells it, a percent to one decimal place."""
    return f"{drift:.1f}"


def parse(text: str | None) -> float | None:
    """The drift a file tag's text carries, or None when it carries no finite number."""
    if text is None:
        return None
    try:
        value = float(text)
    except ValueError:
        return None
    if not math.isfinite(value) or value < 0.0:
        return None
    return value


def reading(score_text: str | None, verdict_text: str | None, cut: float) -> tuple[float | None, str]:
    """The drift and verdict off a file's two tags, against ``cut``.

    THE SCORE IS READ AGAINST THE CUT CONFIGURED NOW, so a changed cut moves
    every row alike; the verdict tag counts only for :data:`UNKNOWN`.
    """

    score = parse(score_text)
    if score is not None:
        return score, verdict(score, cut)
    if (verdict_text or "").strip() == UNKNOWN:
        return None, UNKNOWN
    return None, UNSCORED

