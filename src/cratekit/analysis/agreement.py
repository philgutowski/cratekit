"""How far a head agrees with rekordbox's own analysis of the same file (R-744).

The head is a filename and a Name, never a grid, so a disagreement plays
nothing wrong; it tells a DJ reading the title a tempo the deck will not show.
This module measures that gap and nothing else. It reads a disposable copy of
the database through ``rb_writer.read_only_copy``, compares each row's head
with the row's stored tempo and key, and answers four tempo buckets and two
key buckets. It writes nothing anywhere, and it never opens the live file.

Which rows count as rekordbox's own analysis is the one judgment here. The
back catalogue's tempo was imported with the grid the source system wrote,
which is the same integer the head carries, so those rows agree with
themselves and measure nothing. A stored tempo that is not a whole number was
computed by rekordbox: no tool that fed this library writes a fraction. That
is the sample ``analysed_by_rekordbox`` keeps, and the bias it carries is
stated wherever the numbers are: it leans toward tracks with an unquantised
pulse and understates agreement on programmed music.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from cratekit.core import config, rb_writer
from cratekit.core.naming import NameTemplate, is_camelot, pad_camelot, parse_head

EQUAL = "equal"
OFF_ONE_TO_THREE = "off_one_to_three"
HALF_OR_DOUBLE = "half_or_double"
OTHER_LEVEL = "other_level"
#: The four tempo buckets, in the order the report prints them.
TEMPO_BUCKETS = (EQUAL, OFF_ONE_TO_THREE, HALF_OR_DOUBLE, OTHER_LEVEL)

KEY_EQUAL = "equal"
KEY_DIFFERS = "differs"

#: How far a ratio may sit from two, or from a half, and still be the same
#: pulse read an octave away. Two percent either side of a half is one bin of
#: the estimator at 60; eight percent either side of two holds 166 against
#: 83.13, which the interpolated estimator answers for a 166 pulse.
_DOUBLE_TOLERANCE = 0.08
_HALF_TOLERANCE = 0.02

#: Classic key names, as rekordbox spells them when its display is not set to
#: Camelot, to the unpadded Camelot code. Both enharmonic spellings of every
#: black key are here because rekordbox writes flats and a tag may carry
#: sharps, and a mapping that knows one spelling matches one library.
_CLASSIC_TO_CAMELOT: dict[str, str] = {
    "Abm": "1A", "G#m": "1A",
    "Ebm": "2A", "D#m": "2A",
    "Bbm": "3A", "A#m": "3A",
    "Fm": "4A",
    "Cm": "5A",
    "Gm": "6A",
    "Dm": "7A",
    "Am": "8A",
    "Em": "9A",
    "Bm": "10A",
    "F#m": "11A", "Gbm": "11A",
    "Dbm": "12A", "C#m": "12A",
    "B": "1B",
    "Gb": "2B", "F#": "2B",
    "Db": "3B", "C#": "3B",
    "Ab": "4B", "G#": "4B",
    "Eb": "5B", "D#": "5B",
    "Bb": "6B", "A#": "6B",
    "F": "7B",
    "C": "8B",
    "G": "9B",
    "D": "10B",
    "A": "11B",
    "E": "12B",
}


def camelot_from_scale_name(name: str | None) -> str | None:
    """A rekordbox key name in either notation as a padded Camelot code.

    ``8A`` and ``08A`` both answer ``08A``; ``Am`` answers ``08A`` too. A name
    in neither notation, or no name, answers None, so a row rekordbox has not
    keyed is counted as unkeyed rather than as a disagreement.
    """
    if not name:
        return None
    text = name.strip()
    if not text:
        return None
    classic = _CLASSIC_TO_CAMELOT.get(text)
    if classic is not None:
        return pad_camelot(classic)
    return pad_camelot(text) if is_camelot(text) else None


def round_half_up(value: float) -> int:
    """The integer a head carries for a fractional tempo: 126.5 is 127."""
    return int(math.floor(value + 0.5))


def tempo_bucket(head: int, reference: float) -> str:
    """Which of the four buckets a head's tempo falls in against a reference.

    Equal when the reference rounds to the head. Off by one to three when the
    rounded difference is that small, which is the estimator's bin width. Half
    or double when the ratio sits an octave away within the tolerances above.
    Everything else is another metrical level, three to two or four to three,
    or a track the two methods simply read differently.
    """
    if reference <= 0:
        return OTHER_LEVEL
    distance = abs(head - round_half_up(reference))
    if distance == 0:
        return EQUAL
    if distance <= 3:
        return OFF_ONE_TO_THREE
    ratio = head / reference
    if abs(ratio - 2.0) <= _DOUBLE_TOLERANCE or abs(ratio - 0.5) <= _HALF_TOLERANCE:
        return HALF_OR_DOUBLE
    return OTHER_LEVEL


@dataclass(frozen=True)
class HeadRow:
    """One collection row, as the comparison needs it."""

    identifier: str
    filename: str
    #: The stored tempo in the database's hundredths, None when unanalysed.
    stored_hundredths: int | None
    scale_name: str | None
    folder_path: str | None

    @property
    def reference_tempo(self) -> float | None:
        if not self.stored_hundredths or self.stored_hundredths <= 0:
            return None
        return self.stored_hundredths / 100.0

    @property
    def analysed_by_rekordbox(self) -> bool:
        """True when the stored tempo carries a fraction, see the module note."""
        return bool(self.stored_hundredths) and self.stored_hundredths % 100 != 0


@dataclass
class Agreement:
    """The distribution, with every row that could not be compared counted."""

    files: int = 0
    no_head: int = 0
    unanalysed: int = 0
    unkeyed: int = 0
    tempo: Counter = field(default_factory=Counter)
    within_one: int = 0
    key: Counter = field(default_factory=Counter)
    #: Up to twelve rows from the other-level bucket, head tempo against
    #: reference, so a reader can see what the bucket holds.
    examples: list[tuple[str, int, float]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "files": self.files,
            "no_head": self.no_head,
            "unanalysed": self.unanalysed,
            "unkeyed": self.unkeyed,
            "tempo": {bucket: self.tempo.get(bucket, 0) for bucket in TEMPO_BUCKETS},
            "within_one": self.within_one,
            "key": {KEY_EQUAL: self.key.get(KEY_EQUAL, 0), KEY_DIFFERS: self.key.get(KEY_DIFFERS, 0)},
            "examples": [list(example) for example in self.examples],
        }


_EXAMPLES = 12


#: A head to compare: the padded Camelot code, or None when the head has no
#: key, and the whole number tempo the head names.
Head = tuple[str | None, int]


def head_from_filename(filename: str, *, template: NameTemplate) -> Head | None:
    """The head the filename carries, or None when it carries no tempo."""
    parsed = parse_head(filename or "", template=template)
    if not parsed or "bpm" not in parsed:
        return None
    key = parsed.get("key")
    return (pad_camelot(key) if key else None, int(parsed["bpm"]))


def head_from_detection(found: dict[str, Any] | None) -> Head | None:
    """The head a detector's answer would be stamped with, or None for a terminal."""
    if not found or found.get("terminal") or found.get("rate") is None:
        return None
    camelot = found.get("camelot")
    return (pad_camelot(str(camelot)) if camelot else None, int(found["rate"]))


def compare(
    rows: Iterable[HeadRow],
    *,
    template: NameTemplate | None = None,
    head_of: Callable[[HeadRow], Head | None] | None = None,
) -> Agreement:
    """Bucket every row's head against the row's stored tempo and key.

    ``head_of`` answers the head to compare for a row, by default the one
    parsed off the filename. The re-analysis path hands in one that answers
    the detector's reading of the file instead, so one bucketing serves both.
    """
    template = template or NameTemplate()
    if head_of is None:
        def head_of(row: HeadRow) -> Head | None:
            return head_from_filename(row.filename, template=template)

    found = Agreement()
    for row in rows:
        found.files += 1
        head = head_of(row)
        if head is None:
            found.no_head += 1
            continue
        reference = row.reference_tempo
        if reference is None:
            found.unanalysed += 1
            continue
        head_key, head_tempo = head
        bucket = tempo_bucket(head_tempo, reference)
        found.tempo[bucket] += 1
        if abs(head_tempo - reference) <= 1.0:
            found.within_one += 1
        if bucket == OTHER_LEVEL and len(found.examples) < _EXAMPLES:
            found.examples.append((row.filename, head_tempo, reference))
        reference_key = camelot_from_scale_name(row.scale_name)
        if reference_key is None or head_key is None:
            found.unkeyed += 1
        else:
            found.key[KEY_EQUAL if head_key == reference_key else KEY_DIFFERS] += 1
    return found


def rows_of(db: Any) -> list[HeadRow]:
    """Every live collection row off an open handle, with its key name resolved."""
    names = {str(key.ID): key.ScaleName for key in db.get_key()}
    rows = []
    for content in db.get_content():
        if rb_writer.soft_deleted(
            content,
            message=(
                f"the collection row {getattr(content, 'ID', '?')!r} cannot say "
                f"whether rekordbox removed it, and counting a removed row would "
                f"measure a head nobody can see"
            ),
            origin=("analysis.agreement",),
            detail={"content_id": str(getattr(content, "ID", ""))},
        ):
            continue
        key_id = content.KeyID
        rows.append(
            HeadRow(
                identifier=str(content.ID),
                filename=content.FileNameL or "",
                stored_hundredths=content.BPM,
                scale_name=names.get(str(key_id)) if key_id is not None else None,
                folder_path=content.FolderPath,
            )
        )
    return rows


def read_rows(cfg: config.Config, *, database: Path | None = None) -> list[HeadRow]:
    """The rows, read off a disposable copy of ``database`` or the configured one.

    Refuses while rekordbox or its agent is running, as every read only copy
    does, because a copy taken under the live application describes no
    library that exists.
    """
    source = database if database is not None else cfg.library.db_path
    with rb_writer.read_only_copy(source, cfg=cfg) as db:
        return rows_of(db)


def measure(cfg: config.Config, *, database: Path | None = None) -> Agreement:
    """The heads as they stand on disk, against every row that carries a tempo."""
    return compare(read_rows(cfg, database=database))


def local_path(
    row: HeadRow, *, root: Path, rules: Sequence[Any]
) -> Path | None:
    """The row's file on this machine, through the given prefix rules."""
    from cratekit.core import locations

    if not row.folder_path:
        return None
    resolved = locations.resolve_recorded_path(row.folder_path, root=root, prefix_map=rules)
    if resolved.path is None:
        return None
    path = Path(resolved.path)
    return path if path.is_file() else None


def sample_for_reanalysis(
    rows: Iterable[HeadRow], cfg: config.Config, *, limit: int, step: int = 1
) -> list[tuple[HeadRow, Path]]:
    """Every ``step``-th row rekordbox analysed itself whose file is here, up to ``limit``.

    Lazy on purpose: a row is resolved and its file looked for only until the
    sample is full, so asking for ten files off a library of thousands costs
    ten resolutions and the rows skipped by ``step``, not a walk of the whole
    collection.
    """
    from cratekit.core import locations

    if step < 1:
        raise ValueError(f"step must be one or more, found {step!r}")
    rules = locations.prefix_rules(cfg.resolved_prefix_map())
    chosen: list[tuple[HeadRow, Path]] = []
    eligible = 0
    for row in rows:
        if len(chosen) >= limit:
            break
        if not row.analysed_by_rekordbox:
            continue
        path = local_path(row, root=cfg.library.root, rules=rules)
        if path is None:
            continue
        if eligible % step == 0:
            chosen.append((row, path))
        eligible += 1
    return chosen


def reanalyse(
    rows: Iterable[HeadRow],
    cfg: config.Config,
    *,
    detector: Callable[[Path], dict[str, Any] | None],
    limit: int,
    step: int = 1,
) -> Agreement:
    """Run the detector over a sample of rekordbox's own analyses and bucket it.

    Sequential on purpose: a pool whose worker dies mid file waits for ever,
    which is how the first measurement of R-744 was lost, and the person who
    asked for a number can pick a limit that fits the time they have.
    """
    chosen = sample_for_reanalysis(rows, cfg, limit=limit, step=step)
    measured: dict[str, Head | None] = {
        row.identifier: head_from_detection(detector(path)) for row, path in chosen
    }
    return compare([row for row, _path in chosen], head_of=lambda row: measured.get(row.identifier))


def format_report(found: Agreement, *, title: str) -> str:
    """The distribution as lines, the four tempo buckets first."""
    compared = sum(found.tempo.values())
    lines = [title, f"  rows: {found.files}, compared: {compared}"]
    lines.append(f"  no head: {found.no_head}, no stored tempo: {found.unanalysed}")
    for bucket in TEMPO_BUCKETS:
        count = found.tempo.get(bucket, 0)
        share = f"{100.0 * count / compared:.1f}%" if compared else "n/a"
        lines.append(f"  tempo {bucket.replace('_', ' ')}: {count} ({share})")
    lines.append(f"  tempo within one: {found.within_one}")
    keyed = sum(found.key.values())
    for bucket in (KEY_EQUAL, KEY_DIFFERS):
        count = found.key.get(bucket, 0)
        share = f"{100.0 * count / keyed:.1f}%" if keyed else "n/a"
        lines.append(f"  key {bucket}: {count} ({share})")
    lines.append(f"  unkeyed on one side: {found.unkeyed}")
    for filename, head_tempo, reference in found.examples:
        lines.append(f"    other level: {head_tempo} against {reference:.2f}  {filename}")
    return "\n".join(lines)
