"""U178: a registered label can carry its genre, so tag folder tags its files with it."""

from __future__ import annotations

import dataclasses
import json
import shutil
from pathlib import Path

import pytest

from cratekit.core import config, jobs, tags
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.label import registry as labels
from cratekit.tagging import artifacts, searchers, tag
from cratekit.tagging import cli as tag_cli
from cratekit.tagging.tag import LabelAnswer, SearchHit
from tests.cli_drive import drive
from tests.test_label_registry_verbs import install
from tests.test_label_workers import one_parser as one_parser  # noqa: PLC0414 - fixture
from tests.test_tag_workers import bound, item_causes, resume_argv, tag_job, warning_codes
from tests.test_tag_workers import folder as folder  # noqa: PLC0414 - fixture
from tests.test_tag_workers import silence as silence  # noqa: PLC0414 - fixture
from tests.test_tagging_engine import SPECIFIC, _jpeg, answering, plant

LABEL = "PULS"
GENRE = "Rominimal"


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    """A configured machine on the full profile, so the registry verb has a taxonomy to ask."""
    return install(tmp_path, monkeypatch)


def track(folder: Path, silence: Path, name: str, *, label: str | None = None,
          genre: str | None = None, picture: bool = True) -> Path:
    path = folder / f"{name}.flac"
    shutil.copy2(silence, path)
    fields = {key: value for key, value in (("label", label), ("genre", genre))
              if value is not None}
    if fields:
        assert tags.write_tags(path, fields)
    if picture:
        plant(path, _jpeg(320, 200), dims=(320, 200, 24))
    return path


def registry(*argv: str, code: ExitCode = ExitCode.OK) -> dict:
    got, envelope = drive(["label", "registry", *argv])
    assert got == int(code), envelope
    return envelope


def registered(*argv: str, name: str = LABEL) -> dict:
    return registry("add", name, *argv)


def held(name: str = LABEL) -> labels.LabelEntry:
    entry = labels.RegistryStore().load().by_name(name)
    assert entry is not None, name
    return entry


def seam(table: dict[str, str]):
    """A label seam over ``{label: genre}`` that records every name it was asked."""
    asked: list[str] = []
    def answer(name: str) -> LabelAnswer | None:
        asked.append(name)
        genre = table.get(name)
        return LabelAnswer(label=name, genre=genre) if genre else None
    answer.asked = asked  # type: ignore[attr-defined]
    return answer


def never_searched(artist: str, title: str):
    raise AssertionError(f"a catalogue was searched for {title!r}")


def never_published(hit, isrc):
    raise AssertionError("the general catalogue was offered a file")


def test_a_genre_the_taxonomy_routes_is_stored_as_typed_and_the_screen_says_where(cfg):
    # An exact alias since U155 gave Rominimal a sub of its own under Minimal / Deep Tech.
    envelope = registered("--genre", GENRE)
    assert held().genre == GENRE, "kept as typed, since it is the word written onto files"
    route = envelope["data"]["summary"]["genre_route"]
    assert route == {"genre": GENRE, "bucket": "minimal_deep_tech",
                     "bucket_display": "Minimal / Deep Tech", "match": "exact", "matched_on": GENRE}
    detail = envelope["data"]["checks"][0]["detail"]
    assert "genre Rominimal routes to Minimal / Deep Tech by an alias the taxonomy declares" in detail
    listed = registry("list")
    assert "genre Rominimal" in listed["data"]["checks"][0]["detail"]
    assert listed["data"]["summary"]["labels"][0]["genre"] == GENRE


@pytest.mark.parametrize(
    ("genre", "match", "said"),
    [
        pytest.param("Minimal Techno", ("fuzzy", "minimal"),
                     "genre Minimal Techno routes to Minimal / Deep Tech by the taxonomy's "
                     "keyword rule 'minimal'", id="by-a-keyword-rule"),
        pytest.param(SPECIFIC, ("exact", None), "by an alias the taxonomy declares",
                     id="by-an-alias"),
    ],
)
def test_a_genre_routed_by_the_taxonomy_says_by_what(cfg, genre, match, said):
    """``match`` is the route's match and, where named, what it matched on."""
    registered()
    envelope = registry("set", LABEL, "--genre", genre)
    route = envelope["data"]["summary"]["genre_route"]
    assert route["match"] == match[0]
    if match[1] is not None:
        assert route["matched_on"] == match[1]
    assert said in envelope["data"]["checks"][0]["detail"]


def test_a_genre_routing_only_to_the_fallback_is_refused_and_nothing_is_written(cfg):
    registered()
    before = labels.RegistryStore().path.read_bytes()
    envelope = registry("set", LABEL, "--genre", "Polka", code=ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "label-name-invalid"
    assert "fallback, Electronica / Other" in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["match"] == "fallback"
    assert labels.RegistryStore().path.read_bytes() == before
    envelope = registry("add", "New Label", "--genre", "Polka", code=ExitCode.PRECONDITION)
    assert labels.RegistryStore().load().by_name("New Label") is None


def test_a_fallback_genre_is_kept_when_confirmed_and_the_screen_says_it(cfg):
    registered()
    envelope = registry("set", LABEL, "--genre", "Polka", "--accept-fallback")
    assert held().genre == "Polka"
    assert envelope["data"]["summary"]["genre_route"]["match"] == "fallback"
    assert "only as the taxonomy's fallback" in envelope["data"]["checks"][0]["detail"]


def test_accept_fallback_with_no_genre_is_refused(cfg):
    registered()
    envelope = registry("set", LABEL, "--accept-fallback", code=ExitCode.PRECONDITION)
    assert "--accept-fallback confirms a --genre" in envelope["cause"]["message"]
    envelope = registry("remove", LABEL, "--accept-fallback", code=ExitCode.PRECONDITION)
    assert labels.RegistryStore().load().by_name(LABEL) is not None


def test_a_verb_that_sets_no_field_refuses_a_genre(cfg):
    registered()
    envelope = registry("remove", LABEL, "--genre", GENRE, code=ExitCode.PRECONDITION)
    assert "--genre" in envelope["cause"]["message"]
    assert labels.RegistryStore().load().by_name(LABEL) is not None


def test_the_word_default_clears_a_genre_and_none_keeps_it(cfg):
    registered("--genre", GENRE)
    labels.RegistryStore().edit(LABEL, track_limit=5)
    assert held().genre == GENRE, "a genre of None keeps what is held"
    registry("set", LABEL, "--genre", "Default")
    assert held().genre is None
    registered("--genre", GENRE)
    registered("--genre", "default")
    assert held().genre is None


def test_a_genre_survives_a_rename(cfg):
    registered("--genre", GENRE)
    labels.RegistryStore().rename(held().label_id, "PULS Romania")
    assert held("PULS Romania").genre == GENRE


@pytest.mark.parametrize("value", ["", "   ", "---", "Romi\nnimal", "x" * 65])
def test_a_genre_that_could_never_be_one_refuses_at_the_store(cfg, value):
    registered()
    with pytest.raises(CratekitError) as caught:
        labels.RegistryStore().edit(LABEL, genre=value)
    assert caught.value.cause.reason == "label-name-invalid"
    assert held().genre is None


def test_the_longest_genre_a_label_may_carry_is_sixty_four_characters(cfg):
    """A literal bound, so a drift of the constant is a failure and not a new bound."""
    registered()
    labels.RegistryStore().edit(LABEL, genre="x" * 64)
    assert held().genre == "x" * 64


def test_a_registry_written_before_genres_existed_reads_with_none(cfg):
    registered()
    path = labels.RegistryStore().path
    raw = json.loads(path.read_text(encoding="utf-8"))
    for entry in raw["labels"].values():
        entry.pop("genre", None)
    path.write_text(json.dumps(raw), encoding="utf-8")
    assert held().genre is None


def test_a_puls_file_with_no_genre_gets_its_labels_genre_with_no_searcher_called(folder, silence):
    path = track(folder, silence, "a", label=LABEL)
    result = tag.tag_one(path, searcher=never_searched, published=never_published,
                         label_genre=seam({LABEL: GENRE}))
    assert tags.read_genre_from_file(path) == GENRE
    assert result.genre_written == GENRE
    assert result.skipped is None
    assert (result.source, result.source_genre, result.label) == (tag.LABEL_GENRE, GENRE, LABEL)
    assert result.off_taxonomy is False, "a label genre is not a catalogue's own word"
    assert result.answers == ()
    assert result.art_fetch == tag.ART_PRESENT


def test_a_file_of_a_label_with_no_genre_is_searched_as_today(folder, silence):
    path = track(folder, silence, "a", label="Other Label")
    searcher = answering({"a": SearchHit(genre=SPECIFIC, source=searchers.BEATPORT, source_genre="deep house")})
    labelled = seam({LABEL: GENRE})
    result = tag.tag_one(path, searcher=searcher, label_genre=labelled)
    assert labelled.asked == ["Other Label"]
    assert searcher.asked == [("", "a")]
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert (result.source, result.label) == (searchers.BEATPORT, "")


@pytest.mark.parametrize("picture", [True, False], ids=["with-a-picture", "with-no-picture"])
def test_a_puls_file_already_tagged_keeps_its_genre_and_the_label_is_never_asked(
    folder, silence, picture
):
    path = track(folder, silence, "a", label=LABEL, genre=SPECIFIC, picture=picture)
    labelled = seam({LABEL: GENRE})
    searcher = answering({"a": SearchHit(genre="Techno", source=searchers.BEATPORT)})
    result = tag.tag_one(path, searcher=never_searched if picture else searcher,
                         label_genre=labelled)
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert result.skipped == tag.HAS_GENRE
    assert result.genre_written is None
    assert labelled.asked == []


def test_the_verbs_label_names_the_label_of_a_file_with_no_tag_and_the_tag_wins(folder, silence):
    bare = track(folder, silence, "bare")
    other = track(folder, silence, "other", label="Other Label")
    searcher = answering({"other": SearchHit(genre=SPECIFIC, source=searchers.BEATPORT)})
    labelled = seam({LABEL: GENRE})
    results = {result.path.stem: result for result in
               tag.tag_folder(folder, searcher=searcher, label_genre=labelled, label=LABEL)}
    assert tags.read_genre_from_file(bare) == GENRE
    assert results["bare"].label == LABEL
    assert tags.read_genre_from_file(other) == SPECIFIC, "a file's own label tag outranks --label"
    assert searcher.asked == [("", "other")]


def test_a_folder_of_mixed_labels_tags_each_by_its_own(folder, silence):
    for name, label in (("a", LABEL), ("b", "Sudbeat"), ("c", "Other Label"), ("d", None)):
        track(folder, silence, name, label=label)
    searcher = answering({"c": SearchHit(genre=SPECIFIC, source=searchers.BEATPORT),
                          "d": SearchHit(genre="Techno", source=searchers.BEATPORT)})
    results = tag.tag_folder(
        folder, searcher=searcher, label_genre=seam({LABEL: GENRE, "Sudbeat": "Progressive House"})
    )
    assert [tags.read_genre_from_file(result.path) for result in results] == [
        GENRE, "Progressive House", SPECIFIC, "Techno"
    ]
    assert [result.label for result in results] == [LABEL, "Sudbeat", "", ""]
    assert searcher.asked == [("", "c"), ("", "d")]


def test_a_puls_file_with_no_picture_is_searched_for_its_art_only(folder, silence):
    path = track(folder, silence, "a", label=LABEL, picture=False)
    searcher = answering({"a": SearchHit(genre="Techno", source=searchers.BEATPORT,
                                         source_genre="techno", art_url="https://img/a.jpg")})
    fetched: list[str] = []
    def fetch(url: str) -> bytes:
        fetched.append(url)
        return _jpeg(640, 640)
    result = tag.tag_one(path, searcher=searcher, fetch_image=fetch, label_genre=seam({LABEL: GENRE}))
    assert searcher.asked == [("", "a")]
    assert fetched == ["https://img/a.jpg"]
    assert result.art_fetch == tag.ART_EMBEDDED
    assert tags.read_genre_from_file(path) == GENRE, "the catalogue's genre never replaces the label's"
    assert (result.genre_written, result.source, result.source_genre) == (GENRE, tag.LABEL_GENRE, GENRE)


def test_a_refusal_on_the_art_search_does_not_fail_a_puls_file(folder, silence):
    path = track(folder, silence, "a", label=LABEL, picture=False)
    def refusing(artist: str, title: str):
        raise refuse(searchers.UNREACHABLE_REASON, "no catalogue could be read",
                     remedy=Remedy.RETRY_LATER, retryable=True, origin=("tests",))
    result = tag.tag_one(path, searcher=refusing, label_genre=seam({LABEL: GENRE}))
    assert tags.read_genre_from_file(path) == GENRE, "the genre was saved before the search"
    assert result.genre_written == GENRE
    assert result.label == LABEL
    assert result.art_fetch == tag.ART_UNAVAILABLE
    assert searchers.UNREACHABLE_REASON in result.art_fetch_detail


def test_no_seam_reads_no_label_and_tags_exactly_as_before(folder, silence):
    path = track(folder, silence, "a", label=LABEL)
    searcher = specific_for_a()
    result = tag.tag_one(path, searcher=searcher, label=LABEL)
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert result.label == ""


def queue(*argv: str) -> dict:
    code, queued = drive(["tag", "folder", "--queue-only", *argv])
    assert code == int(ExitCode.OK), queued
    return queued


def resume(job_id: str, *argv: str) -> dict:
    code, resumed = drive([*resume_argv(job_id), *argv])
    assert code == int(ExitCode.OK), resumed
    return resumed


def sweep(*argv: str) -> tuple[jobs.Job, dict]:
    queue(*argv)
    job = tag_job()
    return job, resume(job.job_id)


def warned(envelope: dict) -> dict[str, str]:
    return {warning["code"]: warning["message"] for warning in envelope["warnings"]}


def specific_for_a():
    return answering({"a": SearchHit(genre=SPECIFIC, source=searchers.BEATPORT)})


def test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart(
    cfg, folder, silence, monkeypatch
):
    registered("--genre", GENRE)
    registered("--genre", "Progressive House", name="Sudbeat")
    for name in ("a", "b", "c"):
        track(folder, silence, name)
    track(folder, silence, "d", label="Sudbeat")
    track(folder, silence, "e", label="Other Label")
    searcher = bound(monkeypatch, answering({"e": SearchHit(genre=SPECIFIC, source=searchers.BEATPORT)}))
    job, resumed = sweep(str(folder), "--label", LABEL)
    assert searcher.asked == [("", "e")], "only the file of a label with no genre was searched"
    assert [tags.read_genre_from_file(folder / f"{name}.flac") for name in "abcde"] == [
        GENRE, GENRE, GENRE, "Progressive House", SPECIFIC
    ]
    tagging = resumed["data"]["progress"]["tagging"]
    assert (tagging["tagged"], tagging["tagged_by"][tag.LABEL_GENRE]) == (5, 4)
    assert tagging["tagged_by"][searchers.BEATPORT] == 1
    assert (tagging["label_genres"], tagging["off_taxonomy"]) == ({LABEL: 3, "Sudbeat": 1}, {})
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert (reports["a.flac"]["source"], reports["a.flac"]["label"]) == (tag.LABEL_GENRE, LABEL)
    assert reports["e.flac"]["label"] == ""
    assert job.payload["label"] == LABEL


def test_the_genres_are_frozen_when_the_sweep_is_queued(cfg, folder, silence, monkeypatch):
    registered("--genre", GENRE)
    track(folder, silence, "a")
    bound(monkeypatch, never_searched)
    queue(str(folder), "--label", LABEL)
    labels.RegistryStore().edit(LABEL, genre=SPECIFIC)
    job = tag_job()
    resume(job.job_id)
    assert tags.read_genre_from_file(folder / "a.flac") == GENRE


def test_a_label_tag_reaches_its_genre_with_no_label_named(cfg, folder, silence, monkeypatch):
    registered("--genre", GENRE)
    track(folder, silence, "a", label="puls")
    bound(monkeypatch, never_searched)
    sweep(str(folder))
    assert tags.read_genre_from_file(folder / "a.flac") == GENRE, "matched as the registry matches a name"


def test_a_sweep_with_no_label_genres_queues_the_payload_it_always_did(cfg, folder, silence, monkeypatch):
    registered()
    track(folder, silence, "a")
    bound(monkeypatch, specific_for_a())
    job, _resumed = sweep(str(folder))
    assert job.payload == {"folder": str(folder)}


def test_a_label_nobody_registered_is_refused_and_nothing_is_queued(cfg, folder, silence):
    track(folder, silence, "a")
    code, envelope = drive(["tag", "folder", "--queue-only", str(folder), "--label", "PLUS"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-unknown"
    with jobs.open_store() as store:
        assert tuple(jobs.list_jobs(store)) == ()


def test_a_label_with_no_genre_is_swept_as_before_and_says_so(cfg, folder, silence, monkeypatch):
    registered()
    track(folder, silence, "a")
    searcher = bound(monkeypatch, specific_for_a())
    queued = queue(str(folder), "--label", LABEL)
    assert tag_cli.LABEL_NO_GENRE == "tag-folder-label-no-genre"
    assert warning_codes(queued) == [tag_cli.LABEL_NO_GENRE]
    resume(tag_job().job_id)
    assert searcher.asked == [("", "a")]
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC


def test_an_unreadable_registry_warns_and_refuses_only_a_sweep_that_named_a_label(
    cfg, folder, silence, monkeypatch
):
    track(folder, silence, "a")
    path = labels.RegistryStore().path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json", encoding="utf-8")
    code, envelope = drive(["tag", "folder", "--queue-only", str(folder), "--label", LABEL])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-intent-unusable"
    queued = queue(str(folder))
    assert warning_codes(queued) == [tag_cli.LABEL_REGISTRY_UNREAD]


def test_a_sweep_driven_at_its_queue_keeps_the_label_warning_and_never_calls_its_label_unapplied(
    cfg, folder, silence, monkeypatch
):
    """The ``--label`` typed on the queueing call is frozen, so the resume warns nothing new."""
    registered()
    track(folder, silence, "a")
    searcher = bound(monkeypatch, specific_for_a())
    code, settled = drive(["tag", "folder", str(folder), "--label", LABEL])
    assert code == int(ExitCode.OK), settled
    assert settled["data"]["state"] == "succeeded"
    assert warning_codes(settled) == [tag_cli.LABEL_NO_GENRE]
    assert searcher.asked == [("", "a")]


def test_a_label_typed_on_a_resume_is_still_said_to_be_unapplied(cfg, folder, silence, monkeypatch):
    """The ``--job`` path is unchanged by U192: a label typed there is not the sweep's."""
    registered("--genre", GENRE)
    track(folder, silence, "a")
    bound(monkeypatch, specific_for_a())
    drive(["tag", "folder", "--queue-only", str(folder)])
    resumed = resume(tag_job().job_id, "--label", LABEL)
    assert tag_cli.LABEL_ON_RESUME in warning_codes(resumed)


def refusing_writes(monkeypatch) -> None:
    """A file that will not take a genre, a locked file or a read only volume."""
    monkeypatch.setattr(tags, "write_genre", lambda path, genre: False)


def test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged(
    cfg, folder, silence, monkeypatch
):
    registered("--genre", GENRE)
    track(folder, silence, "a")
    bound(monkeypatch, never_searched)
    refusing_writes(monkeypatch)
    drive(["tag", "folder", "--queue-only", str(folder), "--label", LABEL])
    job = tag_job()
    drive(resume_argv(job.job_id))
    assert item_causes(job.job_id) == {"a.flac": tag.UNWRITTEN_REASON}
    assert tags.read_genre_from_file(folder / "a.flac") is None
    claimed = [r for r in artifacts.committed(cfg, job.job_id) if r.get("genre_written")]
    assert claimed == [], "no report says a genre the file does not carry"


def test_a_file_that_will_not_take_a_catalogues_genre_fails_too(folder, silence, monkeypatch):
    path = track(folder, silence, "a")
    refusing_writes(monkeypatch)
    with pytest.raises(CratekitError) as caught:
        tag.tag_one(path, searcher=specific_for_a())
    assert caught.value.cause.reason == tag.UNWRITTEN_REASON
    assert caught.value.cause.detail["source"] == searchers.BEATPORT


def test_an_art_search_for_a_labelled_file_never_offers_the_general_catalogue_its_isrc(
    folder, silence
):
    path = track(folder, silence, "a", label=LABEL, picture=False)
    assert tags.write_tags(path, {"isrc": "ZZTST2600001"})
    offered: list[object] = []
    def published(hit, isrc):
        offered.append(isrc)
        return hit
    searcher = answering({"a": SearchHit(source=searchers.BEATPORT, answers=())})
    tag.tag_one(path, searcher=searcher, published=published, label_genre=seam({LABEL: GENRE}))
    assert offered == [None], "the genre was the label's, so no ISRC is offered for one"
    assert tags.read_genre_from_file(path) == GENRE


def test_a_label_tag_that_could_never_name_a_label_is_searched_and_never_fails(
    cfg, folder, silence, monkeypatch
):
    registered("--genre", GENRE)
    track(folder, silence, "a", label="---")
    searcher = bound(monkeypatch, specific_for_a())
    sweep(str(folder))
    assert searcher.asked == [("", "a")]
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC


def test_files_whose_own_tag_outranked_the_label_are_counted_and_named(
    cfg, folder, silence, monkeypatch
):
    registered("--genre", GENRE)
    track(folder, silence, "a", label="PULS Records")
    track(folder, silence, "b", label="PULS Records")
    track(folder, silence, "c")
    bound(monkeypatch, answering({}))
    _job, resumed = sweep(str(folder), "--label", LABEL)
    tagging = resumed["data"]["progress"]["tagging"]
    assert (tagging["label_tags"], tagging["label_genres"]) == ({"PULS Records": 2}, {LABEL: 1})
    warnings = warned(resumed)
    assert tag_cli.LABEL_TAG_OUTRANKED == "tag-folder-label-tag-outranked"
    assert "2 files were not given PULS's genre" in warnings[tag_cli.LABEL_TAG_OUTRANKED]
    assert "PULS Records on 2" in warnings[tag_cli.LABEL_TAG_OUTRANKED]


def test_a_tag_naming_no_genre_says_nothing_on_a_sweep_given_no_label(
    cfg, folder, silence, monkeypatch
):
    registered("--genre", GENRE)
    track(folder, silence, "a", label="Other Label")
    bound(monkeypatch, specific_for_a())
    _job, resumed = sweep(str(folder))
    assert tag_cli.LABEL_TAG_OUTRANKED not in warning_codes(resumed)


def test_a_label_typed_on_a_resume_is_not_applied_and_says_so(cfg, folder, silence, monkeypatch):
    registered("--genre", GENRE)
    track(folder, silence, "a")
    searcher = bound(monkeypatch, specific_for_a())
    queue(str(folder))
    resumed = resume(tag_job().job_id, "--label", LABEL)
    assert tag_cli.LABEL_ON_RESUME == "tag-folder-label-on-resume"
    assert tag_cli.LABEL_ON_RESUME in warning_codes(resumed)
    assert searcher.asked == [("", "a")]
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC


def test_a_file_its_own_label_answered_for_is_never_named_as_outranked(
    cfg, folder, silence, monkeypatch
):
    registered("--genre", GENRE)
    registered("--genre", "Progressive House", name="Sudbeat")
    track(folder, silence, "a", label="Sudbeat", picture=False)
    bound(monkeypatch, answering({"a": SearchHit(source=searchers.BEATPORT)}))
    _job, resumed = sweep(str(folder), "--label", LABEL)
    tagging = resumed["data"]["progress"]["tagging"]
    assert tags.read_genre_from_file(folder / "a.flac") == "Progressive House"
    assert (tagging["label_genres"], tagging["label_tags"]) == ({"Sudbeat": 1}, {})
    assert tag_cli.LABEL_TAG_OUTRANKED not in warning_codes(resumed)


# 4. A display name two labels share, R-1476


def two_alphas() -> None:
    """Alpha with a genre, and omega renamed onto Alpha's display name with none."""
    registered("--genre", GENRE, name="Alpha")
    registered(name="Omega")
    registry("rename", "omega", "--to", "Alpha")


def test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre(
    cfg, folder, silence, monkeypatch
):
    two_alphas()
    track(folder, silence, "a")
    searcher = bound(monkeypatch, specific_for_a())
    queued = queue(str(folder), "--label", "omega")
    job = tag_job()
    resumed = resume(job.job_id)
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC, "never the other Alpha's genre"
    assert searcher.asked == [("", "a")], "the file was asked of the catalogues"
    tagging = resumed["data"]["progress"]["tagging"]
    assert (tagging["label_genres"], tagging["tagged_by"][tag.LABEL_GENRE]) == ({}, 0)
    warnings = warned(queued)
    assert "Alpha (omega) is registered with no genre" in warnings[tag_cli.LABEL_NO_GENRE]
    assert "crate label registry set 'omega' --genre WORD" in warnings[tag_cli.LABEL_NO_GENRE]
    assert (job.payload["label"], job.payload["label_id"]) == ("Alpha", "omega")


def test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name(
    cfg, folder, silence, monkeypatch
):
    two_alphas()
    track(folder, silence, "a")
    bound(monkeypatch, never_searched)
    job, resumed = sweep(str(folder), "--label", "alpha")
    assert tags.read_genre_from_file(folder / "a.flac") == GENRE
    assert resumed["data"]["progress"]["tagging"]["label_genres"] == {"Alpha": 1}
    assert tag_cli.LABEL_NO_GENRE not in warning_codes(resumed)
    assert (job.payload["label"], job.payload["label_id"]) == ("Alpha", "alpha")


def test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre(
    cfg, folder, silence, monkeypatch
):
    """The same rule for a file's own tag: a name naming two labels settles neither."""
    two_alphas()
    track(folder, silence, "a", label="Alpha")
    track(folder, silence, "b", label="alpha")
    searcher = bound(monkeypatch, specific_for_a())
    _job, resumed = sweep(str(folder))
    assert sorted(searcher.asked) == [("", "a"), ("", "b")]
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC
    assert tags.read_genre_from_file(folder / "b.flac") is None, "the shared name in any case"
    assert resumed["data"]["progress"]["tagging"]["label_tags"] == {"Alpha": 1, "alpha": 1}


def test_a_shared_name_outranking_the_folders_label_is_named_truly(cfg, folder, silence, monkeypatch):
    two_alphas()
    track(folder, silence, "a", label="Alpha")
    track(folder, silence, "b")
    bound(monkeypatch, answering({}))
    _job, resumed = sweep(str(folder), "--label", "alpha")
    assert tags.read_genre_from_file(folder / "b.flac") == GENRE
    assert tags.read_genre_from_file(folder / "a.flac") is None
    warnings = warned(resumed)
    outranked = warnings[tag_cli.LABEL_TAG_OUTRANKED]
    assert "1 file was not given Alpha's genre" in outranked
    assert "names two labels or more" in outranked
    assert "Alpha on 1" in outranked


def test_the_remedy_names_the_label_by_its_identifier(cfg, folder, silence):
    registered()
    track(folder, silence, "a")
    queued = queue(str(folder), "--label", LABEL)
    message = queued["warnings"][0]["message"]
    assert message.startswith(f"{LABEL} is registered with no genre")
    assert "crate label registry set 'puls' --genre WORD" in message


def renamed(label_id: str, name: str) -> None:
    registry("rename", label_id, "--to", name)


def test_a_name_that_is_another_labels_identifier_is_the_label_named_so(
    cfg, folder, silence, monkeypatch
):
    """A tag ``alpha`` is omega's, renamed so, never the label whose identifier is ``alpha``."""
    registered("--genre", GENRE, name="alpha")
    renamed("alpha", "Alpha Recordings")
    registered(name="Omega")
    renamed("omega", "alpha")
    track(folder, silence, "a", label="alpha")
    track(folder, silence, "b", label="Alpha Recordings")
    searcher = bound(monkeypatch, specific_for_a())
    _job, resumed = sweep(str(folder))
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC, "never Alpha Recordings' genre"
    assert tags.read_genre_from_file(folder / "b.flac") == GENRE
    assert searcher.asked == [("", "a")]
    queued = queue(str(folder), "--label", "omega")
    message = queued["warnings"][0]["message"]
    assert "crate label registry set 'omega' --genre WORD" in message


def test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre(
    cfg, folder, silence, monkeypatch
):
    """Xenon called omega carries the genre, omega called Alpha none: a tag ``omega`` is xenon."""
    registered(name="Omega")
    renamed("omega", "Alpha")
    registered("--genre", GENRE, name="Xenon")
    renamed("xenon", "omega")
    track(folder, silence, "a", label="omega")
    bound(monkeypatch, never_searched)
    _job, resumed = sweep(str(folder))
    assert tags.read_genre_from_file(folder / "a.flac") == GENRE
    assert resumed["data"]["progress"]["tagging"]["label_genres"] == {"omega": 1}


def test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it(
    cfg, folder, silence, monkeypatch
):
    registered("--genre", GENRE)
    renamed("puls", "PULS Romania")
    track(folder, silence, "a", label="PULS")
    bound(monkeypatch, never_searched)
    sweep(str(folder))
    assert tags.read_genre_from_file(folder / "a.flac") == GENRE


ALPHAS = {
    "label_genres": {"alpha": {"name": "Alpha", "genre": GENRE}},
    "label_needles": {"alpha": {"name": "Alpha", "needle": "Alpha"},
                      "omega": {"name": "Alpha", "needle": "Alpha"}},
}


def test_the_folders_label_is_answered_by_its_frozen_identifier_whatever_it_is_called():
    alpha = LabelAnswer(label="Alpha", genre=GENRE)
    assert tag_cli._folder_seam({**ALPHAS, "label_id": "alpha"})("Alpha") == alpha
    assert tag_cli._folder_seam({**ALPHAS, "label_id": "omega"})("Alpha") is None
    assert tag_cli._folder_seam({**ALPHAS, "label_id": "gone"})("Alpha") is None


def test_a_sweep_frozen_with_no_identifier_reads_its_label_as_a_name():
    """A job queued by main before this unit froze the name alone."""
    assert tag_cli._folder_seam(ALPHAS) is None
    assert tag_cli._folder_seam({"label_id": "alpha"}) is None


@pytest.mark.parametrize("name", ["Alpha", "ALPHA", " Alpha ", "alpha", "Alpha.", "(Alpha)", "Álpha"])
def test_a_tag_naming_a_display_name_two_labels_share_names_neither(name):
    assert tag_cli._label_seam(ALPHAS)(name) is None


def test_a_tag_is_read_as_a_name_before_an_identifier():
    """An identifier held by a label with no genre is another label's name."""
    payload = {"label_genres": {"x": {"name": "omega", "genre": GENRE}},
               "label_needles": {"x": {"name": "omega", "needle": "omega"},
                                 "omega": {"name": "Alpha", "needle": "Alpha"}}}
    answer = tag_cli._label_seam(payload)
    assert answer("omega") == LabelAnswer(label="omega", genre=GENRE)
    assert answer("x") == LabelAnswer(label="omega", genre=GENRE), "no label is named x"
    assert answer("Alpha") is None


def test_a_tag_names_one_label_by_its_name_its_slug_or_the_name_it_was_registered_under():
    payload = {
        "label_genres": {"some-label": {"name": "Some Label", "genre": GENRE},
                         "puls": {"name": "PULS Romania", "genre": SPECIFIC}},
        "label_needles": {"some-label": {"name": "Some Label", "needle": "Some Label"},
                          "puls": {"name": "PULS Romania", "needle": "PULS"},
                          "other": {"name": "Other", "needle": "Other"}},
    }
    answer = tag_cli._label_seam(payload)
    assert answer("some label") == LabelAnswer(label="Some Label", genre=GENRE)
    assert answer("Some*Label") == LabelAnswer(label="Some Label", genre=GENRE)
    assert answer("PULS") == LabelAnswer(label="PULS Romania", genre=SPECIFIC)
    assert answer("Other") is None
    assert answer("Elsewhere") is None
    assert answer("---") is None


def test_a_job_queued_before_the_needles_resolves_among_its_genres_as_before():
    answer = tag_cli._label_seam({"label_genres": {"alpha": {"name": "Alpha", "genre": GENRE}}})
    assert answer("Alpha") == LabelAnswer(label="Alpha", genre=GENRE)


def test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares():
    """Review round two: the slug step runs only when no label is called the tag."""
    payload = {"label_genres": {"alpha": {"name": "Alpha", "genre": GENRE}},
               "label_needles": {"alpha": {"name": "Alpha", "needle": "Alpha"},
                                 "loud": {"name": "ALPHA!", "needle": "ALPHA!"}}}
    answer = tag_cli._label_seam(payload)
    assert answer("Alpha") == LabelAnswer(label="Alpha", genre=GENRE)
    assert answer("Alpha?") is None, "a slug both names have settles neither"


def test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name(
    cfg, folder, silence, monkeypatch
):
    """A job queued before the identifier was frozen hands its label's name to the engine."""
    registered("--genre", GENRE)
    track(folder, silence, "a")
    bound(monkeypatch, never_searched)
    queue(str(folder), "--label", LABEL)
    job = tag_job()
    frozen = {key: value for key, value in job.payload.items() if key != "label_id"}
    before = dataclasses.replace(job, payload=frozen)
    with jobs.open_store() as store:
        (item,) = jobs.items(store, job.job_id)
    tag_cli.handle(before, item, cfg)
    assert tags.read_genre_from_file(folder / "a.flac") == GENRE
