"""The name template and the ONE head parser.

Eight regexes once read or wrote the ``{key} - {bpm} - `` head; each delta of the deleted
looser parser has a separating input. Three templates render in one process. D1 applies.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

from cratekit.core.naming import (
    AUDIO_EXTS,
    HEAD_FIELDS,
    MarkerRule,
    NameBudget,
    NameSpec,
    NameTemplate,
    budget_head,
    build,
    claim_target,
    fit_to_budget,
    has_head,
    is_camelot,
    normalize_spec,
    pad_camelot,
    pad_head,
    parse_camelot,
    parse_head,
    render_all,
    split_head,
    strip_head,
    strip_heads,
    strip_trailing_head,
)
from tests.test_config import parsed

# The marker text is configuration (S3), never spelled in cratekit/core/naming.py.
MARKER = "[MP3]"

#: The shipped shape: key and tempo, both required, marker declared.
DEFAULT = NameTemplate(markers=(MarkerRule(field="lossy", literal=MARKER),))

#: No marker declared, to prove R21 refuses rather than writing an unmarked lossy file.
UNMARKED = NameTemplate()

#: Tempo optional: render and parse widen together from one declaration.
OPTIONAL_BPM = NameTemplate(
    head_optional=frozenset({"bpm"}),
    markers=(MarkerRule(field="lossy", literal=MARKER),),
)

#: A genuinely different template: separators, marker text and key padding.
CUSTOM = NameTemplate(
    head_sep="_",
    head_term=" :: ",
    segment_sep=" :: ",
    markers=(MarkerRule(field="lossy", literal="(lossy)"),),
    key_pad="camelot2",
    budget_key_pad="camelot2",
)

BUDGET = NameBudget(path_budget_bytes=250, filename_max_bytes=255)
DIR = "/lib/music/processed/2026/session"


# The one code parser.

CODE_CASES = [
    ("8A", (8, "A")),
    ("08A", (8, "A")),
    ("12B", (12, "B")),
    # Case-tolerant on a code read as data; the head parser is not (see below).
    ("12b", (12, "B")),
    (" 04A ", (4, "A")),
    # The bound that the private copies got wrong.
    ("13A", None),
    ("0A", None),
    ("8", None),
    ("A", None),
    ("", None),
]


@pytest.mark.parametrize("code,expected", CODE_CASES, ids=[c[0] or "empty" for c in CODE_CASES])
def test_parse_camelot(code, expected):
    assert parse_camelot(code) == expected


def test_is_camelot_agrees_with_parse_camelot():
    for code, expected in CODE_CASES:
        assert is_camelot(code) is (expected is not None)


def test_pad_camelot_normalizes_and_refuses():
    assert pad_camelot("1A") == "01A"
    assert pad_camelot("12B") == "12B"
    assert pad_camelot("4a") == "04A"
    with pytest.raises(ValueError, match="not a Camelot code"):
        pad_camelot("13A")


# The one head parser.

# (name, expected fields or None, expected remainder after stripping, note)
HEAD_CASES = [
    ("08A - 124 - Cola", {"key": "08A", "bpm": "124"}, "Cola", "the padded convention"),
    ("8A - 124 - Cola", {"key": "8A", "bpm": "124"}, "Cola",
     "unpadded parses; a strict two-digit copy missed every pre-pad file"),
    ("10A - 124 - Cola", {"key": "10A", "bpm": "124"}, "Cola", "keys 10 to 12"),
    ("12B - 87 - Halftime", {"key": "12B", "bpm": "87"}, "Halftime", "two-digit tempo"),
    ("03B - 9 - Ambient Drone", {"key": "03B", "bpm": "9"}, "Ambient Drone",
     "one-digit tempo parses; a two-to-three-digit copy missed it"),
    ("08A - 124 - [MP3] Cola", {"key": "08A", "bpm": "124"}, "Cola",
     "the marker is part of the head and strips with it"),
    ("99A - 124 - Nonsense", None, "99A - 124 - Nonsense", "99 is off the wheel"),
    ("13A - 124 - Off Wheel", None, "13A - 124 - Off Wheel", "13 is off the wheel"),
    ("0A - 124 - Zero", None, "0A - 124 - Zero", "0 is off the wheel"),
    ("08a - 124 - lowercase key", None, "08a - 124 - lowercase key",
     "lowercase is not the convention"),
    ("8b - 124 - lowercase b", None, "8b - 124 - lowercase b", "lowercase, unpadded"),
    ("08A - 124.5 - Decimal", None, "08A - 124.5 - Decimal",
     "a decimal tempo is not the convention"),
    ("Cola", None, "Cola", "a plain title is untouched"),
    ("Artist - Title", None, "Artist - Title", "a dashed title is untouched"),
    ("4AM in Mallorca", None, "4AM in Mallorca",
     "a title that merely starts key-shaped is not a head"),
    ("  08A - 124 - Cola", {"key": "08A", "bpm": "124"}, "Cola", "leading whitespace tolerated"),
]


@pytest.mark.parametrize("name,fields,rest,note", HEAD_CASES, ids=[c[3] for c in HEAD_CASES])
def test_parse_and_strip_head(name, fields, rest, note):
    assert parse_head(name, template=DEFAULT) == fields
    assert strip_head(name, template=DEFAULT) == rest


class TestTheDeletedDuplicate:
    """The claims that justified deleting the looser parser."""

    #: The pattern as the deleted module actually spelled it.
    LOOSE = re.compile(r"^\s*0?\d{1,2}[ABab]\s*-\s*\d{1,3}\s*-\s*")

    @pytest.mark.parametrize(
        "name",
        ["13A - 124 - Off Wheel", "99A - 124 - Nonsense", "0A - 124 - Zero",
         "00A - 124 - Zero", "08a - 124 - lowercase key", "8b - 124 - lowercase b"],
        ids=["off-wheel-13", "off-wheel-99", "off-wheel-0", "off-wheel-00",
             "lowercase-padded", "lowercase-unpadded"],
    )
    def test_it_accepted_off_wheel_and_lowercase_keys(self, name):
        assert self.LOOSE.match(name), "the historical parser accepted this"
        assert parse_head(name, template=DEFAULT) is None

    def test_it_did_not_know_the_marker_was_part_of_the_head(self):
        """So a marked lossy copy and its lossless twin never deduped."""
        name = "08A - 124 - [MP3] Cola"
        assert self.LOOSE.sub("", name, count=1) == f"{MARKER} Cola"
        assert strip_head(name, template=DEFAULT) == "Cola"


def test_the_case_asymmetry_is_a_choice_not_an_accident():
    """A detected code is normalized, a name on disk held to the convention."""
    assert parse_camelot("12b") == (12, "B")
    assert parse_head("12b - 124 - x", template=DEFAULT) is None


class TestSplitAndPadHead:
    """The operations the source open-coded at four separate call sites."""

    @pytest.mark.parametrize(
        "name,expected",
        [("08A - 124 - [MP3] Cola", (f"08A - 124 - {MARKER} ", "Cola")),
         ("Cola", ("", "Cola")),
         ("13A - 124 - x", ("", "13A - 124 - x"))],
        ids=["head-verbatim-with-marker", "headless", "refuses-unwritable-head"],
    )
    def test_split(self, name, expected):
        assert split_head(name, template=DEFAULT) == expected

    def test_pad_splices_only_the_key(self):
        """Only the key's span moves: an export rewrite and a rename share one rule."""
        before = f"8A - 124 - {MARKER} Cola & Friends!"
        after = pad_head(before, template=DEFAULT)
        assert after == f"08A - 124 - {MARKER} Cola & Friends!"
        assert len(after) == len(before) + 1

    @pytest.mark.parametrize(
        "name,template,expected",
        [("08A - 124 - Cola", DEFAULT, "08A - 124 - Cola"),
         # One hand-rolled copy padded a lowercase key, which no parser then read.
         ("13A - 124 - x", DEFAULT, "13A - 124 - x"),
         ("08a - 124 - x", DEFAULT, "08a - 124 - x"),
         ("Cola", DEFAULT, "Cola"),
         ("8A_124 :: Body", CUSTOM, "08A_124 :: Body")],
        ids=["idempotent", "off-wheel-untouched", "lowercase-untouched", "headless-untouched",
             "follows-the-template"],
    )
    def test_pad(self, name, template, expected):
        assert pad_head(name, template=template) == expected


class TestTrailingHead:
    """Some catalog paths carry the head as a SUFFIX (once a ninth private regex)."""

    @pytest.mark.parametrize(
        "name,expected",
        [("Cola - 08A - 124", "Cola"),
         ("Cola - 13A - 124", "Cola - 13A - 124"),
         ("Cola - 08a - 124", "Cola - 08a - 124"),
         ("Cola - Part 2", "Cola - Part 2")],
        ids=["strips", "same-wheel-bound", "same-case-bound", "ending-in-a-number-untouched"],
    )
    def test_strip_trailing_head(self, name, expected):
        assert strip_trailing_head(name, template=DEFAULT) == expected

    def test_both_ends_strip_together(self):
        assert strip_heads("08A - 124 - Cola - 08A - 124", template=DEFAULT) == "Cola"


class TestHasHead:
    """The idempotency and crash-resume marker, stricter than ``strip_head``."""

    @pytest.mark.parametrize(
        "name,expected",
        [("08A - 124 - Cola", True), (f"08A - 124 - {MARKER} Cola", True), ("Cola", False)],
        ids=["complete-head", "marker-does-not-break-it", "headless"],
    )
    def test_has_head(self, name, expected):
        assert has_head(name, template=DEFAULT) is expected

    def test_a_marker_alone_is_not_a_finished_name(self):
        """It strips, but it is not processed and yields no fields."""
        assert not has_head(f"{MARKER} Cola", template=DEFAULT)
        assert strip_head(f"{MARKER} Cola", template=DEFAULT) == "Cola"
        assert parse_head(f"{MARKER} Cola", template=DEFAULT) is None

    def test_a_key_with_no_tempo_is_not_a_finished_name(self):
        assert not has_head("08A - Cola", template=OPTIONAL_BPM)
        assert strip_head("08A - Cola", template=OPTIONAL_BPM) == "Cola"


# Rendering.


def _rendered(out) -> tuple[str, str, str]:
    return (out.filename, out.title_tag, out.library_name)


class TestRender:
    @pytest.mark.parametrize(
        "spec,filename,title_tag",
        [(NameSpec(stem="Make Luv - Room 5", suffix=".flac", key="8A", bpm=124, title="Make Luv"),
          "08A - 124 - Make Luv - Room 5.flac", "08A - 124 - Make Luv"),
         (NameSpec(stem="Aleteo - Maluman", suffix=".mp3", key="8A", bpm=124, title="Aleteo",
                   lossy=True),
          f"08A - 124 - {MARKER} Aleteo - Maluman.mp3", f"08A - 124 - {MARKER} Aleteo"),
         (NameSpec(stem="Some Bootleg", suffix=".opus", key="4B", bpm=90, lossy=True),
          f"04B - 90 - {MARKER} Some Bootleg.opus", f"04B - 90 - {MARKER} Some Bootleg"),
         (NameSpec(stem="Truncated Stem~ab12cd", suffix=".flac", key="8A", bpm=124),
          "08A - 124 - Truncated Stem~ab12cd.flac", "08A - 124 - Truncated Stem~ab12cd")],
        ids=["lossless-carries-no-marker", "lossy-marks-right-after-the-head",
             "stem-is-the-fallback-title", "fitted-stem-passes-verbatim"],
    )
    def test_render(self, spec, filename, title_tag):
        assert _rendered(render_all(spec, template=DEFAULT)) == (filename, title_tag, title_tag)

    def test_the_key_is_written_and_measured_in_the_same_padded_form(self):
        """U39: written and measured heads match; unpadded still measures padded."""
        spec = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124)
        assert render_all(spec, template=DEFAULT).filename.startswith("08A - 124 - ")
        assert budget_head(spec, template=DEFAULT) == "08A - 124 - "
        legacy = NameTemplate(key_pad="none", markers=(MarkerRule(field="lossy", literal=MARKER),))
        assert render_all(spec, template=legacy).filename.startswith("8A - 124 - ")
        assert budget_head(spec, template=legacy) == "08A - 124 - "

    def test_rendering_is_idempotent(self):
        """A tag write before a failed rename once got a SECOND head next run."""
        spec = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124, title="Body")
        once = render_all(spec, template=DEFAULT)
        again = NameSpec(stem=once.filename[: -len(".flac")], suffix=".flac", key="8A", bpm=124,
                         title=once.title_tag)
        twice = render_all(again, template=DEFAULT)
        assert twice.filename == once.filename
        assert twice.title_tag == once.title_tag

    @pytest.mark.parametrize("template", [DEFAULT, NameTemplate()], ids=["default", "bare"])
    def test_an_unwritable_key_is_refused_rather_than_emitted(self, template):
        """A head this engine cannot read back would never be stripped downstream."""
        with pytest.raises(ValueError, match="cannot"):
            render_all(NameSpec(stem="Body", suffix=".flac", key="13A", bpm=124),
                       template=template)


@pytest.mark.parametrize(
    "key,filename",
    [("1A", "01A - 124 - Cola.flac"), ("12A", "12A - 124 - Cola.flac"),
     ("4a", "04A - 124 - Cola.flac"), ("01A", "01A - 124 - Cola.flac")],
    ids=["pads", "already-padded-unchanged", "data-case-normalized", "padded-output-renders-again"],
)
def test_the_default_template_writes_the_padded_form(key, filename):
    """U39: the default absorbed the retired pad sweep; data case is normalized."""
    out = render_all(NameSpec(stem="Cola", suffix=".flac", key=key, bpm=124),
                     template=NameTemplate())
    assert _rendered(out) == (filename, filename[: -len(".flac")], filename[: -len(".flac")])


class TestAnalysisOff:
    """R20's graceful degradation, new construction with no source to port."""

    def test_no_key_and_no_tempo_renders_the_body_alone(self):
        out = render_all(NameSpec(stem="Some Bootleg", suffix=".flac"), template=DEFAULT)
        assert out.filename == "Some Bootleg.flac"
        assert out.title_tag == "Some Bootleg"

    def test_it_round_trips_through_the_parser(self):
        out = render_all(NameSpec(stem="Some Bootleg", suffix=".flac"), template=DEFAULT)
        stem = out.filename[: -len(".flac")]
        assert parse_head(stem, template=DEFAULT) is None
        assert strip_head(stem, template=DEFAULT) == "Some Bootleg"

    def test_absent_fields_are_omitted_not_rendered_empty(self):
        out = render_all(NameSpec(stem="Title", suffix=".flac"), template=DEFAULT)
        assert "None" not in out.filename
        assert not out.filename.startswith(("-", " "))
        assert " - " not in out.filename

    def test_a_lossy_file_is_still_marked_with_analysis_off(self):
        """R21 still applies: the marker IS the head, and still strips back off."""
        out = render_all(NameSpec(stem="Bootleg", suffix=".mp3", lossy=True), template=DEFAULT)
        assert out.filename == f"{MARKER} Bootleg.mp3"
        assert out.title_tag == f"{MARKER} Bootleg"
        assert strip_head(out.filename[: -len(".mp3")], template=DEFAULT) == "Bootleg"

    def test_a_tempo_without_a_key_renders_no_head_at_all(self):
        """A head led by a bare integer cannot be told from a title starting with one."""
        out = render_all(NameSpec(stem="Body", suffix=".flac", bpm=124), template=DEFAULT)
        assert out.filename == "Body.flac"


class TestAStrippedHeadIsKept:
    """R-740: ``normalize_spec`` once threw away the head it stripped."""

    @pytest.mark.parametrize(
        "spec,filename,title_tag",
        [(dict(stem="Body", suffix=".flac", key="1A", title="01A - 112 - Body"),
          "01A - 112 - Body.flac", "01A - 112 - Body"),
         (dict(stem="Body", suffix=".flac", title="8A - 124 - Body"),
          "08A - 124 - Body.flac", "08A - 124 - Body"),
         (dict(stem="05B - 98 - Body", suffix=".flac", title="08A - 124 - Body"),
          "08A - 124 - Body.flac", "08A - 124 - Body"),
         (dict(stem="05B - 98 - Body", suffix=".flac", title="Body"),
          "05B - 98 - Body.flac", "05B - 98 - Body"),
         # Analysis passes a fresh key and tempo; a stale head must not win.
         (dict(stem="Body", suffix=".flac", key="3B", bpm=126, title="08A - 124 - Body"),
          "03B - 126 - Body.flac", "03B - 126 - Body"),
         # A key disagreeing with the head takes nothing from it.
         (dict(stem="Body", suffix=".flac", key="03B", title="08A - 124 - Body"),
          "Body.flac", "Body"),
         (dict(stem="Body", suffix=".flac", key="Am", title="08A - 124 - Body"),
          "Body.flac", "Body"),
         (dict(stem="Body", suffix=".flac", key="8a", title="08A - 124 - Body"),
          "08A - 124 - Body.flac", "08A - 124 - Body"),
         (dict(stem="05B - 98 - Body", suffix=".flac", key="5B", title="08A - 124 - Body"),
          "05B - 98 - Body.flac", "05B - 98 - Body"),
         (dict(stem=f"Body {MARKER}", suffix=".mp3", title="Body"),
          f"Body {MARKER}.mp3", "Body"),
         (dict(stem="Body", suffix=".mp3", title=f"08A - 124 - {MARKER} Body"),
          f"08A - 124 - {MARKER} Body.mp3", f"08A - 124 - {MARKER} Body"),
         (dict(stem="Body", suffix=".mp3", title=f"{MARKER} Body"),
          f"{MARKER} Body.mp3", f"{MARKER} Body")],
        ids=["key-only-spec-keeps-the-whole-head", "no-fields-takes-both-from-the-head",
             "title-head-read-before-stem-head", "stem-head-fills-when-title-has-none",
             "spec-value-wins-over-the-head", "fresh-key-never-paired-with-stale-tempo",
             "off-wheel-key-not-completed", "unpadded-lowercase-key-agrees-with-head",
             "disagreeing-title-head-leaves-stem-head", "marker-in-body-marks-nothing",
             "marker-in-stripped-head-marks-the-spec", "marker-only-head-invents-no-field"],
    )
    def test_the_head_is_kept(self, spec, filename, title_tag):
        out = render_all(NameSpec(**spec), template=DEFAULT)
        assert _rendered(out) == (filename, title_tag, title_tag)

    def test_no_head_anywhere_leaves_the_spec_alone(self):
        spec = NameSpec(stem="Body", suffix=".flac", key="1A", title="Body")
        assert normalize_spec(spec, template=DEFAULT) is spec
        assert render_all(spec, template=DEFAULT).title_tag == "Body"

    def test_a_rendered_head_renders_again_unchanged(self):
        spec = NameSpec(stem="Body", suffix=".flac", key="1A", title="1A - 112 - Body")
        once = render_all(spec, template=DEFAULT)
        again = NameSpec(stem=once.filename[: -len(".flac")], suffix=".flac", title=once.title_tag)
        twice = render_all(again, template=DEFAULT)
        assert twice == once


class TestMarkerCoupling:
    """R21: the marker is on the filename, the tag and the library field, or none."""

    @pytest.mark.parametrize("lossy", [True, False])
    @pytest.mark.parametrize("key,bpm", [("8A", 124), (None, None), ("8A", None)])
    @pytest.mark.parametrize("title", ["Title", None])
    def test_all_three_surfaces_or_none(self, lossy, key, bpm, title):
        spec = NameSpec(stem="Body", suffix=".flac", key=key, bpm=bpm, title=title, lossy=lossy)
        out = render_all(spec, template=DEFAULT)
        present = [MARKER in out.filename, MARKER in out.title_tag, MARKER in out.library_name]
        assert all(present) if lossy else not any(present)

    def test_a_template_with_no_marker_refuses_a_lossy_file(self):
        """An unmarked lossy file is indistinguishable from a lossless one on disk."""
        with pytest.raises(ValueError, match="R21"):
            render_all(NameSpec(stem="Body", suffix=".mp3", lossy=True), template=UNMARKED)

    def test_a_lossless_file_renders_fine_under_the_same_template(self):
        out = render_all(NameSpec(stem="Body", suffix=".flac"), template=UNMARKED)
        assert out.filename == "Body.flac"

    def test_the_marker_text_is_a_parameter(self):
        out = render_all(NameSpec(stem="Body", suffix=".mp3", key="8A", bpm=124, lossy=True),
                         template=CUSTOM)
        assert out.filename == "08A_124 :: (lossy) Body.mp3"
        assert MARKER not in out.filename


# The round-trip property, over every combination of present and absent fields.

FIELD_COMBINATIONS = [
    (key, bpm, title, lossy)
    for key in ("8A", None)
    for bpm in (124, None)
    for title in ("Title Tag", None)
    for lossy in (True, False)
]
TEMPLATES = pytest.mark.parametrize(
    "template", [DEFAULT, OPTIONAL_BPM, CUSTOM], ids=["default", "optional-bpm", "custom"]
)


@TEMPLATES
@pytest.mark.parametrize("key,bpm,title,lossy", FIELD_COMBINATIONS)
def test_every_rendered_name_strips_back_to_its_body(template, key, bpm, title, lossy):
    """R20 in full: a shape that can be written but not read glues a head to a title."""
    spec = NameSpec(stem="Body Text", suffix=".flac", key=key, bpm=bpm, title=title, lossy=lossy)
    out = render_all(spec, template=template)
    stem = out.filename[: -len(".flac")]
    assert strip_head(stem, template=template) == "Body Text"
    assert strip_head(out.title_tag, template=template) == (title or "Body Text")
    assert "None" not in out.filename


@TEMPLATES
def test_a_full_head_round_trips_its_field_values(template):
    spec = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124)
    out = render_all(spec, template=template)
    parsed = parse_head(out.filename[: -len(".flac")], template=template)
    assert parsed is not None
    assert parse_camelot(parsed["key"]) == (8, "A")
    assert int(parsed["bpm"]) == 124


def test_a_second_template_produces_a_different_correct_tree_with_no_code_change():
    """Two shapes, one process, one engine."""
    spec = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124)
    assert render_all(spec, template=DEFAULT).filename == "08A - 124 - Body.flac"
    assert render_all(spec, template=CUSTOM).filename == "08A_124 :: Body.flac"


def test_an_optional_field_widens_render_and_parse_together():
    spec = NameSpec(stem="Body", suffix=".flac", key="8A")
    assert render_all(spec, template=OPTIONAL_BPM).filename == "08A - Body.flac"
    assert parse_head("8A - Body", template=OPTIONAL_BPM) == {"key": "8A"}
    # Under the default template it is no head, so the body stays whole.
    assert render_all(spec, template=DEFAULT).filename == "Body.flac"
    assert strip_head("8A - Body", template=DEFAULT) == "8A - Body"


# Template validation.


@pytest.mark.parametrize(
    "kwargs,match",
    [
        # A bare integer at the front cannot be told from a title starting with one.
        (dict(head_fields=("bpm",)), "may not begin"),
        # The 2026-07-04 failure, made unconstructable.
        (dict(key_pad="camelot2", budget_key_pad="none"), "narrower"),
        (dict(head_fields=("key", "energy")), "unknown head field"),
        (dict(head_optional=frozenset({"energy"})), "head_optional"),
        (dict(markers=(MarkerRule(field="loud", literal="x"),)), "markable flag"),
    ],
    ids=["unanchored-first-field", "measuring-narrower-than-writing", "unknown-field",
         "undeclared-optional-field", "marker-on-unmarkable-flag"],
)
def test_an_invalid_template_is_refused(kwargs, match):
    with pytest.raises(ValueError, match=match):
        NameTemplate(**kwargs)


def test_every_declared_field_is_anchorable_or_not_on_purpose():
    assert HEAD_FIELDS["key"].anchorable
    assert not HEAD_FIELDS["bpm"].anchorable


# Budget interaction.


class TestBudgetInteraction:
    def test_the_budget_head_equals_the_written_head_since_the_pad_moved_in(self):
        spec = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124)
        written = render_all(spec, template=DEFAULT).filename[: -len("Body.flac")]
        assert budget_head(spec, template=DEFAULT) == written

    def test_the_marker_is_paid_for_in_the_budget_head(self):
        lossy = NameSpec(stem="Body", suffix=".mp3", key="8A", bpm=124, lossy=True)
        clean = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124)
        assert budget_head(lossy, template=DEFAULT) == f"08A - 124 - {MARKER} "
        assert len(budget_head(lossy, template=DEFAULT)) > len(budget_head(clean, template=DEFAULT))

    def test_an_absent_field_contributes_zero_bytes_including_its_separator(self):
        """An analysis-off library gets the whole budget for its body."""
        fit = {"template": DEFAULT, "budget": BUDGET, "parent_dir": DIR}
        analyzed = fit_to_budget(NameSpec(stem="T" * 300, suffix=".flac", key="8A", bpm=124), **fit)
        bare = fit_to_budget(NameSpec(stem="T" * 300, suffix=".flac"), **fit)
        assert budget_head(NameSpec(stem="", suffix=""), template=DEFAULT) == ""
        assert len(bare.stem) > len(analyzed.stem)

    def test_build_fits_and_its_result_is_already_in_the_padded_form(self):
        """The retired pad stage has nothing left to add to a name this writes."""
        spec = NameSpec(stem="U" * 300, suffix=".flac", key="8A", bpm=124)
        out = build(spec, template=DEFAULT, budget=BUDGET, parent_dir=DIR)
        assert len(f"{DIR}/{out.filename}".encode()) <= BUDGET.path_budget_bytes
        assert pad_head(out.filename, template=DEFAULT) == out.filename

    def test_the_same_input_twice_yields_the_same_path(self):
        spec = NameSpec(stem="V" * 300, suffix=".flac", key="8A", bpm=124)
        first = build(spec, template=DEFAULT, budget=BUDGET, parent_dir=DIR)
        assert build(spec, template=DEFAULT, budget=BUDGET, parent_dir=DIR) == first

    def test_dedupe_runs_before_the_fit_and_the_hash_uses_the_original(self):
        spec = NameSpec(stem="Weightless - Marconi Union - Weightless", suffix=".flac", key="8A",
                        bpm=124, title="Weightless", album="Weightless")
        fitted = fit_to_budget(spec, template=DEFAULT, budget=BUDGET, parent_dir=DIR)
        assert fitted.stem == "Weightless - Marconi Union"


# Shape coverage against the live library.

# Measured on 10,070 exported rows: 9,897 readable heads, 169 none, 3 digits, 1 key-only.
SHAPE_CORPUS = [
    ("08A - 124 - Plain Body", True, "Plain Body", "padded head, space in the body"),
    ("8A - 124 - Plain Body", True, "Plain Body", "unpadded head, pre-pad stage"),
    ("03B - 9 - Slow Drone", True, "Slow Drone", "one-digit tempo"),
    ("12B - 87 - Body & Friend", True, "Body & Friend", "ampersand"),
    ("08A - 124 - Body!", True, "Body!", "literal exclamation mark"),
    ("08A - 124 - Café Body", True, "Café Body", "decomposed accent"),
    ("08A - 124 - Café Body", True, "Café Body", "composed accent"),
    ("08A - 124 - Body [Remix]", True, "Body [Remix]", "square brackets in the body"),
    ("08A - 124 - Long Body~ab12cd", True, "Long Body~ab12cd", "truncation disambiguator"),
    (f"08A - 124 - {MARKER} Body", True, "Body", "marked lossy, head position"),
    ("Plain Body", False, "Plain Body", "no head at all, never analyzed"),
    ("1998", False, "1998", "a title that is only digits"),
    ("6AM", False, "6AM", "a title that starts key-shaped"),
    ("1/1 (Remastered 2004)", False, "1/1 (Remastered 2004)", "a title starting with a digit"),
    ("08A - Body", False, "08A - Body", "a key with no tempo, under the shipped template"),
]


@pytest.mark.parametrize("name,parses,rest,note", SHAPE_CORPUS, ids=[c[3] for c in SHAPE_CORPUS])
def test_every_shape_class_in_the_live_library(name, parses, rest, note):
    assert (parse_head(name, template=DEFAULT) is not None) is parses
    assert strip_head(name, template=DEFAULT) == rest


def test_a_composition_form_difference_does_not_change_the_head():
    """Composition form cost 144 still-referenced files in July 2026."""
    decomposed = "08A - 124 - Café"
    composed = "08A - 124 - Café"
    assert decomposed != composed
    assert parse_head(decomposed, template=DEFAULT) == parse_head(composed, template=DEFAULT)


# Conformance: exactly one Camelot parser in the package.

SRC_ROOT = Path(__file__).resolve().parent.parent / "src"

#: A class of exactly the two Camelot letters, so a pattern built from pieces is caught too.
_LETTER_CLASS = re.compile(r"\[\s*[AaBb]{2,4}\s*\]|\[Aa\]\[Bb\]")


def _camelot_regex_literals(source: str) -> list[str]:
    """Every Camelot-shaped pattern literal, ``bytes`` included."""
    found: list[str] = []
    for node in ast.walk(parsed(source)):
        if not isinstance(node, ast.Constant):
            continue
        if isinstance(node.value, str):
            text = node.value
        elif isinstance(node.value, bytes):
            text = node.value.decode("latin-1")
        else:
            continue
        if _LETTER_CLASS.search(text):
            found.append(text)
    return found


def test_the_detector_recognizes_the_historical_spellings():
    """The guard bites on the eight patterns once live in the source, verbatim."""
    historical = [
        r"^0?([1-9]|1[0-2])([AB])$",                                  # the code parser
        r"^\s*(?P<key>0?(?:[1-9]|1[0-2])[AB])\s*-\s*(?P<bpm>\d{1,3})\s*-\s*",  # the head parser
        r"^\s*0?\d{1,2}[ABab]\s*-\s*\d{1,3}\s*-\s*",                  # the deleted duplicate
        r"^([1-9])([AB])(?=\b)",                                      # a folder pad matcher
        r"^([1-9])([AB]) - ",                                         # a title pad matcher
        r"^\s*(\d{1,2}[ABab])\s*-\s*(\d+(?:\.\d+)?)\s*-\s*(.*)$",     # a set-builder prefix
        r"^(\d)([ABab] )",                                            # a hand-rolled budget pad
        r"\s*-\s*\d+[AB]\s*-\s*\d+$",                                 # a trailing suffix stripper
    ]
    for pattern in historical:
        assert _camelot_regex_literals(f"P = {pattern!r}\n"), pattern
    # The byte-level spelling, which a str-only checker would call clean.
    assert _camelot_regex_literals("P = rb'^[1-9][AB] - '\n")


def test_no_module_carries_a_private_camelot_parser():
    """Eight spellings became one; this stops a ninth arriving quietly."""
    offenders = {}
    for path in sorted(SRC_ROOT.rglob("*.py")):
        module = ".".join(path.relative_to(SRC_ROOT).with_suffix("").parts)
        if module == "cratekit.core.naming":
            continue
        found = _camelot_regex_literals(path.read_text())
        if found:
            offenders[module] = found
    assert not offenders, (
        f"private Camelot parsers found: {offenders}. There is one parser, in "
        f"cratekit.core.naming, and every consumer takes its result. Eight copies "
        f"disagreeing at the edges is how the import rejections happened."
    )


def test_the_accepted_extension_set_is_one_tuple():
    """One home, lowercase, dot-prefixed, no duplicates (the source had five)."""
    assert len(set(AUDIO_EXTS)) == len(AUDIO_EXTS)
    assert all(e.startswith(".") and e == e.lower() for e in AUDIO_EXTS)
    assert {".flac", ".aiff", ".aif", ".mp3", ".wav"} <= set(AUDIO_EXTS)


# The one filesystem primitive.


class TestClaimTarget:
    def test_a_free_target_is_claimed_once(self, tmp_path):
        target = tmp_path / "08A - 124 - Body.flac"
        assert claim_target(target) is True
        assert target.exists() and target.stat().st_size == 0

    def test_a_taken_target_is_refused_rather_than_overwritten(self, tmp_path):
        """POSIX rename overwrites in silence; claiming first makes it a collision."""
        target = tmp_path / "08A - 124 - Body.flac"
        target.write_bytes(b"audio")
        assert claim_target(target) is False
        assert target.read_bytes() == b"audio"
