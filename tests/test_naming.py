"""The name template and the ONE head parser.

Two things are being proved here, and they are different claims.

**Consolidation.** The source system had eight independent regexes reading or
writing the ``{key} - {bpm} - `` head. The looser of the two real parsers accepted
off-wheel keys, accepted lowercase, and did not know the lossy marker was part of
the head. Every one of those three deltas has a test below with the concrete input
that separates the two, so deleting that parser is a recorded behaviour change
rather than a silent one.

**Parameterization.** Three templates are exercised in one process. That is the
whole evidence that the engine is template-driven: an engine reading its shape
from global configuration cannot render two different name shapes in one run, and
a "template" that only ever takes one value has never been proved to take another.

No real library string appears here (seam decision D1). The shape corpus at the
bottom is synthesized to cover the character classes and name shapes measured in a
live export of 10,070 collection rows on 2026-08-01, and the measured counts are
recorded beside it so the corpus can be checked against a fresh export later.
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

# The marker text is CONFIGURATION (seam decision S3). It is supplied here as
# data, exactly as the config layer will supply it, and it appears nowhere in
# cratekit/core/naming.py.
MARKER = "[MP3]"

#: The shipped shape: key and tempo, both required, marker declared.
DEFAULT = NameTemplate(markers=(MarkerRule(field="lossy", literal=MARKER),))

#: The same shape with no marker declared. Used to prove R21 refuses rather than
#: quietly writing an unmarked lossy file.
UNMARKED = NameTemplate()

#: Tempo optional, so a key-only head is BOTH emittable and parseable. Widening
#: render without widening parse is how a head gets permanently glued to a title,
#: so the two are derived from one declaration and this template proves it.
OPTIONAL_BPM = NameTemplate(
    head_optional=frozenset({"bpm"}),
    markers=(MarkerRule(field="lossy", literal=MARKER),),
)

#: A genuinely different template: different separators, a different marker text,
#: and the key written padded rather than padded later.
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


# ═══════════════════════════════════════════════════════════════════════════
# The one code parser
# ═══════════════════════════════════════════════════════════════════════════

CODE_CASES = [
    ("8A", (8, "A")),
    ("08A", (8, "A")),
    ("12B", (12, "B")),
    # Case-tolerant on a code READ from a detector or a user. The head parser is
    # deliberately NOT tolerant; see the asymmetry test below.
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


# ═══════════════════════════════════════════════════════════════════════════
# The one head parser
# ═══════════════════════════════════════════════════════════════════════════

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
    """The three claims that justified deleting the looser parser, each with the
    input that separates it from the canonical one. All three were verified
    against the source before the port.

    A live export of 10,070 rows contains ZERO names that only the looser parser
    would have matched, so deleting it removes no real behaviour: no lowercase
    key, no off-wheel key, and no decimal tempo exists in the library.
    """

    #: The pattern as the deleted module actually spelled it.
    LOOSE = re.compile(r"^\s*0?\d{1,2}[ABab]\s*-\s*\d{1,3}\s*-\s*")

    @pytest.mark.parametrize("name", ["13A - 124 - Off Wheel", "99A - 124 - Nonsense",
                                      "0A - 124 - Zero", "00A - 124 - Zero"])
    def test_it_accepted_keys_that_are_not_on_the_wheel(self, name):
        assert self.LOOSE.match(name), "the historical parser accepted this"
        assert parse_head(name, template=DEFAULT) is None

    @pytest.mark.parametrize("name", ["08a - 124 - lowercase key", "8b - 124 - lowercase b"])
    def test_it_accepted_lowercase_variants(self, name):
        assert self.LOOSE.match(name), "the historical parser accepted this"
        assert parse_head(name, template=DEFAULT) is None

    def test_it_did_not_know_the_marker_was_part_of_the_head(self):
        """The consequence was concrete: a stripper built on it left the marker
        behind, so a marked lossy copy and its lossless twin produced different
        match keys and both landed in one playlist as duplicates instead of
        deduping against each other."""
        name = "08A - 124 - [MP3] Cola"
        loose_stripped = self.LOOSE.sub("", name, count=1)
        assert loose_stripped == f"{MARKER} Cola"
        assert strip_head(name, template=DEFAULT) == "Cola"


def test_the_case_asymmetry_is_a_choice_not_an_accident():
    """A code read from a detector is normalized; a name already on disk is held
    to the convention. Both halves asserted so nobody "fixes" one into the other."""
    assert parse_camelot("12b") == (12, "B")
    assert parse_head("12b - 124 - x", template=DEFAULT) is None


class TestSplitAndPadHead:
    """The operations the source open-coded at four separate call sites."""

    def test_split_returns_the_head_verbatim_including_the_marker(self):
        assert split_head("08A - 124 - [MP3] Cola", template=DEFAULT) == (
            f"08A - 124 - {MARKER} ",
            "Cola",
        )

    def test_split_on_a_headless_name(self):
        assert split_head("Cola", template=DEFAULT) == ("", "Cola")

    def test_split_refuses_a_head_the_engine_could_not_have_written(self):
        assert split_head("13A - 124 - x", template=DEFAULT) == ("", "13A - 124 - x")

    def test_pad_splices_only_the_key(self):
        """Only the key's own span moves, so a byte-level rewrite of an export and
        a filename rename can use one rule. The hand-rolled copies each rebuilt
        the head, and disagreed about what happened to the rest of it."""
        before = f"8A - 124 - {MARKER} Cola & Friends!"
        after = pad_head(before, template=DEFAULT)
        assert after == f"08A - 124 - {MARKER} Cola & Friends!"
        assert len(after) == len(before) + 1

    def test_pad_is_idempotent(self):
        assert pad_head("08A - 124 - Cola", template=DEFAULT) == "08A - 124 - Cola"

    @pytest.mark.parametrize("name", ["13A - 124 - x", "08a - 124 - x", "Cola"])
    def test_pad_leaves_alone_what_is_not_a_head(self, name):
        """One hand-rolled copy padded a lowercase key and left its case alone,
        producing a key that neither parser then accepted."""
        assert pad_head(name, template=DEFAULT) == name

    def test_pad_follows_the_template(self):
        assert pad_head("8A_124 :: Body", template=CUSTOM) == "08A_124 :: Body"


class TestTrailingHead:
    """Some catalog paths carry the key and tempo as a SUFFIX. The source stripped
    that with a private regex sitting one line below a call to the canonical
    parser, so it survived the previous consolidation as a ninth spelling."""

    def test_a_trailing_head_strips(self):
        assert strip_trailing_head("Cola - 08A - 124", template=DEFAULT) == "Cola"

    def test_both_ends_strip_together(self):
        assert strip_heads("08A - 124 - Cola - 08A - 124", template=DEFAULT) == "Cola"

    @pytest.mark.parametrize("name", ["Cola - 13A - 124", "Cola - 08a - 124"])
    def test_the_trailing_form_holds_the_same_bound_as_the_leading_form(self, name):
        assert strip_trailing_head(name, template=DEFAULT) == name

    def test_a_name_that_merely_ends_in_a_number_is_untouched(self):
        assert strip_trailing_head("Cola - Part 2", template=DEFAULT) == "Cola - Part 2"


class TestHasHead:
    """The idempotency and crash-resume marker. Deliberately stricter than
    ``strip_head``: a partially named file is not a finished one."""

    def test_a_complete_head_is_recognized(self):
        assert has_head("08A - 124 - Cola", template=DEFAULT)

    def test_the_marker_does_not_break_the_guard(self):
        assert has_head(f"08A - 124 - {MARKER} Cola", template=DEFAULT)

    def test_a_marker_alone_is_not_a_finished_name(self):
        """It still STRIPS, so the marker never leaks into a match key, but it does
        not count as processed and it yields no field values: this file has no key
        and no tempo yet. Three separate answers to three separate questions."""
        assert not has_head(f"{MARKER} Cola", template=DEFAULT)
        assert strip_head(f"{MARKER} Cola", template=DEFAULT) == "Cola"
        assert parse_head(f"{MARKER} Cola", template=DEFAULT) is None

    def test_a_key_with_no_tempo_is_not_a_finished_name(self):
        assert not has_head("08A - Cola", template=OPTIONAL_BPM)
        assert strip_head("08A - Cola", template=OPTIONAL_BPM) == "Cola"

    def test_a_headless_name_is_not_recognized(self):
        assert not has_head("Cola", template=DEFAULT)


# ═══════════════════════════════════════════════════════════════════════════
# Rendering
# ═══════════════════════════════════════════════════════════════════════════


class TestRender:
    def test_lossless_carries_no_marker(self):
        out = render_all(
            NameSpec(stem="Make Luv - Room 5", suffix=".flac", key="8A", bpm=124,
                     title="Make Luv"),
            template=DEFAULT,
        )
        assert out.filename == "8A - 124 - Make Luv - Room 5.flac"
        assert out.title_tag == "8A - 124 - Make Luv"
        assert out.library_name == out.title_tag
        assert MARKER not in out.filename

    def test_lossy_marks_right_after_the_head(self):
        out = render_all(
            NameSpec(stem="Aleteo - Maluman", suffix=".mp3", key="8A", bpm=124,
                     title="Aleteo", lossy=True),
            template=DEFAULT,
        )
        assert out.filename == f"8A - 124 - {MARKER} Aleteo - Maluman.mp3"
        assert out.title_tag == f"8A - 124 - {MARKER} Aleteo"

    def test_the_stem_is_the_fallback_when_there_is_no_title_tag(self):
        out = render_all(
            NameSpec(stem="Some Bootleg", suffix=".opus", key="4B", bpm=90, lossy=True),
            template=DEFAULT,
        )
        assert out.title_tag == f"4B - 90 - {MARKER} Some Bootleg"
        assert out.filename == f"4B - 90 - {MARKER} Some Bootleg.opus"

    def test_an_already_fitted_stem_passes_through_verbatim(self):
        out = render_all(
            NameSpec(stem="Truncated Stem~ab12cd", suffix=".flac", key="8A", bpm=124),
            template=DEFAULT,
        )
        assert out.filename == "8A - 124 - Truncated Stem~ab12cd.flac"

    def test_the_key_is_written_unpadded_and_measured_padded(self):
        spec = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124)
        assert render_all(spec, template=DEFAULT).filename.startswith("8A - 124 - ")
        assert budget_head(spec, template=DEFAULT) == "08A - 124 - "

    def test_rendering_is_idempotent(self):
        """The source had a real decoupling window: when the tag write succeeded
        and the rename then failed, the next run prepended a SECOND head to the
        title, because the builder prepended unconditionally with no head check.
        Normalizing the inputs makes the second pass converge instead."""
        spec = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124, title="Body")
        once = render_all(spec, template=DEFAULT)
        twice = render_all(
            NameSpec(stem=once.filename[: -len(".flac")], suffix=".flac", key="8A", bpm=124,
                     title=once.title_tag),
            template=DEFAULT,
        )
        assert twice.filename == once.filename
        assert twice.title_tag == once.title_tag

    def test_an_unwritable_key_is_refused_rather_than_emitted(self):
        """A head this engine cannot read back would never be stripped by anything
        downstream, and it goes into the filename and the tag at the same moment."""
        with pytest.raises(ValueError, match="cannot"):
            render_all(NameSpec(stem="Body", suffix=".flac", key="13A", bpm=124),
                       template=DEFAULT)


class TestAnalysisOff:
    """R20's graceful degradation. There is no source implementation to port: the
    source terminates a file whose key or tempo detection failed, so no code path
    ever rendered a name without them. This is new construction."""

    def test_no_key_and_no_tempo_renders_the_body_alone(self):
        out = render_all(NameSpec(stem="Some Bootleg", suffix=".flac"), template=DEFAULT)
        assert out.filename == "Some Bootleg.flac"
        assert out.title_tag == "Some Bootleg"

    def test_absent_fields_are_omitted_not_rendered_empty(self):
        """The failure this prevents: ``"None - None - Title"`` or ``" -  - Title"``
        baked into the filename AND the tag, recognized by no parser, so nothing
        ever removes it and every downstream matcher sees it as part of the title."""
        out = render_all(NameSpec(stem="Title", suffix=".flac"), template=DEFAULT)
        assert "None" not in out.filename
        assert not out.filename.startswith(("-", " "))
        assert " - " not in out.filename

    def test_it_round_trips_through_the_parser(self):
        out = render_all(NameSpec(stem="Some Bootleg", suffix=".flac"), template=DEFAULT)
        stem = out.filename[: -len(".flac")]
        assert parse_head(stem, template=DEFAULT) is None
        assert strip_head(stem, template=DEFAULT) == "Some Bootleg"

    def test_a_lossy_file_is_still_marked_with_analysis_off(self):
        """R21 does not stop applying when analysis is off. With no key and no
        tempo the marker IS the head, and it still has to strip back off."""
        out = render_all(NameSpec(stem="Bootleg", suffix=".mp3", lossy=True), template=DEFAULT)
        assert out.filename == f"{MARKER} Bootleg.mp3"
        assert out.title_tag == f"{MARKER} Bootleg"
        assert strip_head(out.filename[: -len(".mp3")], template=DEFAULT) == "Bootleg"

    def test_a_tempo_without_a_key_renders_no_head_at_all(self):
        """A head led by a bare integer cannot be told apart from a title that
        starts with a number, and the live library holds three of those. Rather
        than emit a name nothing can parse, the head is omitted entirely."""
        out = render_all(NameSpec(stem="Body", suffix=".flac", bpm=124), template=DEFAULT)
        assert out.filename == "Body.flac"


class TestMarkerCoupling:
    """R21: the marker is in the filename, the tag, and the library field, or in
    none of them. In the source only the first two were structurally coupled; the
    library field was coupled by data flow alone, with nothing asserting it, so any
    future intake path that built the library name from somewhere else would have
    dropped it from the one surface the dashboard counts."""

    @pytest.mark.parametrize("lossy", [True, False])
    @pytest.mark.parametrize("key,bpm", [("8A", 124), (None, None), ("8A", None)])
    @pytest.mark.parametrize("title", ["Title", None])
    def test_all_three_surfaces_or_none(self, lossy, key, bpm, title):
        out = render_all(
            NameSpec(stem="Body", suffix=".flac", key=key, bpm=bpm, title=title, lossy=lossy),
            template=DEFAULT,
        )
        present = [MARKER in out.filename, MARKER in out.title_tag, MARKER in out.library_name]
        assert all(present) if lossy else not any(present)

    def test_a_template_with_no_marker_refuses_a_lossy_file(self):
        """There is no configuration in which a lossy file goes unmarked. On disk
        an unmarked lossy file is indistinguishable from a lossless one."""
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


# ═══════════════════════════════════════════════════════════════════════════
# The round-trip property, over every combination of present and absent fields
# ═══════════════════════════════════════════════════════════════════════════

FIELD_COMBINATIONS = [
    (key, bpm, title, lossy)
    for key in ("8A", None)
    for bpm in (124, None)
    for title in ("Title Tag", None)
    for lossy in (True, False)
]


@pytest.mark.parametrize("template", [DEFAULT, OPTIONAL_BPM, CUSTOM],
                         ids=["default", "optional-bpm", "custom"])
@pytest.mark.parametrize("key,bpm,title,lossy", FIELD_COMBINATIONS)
def test_every_rendered_name_strips_back_to_its_body(template, key, bpm, title, lossy):
    """One property covering R20 in full, and stronger than any example.

    Whatever fields are present, the rendered name must strip back to exactly the
    body it was built from. A shape that can be written but not read is how a head
    ends up permanently glued to a title, which no downstream matcher can undo.
    """
    spec = NameSpec(stem="Body Text", suffix=".flac", key=key, bpm=bpm, title=title, lossy=lossy)
    out = render_all(spec, template=template)
    stem = out.filename[: -len(".flac")]
    assert strip_head(stem, template=template) == "Body Text"
    assert strip_head(out.title_tag, template=template) == (title or "Body Text")
    assert "None" not in out.filename


@pytest.mark.parametrize("template", [DEFAULT, OPTIONAL_BPM, CUSTOM],
                         ids=["default", "optional-bpm", "custom"])
def test_a_full_head_round_trips_its_field_values(template):
    spec = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124)
    out = render_all(spec, template=template)
    parsed = parse_head(out.filename[: -len(".flac")], template=template)
    assert parsed is not None
    assert parse_camelot(parsed["key"]) == (8, "A")
    assert int(parsed["bpm"]) == 124


def test_a_second_template_produces_a_different_correct_tree_with_no_code_change():
    """Two shapes, one process, one engine. An engine that read its template from
    global configuration could not produce both of these in one run."""
    spec = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124)
    assert render_all(spec, template=DEFAULT).filename == "8A - 124 - Body.flac"
    assert render_all(spec, template=CUSTOM).filename == "08A_124 :: Body.flac"


def test_an_optional_field_widens_render_and_parse_together():
    spec = NameSpec(stem="Body", suffix=".flac", key="8A")
    assert render_all(spec, template=OPTIONAL_BPM).filename == "8A - Body.flac"
    assert parse_head("8A - Body", template=OPTIONAL_BPM) == {"key": "8A"}
    # The same name under the default template is not a head at all, so the body
    # is left whole rather than half-eaten.
    assert render_all(spec, template=DEFAULT).filename == "Body.flac"
    assert strip_head("8A - Body", template=DEFAULT) == "8A - Body"


# ═══════════════════════════════════════════════════════════════════════════
# Template validation
# ═══════════════════════════════════════════════════════════════════════════


class TestTemplateValidation:
    def test_a_head_may_not_begin_with_a_field_that_cannot_anchor_it(self):
        """A bare integer at the front of a name is indistinguishable from a title
        that starts with a number. Refusing at construction is better than emitting
        names that no consumer can ever strip."""
        with pytest.raises(ValueError, match="may not begin"):
            NameTemplate(head_fields=("bpm",))

    def test_measuring_narrower_than_writing_is_refused(self):
        """The exact shape of the 2026-07-04 failure, made unconstructable."""
        with pytest.raises(ValueError, match="narrower"):
            NameTemplate(key_pad="camelot2", budget_key_pad="none")

    def test_an_unknown_field_is_refused(self):
        with pytest.raises(ValueError, match="unknown head field"):
            NameTemplate(head_fields=("key", "energy"))

    def test_an_optional_field_must_be_declared(self):
        with pytest.raises(ValueError, match="head_optional"):
            NameTemplate(head_optional=frozenset({"energy"}))

    def test_a_marker_must_name_a_markable_flag(self):
        with pytest.raises(ValueError, match="markable flag"):
            NameTemplate(markers=(MarkerRule(field="loud", literal="x"),))

    def test_every_declared_field_is_anchorable_or_not_on_purpose(self):
        assert HEAD_FIELDS["key"].anchorable
        assert not HEAD_FIELDS["bpm"].anchorable


# ═══════════════════════════════════════════════════════════════════════════
# Budget interaction
# ═══════════════════════════════════════════════════════════════════════════


class TestBudgetInteraction:
    def test_the_budget_head_is_exactly_one_byte_wider_than_the_written_head(self):
        spec = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124)
        written = render_all(spec, template=DEFAULT).filename[: -len("Body.flac")]
        assert len(budget_head(spec, template=DEFAULT).encode()) == len(written.encode()) + 1

    def test_the_marker_is_paid_for_in_the_budget_head(self):
        lossy = NameSpec(stem="Body", suffix=".mp3", key="8A", bpm=124, lossy=True)
        clean = NameSpec(stem="Body", suffix=".flac", key="8A", bpm=124)
        assert budget_head(lossy, template=DEFAULT) == f"08A - 124 - {MARKER} "
        assert len(budget_head(lossy, template=DEFAULT)) > len(
            budget_head(clean, template=DEFAULT))

    def test_an_absent_field_contributes_zero_bytes_including_its_separator(self):
        """An analysis-off library gets the whole budget for its body rather than
        reserving room for a head that will never exist. This falls out of the
        omit-not-empty rule rather than being a second special case."""
        long_stem = "T" * 300
        analyzed = fit_to_budget(
            NameSpec(stem=long_stem, suffix=".flac", key="8A", bpm=124),
            template=DEFAULT, budget=BUDGET, parent_dir=DIR)
        bare = fit_to_budget(
            NameSpec(stem=long_stem, suffix=".flac"),
            template=DEFAULT, budget=BUDGET, parent_dir=DIR)
        assert budget_head(NameSpec(stem="", suffix=""), template=DEFAULT) == ""
        assert len(bare.stem) > len(analyzed.stem)

    def test_build_fits_then_renders_and_the_result_fits_after_padding(self):
        out = build(
            NameSpec(stem="U" * 300, suffix=".flac", key="8A", bpm=124),
            template=DEFAULT, budget=BUDGET, parent_dir=DIR)
        written = f"{DIR}/{out.filename}"
        padded = f"{DIR}/{pad_head(out.filename, template=DEFAULT)}"
        assert len(written.encode()) <= BUDGET.path_budget_bytes
        assert len(padded.encode()) <= BUDGET.path_budget_bytes
        assert len(padded) == len(written) + 1

    def test_the_same_input_twice_yields_the_same_path(self):
        spec = NameSpec(stem="V" * 300, suffix=".flac", key="8A", bpm=124)
        first = build(spec, template=DEFAULT, budget=BUDGET, parent_dir=DIR)
        second = build(spec, template=DEFAULT, budget=BUDGET, parent_dir=DIR)
        assert first == second

    def test_dedupe_runs_before_the_fit_and_the_hash_uses_the_original(self):
        spec = NameSpec(
            stem="Weightless - Marconi Union - Weightless",
            suffix=".flac", key="8A", bpm=124,
            title="Weightless", album="Weightless")
        fitted = fit_to_budget(spec, template=DEFAULT, budget=BUDGET, parent_dir=DIR)
        assert fitted.stem == "Weightless - Marconi Union"


# ═══════════════════════════════════════════════════════════════════════════
# Shape coverage against the live library
# ═══════════════════════════════════════════════════════════════════════════

# Measured 2026-08-01 against a rekordbox export of 10,070 collection rows.
# 9,897 (98.28%) carry a head this parser reads. Of the 173 that do not:
# 169 have no head at all, 3 are titles beginning with a digit, 1 carries a key
# with no tempo. Zero names matched only the deleted parser.
#
# The names below are SYNTHESIZED (seam decision D1 forbids shipping a real
# library string) and cover every shape class and character class the export
# contains: a space, a literal exclamation mark, an ampersand, an accented
# character in both composition forms, a square bracket, the truncation
# disambiguator, and a body that begins with a digit.
SHAPE_CORPUS = [
    ("08A - 124 - Plain Body", True, "Plain Body", "padded head, space in the body"),
    ("8A - 124 - Plain Body", True, "Plain Body", "unpadded head, pre-pad stage"),
    ("03B - 9 - Slow Drone", True, "Slow Drone", "one-digit tempo"),
    ("12B - 87 - Body & Friend", True, "Body & Friend", "ampersand"),
    ("08A - 124 - Body!", True, "Body!", "literal exclamation mark"),
    ("08A - 124 - Cafe\u0301 Body", True, "Cafe\u0301 Body", "decomposed accent"),
    ("08A - 124 - Caf\u00e9 Body", True, "Caf\u00e9 Body", "composed accent"),
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
    """The two accent forms differ in bytes and must parse identically. Composition
    form is the defect class that cost 144 still-referenced files in July 2026, and
    the head parser must not be a second place it can bite."""
    decomposed = "08A - 124 - Cafe\u0301"
    composed = "08A - 124 - Caf\u00e9"
    assert decomposed != composed
    assert parse_head(decomposed, template=DEFAULT) == parse_head(composed, template=DEFAULT)


# ═══════════════════════════════════════════════════════════════════════════
# Conformance: exactly one Camelot parser in the package
# ═══════════════════════════════════════════════════════════════════════════

SRC_ROOT = Path(__file__).resolve().parent.parent / "src"

#: A character class of exactly the two Camelot letters. That single shape is what
#: every one of the eight copies had in common while agreeing on nothing else, so
#: the detector keys on it rather than on a list of known patterns: a list would
#: have missed six of the eight, since each was a different spelling of the same
#: intent.
#:
#: Deliberately looser than a full Camelot pattern. Matching only complete
#: patterns leaves an obvious way out, which is to assemble one from fragments,
#: and the module under test assembles its own that way. Keying on the fragment
#: closes that route. The cost is that an unrelated two-letter class trips it,
#: which is a review, not a defect.
_LETTER_CLASS = re.compile(r"\[\s*[AaBb]{2,4}\s*\]|\[Aa\]\[Bb\]")


def _camelot_regex_literals(source: str) -> list[str]:
    """Every Camelot-shaped pattern literal, ``bytes`` spellings included.

    The bytes half is not hypothetical. One of the source system's copies is a
    byte-level pattern used to splice a padded key into an export without
    decoding it, and a checker that only looked at ``str`` would have declared
    that file clean.
    """
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
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
    """Fixture first: the guard is proved to bite before it is run over the tree.

    These are the eight patterns that were live in the source system, verbatim.
    Two of them were missing from this unit's own inventory until a fact check
    found them, which is the strongest argument for keying on a shape rather than
    on a list somebody maintained by hand.
    """
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

    # And the byte-level spelling of the same rule, which a str-only checker would
    # have declared clean.
    assert _camelot_regex_literals("P = rb'^[1-9][AB] - '\n")


def test_no_module_carries_a_private_camelot_parser():
    """The whole point of the unit. Eight spellings became one, and this is what
    stops a ninth from arriving quietly in the next module that needs to read a
    key out of a filename."""
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
    """The source's copy of this tuple claims "one tuple, no drift" and there are
    five of them, with three different memberships: a format one tool renames is
    invisible to another. One home, lowercase, dot-prefixed, no duplicates.

    The live export contains .flac, .aiff, .mp3 and .wav and nothing else, so the
    remaining entries are untested by production rather than known-good.
    """
    assert len(set(AUDIO_EXTS)) == len(AUDIO_EXTS)
    assert all(e.startswith(".") and e == e.lower() for e in AUDIO_EXTS)
    assert {".flac", ".aiff", ".aif", ".mp3", ".wav"} <= set(AUDIO_EXTS)


# ═══════════════════════════════════════════════════════════════════════════
# The one filesystem primitive
# ═══════════════════════════════════════════════════════════════════════════


class TestClaimTarget:
    def test_a_free_target_is_claimed_once(self, tmp_path):
        target = tmp_path / "08A - 124 - Body.flac"
        assert claim_target(target) is True
        assert target.exists() and target.stat().st_size == 0

    def test_a_taken_target_is_refused_rather_than_overwritten(self, tmp_path):
        """An exists-then-rename check is racy and POSIX rename overwrites in
        silence, so under any concurrency the loser destroys the winner's audio.
        Claiming first degrades that to a reported collision."""
        target = tmp_path / "08A - 124 - Body.flac"
        target.write_bytes(b"audio")
        assert claim_target(target) is False
        assert target.read_bytes() == b"audio"
