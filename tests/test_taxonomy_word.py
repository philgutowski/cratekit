"""A genre word outside the taxonomy, answered in one command (U194).

Two halves. The planner, ``core.taxonomy_word``, driven on the shipped
template's text and on copies cut from it: which words it answers, the edit it
makes, and that nothing else the copy declares moves. Then the two verbs
through the real dispatcher, on a configured library holding a copy and real
tagged containers: the gate, the stale answer, the writes and the read back.
"""

from __future__ import annotations

import shutil
import tomllib
from pathlib import Path

import pytest

from cratekit.core import config, routing, tags, taxonomy, taxonomy_upgrade
from cratekit.core import taxonomy_word as word_edit
from cratekit.core.exit_codes import ExitCode

WORD = "Latin Electronic"
AFRO = "Afro House"


def _shipped() -> str:
    return taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)


def _parsed_without(text: str, bucket_id: str, key: str) -> dict:
    data = tomllib.loads(text)
    for bucket in data["bucket"]:
        if bucket["id"] == bucket_id:
            bucket.pop(key, None)
    return data


# ═══════════════════════════════════════════════════════════════════════════
# 1. The planner
# ═══════════════════════════════════════════════════════════════════════════


def test_the_word_is_off_taxonomy_on_the_shipped_template():
    """The premise, driven: the shipped resolver passes the word through and flags it."""
    said = routing.suggest_tag(taxonomy.load_taxonomy(_shipped()), WORD)
    assert said.off_taxonomy and said.tag == WORD


def test_an_alias_is_saved_and_tags_the_word_as_the_genre():
    edit = word_edit.alias(_shipped(), WORD, AFRO)
    assert edit.writes and edit.bucket_id == "afro_house" and edit.display == AFRO
    after = taxonomy.load_taxonomy(edit.after)
    assert after.tagging_alias("latin electronic") == ("afro_house", None)
    said = routing.suggest_tag(after, WORD)
    assert said.tag == AFRO and not said.off_taxonomy
    assert said.bucket_id == "afro_house"


def test_the_alias_moves_nothing_else_the_copy_declares():
    """Afro House declares no tagging alias, so the edit gives it the array and nothing more."""
    edit = word_edit.alias(_shipped(), WORD, AFRO)
    assert _parsed_without(edit.after, "afro_house", "tag_aliases") == tomllib.loads(edit.before)
    (bucket,) = [b for b in tomllib.loads(edit.after)["bucket"] if b["id"] == "afro_house"]
    assert bucket["tag_aliases"] == ["latin electronic"]
    # Every line of the copy is still there, in its order.
    before = edit.before.splitlines()
    kept = iter(edit.after.splitlines())
    assert all(line in kept for line in before)


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


def test_an_alias_to_a_genre_the_taxonomy_does_not_declare_is_refused():
    for name in ("Gqom House", "Caribbean"):
        with pytest.raises(word_edit.Refused) as refused:
            word_edit.alias(_shipped(), WORD, name)
        assert refused.value.why == word_edit.NO_SUCH_GENRE, name
        assert AFRO in str(refused.value)


def test_a_sub_is_not_a_genre_an_alias_can_name():
    """Caribbean is a sub of the non electronic folder, and routing recognises
    a bucket's name exactly and a sub's not at all, so a file retagged to it
    would be filed by its alias or the fallback and never by its own name."""
    declared = taxonomy.load_taxonomy(_shipped())
    assert declared.bucket_for_display("Caribbean") is None
    with pytest.raises(word_edit.Refused):
        word_edit.genre(declared, "Caribbean")


@pytest.mark.parametrize("word", ["Electronic", "Electro", "Experimental", "Techno", "Other"])
def test_a_too_coarse_word_is_refused_with_why(word):
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.alias(_shipped(), word, AFRO)
    assert refused.value.why == word_edit.TOO_COARSE
    assert "too coarse" in str(refused.value)
    with pytest.raises(word_edit.Refused) as again:
        word_edit.folder(_shipped(), word) if word != "Techno" else word_edit.folder(_shipped(), "Electronica")
    assert again.value.why == word_edit.TOO_COARSE


def test_a_word_the_taxonomy_already_tags_is_refused_naming_where():
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.alias(_shipped(), "Latin", AFRO)
    assert refused.value.why == word_edit.ALREADY_FILED
    assert "'NonElectronic'" in str(refused.value)


def test_an_alias_already_saved_to_the_genre_plans_no_change():
    once = word_edit.alias(_shipped(), WORD, AFRO)
    again = word_edit.alias(once.after, WORD, AFRO)
    assert not again.writes and again.bucket_id == "afro_house"


def test_an_alias_already_saved_to_another_genre_is_refused():
    once = word_edit.alias(_shipped(), WORD, AFRO)
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.alias(once.after, WORD, "Tech House")
    assert refused.value.why == word_edit.ALREADY_FILED


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


def test_a_genre_folder_is_made_in_the_form_jazz_has():
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


def test_a_track_carrying_the_word_routes_into_the_new_folder():
    after = taxonomy.load_taxonomy(word_edit.folder(_shipped(), WORD).after)
    resolved = routing.resolve_bucket(after, WORD)
    assert resolved.bucket_id == "latin_electronic"
    assert resolved.match is routing.Match.EXACT
    said = routing.suggest_tag(after, "latin electronic")
    assert said.tag == WORD and not said.off_taxonomy


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


def test_a_folder_already_declared_plans_no_change():
    once = word_edit.folder(_shipped(), WORD)
    again = word_edit.folder(once.after, WORD)
    assert not again.writes and again.bucket_id == "latin_electronic"
    assert not word_edit.folder(_shipped(), "Deep House").writes


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


def test_no_word_is_refused():
    with pytest.raises(word_edit.Refused) as refused:
        word_edit.alias(_shipped(), "  ", AFRO)
    assert refused.value.why == word_edit.NO_WORD


# ═══════════════════════════════════════════════════════════════════════════
# 2. The verbs, through the dispatcher
# ═══════════════════════════════════════════════════════════════════════════

from cratekit.cli.verbs import taxonomy_word as word_cli  # noqa: E402
from tests.cli_drive import drive  # noqa: E402
from tests.test_active_taxonomy import write_active  # noqa: E402
from tests.test_config import valid_data  # noqa: E402

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
    run_id, _ = _asked(argv, word_cli.ALIAS_GATE)
    _decided(run_id, word_cli.ALIAS_GATE, "approve")
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
        run_id, _ = _asked(argv, gate)
        _decided(run_id, gate, "approve")
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
    run_id, _ = _asked(ALIAS, word_cli.ALIAS_GATE)
    _decided(run_id, word_cli.ALIAS_GATE, "approve")
    assert tags.write_genre(latin, "Deep House")
    code, acted = drive(["--run", run_id, *ALIAS])
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert copy.read_text(encoding="utf-8") == _shipped() and _genres(latin) == ("Deep House",)


def test_a_file_that_will_not_take_the_genre_is_named_and_the_rerun_finishes(configured, silence, monkeypatch):
    copy = write_active(configured, _shipped())
    stuck = _track(configured, silence, "stuck.flac", WORD)
    took = _track(configured, silence, "took.flac", WORD)
    run_id, _ = _asked(ALIAS, word_cli.ALIAS_GATE)
    _decided(run_id, word_cli.ALIAS_GATE, "approve")
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
    from cratekit.core import active_taxonomy

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
