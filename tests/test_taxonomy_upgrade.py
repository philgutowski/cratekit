"""U132: what the shipped template declares that a library's copy lacks, and the copy with it added.

The planner is a function of two texts, so every scenario here is a copy built
from the shipped text by hand and compared with what the planner answers. The
copies are cut with plain string operations rather than with the planner's own
cut, so an expected value never comes from the code under test.
"""

from __future__ import annotations

import tomllib

import pytest

from cratekit.core import routing, taxonomy
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
HIP_HOP_END = "# JAZZ AT THE TOP LEVEL"


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


GENRE_SUB_START = "# A genre sub (U155)"
GENRE_SUB_END = "[[bucket]]\nid = \"house_funky_disco\""
ROMINIMAL_ALIAS = '  "Minimal / Deep Tech",\n  "Rominimal",\n'


def before_genre_subs(text: str) -> str:
    """``text`` as a copy made before U155 has it: no Rominimal alias and no genre sub."""
    assert text.count(ROMINIMAL_ALIAS) == 1
    text = text.replace(ROMINIMAL_ALIAS, '  "Minimal / Deep Tech",\n')
    return _without(text, GENRE_SUB_START, GENRE_SUB_END)


def behind() -> str:
    """A version 2 copy made before the genre Favorites and the Soul folder shipped.

    Its vocabulary tags the catalogue's soul word as R&B, as the live copy's does.
    It predates the Rominimal genre sub as well (U155), which version 2 cannot
    declare.
    """
    text = _without(before_genre_subs(_shipped()), FAVORITES_START, FAVORITES_END)
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
    assert (found.from_version, found.to_version, found.shipped_version) == (2, 5, 5)
    assert found.classes == ("favorites",)
    assert found.buckets == ("soul",)
    assert found.held == ()
    after = taxonomy.load_taxonomy(found.after)
    assert after.schema_version == 5
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


def _subsequence(short: list[str], long: list[str]) -> bool:
    remaining = iter(long)
    return all(any(line == other for other in remaining) for line in short)


def test_every_line_and_entry_the_copy_held_is_kept_in_its_order():
    copy = behind()
    found = _plan(copy)
    raised = copy.replace("schema_version = 2\n", "schema_version = 5\n", 1)
    assert _subsequence(raised.splitlines(), found.after.splitlines())
    before = taxonomy.load_taxonomy(copy)
    after = {b.id: b for b in taxonomy.load_taxonomy(found.after).buckets}
    for bucket in before.buckets:
        assert after[bucket.id] == bucket
    assert found.after.count("# Added by crate taxonomy upgrade") == 2


def test_an_added_entry_sits_where_the_shipped_template_puts_it():
    """Declared order is behaviour: review menus list buckets in it and a tie
    between two buckets' words goes to the first declared."""
    found = _plan(behind())
    shipped = taxonomy.load_taxonomy(_shipped())
    after = taxonomy.load_taxonomy(found.after)
    assert [b.id for b in after.buckets] == [b.id for b in shipped.buckets]
    assert [c.id for c in after.sub_classes] == [c.id for c in shipped.sub_classes]


def test_headers_that_cannot_be_matched_to_entries_put_the_block_at_the_end():
    """The fallback: a header the scan does not read (a quoted key here) leaves
    the copy's headers and entries uneven, so the block goes at the end, and
    the copy's own entries stay exactly as they were."""
    text = behind()
    assert text.count("[[sub_class]]\n") > 1
    quoted = text.replace("[[sub_class]]\n", '[["sub_class"]]\n', 1)
    found = _plan(quoted)
    assert found.classes == ("favorites",)
    assert found.after.rstrip("\n").endswith(
        upgrade.cut(_shipped(), upgrade.SUB_CLASS, "favorites").rstrip("\n")
    )
    before = [c.id for c in taxonomy.load_taxonomy(quoted).sub_classes]
    assert [c.id for c in taxonomy.load_taxonomy(found.after).sub_classes] == [
        *before,
        "favorites",
    ]


def test_a_placement_that_does_not_parse_is_not_kept_whole():
    """A copy that declares its entries inline cannot take a table at its end;
    that is a hold, not a ValueError read as a shipped template defect."""
    assert upgrade._kept_whole("a = 1\n", "a = 1\nb = \n", upgrade.BUCKET, {}) is False


def test_a_shipped_template_that_does_not_load_is_not_the_copys_fault():
    broken = _shipped().replace('id = "rnb"', 'id = "R and B"', 1)
    with pytest.raises(ValueError) as caught:
        upgrade.plan(behind(), broken, template="default")
    assert not isinstance(caught.value, taxonomy.TaxonomyError)
    assert "shipped" in str(caught.value)


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


JAZZ_START = "# JAZZ AT THE TOP LEVEL"
JAZZ_END = '[[bucket]]\nid = "non_electronic"'
#: The four lines a copy made before U133 files Jazz's words by, outside the bucket.
JAZZ_ALIAS = '  "Indie Rock",\n  "Jazz",\n  "Latin",'
JAZZ_SUB = '[[bucket.sub]]\nid = "jazz"\ndisplay = "Jazz"\ntag_aliases = [\n  "jazz",\n]\n\n'
JAZZ_MAP_ROW = '  { source = "Jazz", sub = "jazz" },\n'
JAZZ_VOCABULARY_ROW = '  { word = "Jazz", tag = "Jazz" },\n'


def _swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old
    return text.replace(old, new)


def before_jazz() -> str:
    """The shipped text as it stood before U133: Jazz a style of NonElectronic.

    Without the two rows of U244's Discogs table that write Jazz, which came
    later and do not load where Jazz is a sub; the upgrade never adds rows to a
    table the copy holds, so the plan here is about the bucket alone.
    """
    text = _shipped()
    for row in (
        '  { word = "Afro-Cuban Jazz", tag = "Jazz" },\n',
        '  { word = "Latin Jazz", tag = "Jazz" },\n',
    ):
        text = _swap(text, row, "")
    text = _without(text, JAZZ_START, JAZZ_END)
    text = _swap(text, '  "Indie Rock",\n  "Latin",', JAZZ_ALIAS)
    text = _swap(text, '[[bucket.sub]]\nid = "classical"', JAZZ_SUB + '[[bucket.sub]]\nid = "classical"')
    text = _swap(
        text,
        '  { source = "Indie Rock", sub = "rock" },\n',
        '  { source = "Indie Rock", sub = "rock" },\n' + JAZZ_MAP_ROW,
    )
    return _swap(text, 'keyword = "jazz"\nbucket = "jazz"', 'keyword = "jazz"\nbucket = "non_electronic"')


def _without_jazz_words(text: str) -> str:
    """The three lines NonElectronic files Jazz by, taken out by hand."""
    text = _swap(text, JAZZ_ALIAS, '  "Indie Rock",\n  "Latin",')
    text = _swap(text, JAZZ_SUB, "")
    return _swap(text, JAZZ_MAP_ROW, "")


def test_jazz_is_held_while_non_electronic_still_files_its_words_and_every_place_is_named():
    """U133. The copy files Jazz three ways, and a vocabulary row writes it."""
    copy = before_jazz()
    assert _bucket(copy, "non_electronic").sub_by_source.map["Jazz"] == "jazz"
    found = _plan(copy)
    assert found.buckets == ()
    (held,) = found.held
    assert (held.kind, held.id) == ("bucket", "jazz")
    reasons = list(held.reasons)
    assert len(reasons) == 4, reasons
    alias, map_row, sub, row = reasons
    assert alias.startswith("the copy's bucket non_electronic already files 'Jazz'")
    assert map_row.startswith("the copy's bucket non_electronic, its source map row to jazz already files 'Jazz'")
    assert sub.startswith("the copy's bucket non_electronic, its sub jazz already files 'jazz'")
    assert row.startswith("the copy's [vocabulary.deezer] row 'Jazz' writes 'Jazz'")
    assert "take the row out with it" in row
    assert not found.writes
    assert found.missing_buckets == ("jazz",)


def test_the_hand_edit_the_hold_names_lets_jazz_in_on_the_next_run():
    """Every line the hold named, out, and the copy loads and takes the bucket.

    The catalogue's Jazz still tags Jazz without its row, by the bucket's own
    word. The copy's keyword rule is the copy's and is left where it was, and
    the plan says so, since the shipped template sends a partial match to Jazz.
    """
    by_hand = _without_jazz_words(before_jazz())
    by_hand = _swap(by_hand, JAZZ_VOCABULARY_ROW, "")
    found = _plan(by_hand)
    assert found.buckets == ("jazz",)
    assert found.held == ()
    shipped = taxonomy.load_taxonomy(_shipped())
    assert _bucket(found.after, "jazz") == [b for b in shipped.buckets if b.id == "jazz"][0]
    after = taxonomy.load_taxonomy(found.after)
    order = [b.id for b in after.buckets]
    assert order.index("hip_hop") + 1 == order.index("jazz") == order.index("non_electronic") - 1
    assert routing.resolve_bucket(after, "Jazz").bucket_id == "jazz"
    assert routing.suggest_tag(after, "Jazz", source="deezer").tag == "Jazz"
    assert routing.resolve_bucket(after, "Acid Jazz").bucket_id == "non_electronic"
    (sentence,) = found.keywords
    assert sentence.startswith("the shipped template's keyword rule 'jazz' sends a partial match")
    assert "the copy sends a partial match to non_electronic" in sentence
    assert "repoint it by hand" in sentence
    assert sentence in upgrade.remedy(found)


def test_a_copy_with_no_jazz_keyword_rule_is_told_it_has_none():
    by_hand = _swap(
        _without_jazz_words(before_jazz()).replace(JAZZ_VOCABULARY_ROW, "", 1),
        '[[fuzzy]]\nkeyword = "jazz"\nbucket = "non_electronic"\n\n',
        "",
    )
    (sentence,) = _plan(by_hand).keywords
    assert "the copy has no rule for it" in sentence


def test_a_bucket_this_does_not_add_is_never_told_about_its_keyword_rule():
    """Held, the bucket is not added, so its rule is not yet a difference."""
    assert _plan(before_jazz()).keywords == ()
    assert _plan(_shipped()).keywords == ()


def test_one_place_filing_a_word_under_two_spellings_names_both_in_one_sentence():
    """An alias "Jazz" and a tagging word "jazz" on one bucket are two lines to
    take out, so the sentence names both rather than sending a person round."""
    copy = _swap(before_jazz(), JAZZ_SUB, "")
    copy = _swap(copy, JAZZ_MAP_ROW, "")
    copy = _swap(copy, JAZZ_VOCABULARY_ROW, "")
    copy = _swap(
        copy,
        'rates = false\nenergy = { enabled = false }\n\n[[bucket.sub]]\nid = "classical"',
        'rates = false\ntag_aliases = [\n  "jazz",\n]\nenergy = { enabled = false }\n\n'
        '[[bucket.sub]]\nid = "classical"',
    )
    assert _bucket(copy, "non_electronic").tag_aliases == ("jazz",)
    (held,) = _plan(copy).held
    assert held.reasons == (
        "the copy's bucket non_electronic already files 'Jazz', 'jazz'; "
        "take those words out of it by hand",
    )


def test_a_copy_with_the_words_out_and_the_row_left_does_not_load():
    """Why the hold names the row: without it the hand edit refuses the copy."""
    by_hand = _without_jazz_words(before_jazz())
    with pytest.raises(taxonomy.TaxonomyError, match="vocabulary.deezer"):
        taxonomy.load_taxonomy(by_hand)


def test_every_bucket_of_the_copy_filing_a_word_is_named_not_the_first():
    """A person's copy whose R&B bucket tags "jazz" as well as NonElectronic
    filing it is two buckets to edit, and the hold names both."""
    rnb = 'aliases = [\n  "MPB",\n  "R&B",\n]\ntag_aliases = [\n  "rnb",\n]'
    copy = _swap(before_jazz(), rnb, rnb.replace('  "rnb",', '  "jazz",\n  "rnb",'))
    assert "jazz" in _bucket(copy, "rnb").tag_aliases
    (held,) = _plan(copy).held
    named = [r for r in held.reasons if r.startswith("the copy's bucket ")]
    assert "the copy's bucket rnb already files 'jazz'; take that word out of it by hand" in named
    assert any(r.startswith("the copy's bucket non_electronic already files 'Jazz'") for r in named)


def test_a_vocabulary_row_whose_tag_files_where_the_template_shares_the_word_is_not_named():
    """The row's tag files in the breaks bucket, which the shipped template
    gives "Trap / Wave" on purpose, so taking R&B's word out leaves it
    loading; only the bucket that clashes is named, not the row."""
    copy = _retag(_without(_shipped(), HIP_HOP_START, HIP_HOP_END), "Rap/Hip Hop", "Hip-Hop", "R&B")
    copy = _swap(copy, 'tag_aliases = [\n  "rnb",\n]', 'tag_aliases = [\n  "rnb",\n  "trap / wave",\n]')
    reggae = '  { word = "Reggae", tag = "Caribbean" },\n'
    copy = _swap(copy, reggae, reggae + '  { word = "Trap", tag = "Trap / Wave" },\n')
    (row,) = [w for v in taxonomy.load_taxonomy(copy).vocabularies for w in v.words if w.word == "Trap"]
    assert row.bucket == "breaks_dnb_dubstep"
    (held,) = _plan(copy).held
    assert held.reasons == (
        "the copy's bucket rnb already files 'trap / wave'; take that word out of it by hand",
    )


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
    assert ("schema_version", "5") in kinds
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
    assert "states 5" in words
    assert "favorites" in words
    assert "soul" in words


def test_the_remedy_names_the_verb_and_the_hand_edit():
    words = upgrade.remedy(_plan(live_shaped()))
    assert "crate taxonomy upgrade raises schema_version to 5 and adds favorites" in words
    assert "soul is held" in words
    assert "run crate taxonomy upgrade again" in words


# ---------------------------------------------------------------------------
# The verb, through the real dispatcher
# ---------------------------------------------------------------------------

from cratekit.cli.verbs import taxonomy as upgrade_cli  # noqa: E402
from cratekit.core import config  # noqa: E402
from cratekit.core.exit_codes import ExitCode  # noqa: E402
from tests.cli_drive import drive  # noqa: E402
from tests.test_active_taxonomy import write_active  # noqa: E402
from tests.test_config import valid_data  # noqa: E402

VERB = ["taxonomy", "upgrade"]
APPLY = upgrade_cli.APPLY_GATE


@pytest.fixture
def configured(tmp_path, monkeypatch) -> config.Config:
    root = tmp_path / "library"
    root.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(valid_data(root))
    config.save(cfg)
    config.reset_cache()
    return config.load()


def _backups(path) -> list:
    return sorted(p for p in path.parent.iterdir() if p.name.endswith(".bak"))


def _asked() -> tuple[str, dict]:
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == APPLY and detail["explicit"] is True
    return refused["run_id"], refused


def _decided(run_id: str, option: str) -> None:
    code, envelope = drive(["run", "decide", run_id, APPLY, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), envelope


def test_the_verb_asks_then_writes_the_upgraded_copy_and_keeps_the_old_one(configured):
    path = write_active(configured, behind())
    run_id, refused = _asked()
    shown = refused["cause"]["detail"]["shown"]
    changes = {(i["kind"], i["id"], i["change"]) for i in shown["items"]}
    assert changes == {
        ("schema_version", "5", "raise"),
        ("sub_class", "favorites", "add"),
        ("bucket", "soul", "add"),
    }
    assert path.read_text(encoding="utf-8") == behind()
    _decided(run_id, "approve")
    code, acted = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), acted
    assert acted["data"]["digest"] == shown["digest"]
    assert [w["code"] for w in acted["warnings"]] == [upgrade_cli.UPGRADED]
    assert path.read_text(encoding="utf-8") == _plan(behind()).after
    (kept,) = _backups(path)
    assert kept.read_text(encoding="utf-8") == behind()
    assert str(kept) in acted["warnings"][0]["message"]


def test_a_second_run_plans_nothing_and_asks_nothing(configured):
    path = write_active(configured, _plan(behind()).after)
    code, acted = drive(VERB)
    assert code == int(ExitCode.OK) and acted["outcome"] == "no_op", acted
    assert [w["code"] for w in acted["warnings"]] == [upgrade_cli.NOTHING_TO_UPGRADE]
    assert _backups(path) == []


def test_what_is_held_is_said_and_written_around(configured):
    path = write_active(configured, live_shaped())
    run_id, _ = _asked()
    _decided(run_id, "approve")
    code, acted = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), acted
    codes = [w["code"] for w in acted["warnings"]]
    assert codes == [upgrade_cli.HELD, upgrade_cli.UPGRADED]
    assert "bucket soul" in acted["warnings"][0]["message"]
    assert "rnb" in acted["warnings"][0]["message"]
    after = path.read_text(encoding="utf-8")
    assert _bucket(after, "rnb") == _bucket(live_shaped(), "rnb")
    code, again = drive(VERB)
    assert again["outcome"] == "no_op"
    assert [w["code"] for w in again["warnings"]] == [upgrade_cli.HELD, upgrade_cli.NOTHING_TO_UPGRADE]


def test_the_upgrade_that_adds_jazz_says_the_copys_keyword_rule_is_left(configured):
    copy = _swap(_without_jazz_words(before_jazz()), JAZZ_VOCABULARY_ROW, "")
    path = write_active(configured, copy)
    run_id, _ = _asked()
    _decided(run_id, "approve")
    code, acted = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), acted
    codes = [w["code"] for w in acted["warnings"]]
    assert codes == [upgrade_cli.KEYWORD_RULE, upgrade_cli.UPGRADED]
    assert "'jazz'" in acted["warnings"][0]["message"]
    after = taxonomy.load_taxonomy(path.read_text(encoding="utf-8"))
    assert "jazz" in after.bucket_ids()
    assert [r.bucket for r in after.fuzzy if r.keyword == "jazz"] == ["non_electronic"]


def test_an_abort_writes_nothing(configured):
    path = write_active(configured, behind())
    run_id, _ = _asked()
    _decided(run_id, "abort")
    code, acted = drive(["--run", run_id, *VERB])
    assert acted["outcome"] == "no_op", acted
    assert path.read_text(encoding="utf-8") == behind()
    assert _backups(path) == []


def test_a_copy_edited_between_the_answer_and_the_write_is_refused_as_stale(configured):
    path = write_active(configured, behind())
    run_id, _ = _asked()
    _decided(run_id, "approve")
    edited = behind().replace('display = "R&B"', 'display = "R&B Edited By Hand"', 1)
    path.write_text(edited, encoding="utf-8")
    code, acted = drive(["--run", run_id, *VERB])
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert path.read_text(encoding="utf-8") == edited
    assert _backups(path) == []


def test_a_library_with_no_copy_is_refused_and_given_nothing(configured):
    path = config.state_path("taxonomy_active", configured)
    assert not path.exists()
    code, refused = drive(VERB)
    assert refused["cause"]["reason"] == "config-unusable", refused
    assert code != int(ExitCode.DECISION_REQUIRED)
    assert not path.exists()


def test_a_copy_that_does_not_load_is_refused_before_the_gate(configured):
    path = write_active(configured, behind().replace('id = "rnb"', 'id = "R and B"', 1))
    code, refused = drive(VERB)
    assert refused["cause"]["reason"] == "config-unusable", refused
    assert code != int(ExitCode.DECISION_REQUIRED)
    assert _backups(path) == []


def test_the_digest_is_a_function_of_the_two_texts_alone():
    """The payload takes no path, so a rehearsal on a disposable copy of the
    same file matches the live plan, and another text is another digest."""
    one = upgrade_cli.payload(_plan(behind()))
    two = upgrade_cli.payload(_plan(behind()))
    assert one["digest"] == two["digest"]
    other = upgrade_cli.payload(_plan(live_shaped()))
    assert other["digest"] != one["digest"]


def test_a_backup_never_takes_an_earlier_backups_name(tmp_path):
    from datetime import datetime

    path = tmp_path / "taxonomy.toml"
    now = datetime(2026, 10, 10, 14, 5, 12)
    first = upgrade_cli.backup_path(path, now)
    assert first.name == "taxonomy.toml.2026-10-10T140512.bak"
    first.write_text("x", encoding="utf-8")
    second = upgrade_cli.backup_path(path, now)
    assert second != first and second.parent == path.parent
    assert not second.exists()


def test_a_copy_that_does_not_read_back_is_replaced_by_the_one_it_replaced(configured, monkeypatch):
    from cratekit.core import active_taxonomy
    from cratekit.core.cause import refuse

    path = write_active(configured, behind())
    run_id, _ = _asked()
    _decided(run_id, "approve")

    def refused(cfg):
        raise refuse("config-unusable", "a loader that disagrees with the planner")

    monkeypatch.setattr(active_taxonomy, "load", refused)
    code, acted = drive(["--run", run_id, *VERB])
    assert acted["cause"]["reason"] == "internal-error", acted
    assert "put back" in acted["cause"]["message"]
    assert path.read_text(encoding="utf-8") == behind()
    (kept,) = _backups(path)
    assert kept.read_text(encoding="utf-8") == behind()


def _resumed(configured, text: str):
    """``text`` as the copy, asked, approved, and the verb resumed."""
    path = write_active(configured, text)
    run_id, _ = _asked()
    _decided(run_id, "approve")
    return path, run_id


def test_a_crlf_copy_is_kept_byte_for_byte_and_upgraded_in_its_own_line_ending(configured):
    crlf = behind().replace("\n", "\r\n")
    path, run_id = _resumed(configured, crlf)
    code, acted = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), acted
    (kept,) = _backups(path)
    assert kept.read_bytes() == crlf.encode("utf-8")
    written = path.read_bytes()
    assert written.count(b"\n") == written.count(b"\r\n")
    assert upgrade_cli.as_read(written) == _plan(behind()).after
    assert "line endings" not in str(acted["warnings"])


def test_a_crlf_copy_plans_the_digest_its_lf_twin_does(configured):
    """A rehearsal on a copy checked out with the other line ending still matches."""
    write_active(configured, behind())
    _, lf = _asked()
    write_active(configured, behind().replace("\n", "\r\n"))
    _, crlf = _asked()
    assert lf["cause"]["detail"]["shown"]["digest"] == crlf["cause"]["detail"]["shown"]["digest"]


def test_mixed_line_endings_are_written_as_lf_and_said(configured):
    mixed = behind().replace("\n", "\r\n", 1)
    path, run_id = _resumed(configured, mixed)
    code, acted = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), acted
    (kept,) = _backups(path)
    assert kept.read_bytes() == mixed.encode("utf-8")
    assert b"\r" not in path.read_bytes()
    assert "mixed line endings were written as LF" in str(acted["warnings"])


def test_an_edit_after_the_second_plan_is_refused_as_stale(configured, monkeypatch):
    path, run_id = _resumed(configured, behind())
    edited = behind().replace('display = "R&B"', 'display = "R&B Edited By Hand"', 1)
    calls = []
    real = upgrade.planned

    def planned_then_edited(cfg):
        out = real(cfg)
        calls.append(1)
        if len(calls) == 2:
            path.write_text(edited, encoding="utf-8")
        return out

    monkeypatch.setattr(upgrade, "planned", planned_then_edited)
    code, acted = drive(["--run", run_id, *VERB])
    assert len(calls) == 2
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert path.read_text(encoding="utf-8") == edited
    assert _backups(path) == []


def test_a_restore_that_fails_says_so_and_names_the_backup(configured, monkeypatch):
    from cratekit.core import active_taxonomy
    from cratekit.core.cause import refuse

    path, run_id = _resumed(configured, behind())

    def refused(cfg):
        raise refuse("config-unusable", "a loader that disagrees with the planner")

    writes = []
    real = config.atomic_write_bytes

    def full_on_the_restore(payload, target, **kwargs):
        if target == path:
            writes.append(payload)
            if len(writes) == 2:
                raise OSError(28, "No space left on device")
        return real(payload, target, **kwargs)

    monkeypatch.setattr(active_taxonomy, "load", refused)
    monkeypatch.setattr(config, "atomic_write_bytes", full_on_the_restore)
    code, acted = drive(["--run", run_id, *VERB])
    cause = acted["cause"]
    assert cause["reason"] == "internal-error", acted
    (kept,) = _backups(path)
    assert "failed too" in cause["message"] and "No space left" in cause["message"]
    assert str(kept) in cause["message"]
    assert cause["detail"]["restored"] is False
    assert kept.read_text(encoding="utf-8") == behind()


def test_the_read_back_names_a_copy_it_cannot_read(configured, tmp_path):
    directory = tmp_path / "a-directory"
    directory.mkdir()
    problem = upgrade_cli._read_back(configured, directory, b"")
    assert problem is not None and "directory" in problem.lower()


def test_the_read_back_names_a_copy_that_is_not_utf8(configured):
    raw = b"schema_version = 4\n\xff\xfe\n"
    path = write_active(configured, "")
    path.write_bytes(raw)
    problem = upgrade_cli._read_back(configured, path, raw)
    assert problem is not None and "utf" in problem.lower(), problem


# ---------------------------------------------------------------------------
# U244: a source's vocabulary table the copy lacks, added whole and never over one it holds
# ---------------------------------------------------------------------------

DISCOGS_START = "# DISCOGS' STYLES (U244)."


def without_discogs(text: str) -> str:
    """``text`` as a copy made before U244 has it: no Discogs table at its end."""
    assert text.count(DISCOGS_START) == 1
    head, _, tail = text.partition(DISCOGS_START)
    assert "\n[" not in tail.split("[vocabulary.discogs]", 1)[1], "the table is the last one"
    return head.rstrip("\n") + "\n"


def _shipped_table(source: str) -> dict:
    return tomllib.loads(_shipped())["vocabulary"][source]


def test_a_copy_made_before_u244_gains_the_discogs_table_whole():
    copy = without_discogs(_shipped())
    assert taxonomy.load_taxonomy(copy).vocabulary("discogs") is None
    found = _plan(copy)
    assert found.vocabularies == ("discogs",)
    assert found.held == ()
    assert found.behind and found.writes
    assert found.missing_vocabularies == ("discogs",)
    assert (found.classes, found.buckets) == ((), ())
    after = tomllib.loads(found.after)
    assert after["vocabulary"]["discogs"] == _shipped_table("discogs")
    assert taxonomy.load_taxonomy(found.after).vocabulary("discogs") is not None
    assert found.after.startswith(copy), "every line the copy held is kept, in order"
    assert DISCOGS_START in found.after, "the table's comments come with it"
    assert _plan(found.after).writes is False, "a rerun plans nothing"


def test_the_copys_own_edits_are_kept_when_the_table_is_added():
    copy = _retag(without_discogs(_shipped()), "Rock", "Rock", "Folk")
    copy = copy.replace('display = "R&B"', 'display = "R&B Edited By Hand"', 1)
    found = _plan(copy)
    assert found.vocabularies == ("discogs",)
    kept = taxonomy.load_taxonomy(found.after)
    deezer = kept.vocabulary("deezer")
    assert deezer is not None and deezer["rock"].tag == "Folk"
    assert _bucket(found.after, "rnb").display == "R&B Edited By Hand"
    old = tomllib.loads(copy)
    new = tomllib.loads(found.after)
    assert {k: v for k, v in old.items() if k != "vocabulary"} == {
        k: v for k, v in new.items() if k != "vocabulary"
    }
    assert new["vocabulary"]["deezer"] == old["vocabulary"]["deezer"]


def test_a_discogs_table_the_copy_declares_is_never_touched():
    edited = _retag(_shipped(), "Techno", "Techno", "Tech House")
    found = _plan(edited)
    assert found.vocabularies == ()
    assert not found.behind and not found.writes
    assert found.after == edited


def test_an_empty_discogs_table_the_copy_declares_is_its_choice():
    copy = without_discogs(_shipped()) + "\n[vocabulary.discogs]\nwords = []\n"
    found = _plan(copy)
    assert found.vocabularies == () and not found.writes


def test_a_copy_made_before_r799_gains_both_tables():
    start = "# A SOURCE'S OWN VOCABULARY (R-799)."
    copy = _shipped()
    assert copy.count(start) == 1
    copy = copy.partition(start)[0].rstrip("\n") + "\n"
    found = _plan(copy)
    assert found.vocabularies == ("deezer", "discogs")
    after = tomllib.loads(found.after)["vocabulary"]
    assert after == {"deezer": _shipped_table("deezer"), "discogs": _shipped_table("discogs")}


def test_a_table_whose_row_names_no_folder_in_the_copy_is_held_with_the_loaders_words():
    """The copy renamed the Techno folder, so the row writing Techno names no
    folder there and the copy would not load with the table."""
    copy = without_discogs(_shipped()).replace('display = "Techno"', 'display = "Techno By Hand"', 1)
    taxonomy.load_taxonomy(copy)
    found = _plan(copy)
    assert found.vocabularies == ()
    (held,) = found.held
    assert (held.kind, held.id) == (upgrade.VOCABULARY, "discogs")
    assert any("Techno" in reason for reason in held.reasons)
    assert found.after == copy, "nothing is written around a held table"
    assert found.missing_vocabularies == ("discogs",) and found.behind
    assert "[vocabulary.discogs] is held" in upgrade.remedy(found)


def test_a_copy_that_declares_its_vocabulary_inline_is_held_not_forced():
    start = "# A SOURCE'S OWN VOCABULARY (R-799)."
    copy = _shipped().partition(start)[0].rstrip("\n") + "\n"
    line = f"schema_version = {taxonomy.load_taxonomy(copy).schema_version}\n"
    assert copy.count(line) == 1
    inline = 'vocabulary = { deezer = { words = [{ word = "Rock", tag = "Rock" }] } }\n'
    copy = copy.replace(line, line + inline)
    assert taxonomy.load_taxonomy(copy).vocabulary("deezer") is not None
    found = _plan(copy)
    (held,) = found.held
    assert (held.kind, held.id) == (upgrade.VOCABULARY, "discogs")
    assert "could not take [vocabulary.discogs]" in held.reasons[0]
    assert found.after == copy


def test_every_shipped_table_cuts_whole_and_a_missing_one_refuses():
    for source in tomllib.loads(_shipped())["vocabulary"]:
        cut = upgrade.cut_table(_shipped(), source)
        assert tomllib.loads(cut)["vocabulary"][source] == _shipped_table(source)
    with pytest.raises(ValueError):
        upgrade.cut_table(_shipped(), "juno")


def test_the_gap_and_the_remedy_name_the_missing_table():
    found = _plan(without_discogs(_shipped()))
    assert "it lacks the vocabulary table(s) [vocabulary.discogs]" in upgrade.gap(found)
    assert "adds [vocabulary.discogs]" in upgrade.remedy(found)


def test_the_verb_asks_then_adds_the_discogs_table(configured):
    copy = without_discogs(_shipped())
    path = write_active(configured, copy)
    run_id, refused = _asked()
    shown = refused["cause"]["detail"]["shown"]
    assert {(i["kind"], i["id"], i["change"]) for i in shown["items"]} == {
        ("vocabulary", "discogs", "add")
    }
    _decided(run_id, "approve")
    code, acted = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), acted
    assert acted["data"]["totals"]["vocabularies"] == 1
    assert path.read_text(encoding="utf-8") == _plan(copy).after
    assert "[vocabulary.discogs]" in acted["warnings"][0]["message"]
