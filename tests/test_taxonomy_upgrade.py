"""U132: what the shipped template declares that a library's copy lacks, and the copy with it added.

The planner is a function of two texts, so every scenario here is a copy built
from the shipped text by hand and compared with what the planner answers. The
copies are cut with plain string operations rather than with the planner's own
cut, so an expected value never comes from the code under test.
"""

from __future__ import annotations

import tomllib

import pytest

from cratekit.core import taxonomy
from cratekit.core import taxonomy_upgrade as upgrade


def _shipped() -> str:
    return taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)


def _without(text: str, first: str, until: str) -> str:
    """``text`` with the span from ``first`` up to, not including, ``until`` taken out."""
    assert text.count(first) == 1, first
    head, _, tail = text.partition(first)
    assert tail.count(until) >= 1, until
    _, _, rest = tail.partition(until)
    return head + until + rest


FAVORITES_START = '[[sub_class]]\nid = "favorites"'
FAVORITES_END = "# The set-builder's family vocabulary"
SOUL_START = '[[bucket]]\nid = "soul"'
SOUL_END = "# HIP-HOP AT THE TOP LEVEL"
HIP_HOP_START = '[[bucket]]\nid = "hip_hop"'
HIP_HOP_END = '[[bucket]]\nid = "non_electronic"'


def _version(text: str, version: int) -> str:
    shipped = taxonomy.load_taxonomy(_shipped()).schema_version
    line = f"schema_version = {shipped}\n"
    assert text.count(line) == 1
    return text.replace(line, f"schema_version = {version}\n")


def _retag(text: str, word: str, was: str, now: str) -> str:
    """One vocabulary row's tag changed, as a copy made before a bucket shipped has it."""
    old = f'{{ word = "{word}", tag = "{was}" }}'
    assert text.count(old) == 1, old
    return text.replace(old, f'{{ word = "{word}", tag = "{now}" }}')


def behind() -> str:
    """A version 2 copy made before the genre Favorites and the Soul folder shipped.

    Its vocabulary tags the catalogue's soul word as R&B, as the live copy's does.
    """
    text = _without(_shipped(), FAVORITES_START, FAVORITES_END)
    text = _without(text, SOUL_START, SOUL_END)
    return _version(_retag(text, "Soul & Funk", "Soul", "R&B"), 2)


def live_shaped() -> str:
    """``behind`` with R&B still filing Soul's words, as the live library's copy does."""
    text = behind()
    old = 'aliases = [\n  "MPB",\n  "R&B",\n]\ntag_aliases = [\n  "rnb",\n]'
    assert text.count(old) == 1
    return text.replace(
        old,
        'aliases = [\n  "MPB",\n  "R&B",\n  "Soul",\n  "Soul / R&B",\n]\n'
        'tag_aliases = [\n  "rnb",\n  "soul & funk",\n]',
    )


def _bucket(text: str, bucket_id: str) -> taxonomy.Bucket:
    (found,) = [b for b in taxonomy.load_taxonomy(text).buckets if b.id == bucket_id]
    return found


def _plan(text: str) -> upgrade.Plan:
    return upgrade.plan(text, _shipped(), template=taxonomy.DEFAULT_TEMPLATE_NAME)


# ---------------------------------------------------------------------------
# The brief's four scenarios
# ---------------------------------------------------------------------------


def test_a_version_2_copy_gains_favorites_and_soul_and_the_shipped_version():
    copy = behind()
    assert taxonomy.load_taxonomy(copy).schema_version == 2
    found = _plan(copy)
    assert (found.from_version, found.to_version, found.shipped_version) == (2, 4, 4)
    assert found.classes == ("favorites",)
    assert found.buckets == ("soul",)
    assert found.held == ()
    after = taxonomy.load_taxonomy(found.after)
    assert after.schema_version == 4
    assert [c.id for c in after.sub_classes if c.signal == taxonomy.SIGNAL_PLAYLIST] == ["favorites"]
    shipped = taxonomy.load_taxonomy(_shipped())
    assert _bucket(found.after, "soul") == [b for b in shipped.buckets if b.id == "soul"][0]
    (fav,) = [c for c in after.sub_classes if c.id == "favorites"]
    assert fav == [c for c in shipped.sub_classes if c.id == "favorites"][0]


def test_a_version_4_copy_with_every_entry_plans_nothing():
    found = _plan(_shipped())
    assert not found.writes
    assert not found.behind
    assert found.after == found.before
    assert (found.classes, found.buckets, found.held) == ((), (), ())


def test_an_edited_bucket_is_left_alone():
    copy = behind().replace('display = "R&B"', 'display = "R&B Edited By Hand"', 1)
    edited = _bucket(copy, "rnb")
    assert edited.display == "R&B Edited By Hand"
    found = _plan(copy)
    assert found.buckets == ("soul",)
    assert _bucket(found.after, "rnb") == edited


def test_a_rerun_plans_nothing():
    first = _plan(behind())
    assert first.writes
    again = _plan(first.after)
    assert not again.writes
    assert not again.behind
    assert again.after == first.after


# ---------------------------------------------------------------------------
# What the copy keeps
# ---------------------------------------------------------------------------


def test_every_entry_the_copy_held_is_unchanged_and_its_text_is_a_prefix():
    copy = behind()
    found = _plan(copy)
    raised = copy.replace("schema_version = 2\n", "schema_version = 4\n", 1)
    assert found.after.startswith(raised)
    before = taxonomy.load_taxonomy(copy)
    after = {b.id: b for b in taxonomy.load_taxonomy(found.after).buckets}
    for bucket in before.buckets:
        assert after[bucket.id] == bucket
    assert found.after.count("# Added by crate taxonomy upgrade") == 1


def test_the_added_text_parses_back_to_the_shipped_entries():
    found = _plan(behind())
    shipped = tomllib.loads(_shipped())
    after = tomllib.loads(found.after)
    for kind, ids in (("sub_class", found.classes), ("bucket", found.buckets)):
        for entry_id in ids:
            (want,) = [e for e in shipped[kind] if e["id"] == entry_id]
            (got,) = [e for e in after[kind] if e["id"] == entry_id]
            assert got == want


# ---------------------------------------------------------------------------
# What is held, and the hand edit it names
# ---------------------------------------------------------------------------


def test_soul_is_held_while_rnb_still_files_its_words():
    copy = live_shaped()
    found = _plan(copy)
    assert found.classes == ("favorites",)
    assert found.buckets == ()
    (held,) = found.held
    assert (held.kind, held.id) == ("bucket", "soul")
    (reason,) = held.reasons
    assert "rnb" in reason
    for word in ("'Soul'", "'Soul / R&B'", "'soul & funk'"):
        assert word in reason
    assert _bucket(found.after, "rnb") == _bucket(copy, "rnb")
    assert found.missing_buckets == ("soul",)
    assert found.behind
    taxonomy.load_taxonomy(found.after)


def test_the_hand_edit_lets_soul_in_on_the_next_run():
    held = _plan(live_shaped())
    assert [h.id for h in held.held] == ["soul"]
    by_hand = held.after.replace('  "Soul",\n  "Soul / R&B",\n', "", 1).replace(
        '  "soul & funk",\n', "", 1
    )
    found = _plan(by_hand)
    assert found.buckets == ("soul",)
    assert found.held == ()


def test_a_word_the_shipped_template_files_twice_is_not_a_clash():
    """Trap / Wave routes to breaks and tags as Hip-Hop in the shipped template."""
    copy = _retag(_without(_shipped(), HIP_HOP_START, HIP_HOP_END), "Rap/Hip Hop", "Hip-Hop", "R&B")
    breaks = [b for b in taxonomy.load_taxonomy(copy).buckets if "Trap / Wave" in b.aliases]
    assert breaks, "the shipped breaks bucket no longer routes Trap / Wave"
    found = _plan(copy)
    assert found.buckets == ("hip_hop",)
    assert found.held == ()


def test_a_second_playlist_class_under_another_id_holds_favorites():
    copy = _shipped().replace('id = "favorites"', 'id = "my_favourites"', 1)
    found = _plan(copy)
    (held,) = found.held
    assert (held.kind, held.id) == ("sub_class", "favorites")
    assert any("only one is supported per signal" in r for r in held.reasons)
    assert not found.writes


def test_a_version_line_the_planner_cannot_find_holds_the_raise_and_what_needs_it():
    copy = behind().replace("schema_version = 2\n", '"schema_version" = 2\n', 1)
    assert taxonomy.load_taxonomy(copy).schema_version == 2
    found = _plan(copy)
    assert found.to_version == 2
    kinds = {(h.kind, h.id) for h in found.held}
    assert ("schema_version", "4") in kinds
    assert ("sub_class", "favorites") in kinds
    taxonomy.load_taxonomy(found.after)


def test_a_copy_that_does_not_load_is_refused_by_the_loader():
    with pytest.raises(taxonomy.TaxonomyError):
        _plan(behind().replace('id = "rnb"', 'id = "R and B"', 1))


# ---------------------------------------------------------------------------
# The cut
# ---------------------------------------------------------------------------


def test_every_shipped_class_and_bucket_cuts_whole():
    data = tomllib.loads(_shipped())
    for kind in ("sub_class", "bucket"):
        for entry in data[kind]:
            text = upgrade.cut(_shipped(), kind, entry["id"])
            assert tomllib.loads(text)[kind] == [entry]


def test_a_cut_that_parses_to_something_else_refuses():
    reshaped = _shipped().replace(
        '[[bucket.split_from]]\nid = "rnb_low"', '[bucket_split]\nid = "rnb_low"', 1
    )
    with pytest.raises(ValueError):
        upgrade.cut(reshaped, "bucket", "soul")


# ---------------------------------------------------------------------------
# The words a person reads
# ---------------------------------------------------------------------------


def test_the_gap_names_both_versions_and_each_missing_entry():
    words = upgrade.gap(_plan(live_shaped()))
    assert "schema_version 2" in words
    assert "states 4" in words
    assert "favorites" in words
    assert "soul" in words


def test_the_remedy_names_the_verb_and_the_hand_edit():
    words = upgrade.remedy(_plan(live_shaped()))
    assert "crate taxonomy upgrade raises schema_version to 4 and adds favorites" in words
    assert "soul is held" in words
    assert "run crate taxonomy upgrade again" in words
