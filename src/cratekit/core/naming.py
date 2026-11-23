"""The one name builder and the one head parser.

One module, because independent copies of the ``{key} - {bpm} - `` head drifted
and caused the 2026-07-04 import rejections. Three rules:

1. The budget is measured with the widest form the name will ever take, the
   padded key, so a later widening cannot push a fitted name over the ceiling.
2. Truncation is deterministic: a shortened stem carries a hash of the
   original, so distinct titles cannot collide and a resumed run re-derives the
   same path, which the resume marker depends on.
3. Absent fields are omitted, never rendered empty (R20); an empty head is junk
   the parser cannot strip.

Configuration arrives as parameters, never imported (S3), so two templates can
be exercised in one process. Pure functions only, except ``claim_target``.
"""

from __future__ import annotations

import hashlib
import itertools
import os
import re
from dataclasses import dataclass, replace
from functools import lru_cache

# Audio formats a renamer will consider, lossy included for fallback
# acquisitions. ``.alac`` is inert (ALAC ships in .m4a) but kept so an adopted
# library is not skipped.
AUDIO_EXTS = (
    ".flac", ".aiff", ".aif", ".wav", ".alac",
    ".mp3", ".m4a", ".aac", ".opus", ".ogg", ".webm",
)


# The head field vocabulary


@dataclass(frozen=True)
class HeadField:
    """One field a name head may carry.

    ``pattern`` and ``anchorable`` make render and parse two views of one
    declaration. Fields are added in code, since each needs a pattern a parser
    reads back and a judgement whether it can lead a head.
    """

    name: str
    pattern: str
    anchorable: bool
    #: Human wording used in refusals, so an invalid template says what is wrong.
    describe: str


# The wheel bound, written once, so 0, 13 and 99 are never keys.
_CAMELOT_NUMBER = r"(?:[1-9]|1[0-2])"
_CAMELOT_LETTER = r"[AB]"

# The Camelot code, padded or unpadded. Case-sensitive inside a head, unlike
# `parse_camelot`, on purpose: a lowercase name on disk was written off
# convention and must not be accepted as a head.
_KEY_FIELD = HeadField(
    name="key",
    pattern=rf"0?{_CAMELOT_NUMBER}{_CAMELOT_LETTER}",
    anchorable=True,
    describe="a Camelot code, 1A..12B, padded or not",
)

# Integer tempo, 1 to 3 digits. Not anchorable: a leading integer cannot be told
# from a title that starts with a number, so a tempo-led head is refused.
_BPM_FIELD = HeadField(
    name="bpm",
    pattern=r"\d{1,3}",
    anchorable=False,
    describe="an integer tempo, 1-3 digits",
)

HEAD_FIELDS: dict[str, HeadField] = {f.name: f for f in (_KEY_FIELD, _BPM_FIELD)}

#: Spec flags a template may mark; R21 makes the marker mandatory when set.
MARKED_FLAGS = ("lossy",)

#: Key padding policies, ordered by width, so a template can check the budget
#: form is never narrower than the written form.
KEY_PADS = ("none", "camelot2")


# The declarations: template, budget, spec


@dataclass(frozen=True)
class MarkerRule:
    """A flag on the spec that becomes a literal inside the head.

    ``literal`` has no default: config owns the marker text (S3).
    """

    field: str
    literal: str
    sep: str = " "


@dataclass(frozen=True)
class NameTemplate:
    """The declared shape of a name.

    Defaults describe structure only; no value config owns appears here.
    """

    head_fields: tuple[str, ...] = ("key", "bpm")
    #: Head fields that may be absent while the head still renders. Empty by
    #: default (all or nothing). Widens render and parse together, via one
    #: shape table, so every written shape can be read back.
    head_optional: frozenset[str] = frozenset()
    head_sep: str = " - "
    head_term: str = " - "
    #: The body segment separator, distinct from ``head_sep`` so changing the
    #: head cannot change dedupe, which parses on this one.
    segment_sep: str = " - "
    markers: tuple[MarkerRule, ...] = ()
    #: How the key is written: padded, the library's two-digit form (U39).
    key_pad: str = "camelot2"
    #: How the key is measured: the widest form it will ever take.
    budget_key_pad: str = "camelot2"

    @classmethod
    def lossy(cls, marker: str) -> NameTemplate:
        """The library's shape: the lossy marker inside the head, in config's text.

        An empty marker is refused by the template's own check.
        """
        return cls(markers=(MarkerRule(field="lossy", literal=marker),))

    @classmethod
    def lossy_if_marked(cls, marker: str | None) -> NameTemplate:
        """:meth:`lossy`, or the plain shape when configuration holds no marker text.

        A template must declare the marker to strip it (R21). With no marker
        text configured no file carries one, so the plain shape is right rather
        than a refusal.
        """
        text = (marker or "").strip()
        return cls.lossy(text) if text else cls()

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

    No defaults: config owns both values (S3). Bytes, not characters, since
    multibyte text passes a character count and still overflows on disk.
    """

    #: Ceiling on the UTF-8 byte length of the whole absolute path.
    path_budget_bytes: int
    #: Per-component cap. Independent of the path ceiling; both are enforced.
    filename_max_bytes: int
    #: Hex characters of the truncation disambiguator; mechanism, so defaulted.
    hash_len: int = 6

    @classmethod
    def of(cls, naming) -> NameBudget:
        """The two ceilings as a configuration's ``naming`` section holds them."""
        return cls(
            path_budget_bytes=naming.path_budget_bytes,
            filename_max_bytes=naming.filename_max_bytes,
        )


@dataclass(frozen=True)
class NameSpec:
    """Everything a name is built from. Analysis results arrive as VALUES.

    ``lossy`` is supplied, never probed: probing runs a binary and would make
    naming non-deterministic.
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

    One value because R21 requires the marker in all three or in none.
    """

    filename: str
    title_tag: str
    library_name: str


# Shape derivation: one table drives both render and parse


@lru_cache(maxsize=None)
def head_shapes(template: NameTemplate) -> tuple[tuple[str, ...], ...]:
    """Head field combinations this template can emit, longest first.

    Longest first, because a shorter shape is a prefix of a longer one and
    would leave the tempo stranded at the front of the title.
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

    Left behind, a marker gives a lossy copy and its lossless twin different
    match keys.
    """
    return "".join(rf"(?:{re.escape(r.literal)}\s*)?" for r in template.markers)


@lru_cache(maxsize=None)
def _leading_head_res(template: NameTemplate) -> tuple[re.Pattern[str], ...]:
    """One compiled pattern per emittable shape, longest first.

    The last entry is the marker-only head, present whenever a marker is
    declared: with analysis off a lossy file is still marked (R21), and that
    name must strip.
    """
    sep = rf"\s*{re.escape(template.head_sep.strip() or template.head_sep)}\s*"
    term = rf"\s*{re.escape(template.head_term.strip() or template.head_term)}\s*"
    markers = _marker_pattern(template)
    out = []
    for shape in head_shapes(template):
        body = sep.join(rf"(?P<{n}>{HEAD_FIELDS[n].pattern})" for n in shape)
        out.append(re.compile(rf"^\s*{body}{term}{markers}"))
    if template.markers:
        # The lookahead stops this matching the empty string on every name.
        first = "|".join(re.escape(r.literal) for r in template.markers)
        out.append(re.compile(rf"^\s*(?={first}){markers}"))
    return tuple(out)


@lru_cache(maxsize=None)
def _trailing_head_res(template: NameTemplate) -> tuple[re.Pattern[str], ...]:
    """The same head written at the END of a name.

    Some catalog and scraper paths carry it as a suffix. Derived from the same
    template so it accepts exactly what the leading parser does.
    """
    sep = rf"\s*{re.escape(template.head_sep.strip() or template.head_sep)}\s*"
    out = []
    for shape in head_shapes(template):
        body = sep.join(rf"(?P<{n}>{HEAD_FIELDS[n].pattern})" for n in shape)
        out.append(re.compile(rf"{sep}{body}\s*$"))
    return tuple(out)


# The Camelot code: the ONE code parser

# Case-insensitive, unlike the head parser: a code arriving as data is
# normalized, one written in a filename is held to convention. Both are tested.
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


# The head: parse, strip, split, pad


def _match_leading(name: str, template: NameTemplate) -> re.Match[str] | None:
    for pattern in _leading_head_res(template):
        m = pattern.match(name)
        if m:
            return m
    return None


def parse_head(name: str, *, template: NameTemplate) -> dict[str, str] | None:
    """Head field values as written, or None when there is no head.

    Values keep their on-disk form, unpadded stays unpadded, so the repair path
    gets the head back byte for byte. A marker-only head reports None, though
    ``strip_head`` removes it: field values and what to strip are different
    questions.
    """
    m = _match_leading(name, template)
    if m is None:
        return None
    return {k: v for k, v in m.groupdict().items() if v is not None} or None


def has_head(name: str, *, template: NameTemplate) -> bool:
    """True when ``name`` carries a COMPLETE head, the longest this template emits.

    The idempotency and resume marker for a renaming pass. Stricter than
    ``strip_head`` on purpose: a name with only a marker, or only a key, is not
    finished and must not be skipped.
    """
    patterns = _leading_head_res(template)
    return bool(patterns) and patterns[0].match(name) is not None


def split_head(name: str, *, template: NameTemplate) -> tuple[str, str]:
    """(head verbatim including any marker, remainder). No head gives ("", name).

    Verbatim, so a repair re-emits the existing head unchanged, padded or not.
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

    Splices only the key's own span, so a byte-level export rewrite and a
    filename rename share one rule.
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


# Body helpers: sanitize, trim, dedupe

_DANGLING_RE = re.compile(r"[\s\-(\[]+$")


def sanitize_segment(s: str) -> str:
    """A tag value in the form it takes inside a filename stem.

    Not the playlist name normalizer: filenames turn a slash into a bare dash,
    playlist names into a spaced one, and merging them corrupts one side.
    """
    no_slash = re.sub(r"[\\/]+", "-", s)
    return re.sub(r"\s+", " ", no_slash).strip()


def trim_dangling(s: str) -> str:
    """Strip a trailing fragment a byte cut can leave, so a name never ends mid-phrase."""
    return _DANGLING_RE.sub("", s)


def compose_body(artist: str | None, title: str | None, *, sep: str = " - ") -> str:
    """``Artist - Title`` from tag values, each in its segment form, empties dropped.

    The one composer, so a track takes one stem whichever path it arrived by
    (R-669). Input requirements, such as both tags or a length cap, are the
    caller's; the join is not.
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

    Two rules in order: a structural one needing no tags, then a tag-confirmed
    one for titles containing the separator. Anything ambiguous passes through
    byte-identical, which makes this safe to run on every file.
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


# The byte budget


def _truncate_utf8(s: str, max_bytes: int) -> str:
    """Cut to at most ``max_bytes`` on a codepoint boundary.

    ``errors="ignore"`` drops a partial multibyte sequence at the boundary.
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

    ``head`` must be the budget head from ``budget_head``. ``hash_source`` must
    be the original pre-dedupe stem, or two stems that dedupe alike hash alike.
    Raises ValueError when directory, head and suffix alone leave no room.
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


# Rendering


def _field_value(name: str, spec: NameSpec) -> object | None:
    return getattr(spec, name)


def _format_field(name: str, spec: NameSpec, key_pad: str) -> str:
    value = _field_value(name, spec)
    if name == "key":
        rendered = str(value)
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:
            # An off-wheel value falls through to the one refusal below.
            rendered = pad_camelot(rendered)
    else:
        rendered = str(value)
    field = HEAD_FIELDS[name]
    if not re.fullmatch(field.pattern, rendered):
        # Refuse a head this engine could not parse back, so never strip.
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
            # R21: a marked condition never goes unmarked.
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
        # No field survived, so the terminator goes too (R20).
        return markers
    parts = [_format_field(name, spec, key_pad) for name in shape]
    return template.head_sep.join(parts) + template.head_term + markers


def stamp_head(name: str, *, key: str, bpm: int, template: NameTemplate) -> str | None:
    """``name`` with a head carrying ``key`` and ``bpm`` set before it, every byte kept (U342).

    For a name that carries no head field, and some text to follow it. The head
    is the one :func:`render_all` renders, the key padded by the template's ``key_pad``, and the whole name
    follows it, so a marker only head (R21) comes after the fields exactly where
    a lossy render places it. Not :func:`build`, which dedupes and shortens the
    stem to a path budget and so would change bytes of the name.

    None, and nothing to write, when ``name`` already carries a head field at
    either end, when nothing but a marker would follow the head, when
    either value cannot be rendered as a head this engine reads, or when the
    result does not read back as a complete head of exactly those values over
    the same body: a head that could not be stripped again is never written.
    """
    # NOTHING TO FOLLOW, A HEAD AT THE END: a marker alone is no title, and a head
    # written as a suffix is a head, so neither is given a second one.
    if (
        parse_head(name, template=template) is not None
        or not strip_head(name, template=template).strip()
        or strip_trailing_head(name, template=template) != name
    ):
        return None
    spec = NameSpec(stem="", suffix="", key=key, bpm=bpm)
    try:
        head = _render_head(spec, template, template.key_pad)
        rendered = {
            field: _format_field(field, spec, template.key_pad)
            for field in head_shapes(template)[0]
        }
    except ValueError:
        return None
    stamped = head + name
    if (
        not has_head(stamped, template=template)
        or parse_head(stamped, template=template) != rendered
        or strip_head(stamped, template=template) != strip_head(name, template=template)
    ):
        return None
    return stamped


def budget_head(spec: NameSpec, *, template: NameTemplate) -> str:
    """The WIDEST head this name will ever carry.

    Every caller uses this rather than assembling a head string.
    """
    return _render_head(spec, template, template.budget_key_pad)


def normalize_spec(spec: NameSpec, *, template: NameTemplate) -> NameSpec:
    """Strip any head already present on the stem and title, keeping what it said.

    Makes rendering idempotent, so a run after a tag write whose rename failed
    does not prepend a second head.

    A stripped head fills the fields the spec left empty (R-740), title's head
    first, then the stem's; a spec built from tags has no tempo. The head is
    text in a name, never a tempo tag. A head is taken whole or not at all: it
    fills only a spec whose every supplied value agrees with it. A marker inside
    a stripped head marks the spec regardless (R21); one in the body marks
    nothing.
    """
    title_head, title_fields, title = (
        _split_fields(spec.title, template) if spec.title else ("", {}, spec.title)
    )
    stem_head, stem_fields, stem = _split_fields(spec.stem, template)
    if stem == spec.stem and title == spec.title:
        return spec
    filled: dict[str, object] = {}
    for head, fields in ((title_head, title_fields), (stem_head, stem_fields)):
        values = {
            name: int(value) if name == _BPM_FIELD.name else value
            for name, value in fields.items()
        }
        current = {name: filled.get(name, getattr(spec, name)) for name in values}
        if all(_agrees(name, current[name], values[name]) for name in values):
            filled.update(
                (name, value) for name, value in values.items() if current[name] is None
            )
        for rule in template.markers:
            if rule.literal in head:
                filled[rule.field] = True
    return replace(spec, stem=stem, title=title, **filled)


def _split_fields(
    name: str, template: NameTemplate
) -> tuple[str, dict[str, str], str]:
    """(head verbatim, its field values, remainder), from one match."""
    m = _match_leading(name, template)
    if m is None:
        return "", {}, name
    fields = {k: v for k, v in m.groupdict().items() if v is not None}
    return name[: m.end()], fields, name[m.end():]


def _agrees(name: str, supplied: object | None, written: object) -> bool:
    """True when a spec value is absent or names the same thing the head does."""
    if supplied is None:
        return True
    if name == _KEY_FIELD.name:
        parsed = parse_camelot(str(supplied))
        return parsed is not None and parsed == parse_camelot(str(written))
    return supplied == written


def render_all(spec: NameSpec, *, template: NameTemplate) -> RenderedName:
    """The three surfaces, built once from one head.

    The title tag prefers the title over the stem. The library name is derived
    here, not re-read from the tag, so the marker is on all three or none.
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

    ``parent_dir`` is the final directory, known because the rename follows the
    move, so the total path budget can be enforced.
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


# The module's single filesystem primitive


def claim_target(path) -> bool:
    """Atomically reserve a rename target. True when this call created the claim.

    POSIX ``rename`` overwrites silently, so claiming first turns a race into a
    reported collision. After True, the caller unlinks the zero-byte claim on
    any failure, or it is left as a phantom track.
    """
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL)
    except FileExistsError:
        return False
    os.close(fd)
    return True
