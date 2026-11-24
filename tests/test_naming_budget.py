"""The byte budget and album-dedupe rule every renamer shares: both ceilings arrive as one
``NameBudget`` (S3). Pure; directory literals are synthetic (D1) at real byte lengths."""

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

# The shipped ceilings, stated here so a changed default cannot move these tests.
BUDGET = NameBudget(path_budget_bytes=250, filename_max_bytes=255)

# A directory of realistic depth and length, naming nothing real.
DEEP_DIR = "/lib/music/processed/2026/" + "s" * 40
SHALLOW_DIR = "/lib/music/processed/2026/session"


def _hash(s: str, budget: NameBudget = BUDGET) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[: budget.hash_len]


DEDUPE_CASES = [
    ("Weightless - Marconi Union - Weightless", {}, "Weightless - Marconi Union",
     "drops-trailing-segment-equal-to-leading"),
    ("Weightless - Marconi Union - Weightless", {"title": "Weightless", "album": "Weightless"},
     "Weightless - Marconi Union", "tag-confirmed-when-album-equals-title"),
    # One acquisition path writes no album tag, so a tag-only rule never fires there.
    ("Home - Artist - Home", {"title": "Home", "album": None}, "Home - Artist",
     "structural-rule-fires-without-an-album-tag"),
    ("Track - Artist - Some Album", {"title": "Track", "album": "Some Album"},
     "Track - Artist - Some Album", "identity-when-segments-differ"),
    ("Track - Artist - Track (Deluxe Edition)",
     {"title": "Track", "album": "Track (Deluxe Edition)"},
     "Track - Artist - Track (Deluxe Edition)", "identity-on-near-match-album"),
    ("Foo - Foo", {}, "Foo - Foo", "identity-on-two-segments"),
    ("Just A Plain Name", {}, "Just A Plain Name", "identity-on-no-separator"),
    ("A - B - Artist - A - B", {}, "A - B - Artist - A - B",
     "separator-in-title-is-ambiguous-structurally"),
    # Tags see what structure cannot: the title itself contains the separator.
    ("A - B - Artist - A - B", {"title": "A - B", "album": "A - B"}, "A - B - Artist",
     "separator-in-title-deduped-via-tags"),
    ("AC-DC Tribute - Band - AC-DC Tribute", {"title": "AC/DC Tribute", "album": "AC/DC Tribute"},
     "AC-DC Tribute - Band", "sanitized-album-matches-the-stem-segment"),
    # The separator is a parameter; hardcoding it lets the head and body drift.
    ("Home :: Artist :: Home", {"sep": " :: "}, "Home :: Artist", "separator-is-a-parameter"),
    ("Home :: Artist :: Home", {}, "Home :: Artist :: Home", "default-separator-ignores-another"),
]


class TestDedupeStem:
    """Every identity case is a file a greedier rule would have mutilated."""

    @pytest.mark.parametrize(
        "stem,kwargs,expected", [c[:3] for c in DEDUPE_CASES], ids=[c[3] for c in DEDUPE_CASES]
    )
    def test_dedupe_stem(self, stem, kwargs, expected):
        assert dedupe_stem(stem, **kwargs) == expected

    def test_deterministic(self):
        s = "Weightless - Marconi Union - Weightless"
        assert dedupe_stem(s) == dedupe_stem(s)


@pytest.mark.parametrize(
    "raw,expected",
    [("AC/DC", "AC-DC"), ("a\\b", "a-b"), ("  a   b  ", "a b")],
    ids=["slashes-become-dashes", "backslashes-become-dashes", "whitespace-collapsed-and-stripped"],
)
def test_sanitize_segment(raw, expected):
    assert sanitize_segment(raw) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [("Some Title -", "Some Title"), ("Some Title - ", "Some Title"),
     ("Some Title (", "Some Title"), ("Some Title [", "Some Title"),
     ("Some Title   ", "Some Title"),
     ("Some Title (Extended Mix)", "Some Title (Extended Mix)")],
    ids=["separator-fragment", "separator-fragment-with-space", "open-paren", "open-bracket",
         "trailing-whitespace", "clean-string-unchanged"],
)
def test_trim_dangling(raw, expected):
    assert trim_dangling(raw) == expected


class TestFitStemToBudget:
    #: The BUDGET head (padded key); callers get it from ``budget_head``.
    HEAD = "08A - 124 - "
    SUFFIX = ".flac"

    def fit(self, stem, parent=DEEP_DIR, budget=BUDGET, **kwargs):
        return fit_stem_to_budget(parent, self.HEAD, stem, self.SUFFIX, budget=budget, **kwargs)

    def assert_path_fits(self, out, parent=DEEP_DIR, head=HEAD):
        full = f"{parent}/{head}{out}{self.SUFFIX}"
        assert len(full.encode("utf-8")) <= BUDGET.path_budget_bytes

    def test_a_short_stem_passes_through_byte_identical(self):
        stem = "Nice Track - Artist - Album"
        assert self.fit(stem, SHALLOW_DIR) == stem

    def test_over_budget_truncates_and_the_assembled_path_fits(self):
        stem = "X" * 300
        out = self.fit(stem)
        assert out != stem
        assert out.endswith("~" + _hash(stem))
        self.assert_path_fits(out)

    def test_padding_a_single_digit_key_cannot_push_a_fitted_name_over(self):
        """The 2026-07-04 failure, locked: measured padded, so both forms fit."""
        out = self.fit("Y" * 300)
        self.assert_path_fits(out, head="08A - 124 - ")
        self.assert_path_fits(out, head="8A - 124 - ")

    def test_distinct_long_stems_get_distinct_names(self):
        """Remix variants differ only in the part the cut removes."""
        assert self.fit("Z" * 200 + " (Extended Mix)") != self.fit("Z" * 200 + " (Original Mix)")

    def test_the_hash_derives_from_the_pre_dedupe_stem(self):
        """Two sources deduping to one visible stem must still differ."""
        original = "W" * 300 + " - Artist - " + "W" * 300
        out = self.fit("W" * 300 + " - Artist", hash_source=original)
        assert out.endswith("~" + _hash(original))

    def test_the_visible_part_never_ends_mid_phrase(self):
        out = self.fit(("Q" * 150) + " - " + ("R" * 150))
        visible = out[: -(BUDGET.hash_len + 1)]
        assert not visible.endswith(("-", " ", "(", "["))

    def test_multibyte_never_splits_a_codepoint(self):
        out = self.fit("日本語の長いタイトル" * 20)
        assert out.encode("utf-8").decode("utf-8") == out
        self.assert_path_fits(out)

    def test_a_character_count_would_have_passed_this_and_the_byte_count_does_not(self):
        """170 Japanese characters pass a character ceiling and are ~510 bytes."""
        parent = "/lib/music/processed/2026/sess"
        stem = "あ" * 170
        assert len(f"{parent}/{self.HEAD}{stem}{self.SUFFIX}") < 255
        out = self.fit(stem, parent)
        assert out != stem
        self.assert_path_fits(out, parent)

    def test_the_component_cap_applies_even_under_a_short_directory(self):
        """The two ceilings are independent: a short path can carry a too-long name."""
        filename = f"{self.HEAD}{self.fit('L' * 400, '/x/y')}{self.SUFFIX}"
        assert len(filename.encode("utf-8")) <= BUDGET.filename_max_bytes

    def test_untruncated_names_carry_no_disambiguator(self):
        assert "~" not in self.fit("Short - Artist", SHALLOW_DIR)

    def test_the_same_input_twice_yields_the_same_name(self):
        """Determinism is the crash-resume guarantee: a relaunch sweeps its old stub."""
        assert self.fit("M" * 280) == self.fit("M" * 280)

    def test_an_unsatisfiable_budget_raises_rather_than_emitting(self):
        parent = "/x/" + "d" * (BUDGET.path_budget_bytes + 20)
        with pytest.raises(ValueError, match="unsatisfiable"):
            self.fit("Anything", parent)

    def test_two_budgets_in_one_process_give_two_answers(self):
        """The ceilings are parameters, which U3's second template also relies on."""
        stem = "N" * 120
        generous = NameBudget(path_budget_bytes=400, filename_max_bytes=255)
        tight = NameBudget(path_budget_bytes=150, filename_max_bytes=255)
        assert self.fit(stem, SHALLOW_DIR, generous) == stem
        assert self.fit(stem, SHALLOW_DIR, tight) != stem

    def test_the_disambiguator_length_is_a_parameter(self):
        stem = "P" * 300
        wide = NameBudget(path_budget_bytes=250, filename_max_bytes=255, hash_len=12)
        assert self.fit(stem, budget=wide).endswith("~" + _hash(stem, wide))
