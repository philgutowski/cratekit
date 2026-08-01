"""The byte budget and the album-dedupe rule: the two rules every renamer shares.

Ported whole from the source system's budget suite, with one structural change.
Both ceilings now arrive as a ``NameBudget`` parameter instead of being read from
module constants, per seam decision S3. That is not cosmetic here: the last test
in this file measures the SAME name against two different budgets in one process,
which is impossible for an engine that reads its ceilings from global state, and
it is the only way to prove the arithmetic is driven by configuration rather than
by a number that happens to be right.

Pure functions throughout. No filesystem, no audio, no configuration.

Directory literals are synthetic. Seam decision D1 forbids a real library string
in any shipped artifact including tests, so the paths below are built to the same
BYTE LENGTHS as real session directories rather than copied from one.
"""

from __future__ import annotations

import hashlib

import pytest

from cratekit.core.naming import (
    NameBudget,
    dedupe_stem,
    fit_stem_to_budget,
    sanitize_segment,
    trim_dangling,
)

# The shipped ceilings. Config owns these values; the suite states them here so a
# change to the shipped default cannot silently move what these tests assert.
BUDGET = NameBudget(path_budget_bytes=250, filename_max_bytes=255)

# A directory of realistic depth and length, naming nothing real.
DEEP_DIR = "/lib/music/processed/2026/" + "s" * 40
SHALLOW_DIR = "/lib/music/processed/2026/session"


def _hash(s: str, budget: NameBudget = BUDGET) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[: budget.hash_len]


class TestDedupeStem:
    """Ambiguity means identity. Every identity case below is a file that a
    greedier rule would have mutilated in a way nothing downstream could undo."""

    def test_drops_trailing_segment_equal_to_leading(self):
        assert (
            dedupe_stem("Weightless - Marconi Union - Weightless")
            == "Weightless - Marconi Union"
        )

    def test_tag_confirmed_dedupe_when_album_equals_title(self):
        assert (
            dedupe_stem(
                "Weightless - Marconi Union - Weightless",
                title="Weightless",
                album="Weightless",
            )
            == "Weightless - Marconi Union"
        )

    def test_structural_rule_fires_without_an_album_tag(self):
        """One acquisition path fabricates the stem and writes no album tag, so a
        tag-only rule would never fire on exactly the files that need it."""
        assert dedupe_stem("Home - Artist - Home", title="Home", album=None) == "Home - Artist"

    def test_identity_when_segments_differ(self):
        s = "Track - Artist - Some Album"
        assert dedupe_stem(s, title="Track", album="Some Album") == s

    def test_identity_on_near_match_album(self):
        s = "Track - Artist - Track (Deluxe Edition)"
        assert dedupe_stem(s, title="Track", album="Track (Deluxe Edition)") == s

    def test_identity_on_two_segments(self):
        assert dedupe_stem("Foo - Foo") == "Foo - Foo"

    def test_identity_on_no_separator(self):
        assert dedupe_stem("Just A Plain Name") == "Just A Plain Name"

    def test_title_containing_the_separator_is_ambiguous_structurally(self):
        s = "A - B - Artist - A - B"
        assert dedupe_stem(s) == s

    def test_title_containing_the_separator_is_deduped_via_tags(self):
        """Tags see what structure cannot: the title itself contains the separator."""
        assert (
            dedupe_stem("A - B - Artist - A - B", title="A - B", album="A - B")
            == "A - B - Artist"
        )

    def test_sanitized_album_matches_the_stem_segment(self):
        assert (
            dedupe_stem(
                "AC-DC Tribute - Band - AC-DC Tribute",
                title="AC/DC Tribute",
                album="AC/DC Tribute",
            )
            == "AC-DC Tribute - Band"
        )

    def test_deterministic(self):
        s = "Weightless - Marconi Union - Weightless"
        assert dedupe_stem(s) == dedupe_stem(s)

    def test_the_separator_is_a_parameter(self):
        """A template that changes the segment separator changes what dedupe sees.
        Hardcoding it here is how the head and the body drift apart."""
        assert dedupe_stem("Home :: Artist :: Home", sep=" :: ") == "Home :: Artist"
        assert dedupe_stem("Home :: Artist :: Home") == "Home :: Artist :: Home"


class TestSanitizeSegment:
    def test_slashes_become_dashes(self):
        assert sanitize_segment("AC/DC") == "AC-DC"

    def test_backslashes_become_dashes(self):
        assert sanitize_segment("a\\b") == "a-b"

    def test_whitespace_collapsed_and_stripped(self):
        assert sanitize_segment("  a   b  ") == "a b"


class TestTrimDangling:
    def test_strips_a_trailing_separator_fragment(self):
        assert trim_dangling("Some Title -") == "Some Title"
        assert trim_dangling("Some Title - ") == "Some Title"

    def test_strips_a_trailing_open_paren_and_bracket(self):
        assert trim_dangling("Some Title (") == "Some Title"
        assert trim_dangling("Some Title [") == "Some Title"

    def test_strips_trailing_whitespace(self):
        assert trim_dangling("Some Title   ") == "Some Title"

    def test_a_clean_string_is_unchanged(self):
        assert trim_dangling("Some Title (Extended Mix)") == "Some Title (Extended Mix)"


class TestFitStemToBudget:
    #: The BUDGET head: padded key, so the later padding stage's growth is already
    #: paid for. Callers get this from ``budget_head`` and never build it by hand.
    HEAD = "08A - 124 - "
    SUFFIX = ".flac"

    def test_a_short_stem_passes_through_byte_identical(self):
        stem = "Nice Track - Artist - Album"
        assert fit_stem_to_budget(SHALLOW_DIR, self.HEAD, stem, self.SUFFIX, budget=BUDGET) == stem

    def test_over_budget_truncates_and_the_assembled_path_fits(self):
        stem = "X" * 300
        out = fit_stem_to_budget(DEEP_DIR, self.HEAD, stem, self.SUFFIX, budget=BUDGET)
        assert out != stem
        assert out.endswith("~" + _hash(stem))
        full = f"{DEEP_DIR}/{self.HEAD}{out}{self.SUFFIX}"
        assert len(full.encode("utf-8")) <= BUDGET.path_budget_bytes

    def test_padding_a_single_digit_key_cannot_push_a_fitted_name_over(self):
        """The 2026-07-04 failure, locked. The name is measured with the padded
        head and written with the single-digit one, so the padding stage's one
        extra byte was already reserved and both forms fit."""
        stem = "Y" * 300
        out = fit_stem_to_budget(DEEP_DIR, self.HEAD, stem, self.SUFFIX, budget=BUDGET)
        padded = f"{DEEP_DIR}/08A - 124 - {out}{self.SUFFIX}"
        unpadded = f"{DEEP_DIR}/8A - 124 - {out}{self.SUFFIX}"
        assert len(padded.encode("utf-8")) <= BUDGET.path_budget_bytes
        assert len(unpadded.encode("utf-8")) <= BUDGET.path_budget_bytes

    def test_distinct_long_stems_get_distinct_names(self):
        """Remix variants are the concrete case: identical for 200 characters and
        different only in the part the cut removes. Without the disambiguator the
        second file either overwrites the first or is reported as a collision and
        left unprocessed forever."""
        a = "Z" * 200 + " (Extended Mix)"
        b = "Z" * 200 + " (Original Mix)"
        out_a = fit_stem_to_budget(DEEP_DIR, self.HEAD, a, self.SUFFIX, budget=BUDGET)
        out_b = fit_stem_to_budget(DEEP_DIR, self.HEAD, b, self.SUFFIX, budget=BUDGET)
        assert out_a != out_b

    def test_the_hash_derives_from_the_pre_dedupe_stem(self):
        """Two sources that dedupe to the same visible stem must still differ. If
        the hash came from the deduped form they would not, which defeats the
        disambiguator at the one point it is needed."""
        original = "W" * 300 + " - Artist - " + "W" * 300
        deduped = "W" * 300 + " - Artist"
        out = fit_stem_to_budget(
            DEEP_DIR, self.HEAD, deduped, self.SUFFIX, budget=BUDGET, hash_source=original
        )
        assert out.endswith("~" + _hash(original))

    def test_the_visible_part_never_ends_mid_phrase(self):
        stem = ("Q" * 150) + " - " + ("R" * 150)
        out = fit_stem_to_budget(DEEP_DIR, self.HEAD, stem, self.SUFFIX, budget=BUDGET)
        visible = out[: -(BUDGET.hash_len + 1)]
        assert not visible.endswith(("-", " ", "(", "["))

    def test_multibyte_never_splits_a_codepoint(self):
        stem = "日本語の長いタイトル" * 20
        out = fit_stem_to_budget(DEEP_DIR, self.HEAD, stem, self.SUFFIX, budget=BUDGET)
        assert out.encode("utf-8").decode("utf-8") == out
        full = f"{DEEP_DIR}/{self.HEAD}{out}{self.SUFFIX}"
        assert len(full.encode("utf-8")) <= BUDGET.path_budget_bytes

    def test_a_character_count_would_have_passed_this_and_the_byte_count_does_not(self):
        """Why the budget is measured in bytes. 170 Japanese characters are well
        inside any character-based ceiling and are roughly 510 bytes on disk."""
        parent = "/lib/music/processed/2026/sess"
        stem = "あ" * 170
        assert len(f"{parent}/{self.HEAD}{stem}{self.SUFFIX}") < 255
        out = fit_stem_to_budget(parent, self.HEAD, stem, self.SUFFIX, budget=BUDGET)
        assert out != stem
        full = f"{parent}/{self.HEAD}{out}{self.SUFFIX}"
        assert len(full.encode("utf-8")) <= BUDGET.path_budget_bytes

    def test_the_component_cap_applies_even_under_a_short_directory(self):
        """The two ceilings are independent. A shallow directory leaves the path
        budget satisfied while the filename alone still exceeds what the
        filesystem will accept."""
        parent = "/x/y"
        stem = "L" * 400
        out = fit_stem_to_budget(parent, self.HEAD, stem, self.SUFFIX, budget=BUDGET)
        filename = f"{self.HEAD}{out}{self.SUFFIX}"
        assert len(filename.encode("utf-8")) <= BUDGET.filename_max_bytes

    def test_untruncated_names_carry_no_disambiguator(self):
        out = fit_stem_to_budget(SHALLOW_DIR, self.HEAD, "Short - Artist", self.SUFFIX,
                                 budget=BUDGET)
        assert "~" not in out

    def test_the_same_input_twice_yields_the_same_name(self):
        """Determinism is the crash-resume guarantee. A relaunched run derives the
        identical path, so it recognizes and sweeps the previous run's claim stub
        instead of orphaning it and accumulating one more on every relaunch."""
        stem = "M" * 280
        first = fit_stem_to_budget(DEEP_DIR, self.HEAD, stem, self.SUFFIX, budget=BUDGET)
        second = fit_stem_to_budget(DEEP_DIR, self.HEAD, stem, self.SUFFIX, budget=BUDGET)
        assert first == second

    def test_an_unsatisfiable_budget_raises_rather_than_emitting(self):
        parent = "/x/" + "d" * (BUDGET.path_budget_bytes + 20)
        with pytest.raises(ValueError, match="unsatisfiable"):
            fit_stem_to_budget(parent, self.HEAD, "Anything", self.SUFFIX, budget=BUDGET)

    def test_two_budgets_in_one_process_give_two_answers(self):
        """The proof that the ceilings are parameters. An engine reading them from
        global configuration cannot produce both of these in one run, and this is
        the property U3's second-template verification also depends on."""
        stem = "N" * 120
        generous = NameBudget(path_budget_bytes=400, filename_max_bytes=255)
        tight = NameBudget(path_budget_bytes=150, filename_max_bytes=255)
        assert fit_stem_to_budget(SHALLOW_DIR, self.HEAD, stem, self.SUFFIX,
                                  budget=generous) == stem
        assert fit_stem_to_budget(SHALLOW_DIR, self.HEAD, stem, self.SUFFIX,
                                  budget=tight) != stem

    def test_the_disambiguator_length_is_a_parameter(self):
        stem = "P" * 300
        wide = NameBudget(path_budget_bytes=250, filename_max_bytes=255, hash_len=12)
        out = fit_stem_to_budget(DEEP_DIR, self.HEAD, stem, self.SUFFIX, budget=wide)
        assert out.endswith("~" + _hash(stem, wide))
