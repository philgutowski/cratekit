"""How far a track's tempo moves, as a verdict a landing can mark (U157).

rekordbox analyses a row with one of two modes, Normal, which lays one tempo
over the whole track, and Dynamic, which follows a tempo that moves. Run on
the wrong rows each one costs: Dynamic on a steady 4/4 track lays a wobbling
grid with spurious tempo changes on breakdowns and beatless intros (on
2026-10-27 it did so on 116 rows of 116), and Normal on a live drummed track
lays a grid the drummer drifts off. Cratekit never writes a grid, so it cannot
choose the mode itself. The analysis run measures a DRIFT, the spread of
the tempo over the track's length as a percent of its middle, and writes it
with a verdict as two file tags; the native landing reads them against the
configured cut and marks every variable row with the ``dyn`` My Tag, and the
person running Analyze Tracks chooses each row's mode from the mark.

THE DRIFT IS NOT A TEMPO. It is a percent spread, and no field here or in the
tag table carries a tempo value in any container (R17). A drift of 4.4 says
the track's tempo moves by about four percent between its steady sections;
it says nothing about what the tempo is.

Here rather than in the analysis package, because the landing reads the same
words and makes the same comparison, and an intake module importing the
analysis module would make the feature modules depend on each other.

Layer: infrastructure. Imports nothing of the package.
"""

from __future__ import annotations

import math

#: The verdicts a drift reading takes. ``unknown`` is a file with too little
#: rhythmic material to judge, beatless, ambient or very short, and is never a
#: guess either way; a landing treats it as steady.
STEADY = "steady"
VARIABLE = "variable"
UNKNOWN = "unknown"
VERDICTS = (STEADY, VARIABLE, UNKNOWN)

#: What a landing calls a file that carries no drift reading at all, one
#: analysed before U157 for instance. Never written to a file.
UNSCORED = "unscored"

#: The rekordbox Analyze Tracks settings each kind of row takes, Phillip's
#: standard since 2026-10-27 (sitting 47, ``cli.tail.REKORDBOX_STEPS`` and the
#: rekordbox visit skill's table), so every sentence that names them names
#: the same ones.
NORMAL_SETTINGS = "Analysis Mode Normal, high precision off, BPM/Grid, Phrase and KEY on"
DYNAMIC_SETTINGS = "Analysis Mode Dynamic, every other setting the same"


def verdict(drift: float | None, cut: float) -> str:
    """The verdict a measured drift reads as against ``cut``, at or above it variable.

    None is no measurement, which is :data:`UNKNOWN`. At the cut is variable,
    as a vocal score at the cut is tagged, so one rule reads both marks.
    """
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
    """The drift and verdict a landing reads off a file's two tags, against ``cut``.

    THE SCORE IS READ AGAINST THE CUT CONFIGURED NOW, not the verdict the
    analysis wrote beside it, as a vocal score is read against the cut of the
    landing and not the one of the analysis, so a changed cut moves every row
    the same way. The verdict tag is read only for :data:`UNKNOWN`, which
    carries no score. A file with neither, or a score that is not a number,
    is :data:`UNSCORED`, and gets no mark.
    """
    score = parse(score_text)
    if score is not None:
        return score, verdict(score, cut)
    if (verdict_text or "").strip() == UNKNOWN:
        return None, UNKNOWN
    return None, UNSCORED


__all__ = [
    "DYNAMIC_SETTINGS",
    "NORMAL_SETTINGS",
    "STEADY",
    "UNKNOWN",
    "UNSCORED",
    "VARIABLE",
    "VERDICTS",
    "parse",
    "reading",
    "shown",
    "verdict",
]
