"""A genre word outside the taxonomy, answered in one command (U194).

The planner, ``core.taxonomy_word``, on the shipped text and copies cut from
it: which words it answers, the edit it makes, and that nothing else moves.
Then the two verbs through the real dispatcher, on a library holding a copy and
real tagged containers: the gate, the stale answer, the writes and the read back.
"""

from __future__ import annotations

import shutil
import tomllib
from pathlib import Path

import pytest

from cratekit.cli.verbs import taxonomy_word as word_cli
from cratekit.core import active_taxonomy, config, routing, tags, taxonomy, taxonomy_upgrade
from cratekit.core import taxonomy_word as word_edit
from cratekit.core.exit_codes import ExitCode
from tests.cli_drive import drive
from tests.test_active_taxonomy import write_active
from tests.test_config import valid_data
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414

WORD = "Latin Electronic"
AFRO = "Afro House"
BREAKS = "Breaks / D&B / Dubstep"
BREAKS_LOWER = "breaks / d&b / dubstep"


def _shipped() -> str:
    return taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)


def _parsed_without(text: str, bucket_id: str, key: str) -> dict:
    data = tomllib.loads(text)
    for bucket in data["bucket"]:
        if bucket["id"] == bucket_id:
            bucket.pop(key, None)
    return data


# The planner.


def test_the_word_is_off_taxonomy_on_the_shipped_template():
    """The premise, driven: the shipped resolver passes the word through and flags it."""
    said = routing.suggest_tag(taxonomy.load_taxonomy(_shipped()), WORD)
    assert said.off_taxonomy and said.tag == WORD


def test_an_alias_is_saved_tags_the_word_as_the_genre_and_moves_nothing_else():
    edit = word_edit.alias(_shipped(), WORD, AFRO)
    assert edit.writes and edit.bucket_id == "afro_house" and edit.display == AFRO
    after = taxonomy.load_taxonomy(edit.after)
    assert after.tagging_alias("latin electronic") == ("afro_house", None)
    said = routing.suggest_tag(after, WORD)
    assert said.tag == AFRO and not said.off_taxonomy
    assert said.bucket_id == "afro_house"
    # Afro House declares no tagging alias, so the edit gives it the array and
    # moves nothing else the copy declares.
    assert _parsed_without(edit.after, "afro_house", "tag_aliases") == tomllib.loads(edit.before)
    (bucket,) = [b for b in tomllib.loads(edit.after)["bucket"] if b["id"] == "afro_house"]
    assert bucket["tag_aliases"] == ["latin electronic"]
    # Every line of the copy is still there, in its order.
    before = edit.before.splitlines()
    kept = iter(edit.after.splitlines())
    assert all(line in kept for line in before)
    # Saved once, the same alias again plans no change.
    again = word_edit.alias(edit.after, WORD, AFRO)
    assert not again.writes and again.bucket_id == "afro_house"


def test_an_alias_joins_the_array_a_bucket_already_has_last():
    edit = word_edit.alias(_shipped(), WORD, "Tech House")
    (bucket,) = [b for b in tomllib.loads(edit.after)["bucket"] if b["id"] == "tech_house"]
    assert bucket["tag_aliases"] == ["tech-house", "latin electronic"]
    assert _parsed_without(edit.after, "tech_house", "tag_aliases") == _parsed_without(
        edit.before, "tech_house", "tag_aliases"
    )


def test_an_alias_joins_an_array_written_on_one_line():
    text = _shipped().replace('tag_aliases = [\n  "tech-house",\n]', 'tag_aliases = ["tech-house"]', 1)
    assert 'tag_aliases = ["tech-house"]' in text
    edit = word_edit.alias(text, WORD, "Tech House")
    assert 'tag_aliases = ["tech-house", "latin electronic"]' in edit.after


def test_the_genre_is_named_by_its_folder_name_its_id_or_its_name_in_another_case():
    for name in (AFRO, "afro_house", "afro house"):
        assert word_edit.alias(_shipped(), WORD, name).bucket_id == "afro_house", name


def refusal(id_, answer, why, *said, unsaid=(), step_end=None):
    """An answer refused: ``why`` (None when not asserted), texts the refusal
    says and does not say, and the end of its step."""
    return pytest.param(answer, why, said, unsaid, step_end, id=id_)


def _alias(word, genre):
    return lambda: word_edit.alias(_shipped(), word, genre)


def _folder(word):
    return lambda: word_edit.folder(_shipped(), word)


REFUSALS = [
    *[refusal(f"undeclared-genre-{n}", _alias(WORD, n), word_edit.NO_SUCH_GENRE, AFRO) for n in ("Gqom House", "Caribbean")],
    *[
        refusal(f"too-coarse-alias-{w}", _alias(w, AFRO), word_edit.TOO_COARSE, "too coarse")
        for w in ("Electronic", "Electro", "Experimental", "Electronica", "Other")
    ],
    *[refusal(f"too-coarse-folder-{w}", _folder(w), word_edit.TOO_COARSE) for w in ("Electronic", "Electro", "Experimental", "Other")],
    # Since U118 another bucket's tagging alias wins over the fallback's routing
    # alias, so the refusal must not say an alias cannot answer the word.
    refusal("fallback-says-a-hand-alias-would-override", _alias("Electro", AFRO), None, "by hand would override",
            unsaid=("neither an alias",)),
    refusal("bare-folder-step-names-the-folder-verb", _alias(WORD, "NonElectronic"), word_edit.BARE_FOLDER,
            step_end=f"{word_edit.FOLDER_VERB} '{WORD}'"),
    # The word is asked first, so the bare folder's step never offers the folder
    # verb for a word that verb refuses.
    refusal("too-coarse-word-to-a-bare-folder", _alias("Electronic", "NonElectronic"), word_edit.TOO_COARSE),
    refusal("genre-in-a-case-two-folders-share", lambda: word_edit.genre(taxonomy.load_taxonomy(
        _shipped().replace('display = "Organic House"', 'display = "afro house"', 1)), "AFRO HOUSE"), None, "2 genre folders"),
    refusal("word-already-tagged-names-where", _alias("Latin", AFRO), word_edit.ALREADY_FILED, "'NonElectronic'"),
    refusal("alias-already-saved-to-another-genre", lambda: word_edit.alias(
        word_edit.alias(_shipped(), WORD, AFRO).after, WORD, "Tech House"), word_edit.ALREADY_FILED),
    refusal("no-word", _alias("  ", AFRO), word_edit.NO_WORD),
]


@pytest.mark.parametrize(("answer", "why", "said", "unsaid", "step_end"), REFUSALS)
def test_an_answer_the_planner_cannot_give_is_refused_with_why(answer, why, said, unsaid, step_end):
    with pytest.raises(word_edit.Refused) as caught:
        answer()
    refused = caught.value
    if why is not None:
        assert refused.why == why
    for text in said:
        assert text in str(refused)
    for text in unsaid:
        assert text not in str(refused)
    if step_end is not None:
        assert refused.step.endswith(step_end)


def test_a_sub_is_not_a_genre_an_alias_can_name():
    """Routing recognises a bucket's name and never a sub's (Caribbean), so a
    file retagged to a sub would never be filed by its own name."""
    declared = taxonomy.load_taxonomy(_shipped())
    assert declared.bucket_for_display("Caribbean") is None
    with pytest.raises(word_edit.Refused):
        word_edit.genre(declared, "Caribbean")


@pytest.mark.parametrize("name", ["Electronica / Other", "NonElectronic"])
def test_an_alias_to_a_folder_whose_name_files_nothing_by_itself_is_refused(name):
    """The fallback's name is a catch-all, and the non electronic folder files by
    the track's own genre, so either name on a file files it by a default."""
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.alias(_shipped(), WORD, name)
    assert refused.value.why == word_edit.BARE_FOLDER
    assert word_edit.FOLDER_VERB in str(refused.value)
    # Each may still lend a new folder its priors.
    assert word_edit.folder(_shipped(), WORD, name).writes


def test_a_declined_word_that_is_a_folders_name_is_a_folder_already_declared():
    """Techno declines for tagging and is the Techno folder's name, so the
    folder answer is already given and plans nothing."""
    edit = word_edit.folder(_shipped(), "Techno")
    assert not edit.writes and edit.bucket_id == "techno"
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.alias(_shipped(), "Techno", AFRO)
    assert refused.value.why == word_edit.ALREADY_FILED


@pytest.mark.parametrize("word", [BREAKS_LOWER, "nonelectronic", "AFRO HOUSE"])
def test_a_folders_own_name_in_another_case_is_refused_to_any_other_folder(word):
    """R-1184: a folder's lowercased name is off taxonomy, and an alias of
    another folder would retag the exact name too, a folder of its own would be
    a second of that name, so both refuse saying where the files are filed now."""
    declared = taxonomy.load_taxonomy(_shipped())
    if word != "AFRO HOUSE":
        assert routing.suggest_tag(declared, word).off_taxonomy
    for answer in (lambda: word_edit.alias(_shipped(), word, "Tech House"), lambda: word_edit.folder(_shipped(), word)):
        with pytest.raises(word_edit.Refused) as refused:
            answer()
        assert refused.value.why == word_edit.OWN_NAME
        message = str(refused.value)
        assert "in another case" in message and "is filed in" in message
        assert "already has a place" not in message
        assert refused.value.step


def test_the_premise_routing_knows_a_folders_name_only_exactly():
    """Driven on the shipped template: each lowercased name is filed by a
    keyword rule, nonelectronic in the fallback and not in NonElectronic."""
    declared = taxonomy.load_taxonomy(_shipped())
    breaks = routing.resolve_bucket(declared, BREAKS_LOWER)
    assert breaks.match is routing.Match.FUZZY and breaks.bucket_id == "breaks_dnb_dubstep"
    non = routing.resolve_bucket(declared, "nonelectronic")
    assert non.match is routing.Match.FUZZY and non.bucket_id == declared.fallback.bucket
    assert routing.resolve_bucket(declared, BREAKS).match is routing.Match.PASSTHROUGH


@pytest.mark.parametrize("name", [BREAKS, "breaks_dnb_dubstep", BREAKS_LOWER])
def test_a_folders_own_name_in_another_case_is_answered_by_its_own_folder(name):
    """A plan that changes no text, since the word is the folder's name, and
    files the word's files under the exact name, which files them by itself."""
    edit = word_edit.alias(_shipped(), BREAKS_LOWER, name)
    assert not edit.writes and edit.own_name
    assert edit.bucket_id == "breaks_dnb_dubstep" and edit.display == BREAKS


def test_a_folders_own_name_whose_folder_files_nothing_by_its_name_is_refused_truly():
    """NonElectronic files by each track's own genre, so its bare name files
    nothing: refused by its own folder, the one step is a retag by hand, never
    the folder verb that refuses it too."""
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.alias(_shipped(), "nonelectronic", "NonElectronic")
    assert refused.value.why == word_edit.OWN_NAME
    message = str(refused.value)
    assert "is filed in Electronica / Other by the keyword rule 'electronic'" in message
    assert "neither answer takes the word" in message
    assert "already has a place" not in message
    assert "by hand" in refused.value.step
    assert word_edit.FOLDER_VERB not in refused.value.step
    assert word_edit.ALIAS_VERB not in refused.value.step


def test_the_folder_refusal_of_an_own_name_names_the_alias_that_answers_it():
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.folder(_shipped(), BREAKS_LOWER)
    step = refused.value.step
    assert step.startswith(f"run {word_edit.ALIAS_VERB} '{BREAKS_LOWER}' '{BREAKS}'")
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.folder(_shipped(), "nonelectronic")
    assert word_edit.ALIAS_VERB not in refused.value.step


def test_a_folders_name_exactly_already_has_a_place():
    """Routing recognises a folder's name exactly, so there the sentence holds."""
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.alias(_shipped(), BREAKS, AFRO)
    assert refused.value.why == word_edit.ALREADY_FILED
    assert "already has a place" in str(refused.value)
    assert not word_edit.folder(_shipped(), BREAKS).writes


def test_the_warnings_name_each_own_name_with_its_one_answer():
    declared = taxonomy.load_taxonomy(_shipped())
    said = word_edit.own_names(declared, ["gqom", BREAKS_LOWER, "nonelectronic"])
    assert f"{word_edit.ALIAS_VERB} '{BREAKS_LOWER}' '{BREAKS}'" in said
    assert "'nonelectronic' is the name of the genre folder NonElectronic" in said
    assert "gqom" not in said
    assert said.startswith(". A word that is a genre folder's name in another case")
    assert word_edit.own_names(declared, ["gqom", WORD]) == ""
    assert word_edit.own_names(None, [BREAKS_LOWER]) == ""


def test_an_edit_the_loader_refuses_is_refused_with_its_problems(monkeypatch):
    monkeypatch.setattr(taxonomy_upgrade, "loads", lambda text: ["a problem the loader names"])
    for answer in (lambda: word_edit.alias(_shipped(), WORD, AFRO), lambda: word_edit.folder(_shipped(), WORD)):
        with pytest.raises(word_edit.Refused) as refused:
            answer()
        assert refused.value.why == word_edit.WOULD_NOT_LOAD
        assert refused.value.problems == ("a problem the loader names",)


def test_a_copy_whose_headers_do_not_match_its_buckets_is_not_edited():
    """A header written indented loads, and cannot be matched to its entry, so
    the alias is refused with the hand edit rather than placed by a guess."""
    text = _shipped().replace('[[bucket]]\nid = "afro_house"', '  [[bucket]]\nid = "afro_house"', 1)
    assert taxonomy.load_taxonomy(text).bucket("afro_house").display == AFRO
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.alias(text, WORD, AFRO)
    assert refused.value.why == word_edit.NOT_EDITABLE
    assert '"latin electronic"' in str(refused.value)


def test_a_genre_folder_is_made_in_the_form_jazz_has_and_the_word_routes_into_it():
    edit = word_edit.folder(_shipped(), WORD)
    assert edit.writes and edit.bucket_id == "latin_electronic" and edit.display == WORD
    after = taxonomy.load_taxonomy(edit.after)
    made = after.bucket("latin_electronic")
    assert made.display == WORD and made.aliases == (WORD,)
    assert made.tag_aliases == ("latin electronic",)
    assert made.energy.enabled and not made.subs and made.sub_by_source is None
    # The bucket the word routed to before lends its family, window and rating.
    was = taxonomy.load_taxonomy(_shipped())
    like = was.bucket(routing.resolve_bucket(was, WORD).bucket_id)
    assert edit.like == like.id
    assert (made.family, made.bpm, made.rates) == (like.family, like.bpm, like.rates)
    # Last of the buckets, everything else as it was.
    assert after.bucket_ids() == (*was.bucket_ids(), "latin_electronic")
    data = tomllib.loads(edit.after)
    data["bucket"] = data["bucket"][:-1]
    assert data == tomllib.loads(edit.before)
    # A track carrying the word routes into the new folder.
    resolved = routing.resolve_bucket(after, WORD)
    assert resolved.bucket_id == "latin_electronic"
    assert resolved.match is routing.Match.EXACT
    said = routing.suggest_tag(after, "latin electronic")
    assert said.tag == WORD and not said.off_taxonomy
    # A folder already declared plans no change.
    again = word_edit.folder(edit.after, WORD)
    assert not again.writes and again.bucket_id == "latin_electronic"
    assert not word_edit.folder(_shipped(), "Deep House").writes


def test_like_names_the_bucket_the_folder_takes_its_priors_from():
    edit = word_edit.folder(_shipped(), WORD, "Jazz")
    made = taxonomy.load_taxonomy(edit.after).bucket("latin_electronic")
    jazz = taxonomy.load_taxonomy(_shipped()).bucket("jazz")
    assert edit.like == "jazz"
    assert (made.family, made.bpm, made.rates) == (jazz.family, jazz.bpm, False)
    assert "rates = false" in edit.after
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.folder(_shipped(), WORD, "No Such Genre")
    assert refused.value.why == word_edit.NO_SUCH_GENRE


def test_a_word_fuzzy_routed_to_a_real_bucket_takes_that_buckets_priors():
    """Psy-Trance is off taxonomy and a keyword rule files it in Trance (CONCEPTS, Off taxonomy)."""
    edit = word_edit.folder(_shipped(), "Psy-Trance")
    assert edit.like == "trance" and edit.bucket_id == "psy_trance"


def test_a_new_bucket_id_is_lowercase_snake_and_never_one_the_copy_holds():
    assert word_edit.bucket_id_for("Café Del Mar", set()) == "cafe_del_mar"
    assert word_edit.bucket_id_for("2-Step", set()) == "genre_2_step"
    assert word_edit.bucket_id_for("???", set()) == "genre"
    assert word_edit.bucket_id_for("Jazz", {"jazz", "jazz_2"}) == "jazz_3"


def test_a_word_with_a_quote_is_written_as_a_toml_string_that_reads_back():
    word = 'Baile "Funk" \\ Latino'
    edit = word_edit.folder(_shipped(), word)
    assert taxonomy.load_taxonomy(edit.after).bucket(edit.bucket_id).display == word
    alias = word_edit.alias(_shipped(), word, AFRO)
    assert taxonomy.load_taxonomy(alias.after).tagging_alias(word.lower()) == ("afro_house", None)


# The verbs, through the dispatcher.

ALIAS = ["taxonomy", "alias", WORD, AFRO]
FOLDER = ["taxonomy", "folder", WORD]


@pytest.fixture
def configured(tmp_path, monkeypatch) -> config.Config:
    root = tmp_path / "library"
    root.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(valid_data(root))
    config.save(cfg)
    config.reset_cache()
    return config.load()


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    from tests._containers import synth_container

    return synth_container(tmp_path_factory.mktemp("synth"), ".flac")


def _track(cfg: config.Config, silence: Path, relative: str, *genres: str) -> Path:
    path = Path(cfg.library.root) / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(silence, path)
    if len(genres) == 1:
        assert tags.write_genre(path, genres[0])
    elif genres:
        from mutagen.flac import FLAC

        handle = FLAC(path)
        handle["genre"] = list(genres)
        handle.save()
    return path


def _genres(path: Path) -> tuple[str, ...]:
    return tags.read_tag_values_checked(path, "genre") or ()


def _backups(path: Path) -> list[Path]:
    return sorted(p for p in path.parent.iterdir() if p.name.endswith(".bak"))


def _asked(argv: list[str], gate: str) -> tuple[str, dict]:
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == gate and detail["explicit"] is True
    return refused["run_id"], refused


def _decided(run_id: str, gate: str, option: str) -> None:
    code, envelope = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), envelope


def _approved(argv: list[str], gate: str) -> str:
    run_id, _ = _asked(argv, gate)
    _decided(run_id, gate, "approve")
    return run_id


def _codes(envelope: dict) -> list[str]:
    return [w["code"] for w in envelope["warnings"]]


def test_the_alias_is_saved_and_the_file_retagged(configured, silence):
    copy = write_active(configured, _shipped())
    latin = _track(configured, silence, "2026/batch/latin.flac", WORD)
    lower = _track(configured, silence, "2026/batch/lower.flac", "latin electronic")
    other = _track(configured, silence, "2026/batch/other.flac", "Deep House")
    run_id, refused = _asked(ALIAS, word_cli.ALIAS_GATE)
    shown = refused["cause"]["detail"]["shown"]
    planned = {(i["kind"], i.get("path", i.get("word")), i["change"]) for i in shown["items"]}
    assert planned == {
        ("tag_alias", "latin electronic", "add"),
        ("file", "2026/batch/latin.flac", "write"),
        ("file", "2026/batch/lower.flac", "write"),
    }
    assert copy.read_text(encoding="utf-8") == _shipped() and _genres(latin) == (WORD,)

    _decided(run_id, word_cli.ALIAS_GATE, "approve")
    code, acted = drive(["--run", run_id, *ALIAS])

    assert code == int(ExitCode.OK), acted
    assert acted["data"]["digest"] == shown["digest"]
    assert _codes(acted) == [word_cli.ALIAS_SAVED, word_cli.FILES_RETAGGED]
    assert "crate tag rows" in acted["warnings"][1]["message"]
    assert "crate route resort" in acted["warnings"][1]["message"]
    assert copy.read_text(encoding="utf-8") == word_edit.alias(_shipped(), WORD, AFRO).after
    assert _genres(latin) == (AFRO,) and _genres(lower) == (AFRO,)
    assert _genres(other) == ("Deep House",)
    (kept,) = _backups(copy)
    assert kept.read_text(encoding="utf-8") == _shipped()

    # A second run has nothing left to do and asks nothing.
    code, again = drive(ALIAS)
    assert code == int(ExitCode.OK) and again["outcome"] == "no_op", again
    assert _codes(again) == [word_cli.NOTHING_TO_DO]


def test_a_file_with_two_genres_is_left_and_named(configured, silence):
    write_active(configured, _shipped())
    both = _track(configured, silence, "both.flac", WORD, "Afro House")
    run_id, refused = _asked(ALIAS, word_cli.ALIAS_GATE)
    items = refused["cause"]["detail"]["shown"]["items"]
    assert {"kind": "file", "path": "both.flac", "change": "left", "current": f"{WORD} | {AFRO}",
            "reason": word_cli.SEVERAL_GENRES} in items
    _decided(run_id, word_cli.ALIAS_GATE, "approve")
    code, acted = drive(["--run", run_id, *ALIAS])
    assert code == int(ExitCode.OK), acted
    assert _codes(acted) == [word_cli.FILES_LEFT, word_cli.ALIAS_SAVED]
    assert _genres(both) == (WORD, AFRO)


def test_folder_narrows_the_files_retagged(configured, silence):
    write_active(configured, _shipped())
    inside = _track(configured, silence, "batch/in.flac", WORD)
    outside = _track(configured, silence, "elsewhere/out.flac", WORD)
    argv = [*ALIAS, "--folder", str(inside.parent)]
    run_id = _approved(argv, word_cli.ALIAS_GATE)
    code, acted = drive(["--run", run_id, *argv])
    assert code == int(ExitCode.OK), acted
    assert _genres(inside) == (AFRO,) and _genres(outside) == (WORD,)


def test_an_alias_to_an_undeclared_genre_is_refused_before_the_gate(configured, silence):
    copy = write_active(configured, _shipped())
    latin = _track(configured, silence, "latin.flac", WORD)
    code, refused = drive(["taxonomy", "alias", WORD, "Gqom House"])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "taxonomy-genre-unknown"
    assert "nothing was written" in refused["cause"]["message"]
    assert copy.read_text(encoding="utf-8") == _shipped() and _genres(latin) == (WORD,)
    assert _backups(copy) == []


def test_a_file_carrying_a_folders_own_name_is_never_retagged(configured, silence):
    """The tagger writes the breaks folder's name; its lowercased twin on
    another file must not retag either."""
    copy = write_active(configured, _shipped())
    exact = _track(configured, silence, "exact.flac", "Breaks / D&B / Dubstep")
    lower = _track(configured, silence, "lower.flac", "breaks / d&b / dubstep")
    code, refused = drive(["taxonomy", "alias", "breaks / d&b / dubstep", AFRO])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "taxonomy-word-refused"
    (step,) = refused["cause"]["remediation"]["steps"]
    assert step.startswith(f"run {word_edit.ALIAS_VERB} '{BREAKS_LOWER}' '{BREAKS}'"), step
    assert _genres(exact) == ("Breaks / D&B / Dubstep",)
    assert _genres(lower) == ("breaks / d&b / dubstep",)
    assert copy.read_text(encoding="utf-8") == _shipped()


def test_a_folders_own_name_in_another_case_is_retagged_to_the_exact_name(configured, silence):
    """R-1184 through the verb: the lowercased name is retagged to the exact
    one, the copy is not rewritten and the exact name's file is not touched."""
    copy = write_active(configured, _shipped())
    exact = _track(configured, silence, "exact.flac", BREAKS)
    lower = _track(configured, silence, "lower.flac", BREAKS_LOWER)
    other = _track(configured, silence, "other.flac", "Deep House")
    argv = ["taxonomy", "alias", BREAKS_LOWER, BREAKS]
    run_id, refused = _asked(argv, word_cli.ALIAS_GATE)
    shown = refused["cause"]["detail"]["shown"]
    assert [(i["kind"], i.get("path"), i["change"]) for i in shown["items"]] == [("file", "lower.flac", "write")]
    assert not any(i["kind"] == "tag_alias" for i in shown["items"])

    _decided(run_id, word_cli.ALIAS_GATE, "approve")
    code, acted = drive(["--run", run_id, *argv])

    assert code == int(ExitCode.OK), acted
    assert _codes(acted) == [word_cli.FILES_RETAGGED]
    assert _genres(lower) == (BREAKS,) and _genres(exact) == (BREAKS,)
    assert _genres(other) == ("Deep House",)
    assert copy.read_text(encoding="utf-8") == _shipped() and not _backups(copy)

    code, again = drive(argv)
    assert code == int(ExitCode.OK) and again["outcome"] == "no_op", again
    assert _codes(again) == [word_cli.NOTHING_TO_DO]
    message = again["warnings"][0]["message"]
    assert "in another case" in message and "already a tagging alias" not in message


def test_a_folders_own_name_its_folder_cannot_take_is_refused_with_its_step(configured, silence):
    copy = write_active(configured, _shipped())
    lower = _track(configured, silence, "lower.flac", "nonelectronic")
    code, refused = drive(["taxonomy", "alias", "nonelectronic", "NonElectronic"])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "taxonomy-word-refused"
    assert refused["cause"]["detail"]["why"] == word_edit.OWN_NAME
    (step,) = refused["cause"]["remediation"]["steps"]
    assert "by hand" in step
    assert _genres(lower) == ("nonelectronic",)
    assert copy.read_text(encoding="utf-8") == _shipped()


def test_the_bare_folder_refusal_names_the_folder_verb_as_its_step(configured):
    write_active(configured, _shipped())
    code, refused = drive(["taxonomy", "alias", WORD, "NonElectronic"])
    assert code == int(ExitCode.PRECONDITION), refused
    (step,) = refused["cause"]["remediation"]["steps"]
    assert word_edit.FOLDER_VERB in step and "leave the word" not in step


def test_nothing_to_do_does_not_claim_a_file_it_could_not_read(configured):
    write_active(configured, word_edit.alias(_shipped(), WORD, AFRO).after)
    (Path(configured.library.root) / "bad.flac").write_bytes(b"not a flac at all")
    code, acted = drive(ALIAS)
    assert acted["outcome"] == "no_op", acted
    assert _codes(acted) == [word_cli.FILES_NOT_READ, word_cli.NOTHING_TO_DO]
    assert "could not be read" in acted["warnings"][1]["message"]


def test_a_too_coarse_word_is_refused_before_the_gate(configured, silence):
    copy = write_active(configured, _shipped())
    coarse = _track(configured, silence, "coarse.flac", "Electronic")
    for argv in (["taxonomy", "alias", "Electronic", AFRO], ["taxonomy", "folder", "Electronic"]):
        code, refused = drive(argv)
        assert code == int(ExitCode.PRECONDITION), refused
        assert refused["cause"]["reason"] == "taxonomy-word-refused"
        assert refused["cause"]["detail"]["why"] == word_edit.TOO_COARSE
    assert copy.read_text(encoding="utf-8") == _shipped() and _genres(coarse) == ("Electronic",)


def test_a_copy_that_does_not_load_is_refused_with_nothing_written(configured, silence):
    broken = _shipped().replace('id = "rnb"', 'id = "R and B"', 1)
    copy = write_active(configured, broken)
    latin = _track(configured, silence, "latin.flac", WORD)
    for argv in (ALIAS, FOLDER):
        code, refused = drive(argv)
        assert refused["cause"]["reason"] == "config-unusable", refused
        assert code != int(ExitCode.DECISION_REQUIRED)
    assert copy.read_text(encoding="utf-8") == broken and _genres(latin) == (WORD,)
    assert _backups(copy) == []


def test_an_edit_that_would_not_load_is_refused_with_nothing_written(configured, silence, monkeypatch):
    copy = write_active(configured, _shipped())
    latin = _track(configured, silence, "latin.flac", WORD)
    monkeypatch.setattr(taxonomy_upgrade, "loads", lambda text: ["claimed by both"])
    for argv in (ALIAS, FOLDER):
        code, refused = drive(argv)
        assert refused["cause"]["reason"] == "config-unusable", refused
        assert "claimed by both" in refused["cause"]["message"]
        assert "nothing was written" in refused["cause"]["message"]
    assert copy.read_text(encoding="utf-8") == _shipped() and _genres(latin) == (WORD,)
    assert _backups(copy) == []


def test_a_library_with_no_copy_is_refused(configured):
    code, refused = drive(ALIAS)
    assert refused["cause"]["reason"] == "config-unusable", refused
    assert not config.state_path("taxonomy_active", configured).exists()


def test_an_abort_writes_nothing(configured, silence):
    copy = write_active(configured, _shipped())
    latin = _track(configured, silence, "latin.flac", WORD)
    for argv, gate in ((ALIAS, word_cli.ALIAS_GATE), (FOLDER, word_cli.FOLDER_GATE)):
        run_id, _ = _asked(argv, gate)
        _decided(run_id, gate, "abort")
        code, acted = drive(["--run", run_id, *argv])
        assert acted["outcome"] == "no_op", acted
    assert copy.read_text(encoding="utf-8") == _shipped() and _genres(latin) == (WORD,)
    assert _backups(copy) == []


def test_a_copy_edited_after_the_answer_is_refused_as_stale(configured, silence):
    copy = write_active(configured, _shipped())
    latin = _track(configured, silence, "latin.flac", WORD)
    for argv, gate in ((ALIAS, word_cli.ALIAS_GATE), (FOLDER, word_cli.FOLDER_GATE)):
        copy.write_text(_shipped(), encoding="utf-8")
        run_id = _approved(argv, gate)
        edited = _shipped().replace('display = "R&B"', 'display = "R&B Edited By Hand"', 1)
        copy.write_text(edited, encoding="utf-8")
        code, acted = drive(["--run", run_id, *argv])
        assert code == int(ExitCode.DECISION_STALE), acted
        assert acted["cause"]["reason"] == "decision-stale"
        assert copy.read_text(encoding="utf-8") == edited
    assert _genres(latin) == (WORD,) and _backups(copy) == []


def test_a_file_retagged_after_the_answer_is_refused_as_stale(configured, silence):
    copy = write_active(configured, _shipped())
    latin = _track(configured, silence, "latin.flac", WORD)
    run_id = _approved(ALIAS, word_cli.ALIAS_GATE)
    assert tags.write_genre(latin, "Deep House")
    code, acted = drive(["--run", run_id, *ALIAS])
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert copy.read_text(encoding="utf-8") == _shipped() and _genres(latin) == ("Deep House",)


def test_a_file_that_will_not_take_the_genre_is_named_and_the_rerun_finishes(configured, silence, monkeypatch):
    copy = write_active(configured, _shipped())
    stuck = _track(configured, silence, "stuck.flac", WORD)
    took = _track(configured, silence, "took.flac", WORD)
    run_id = _approved(ALIAS, word_cli.ALIAS_GATE)
    real = tags.write_genre
    monkeypatch.setattr(tags, "write_genre", lambda path, genre: False if path == stuck else real(path, genre))
    code, acted = drive(["--run", run_id, *ALIAS])
    assert code == int(ExitCode.PRECONDITION), acted
    assert acted["cause"]["reason"] == "taxonomy-word-unwritten"
    assert acted["cause"]["detail"]["failed"] == ["stuck.flac"]
    assert acted["cause"]["detail"]["written"] == ["took.flac"]
    assert "crate tag rows" in " ".join(acted["cause"]["remediation"]["steps"])
    assert _genres(took) == (AFRO,) and _genres(stuck) == (WORD,)
    assert copy.read_text(encoding="utf-8") == word_edit.alias(_shipped(), WORD, AFRO).after

    monkeypatch.setattr(tags, "write_genre", real)
    run_id, refused = _asked(ALIAS, word_cli.ALIAS_GATE)
    assert [i["change"] for i in refused["cause"]["detail"]["shown"]["items"]] == ["write"]
    _decided(run_id, word_cli.ALIAS_GATE, "approve")
    code, acted = drive(["--run", run_id, *ALIAS])
    assert code == int(ExitCode.OK), acted
    assert _codes(acted) == [word_cli.FILES_RETAGGED]
    assert _genres(stuck) == (AFRO,) and len(_backups(copy)) == 1


def test_the_genre_folder_is_made_and_the_files_route_into_it(configured, silence):
    copy = write_active(configured, _shipped())
    latin = _track(configured, silence, "latin.flac", WORD)
    run_id, refused = _asked(FOLDER, word_cli.FOLDER_GATE)
    (item,) = refused["cause"]["detail"]["shown"]["items"]
    assert item == {"kind": "bucket", "id": "latin_electronic", "display": WORD,
                    "like": "electronica_other", "change": "add"}
    _decided(run_id, word_cli.FOLDER_GATE, "approve")
    code, acted = drive(["--run", run_id, *FOLDER])
    assert code == int(ExitCode.OK), acted
    assert _codes(acted) == [word_cli.FOLDER_MADE]
    assert "crate route resort" in acted["warnings"][0]["message"]
    declared = active_taxonomy.load(config.load())
    (genre,) = _genres(latin)
    assert routing.resolve_bucket(declared, genre).bucket_id == "latin_electronic"
    (kept,) = _backups(copy)
    assert kept.read_text(encoding="utf-8") == _shipped()

    code, again = drive(FOLDER)
    assert code == int(ExitCode.OK) and again["outcome"] == "no_op", again
    assert _codes(again) == [word_cli.FOLDER_ALREADY]


def test_the_digest_takes_no_folder_so_a_rehearsal_on_a_copy_matches(tmp_path, silence):
    """Two libraries holding the same files under two roots plan one digest."""
    edit = word_edit.alias(_shipped(), WORD, AFRO)
    digests = []
    for name in ("live", "rehearsal"):
        root = tmp_path / name
        (root / "batch").mkdir(parents=True)
        path = root / "batch" / "latin.flac"
        shutil.copyfile(silence, path)
        assert tags.write_genre(path, WORD)
        digests.append(word_cli._alias_payload(edit, word_cli.carrying(root, WORD, AFRO))["digest"])
    assert digests[0] == digests[1]


def test_a_file_whose_genre_cannot_be_read_is_named_and_never_called_clean(configured, silence):
    write_active(configured, _shipped())
    latin = _track(configured, silence, "latin.flac", WORD)
    broken = Path(configured.library.root) / "broken.aac"
    broken.write_bytes(b"not audio at all")
    run_id, refused = _asked(ALIAS, word_cli.ALIAS_GATE)
    items = refused["cause"]["detail"]["shown"]["items"]
    assert {"kind": "file", "path": "broken.aac", "change": "unread", "current": ""} in items
    _decided(run_id, word_cli.ALIAS_GATE, "approve")
    code, acted = drive(["--run", run_id, *ALIAS])
    assert code == int(ExitCode.OK), acted
    assert _codes(acted) == [word_cli.FILES_NOT_READ, word_cli.ALIAS_SAVED, word_cli.FILES_RETAGGED]
    assert "broken.aac" in acted["warnings"][0]["message"]
    assert acted["data"]["totals"]["unread"] == 1
    assert _genres(latin) == (AFRO,)


def test_a_folder_that_is_not_there_is_refused_with_nothing_written(configured, tmp_path):
    copy = write_active(configured, _shipped())
    code, refused = drive([*ALIAS, "--folder", str(tmp_path / "gone")])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "source-missing"
    assert copy.read_text(encoding="utf-8") == _shipped() and _backups(copy) == []


def test_a_file_changed_after_the_second_plan_is_left_and_named(configured, silence, monkeypatch):
    """The second plan saw the word; the write reads the file again and finds another genre."""
    write_active(configured, _shipped())
    latin = _track(configured, silence, "latin.flac", WORD)
    seen = word_cli.carrying(Path(configured.library.root), WORD, AFRO)
    run_id = _approved(ALIAS, word_cli.ALIAS_GATE)
    assert tags.write_genre(latin, "Deep House")
    monkeypatch.setattr(word_cli, "carrying", lambda root, word, display: seen)
    code, acted = drive(["--run", run_id, *ALIAS])
    assert code == int(ExitCode.PRECONDITION), acted
    assert acted["cause"]["reason"] == "taxonomy-word-unwritten"
    assert acted["cause"]["detail"]["moved"] == ["latin.flac"]
    assert _genres(latin) == ("Deep House",)


def test_a_write_that_does_not_read_back_is_named_apart_from_one_never_made(configured, silence, monkeypatch):
    write_active(configured, _shipped())
    latin = _track(configured, silence, "latin.flac", WORD)
    run_id = _approved(ALIAS, word_cli.ALIAS_GATE)
    monkeypatch.setattr(tags, "write_genre", lambda path, genre: True)
    code, acted = drive(["--run", run_id, *ALIAS])
    assert code == int(ExitCode.PRECONDITION), acted
    assert acted["cause"]["detail"]["wrong"] == ["latin.flac"]
    assert acted["cause"]["detail"]["failed"] == []
    assert "do not read back" in acted["cause"]["message"]
    assert _genres(latin) == (WORD,)
