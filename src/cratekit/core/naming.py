"""The one name builder and the one head parser.

Every renamer in the source system agreed on the name shape by convention and
disagreed at the edges by accident. Eight independent regexes read or wrote the
``{key} - {bpm} - `` head, and two independent call sites hand-assembled the head
string used for byte-budget measurement. The drift was not theoretical: it is how
the 2026-07-04 import rejections happened, and the file-length rule below records
what that cost.

Three rules this module exists to hold, each with the failure it prevents:

1. **Budget measurement uses the WIDEST form the name will ever take, not the
   form being written now.** The library convention emits a single-digit Camelot
   key and a separate later stage zero-pads it, growing every filename by exactly
   one byte. A name fitted to exactly the ceiling therefore *exceeds* it the
   moment padding runs, and the padding stage is a pure rename with no budget
   check of its own, so nothing downstream catches it. rekordbox then refuses the
   import. Measuring with the padded key pre-reserves that byte.

2. **Truncation is deterministic.** A shortened stem carries a hash of the
   original, so two distinct long titles that share a prefix cannot collapse onto
   one filename, and a killed run re-derives the identical path on resume. The
   resume marker for the whole analysis pass is the presence of the head on disk,
   so a nondeterministic name would orphan the previous run's claim stub and
   accumulate one more stub on every relaunch.

3. **Absent fields are omitted, never rendered empty.** A naive template with no
   key and no tempo emits ``"None - None - Title"`` or ``" -  - Title"``, and that
   string is then baked into the filename AND the tag. The head parser does not
   recognize it, so nothing ever removes it, and every downstream matcher sees the
   junk as part of the title and stops matching the track against its own library
   copy. This is R20's real content.

**This module takes configuration as PARAMETERS and imports no configuration**
(seam decision S3). Config owns the values: the marker text, the path byte budget,
the filename byte budget. This module owns the mechanism. The separation is not
tidiness. A function that reads global configuration cannot be exercised against
two different templates in one process, and proving that a second template renders
and parses correctly with no code change is the only evidence that this engine is
template-driven rather than convention-driven with a settings file bolted on.

Pure functions only, with one exception: ``claim_target``, the no-overwrite rename
claim. No clock, no randomness, no environment, no configuration.

LIVE-LIBRARY EVIDENCE (2026-08-01, an export of 10,070 collection rows). 98.28% of
names carry a head this parser reads. The remaining 1.72% are 169 names with no
head at all (never analyzed), 3 titles that merely begin with a digit, and 1 name
carrying a key with no tempo. Zero names matched only the looser deleted parser:
no lowercase key, no off-wheel key, and no decimal tempo exists in the library, so
deleting that parser removes nothing real. All 15 marked names carry the marker in
head position, which is the coupling rule below asserted against production.
"""

from __future__ import annotations

import hashlib
import itertools
import os
import re
from dataclasses import dataclass, replace
from functools import lru_cache

# Audio formats a renamer will consider. Lossy extensions are present because a
# fallback acquisition still has to be analyzed, renamed, and repaired like any
# other file.
#
# KNOWN DRIFT, recorded rather than silently reproduced: the source system has
# five independent copies of this tuple with three different memberships, so a
# format one tool renames is invisible to another. The live library today holds
# only .flac, .aiff, .mp3 and .wav, which means every other entry here is
# untested by production. ``.alac`` in particular is inert: ALAC ships inside an
# .m4a container and no file carries that extension. It is kept so that a library
# adopted from another tool is not silently skipped, not because it is expected.
AUDIO_EXTS = (
    ".flac", ".aiff", ".aif", ".wav", ".alac",
    ".mp3", ".m4a", ".aac", ".opus", ".ogg", ".webm",
)


# ---------------------------------------------------------------------------
# The head field vocabulary
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HeadField:
    """One field a name head may carry.

    ``pattern`` and ``anchorable`` are what make render and parse two views of one
    declaration rather than two implementations that drift. A field type is added
    in code, deliberately: each new field needs a pattern that a parser can read
    back and a judgement about whether its shape can safely LEAD a head, and
    neither of those is something a configuration file can be trusted to assert.
    """

    name: str
    pattern: str
    anchorable: bool
    #: Human wording used in refusals, so an invalid template says what is wrong.
    describe: str


# The wheel bound, written once. Private copies elsewhere in the source used a
# bare two-digit class and accepted 13, 0, and 99, so a harmonic lookup returned a
# confident answer for a key that does not exist on the wheel.
_CAMELOT_NUMBER = r"(?:[1-9]|1[0-2])"
_CAMELOT_LETTER = r"[AB]"

# The Camelot code, padded or unpadded. Case-SENSITIVE inside a head, and the
# asymmetry with `parse_camelot` below is deliberate rather than an oversight:
# a code READ from a detector or a user may be lowercase and is normalized, but a
# name already written to disk in lowercase was written by something that was not
# following the convention, and silently accepting it lets that writer keep
# existing. The deleted duplicate parser accepted lowercase, which is how a
# marked lossy copy and its lossless twin normalized to different match keys and
# both landed in the same playlist as duplicates.
_KEY_FIELD = HeadField(
    name="key",
    pattern=rf"0?{_CAMELOT_NUMBER}{_CAMELOT_LETTER}",
    anchorable=True,
    describe="a Camelot code, 1A..12B, padded or not",
)

# Integer tempo, 1 to 3 digits. NOT anchorable: a bare integer at the start of a
# name is indistinguishable from a title that begins with a number, and the live
# library contains three of those. A head led by tempo could not be parsed back,
# so a template declaring one is refused at construction rather than emitting
# names that no consumer can strip.
_BPM_FIELD = HeadField(
    name="bpm",
    pattern=r"\d{1,3}",
    anchorable=False,
    describe="an integer tempo, 1-3 digits",
)

HEAD_FIELDS: dict[str, HeadField] = {f.name: f for f in (_KEY_FIELD, _BPM_FIELD)}

#: Spec flags that a template may attach a marker to. R21 makes marking mandatory
#: whenever the flag is set, so this list is also the list of flags whose marking
#: is enforced at render time.
MARKED_FLAGS = ("lossy",)

#: Key padding policies, ordered by the width they produce. Ordering is what lets
#: a template be validated: the form measured for the budget must never be
#: narrower than the form actually written, or the budget under-measures and the
#: 2026-07-04 failure returns by a different route.
KEY_PADS = ("none", "camelot2")


# ---------------------------------------------------------------------------
# The declarations: template, budget, spec
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MarkerRule:
    """A flag on the spec that becomes a literal inside the head.

    ``literal`` has no default. Config owns the marker text (S3), and a default
    here would be a second place for it to live, which is the drift this whole
    module exists to end. The template references the marker by FIELD NAME; the
    text arrives as data.
    """

    field: str
    literal: str
    sep: str = " "


@dataclass(frozen=True)
class NameTemplate:
    """The declared shape of a name.

    Defaults describe STRUCTURE only: which fields, in what order, joined by what.
    No value config owns appears here, which is why a template can be constructed
    in a test without a config file and why two templates can coexist in one
    process.
    """

    head_fields: tuple[str, ...] = ("key", "bpm")
    #: Head fields that may be absent while the head still renders. Empty by
    #: default, which reproduces the source convention exactly: the head is
    #: all-or-nothing. Declaring a field optional widens BOTH render and parse
    #: together, because they are derived from the same shape table below. That
    #: coupling is the point: a name shape that can be written but not read is
    #: how a head ends up permanently glued to a title.
    head_optional: frozenset[str] = frozenset()
    head_sep: str = " - "
    head_term: str = " - "
    #: The separator between segments of the body. Distinct from ``head_sep``
    #: even though both are " - " today, because the dedupe rule parses on this
    #: one and a template that changes the head must not silently change dedupe.
    segment_sep: str = " - "
    markers: tuple[MarkerRule, ...] = ()
    #: How the key is WRITTEN. Padded at write time (U39): the library holds
    #: the two-digit form, and writing it here is what absorbed the source
    #: system's separate padding sweep. The budget below was measured against
    #: this form from the start, so the flip widens nothing.
    key_pad: str = "camelot2"
    #: How the key is MEASURED. The widest form the key will ever take, so a later
    #: padding stage cannot push a fitted name over the ceiling.
    budget_key_pad: str = "camelot2"

    def __post_init__(self) -> None:
        for name in self.head_fields:
            if name not in HEAD_FIELDS:
                raise ValueError(
                    f"unknown head field {name!r}; declared fields are "
                    f"{sorted(HEAD_FIELDS)}. A field needs a pattern a parser can "
                    f"read back, so it is added in code, not in configuration."
                )
        if len(set(self.head_fields)) != len(self.head_fields):
            raise ValueError(f"duplicate head field in {self.head_fields!r}")
        unknown_optional = set(self.head_optional) - set(self.head_fields)
        if unknown_optional:
            raise ValueError(
                f"head_optional names {sorted(unknown_optional)}, which are not in "
                f"head_fields {self.head_fields!r}"
            )
        for pad in (self.key_pad, self.budget_key_pad):
            if pad not in KEY_PADS:
                raise ValueError(f"unknown key padding {pad!r}; known: {list(KEY_PADS)}")
        if KEY_PADS.index(self.budget_key_pad) < KEY_PADS.index(self.key_pad):
            raise ValueError(
                f"budget_key_pad {self.budget_key_pad!r} is narrower than key_pad "
                f"{self.key_pad!r}; the budget must be measured against the widest "
                f"form the name will ever take, or a later widening re-exceeds it"
            )
        for rule in self.markers:
            if rule.field not in MARKED_FLAGS:
                raise ValueError(
                    f"marker rule names {rule.field!r}, which is not a markable flag "
                    f"({list(MARKED_FLAGS)})"
                )
            if not rule.literal:
                raise ValueError(f"marker rule for {rule.field!r} has an empty literal")
        for shape in head_shapes(self):
            lead = HEAD_FIELDS[shape[0]]
            if not lead.anchorable:
                raise ValueError(
                    f"a head may not begin with {lead.name!r} ({lead.describe}): a name "
                    f"starting that way cannot be told apart from a title that happens "
                    f"to start the same way, so the head could be written and never "
                    f"stripped again"
                )


@dataclass(frozen=True)
class NameBudget:
    """The two byte ceilings, both required.

    Neither has a default, on purpose. Config owns both values (S3), and a default
    here would let a caller silently measure against a number nobody configured.
    Bytes, not characters: 170 characters of Japanese pass any character count and
    are 510 bytes on disk.
    """

    #: Ceiling on the UTF-8 byte length of the whole absolute path.
    path_budget_bytes: int
    #: Per-component cap. Independent of the path ceiling; both are enforced.
    filename_max_bytes: int
    #: Hex characters of the truncation disambiguator. Mechanism, not policy, so
    #: it lives here with a default: 6 hex characters is 24 bits of collision
    #: space against a population of one library's long titles.
    hash_len: int = 6


@dataclass(frozen=True)
class NameSpec:
    """Everything a name is built from. Analysis results arrive as VALUES.

    ``lossy`` is a boolean the caller supplies, never something this module
    probes. Probing means running an external binary, which would make naming
    non-deterministic and destroy the resume guarantee above.
    """

    stem: str
    suffix: str
    key: str | None = None
    bpm: int | None = None
    #: The title tag, preferred over the stem for the tag and library surfaces.
    title: str | None = None
    #: The album tag. Read only by the dedupe rule.
    album: str | None = None
    lossy: bool = False


@dataclass(frozen=True)
class RenderedName:
    """The three surfaces a name occupies, produced together.

    They are returned as one value because R21 requires the marker to appear in
    all three or in none, and in the source system only two of the three were
    structurally coupled. The library name was coupled by data flow alone: it
    happened to be copied from the title tag, with nothing asserting it. Any
    future intake path that built the library name from the filename stem, or from
    a service response, would have silently dropped the marker from the one
    surface the dashboard counts, and no test would have failed.
    """

    filename: str
    title_tag: str
    library_name: str


# ---------------------------------------------------------------------------
# Shape derivation: one table drives both render and parse
# ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def head_shapes(template: NameTemplate) -> tuple[tuple[str, ...], ...]:
    """Head field combinations this template can emit, longest first.

    Longest first is load-bearing for parsing: a shorter shape is a prefix of a
    longer one, so trying the short one first would match the key of a full head
    and leave the tempo stranded at the front of the title.
    """
    required = [f for f in template.head_fields if f not in template.head_optional]
    shapes: list[tuple[str, ...]] = []
    for size in range(len(template.head_fields), 0, -1):
        for combo in itertools.combinations(template.head_fields, size):
            if all(name in combo for name in required):
                shapes.append(combo)
    return tuple(shapes)


def _marker_pattern(template: NameTemplate) -> str:
    """Markers are optional in a parse and strip WITH the head.

    A stripper that left the marker behind is why a marked lossy copy and its
    lossless twin produced different match keys, so both landed in one playlist as
    duplicates instead of deduping against each other.
    """
    return "".join(rf"(?:{re.escape(r.literal)}\s*)?" for r in template.markers)


@lru_cache(maxsize=None)
def _leading_head_res(template: NameTemplate) -> tuple[re.Pattern[str], ...]:
    """One compiled pattern per emittable shape, longest first.

    The last entry is the MARKER-ONLY head, present whenever the template declares
    a marker at all. It exists because R21 does not stop applying when analysis is
    off: a lossy file still has to be marked, and with no key and no tempo the
    marker is the entire head. Without this pattern that name could be written and
    never stripped, so the marker would leak into every match key downstream.
    """
    sep = rf"\s*{re.escape(template.head_sep.strip() or template.head_sep)}\s*"
    term = rf"\s*{re.escape(template.head_term.strip() or template.head_term)}\s*"
    markers = _marker_pattern(template)
    out = []
    for shape in head_shapes(template):
        body = sep.join(rf"(?P<{n}>{HEAD_FIELDS[n].pattern})" for n in shape)
        out.append(re.compile(rf"^\s*{body}{term}{markers}"))
    if template.markers:
        # The lookahead is what stops this from matching the empty string and so
        # reporting a head on every name in the library.
        first = "|".join(re.escape(r.literal) for r in template.markers)
        out.append(re.compile(rf"^\s*(?={first}){markers}"))
    return tuple(out)


@lru_cache(maxsize=None)
def _trailing_head_res(template: NameTemplate) -> tuple[re.Pattern[str], ...]:
    """The same head written at the END of a name.

    Some catalog and scraper paths carry the key and tempo as a suffix rather than
    a prefix. The source stripped that shape with a private regex sitting one line
    below a call to the canonical parser, accepting off-wheel keys the canonical
    parser rejects. Deriving it from the same template is what stops that copy
    from surviving consolidation.
    """
    sep = rf"\s*{re.escape(template.head_sep.strip() or template.head_sep)}\s*"
    out = []
    for shape in head_shapes(template):
        body = sep.join(rf"(?P<{n}>{HEAD_FIELDS[n].pattern})" for n in shape)
        out.append(re.compile(rf"{sep}{body}\s*$"))
    return tuple(out)


# ---------------------------------------------------------------------------
# The Camelot code: the ONE code parser
# ---------------------------------------------------------------------------

# Case-INSENSITIVE, unlike the head parser above. A code arriving from a detector,
# a user, or a foreign library is normalized; a code already written into a
# filename is held to the convention. Both halves are tested so the asymmetry is a
# recorded choice rather than an accident waiting to be "fixed".
_CAMELOT_RE = re.compile(rf"^0?({_CAMELOT_NUMBER})({_CAMELOT_LETTER})$", re.IGNORECASE)


def is_camelot(code: str) -> bool:
    """True for a valid Camelot code, padded or not."""
    return bool(code) and bool(_CAMELOT_RE.match(code.strip()))


def parse_camelot(code: str) -> tuple[int, str] | None:
    """(1-12, 'A'|'B') or None."""
    m = _CAMELOT_RE.match(code.strip())
    return (int(m.group(1)), m.group(2).upper()) if m else None


def pad_camelot(code: str) -> str:
    """Zero-pad a Camelot code to the two-digit library convention."""
    parsed = parse_camelot(code)
    if parsed is None:
        raise ValueError(f"not a Camelot code: {code!r}")
    number, letter = parsed
    return f"{number:02d}{letter}"


# ---------------------------------------------------------------------------
# The head: parse, strip, split, pad
# ---------------------------------------------------------------------------


def _match_leading(name: str, template: NameTemplate) -> re.Match[str] | None:
    for pattern in _leading_head_res(template):
        m = pattern.match(name)
        if m:
            return m
    return None


def parse_head(name: str, *, template: NameTemplate) -> dict[str, str] | None:
    """Head field values as written, or None when there is no head.

    Values keep their on-disk form: an unpadded key stays unpadded. Normalizing
    here would make the parse lossy, and the repair path needs the head back
    byte-for-byte because the padding stage, not the repair, owns padding.

    A marker-only head carries no field values, so it reports None here even
    though ``strip_head`` removes it. The two questions are genuinely different:
    "what did analysis find" and "what has to come off the front of this name".
    Collapsing them would make an empty result mean both "no head" and "a head
    with nothing in it", and a caller cannot act on that.
    """
    m = _match_leading(name, template)
    if m is None:
        return None
    return {k: v for k, v in m.groupdict().items() if v is not None} or None


def has_head(name: str, *, template: NameTemplate) -> bool:
    """True when ``name`` carries a COMPLETE head, the longest this template emits.

    This is the idempotency and crash-resume marker for any pass that renames: a
    file already carrying a full head has been processed, and re-processing it
    would prepend a second one. It is deliberately stricter than ``strip_head``,
    which removes any declared head shape. A name carrying only the marker, or
    only a key with the tempo detection having failed, is NOT finished, and
    treating it as finished would strand it unprocessed forever.

    The source ran this guard off the looser parser, so it also skipped files
    whose "head" was an off-wheel key that no writer here can emit.
    """
    patterns = _leading_head_res(template)
    return bool(patterns) and patterns[0].match(name) is not None


def split_head(name: str, *, template: NameTemplate) -> tuple[str, str]:
    """(head verbatim including any marker, remainder). No head gives ("", name).

    Verbatim matters: a repair that re-fits a name to the budget must re-emit the
    existing head unchanged, padded or not, because padding belongs to a different
    stage and a repair that quietly padded would race it.
    """
    m = _match_leading(name, template)
    if m is None:
        return "", name
    return name[: m.end()], name[m.end():]


def strip_head(name: str, *, template: NameTemplate) -> str:
    """Remove a leading head, marker included."""
    return split_head(name, template=template)[1]


def strip_trailing_head(name: str, *, template: NameTemplate) -> str:
    """Remove a head written as a suffix."""
    for pattern in _trailing_head_res(template):
        m = pattern.search(name)
        if m:
            return name[: m.start()]
    return name


def strip_heads(name: str, *, template: NameTemplate) -> str:
    """Remove a head at either end, so a name searches like its release title."""
    return strip_trailing_head(strip_head(name, template=template), template=template).strip()


def pad_head(name: str, *, template: NameTemplate) -> str:
    """Zero-pad the key inside a leading head, leaving every other byte alone.

    The two hand-rolled copies of this in the source disagreed with each other and
    with the canonical parser: one silently no-opped on an already-padded key and
    padded a lowercase key while leaving its case alone. Splicing only the key's
    own span is what lets a byte-level rewrite of an export use the same rule as a
    filename rename without a second pattern.
    """
    m = _match_leading(name, template)
    if m is None or "key" not in (m.groupdict() or {}) or m.group("key") is None:
        return name
    written = m.group("key")
    padded = pad_camelot(written)
    if padded == written:
        return name
    start, end = m.span("key")
    return name[:start] + padded + name[end:]


# ---------------------------------------------------------------------------
# Body helpers: sanitize, trim, dedupe
# ---------------------------------------------------------------------------

_DANGLING_RE = re.compile(r"[\s\-(\[]+$")


def sanitize_segment(s: str) -> str:
    """A tag value in the form it takes inside a filename stem.

    Deliberately NOT the same normalizer as the one for playlist names, which
    turns a slash into a spaced dash. Two normalizers exist because the acquisition
    tools strip slashes to a bare dash in filenames while playlist names keep the
    spaced form; collapsing them into one corrupts whichever side loses.
    """
    no_slash = re.sub(r"[\\/]+", "-", s)
    return re.sub(r"\s+", " ", no_slash).strip()


def trim_dangling(s: str) -> str:
    """Strip a trailing fragment a byte cut can leave, so a name never ends mid-phrase."""
    return _DANGLING_RE.sub("", s)


def compose_body(artist: str | None, title: str | None, *, sep: str = " - ") -> str:
    """``Artist - Title`` from tag values, each in its segment form, empties dropped.

    THE ONE COMPOSER. The fallback acquisition path built this join for the stem
    it commits a fetched upload under, and the naming verb built it again for an
    acquired file named for its provider identifier (R-669), with a different
    rule set, so one track could take two stems by the path it arrived through.
    What each caller requires of its inputs, both tags or nothing, a length cap,
    is the caller's; the join is not.
    """
    return sep.join(
        part for part in (sanitize_segment(artist or ""), sanitize_segment(title or "")) if part
    )


def dedupe_stem(
    stem: str,
    title: str | None = None,
    album: str | None = None,
    *,
    sep: str = " - ",
) -> str:
    """Drop a trailing segment that merely repeats the title.

    Two rules, tried in order. The structural rule works with no tags at all,
    which is required because one acquisition path fabricates a stem and writes no
    album tag. The tag-confirmed rule catches titles that themselves contain the
    separator, which structure cannot see.

    AMBIGUITY MEANS IDENTITY. Anything that does not match exactly passes through
    byte-identical. That is what keeps a legitimate ``"Track - Artist - Track
    (Deluxe Edition)"`` from being mutilated, and it is the rule that makes this
    safe to run on every file unconditionally.
    """
    parts = stem.split(sep)
    if len(parts) >= 3:
        lead = parts[0]
        if lead and stem.endswith(sep + lead):
            candidate = stem[: -(len(sep + lead))]
            if sep in candidate:
                return candidate
    if title and album:
        st = sanitize_segment(title)
        sa = sanitize_segment(album)
        if st and st == sa and stem.endswith(sep + sa):
            candidate = stem[: -(len(sep + sa))]
            if candidate and sep in candidate:
                return candidate
    return stem


# ---------------------------------------------------------------------------
# The byte budget
# ---------------------------------------------------------------------------


def _truncate_utf8(s: str, max_bytes: int) -> str:
    """Cut to at most ``max_bytes`` on a codepoint boundary.

    ``errors="ignore"`` is what makes the cut safe: a partial multibyte sequence
    at the boundary is dropped rather than decoded into a lone surrogate that no
    filesystem call will accept.
    """
    raw = s.encode("utf-8")
    if len(raw) <= max_bytes:
        return s
    return raw[:max_bytes].decode("utf-8", errors="ignore")


def fit_stem_to_budget(
    parent_dir: str,
    head: str,
    stem: str,
    suffix: str,
    *,
    budget: NameBudget,
    hash_source: str | None = None,
) -> str:
    """Return ``stem``, shortened if needed so the assembled path fits both ceilings.

    ``head`` must be the BUDGET head, from ``budget_head``, not the head being
    written. ``hash_source`` must be the original pre-dedupe stem: without it, two
    sources that dedupe to the same visible stem also hash to the same value,
    which defeats the disambiguator at exactly the point it is needed.

    Raises ValueError when the directory, head, and suffix alone leave no room.
    Nothing this function can cut would help, so the caller has to report it
    rather than emit a name that will be rejected on import.
    """
    fixed_path = (
        len(parent_dir.encode("utf-8"))
        + 1  # the path separator
        + len(head.encode("utf-8"))
        + len(suffix.encode("utf-8"))
    )
    fixed_name = len(head.encode("utf-8")) + len(suffix.encode("utf-8"))
    max_stem = min(
        budget.path_budget_bytes - fixed_path,
        budget.filename_max_bytes - fixed_name,
    )

    if len(stem.encode("utf-8")) <= max_stem:
        return stem

    digest = hashlib.sha1((hash_source or stem).encode("utf-8")).hexdigest()[: budget.hash_len]
    tail = "~" + digest
    avail = max_stem - len(tail)
    if avail < 1:
        raise ValueError(
            f"path budget unsatisfiable: {parent_dir!r} + {head!r} + {suffix!r} "
            f"leave no room for a stem within {budget.path_budget_bytes} bytes"
        )
    truncated = _truncate_utf8(stem, avail)
    visible = trim_dangling(truncated) or truncated.strip() or "x"
    return visible + tail


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _field_value(name: str, spec: NameSpec) -> object | None:
    return getattr(spec, name)


def _format_field(name: str, spec: NameSpec, key_pad: str) -> str:
    value = _field_value(name, spec)
    if name == "key":
        rendered = str(value)
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:
            # Padding owns normalization for a code arriving as DATA. A value
            # the wheel does not hold falls through unchanged so the refusal
            # below stays the one refusal for every unwritable key.
            rendered = pad_camelot(rendered)
    else:
        rendered = str(value)
    field = HEAD_FIELDS[name]
    if not re.fullmatch(field.pattern, rendered):
        # Refusing here rather than emitting is the point. A head this engine
        # cannot parse back is a head that no consumer will ever strip, and it is
        # written into the filename and the tag at the same moment.
        raise ValueError(
            f"{name}={value!r} renders as {rendered!r}, which this engine cannot "
            f"read back; expected {field.describe}"
        )
    return rendered


def _shape_for(spec: NameSpec, template: NameTemplate) -> tuple[str, ...]:
    """The longest declared shape whose every field is present on ``spec``."""
    for shape in head_shapes(template):
        if all(_field_value(name, spec) is not None for name in shape):
            return shape
    return ()


def _render_markers(spec: NameSpec, template: NameTemplate) -> str:
    declared = {rule.field for rule in template.markers}
    for flag in MARKED_FLAGS:
        if getattr(spec, flag) and flag not in declared:
            # R21: there is no configuration in which a marked condition goes
            # unmarked. A template that permits the condition without declaring
            # its marker is a configuration error, and the file it would produce
            # is indistinguishable on disk from a lossless one.
            raise ValueError(
                f"spec sets {flag}=True but the template declares no marker for it; "
                f"R21 makes marking mandatory whenever the condition is permitted"
            )
    return "".join(
        rule.literal + rule.sep for rule in template.markers if getattr(spec, rule.field)
    )


def _render_head(spec: NameSpec, template: NameTemplate, key_pad: str) -> str:
    shape = _shape_for(spec, template)
    markers = _render_markers(spec, template)
    if not shape:
        # No field survived, so the head TERMINATOR is omitted with them. This is
        # the whole of R20's graceful degradation: with analysis off the name is
        # just the body, not a skeleton of separators around nothing.
        return markers
    parts = [_format_field(name, spec, key_pad) for name in shape]
    return template.head_sep.join(parts) + template.head_term + markers


def budget_head(spec: NameSpec, *, template: NameTemplate) -> str:
    """The WIDEST head this name will ever carry.

    The one call every caller must make instead of assembling a head string. Two
    call sites in the source hand-assembled it independently and disagreed, in a
    repository whose shared naming module exists because exactly that drift caused
    a wave of import rejections.
    """
    return _render_head(spec, template, template.budget_key_pad)


def normalize_spec(spec: NameSpec, *, template: NameTemplate) -> NameSpec:
    """Strip any head already present on the stem and title, keeping what it said.

    Rendering is then idempotent, which fixes a real decoupling window in the
    source: when the tag write succeeds and the rename then fails, the file is
    left with the head in its title and not in its filename. The next run does not
    skip it, because the filename has no head, and the title gets a SECOND head
    prepended. Normalizing the inputs makes the second pass converge instead of
    compounding.

    A STRIPPED HEAD FILLS THE FIELDS THE SPEC LEFT EMPTY (R-740). The head is
    all or nothing by default, and the tempo has no tag field at all, so a spec
    built from tags carries a key and no tempo. Stripping the head and rendering
    from that spec wrote the bare title, and every landed track reached rekordbox
    without the head its own file carried. The title's head is read first and the
    stem's second, a value the spec supplies always wins, and a marker in the
    stripped head marks the spec, so R21 cannot be undone by a caller that forgot
    to pass the flag. The head is text in a name here, never a tempo tag.
    """
    stem_head, stem = split_head(spec.stem, template=template)
    title_head, title = (
        split_head(spec.title, template=template) if spec.title else ("", spec.title)
    )
    if stem == spec.stem and title == spec.title:
        return spec
    filled: dict[str, object] = {}
    for head in (title_head, stem_head):
        for name, value in (parse_head(head, template=template) or {}).items():
            if getattr(spec, name) is None and name not in filled:
                filled[name] = int(value) if HEAD_FIELDS[name] is _BPM_FIELD else value
        for rule in template.markers:
            if rule.literal in head and not getattr(spec, rule.field):
                filled[rule.field] = True
    return replace(spec, stem=stem, title=title, **filled)


def render_all(spec: NameSpec, *, template: NameTemplate) -> RenderedName:
    """The three surfaces, built once from one head.

    The title tag prefers the title over the stem, and the library name is derived
    HERE rather than re-read from the tag later, so the marker cannot go missing
    from one surface without going missing from all three.
    """
    spec = normalize_spec(spec, template=template)
    head = _render_head(spec, template, template.key_pad)
    body_tag = spec.title if spec.title else spec.stem
    title_tag = head + body_tag
    return RenderedName(
        filename=head + spec.stem + spec.suffix,
        title_tag=title_tag,
        library_name=title_tag,
    )


def fit_to_budget(
    spec: NameSpec,
    *,
    template: NameTemplate,
    budget: NameBudget,
    parent_dir: str,
) -> NameSpec:
    """Dedupe the stem, then shorten it so the final path fits.

    ``parent_dir`` is the FINAL directory. The rename happens after the move, so
    the destination is known at name time, which is the only reason a total-path
    budget can be enforced at all rather than guessed at.
    """
    spec = normalize_spec(spec, template=template)
    deduped = dedupe_stem(spec.stem, spec.title, spec.album, sep=template.segment_sep)
    fitted = fit_stem_to_budget(
        parent_dir,
        budget_head(spec, template=template),
        deduped,
        spec.suffix,
        budget=budget,
        hash_source=spec.stem,
    )
    return replace(spec, stem=fitted)


def build(
    spec: NameSpec,
    *,
    template: NameTemplate,
    budget: NameBudget,
    parent_dir: str,
) -> RenderedName:
    """Fit, then render. The one entry point a rename path should call."""
    return render_all(fit_to_budget(spec, template=template, budget=budget,
                                    parent_dir=parent_dir), template=template)


# ---------------------------------------------------------------------------
# The module's single filesystem primitive
# ---------------------------------------------------------------------------


def claim_target(path) -> bool:
    """Atomically reserve a rename target. True when this call created the claim.

    An ``exists()`` check followed by a rename is racy, and POSIX ``rename``
    silently overwrites, so under any concurrency the loser of the race destroys
    the winner's audio. Claiming first degrades that to a reported collision. The
    caller owns unlinking the zero-byte claim on any failure after a True, or the
    stub is left behind as a phantom track.
    """
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL)
    except FileExistsError:
        return False
    os.close(fd)
    return True
