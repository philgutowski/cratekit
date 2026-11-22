"""U75: ``crate label approved``, driven through the real dispatcher."""

from __future__ import annotations

import errno
import io
import json
import re
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.acquire import listdoc, match_cli
from cratekit.cli import registry
from cratekit.core import config, review
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.deletion import stores
from cratekit.deletion.library import RemovedRow
from cratekit.label import approved_cli, catalogue, harvest, sweep
from cratekit.sync import run
from tests.cli_drive import drive
from tests.label_fakes import StrictCatalogue, UnreadableCatalogue, catalogue_factory
from tests.test_config import valid_data
from tests.test_label_workers import one_parser as one_parser  # noqa: PLC0414 - fixture

#: What a payload written before R-379 carries where the artist belongs.
ADDRESS = "<provider.artist.Artist object at 0x10b77ec00>"


# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library) -> config.Config:
    built = config.from_dict(valid_data(library, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


class Track:
    """A provider row in the shape the provider reader reads."""

    def __init__(
        self, track_id: str, artist: str, name: str, *, version: str = "", genre: str = ""
    ) -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = ""
        if version:
            self.version = version
        if genre:
            self.genre = genre


def offer(
    items, release_id: str, *, title: str = "Harbour Lights EP", label_id: str = "tide-works",
    label_name: str = "Tide Works", artist: str = ADDRESS,
) -> str:
    payload = {
        "artist": artist, "title": title, "label_id": label_id, "label_name": label_name,
        "identity": release_id,
    }
    candidate = run.Candidate(identity=release_id, recency="2024", payload=payload)
    return sweep.offer_release(items, candidate).item_id


def offered(cfg: config.Config, release_id: str, **fields: str) -> str:
    """One release offered by the sweep's own producer. Returns the item id."""
    with review.open_store(cfg) as items:
        return offer(items, release_id, **fields)


def answered(cfg: config.Config, item_id: str, verdict: review.Verdict) -> None:
    with review.open_store(cfg) as items:
        review.resolve(items, item_id, verdict, actor="suite")


def accepted_raw(
    cfg: config.Config, identity: dict, payload: dict, *, kind: str = sweep.KIND,
    handler_key: str = sweep.HANDLER_KEY,
) -> str:
    """An item offered straight into the label queue, then accepted. Its id."""
    with review.open_store(cfg) as items:
        item = review.offer(
            items, queue=str(review.Queue.LABEL_RELEASE), kind=kind, identity=identity,
            payload=payload, handler_key=handler_key,
        )
        review.resolve(items, item.item_id, review.Verdict.ACCEPTED, actor="suite")
    return item.item_id


def accepted(cfg: config.Config, *release_ids: str, **fields: str) -> str:
    """Each release offered and accepted, in one store session. The last item id."""
    with review.open_store(cfg) as items:
        for release_id in release_ids:
            item_id = offer(items, release_id, **fields)
            review.resolve(items, item_id, review.Verdict.ACCEPTED, actor="suite")
    return item_id


def bind(monkeypatch, fake) -> None:
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))


def approved(*extra: str) -> tuple[int, dict]:
    return drive(["label", "approved", *extra])


def listed(monkeypatch, fake=None, *extra: str) -> dict:
    """Bind ``fake`` (unless None) and run the verb, which must succeed. Its envelope."""
    if fake is not None:
        bind(monkeypatch, fake)
    code, envelope = approved(*extra)
    assert code == int(ExitCode.OK), envelope
    return envelope


def unusable(monkeypatch, fake=None, *extra: str) -> dict:
    """Bind ``fake`` (unless None) and run the verb, which must refuse the list. Its cause."""
    if fake is not None:
        bind(monkeypatch, fake)
    code, envelope = approved(*extra)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-list-unusable"
    return envelope["cause"]


def one_release(cfg, monkeypatch, year: int | None = 2024) -> StrictCatalogue:
    """``r-1`` accepted and its two tracks bound under ``year``. The fake."""
    accepted(cfg, "r-1")
    fake = StrictCatalogue(releases={"r-1": (two_track_release()[0], year)})
    bind(monkeypatch, fake)
    return fake


def listed_one(cfg, monkeypatch, year: int | None = 2024) -> dict:
    one_release(cfg, monkeypatch, year)
    return listed(monkeypatch)


def human(argv: list[str]) -> tuple[int, str]:
    """The DEFAULT output a person reads. ``drive`` always asks for json."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue() + err.getvalue()


def lists_dir(library: Path) -> Path:
    return library.parent / "staging" / "lists"


def owned(library: Path, name: str) -> None:
    (library / "Music" / name).write_bytes(b"")


#: The shape of a list's name: the prefix, then six bytes of digest as hex.
LIST_NAME = re.compile(r"label-approved-[0-9a-f]{12}\.list\.json")


def the_list(folder: Path) -> Path:
    """The ONE list in a folder, found on disk and never derived from the digest."""
    found = sorted(folder.glob("*.list.json"))
    assert len(found) == 1, found
    assert LIST_NAME.fullmatch(found[0].name), found[0].name
    return found[0]


def check(envelope: dict, key: str) -> dict:
    found = [one for one in envelope["data"]["checks"] if one["key"] == f"label.approved.{key}"]
    assert len(found) == 1, (key, envelope["data"]["checks"])
    return found[0]


def two_track_release() -> tuple[list[Track], int]:
    return [Track("301", "Aurora Bloom", "Sun Path"), Track("302", "Nova Reef", "Tide")], 2024


# ── What is read, and what is listed ─────────────────────────────────────────


def test_an_accepted_release_is_listed_and_a_rejected_or_open_one_is_never_read(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-1")
    answered(cfg, offered(cfg, "r-2"), review.Verdict.REJECTED)
    offered(cfg, "r-3")
    fake = StrictCatalogue(
        releases={
            "r-1": two_track_release(), "r-2": ([Track("401", "Mira Vale", "Glass Hour")], 2023),
            "r-3": ([Track("501", "Lumen Drift", "Salt Road")], 2022),
        }
    )
    envelope = listed(monkeypatch, fake)
    assert envelope["outcome"] == "ok"
    assert fake.releases_asked_for == ["r-1"]
    summary = envelope["data"]["summary"]
    expected = the_list(lists_dir(library))
    assert summary["list"] == str(expected)
    assert (summary["accepted"], summary["rejected"], summary["open"]) == (1, 1, 1)
    assert (summary["written"], summary["read"]) == (2, 1)
    body = json.loads(expected.read_text())
    assert body["origin"] == "tidal"
    assert [(t["id"], t["artist"], t["title"]) for t in body["tracks"]] == [
        ("301", "Aurora Bloom", "Sun Path"), ("302", "Nova Reef", "Tide"),
    ]
    assert "1 rejected and 1 not yet answered" in check(envelope, "queue")["detail"]


def test_the_written_list_is_one_the_download_verbs_reader_accepts(cfg, library, monkeypatch):
    envelope = listed_one(cfg, monkeypatch)
    wanted = match_cli.read_list(Path(envelope["data"]["summary"]["list"]))
    assert [(one.ref, one.artist, one.title) for one in wanted] == [
        ("301", "Aurora Bloom", "Sun Path"), ("302", "Nova Reef", "Tide"),
    ]


def test_an_owned_track_is_skipped(cfg, library, monkeypatch):
    owned(library, "Aurora Bloom - Sun Path.flac")
    envelope = listed_one(cfg, monkeypatch)
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["owned"], summary["missing"]) == (1, 1, 1)
    assert listed_ids(envelope) == ["302"]
    assert check(envelope, "owned")["detail"].startswith("1 already in the library")


def test_the_manifest_carries_the_label_the_year_and_the_release(cfg, library, monkeypatch):
    accepted(cfg, "r-1")
    accepted(cfg, "r-2", label_id="glass-bay", label_name="Glass Bay", title="Low Water")
    glass = ([Track("401", "Mira Vale", "Glass Hour")], 2019)
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release(), "r-2": glass}))
    _code, envelope = approved()
    sidecar = json.loads(Path(envelope["data"]["summary"]["manifest"]).read_text())
    rows = sidecar["rows"]
    assert set(rows) == {"301", "302", "401"}
    assert {
        ref: (row["source"], row["label_id"], row["label_name"], row["year"], row["release_id"])
        for ref, row in rows.items()
    } == {
        "301": ("label", "tide-works", "Tide Works", 2024, "r-1"),
        "302": ("label", "tide-works", "Tide Works", 2024, "r-1"),
        "401": ("label", "glass-bay", "Glass Bay", 2019, "r-2"),
    }
    assert rows["401"]["source_ref"] == "r-2"


def test_the_artist_comes_from_the_provider_and_never_from_the_review_payload(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-1", artist=ADDRESS)
    envelope = listed(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))
    summary = envelope["data"]["summary"]
    written = Path(summary["list"]).read_text() + Path(summary["manifest"]).read_text()
    assert "0x10b77ec00" not in written
    assert "object at" not in written
    assert "0x10b77ec00" not in json.dumps(envelope)


def test_the_default_human_output_names_the_list_and_the_next_command(cfg, library, monkeypatch):
    one_release(cfg, monkeypatch)
    code, text = human(["label", "approved"])
    assert code == int(ExitCode.OK), text
    path = the_list(lists_dir(library))
    assert (
        f"[ok  ] label.approved.written: 2 missing track(s) from 1 accepted release(s) "
        f"written to {path}" in text
    )
    assert f"next: crate acquire download {path}" in text


def test_out_names_the_folder_the_list_is_written_into(cfg, library, tmp_path, monkeypatch):
    one_release(cfg, monkeypatch)
    elsewhere = tmp_path / "elsewhere"
    _code, envelope = approved("--out", str(elsewhere))
    assert envelope["data"]["summary"]["list"] == str(the_list(elsewhere))
    assert not lists_dir(library).exists()


# ── A release that cannot be read ────────────────────────────────────────────


def test_a_vanished_release_is_named_and_the_others_still_list(cfg, library, monkeypatch):
    gone_item = accepted(cfg, "r-gone", title="Withdrawn EP")
    envelope = listed_one(cfg, monkeypatch)
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["read"], summary["accepted"]) == (2, 1, 2)
    assert [(one["release_id"], one["item_id"], one["gone"]) for one in summary["failed"]] == [
        ("r-gone", gone_item, True)
    ]
    named_failure = check(envelope, "release.r-gone")
    assert named_failure["status"] == "fail"
    said = named_failure["detail"]
    assert "release r-gone ('Withdrawn EP' on Tide Works) is gone from the provider" in said
    assert f"crate review clear {gone_item}" in named_failure["detail"]
    assert check(envelope, "releases")["status"] == "fail"
    assert check(envelope, "releases")["detail"].startswith("1 accepted release(s) could not")


class OneOutage(StrictCatalogue):
    """Answers every release but one, which fails the way an outage fails."""

    def release_tracks(self, release_id: str):
        if release_id == "r-down":
            self.releases_asked_for.append(release_id)
            raise RuntimeError("the provider timed out")
        return super().release_tracks(release_id)


def test_a_release_the_provider_could_not_answer_for_is_a_retry_and_not_a_revoke(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-down")
    accepted(cfg, "r-1")
    envelope = listed(monkeypatch, OneOutage(releases={"r-1": two_track_release()}))
    failure = check(envelope, "release.r-down")
    assert "could not be read" in failure["detail"]
    assert "RuntimeError: the provider timed out" in failure["detail"]
    assert "run this again once the provider answers" in failure["detail"]
    assert "review clear" not in failure["detail"]
    assert envelope["data"]["summary"]["failed"][0]["gone"] is False


def test_every_release_read_is_said_so(cfg, library, monkeypatch):
    envelope = listed_one(cfg, monkeypatch)
    assert check(envelope, "releases") == {
        "key": "label.approved.releases", "title": "releases", "status": "ok",
        "detail": "every accepted release was read", "remedy": None,
    }
    assert envelope["data"]["summary"]["failed"] == []


def test_no_release_read_is_refused_and_never_a_clean_no_op(cfg, library, monkeypatch):
    accepted(cfg, "r-1", "r-2")
    cause = unusable(monkeypatch, UnreadableCatalogue())
    assert "none of the 2 accepted release(s) could be read" in cause["message"]
    assert [one["release_id"] for one in cause["detail"]["failed"]] == ["r-1", "r-2"]
    assert not lists_dir(library).exists()


def test_nothing_missing_with_a_release_unread_is_refused_too(cfg, library, monkeypatch):
    owned(library, "Aurora Bloom - Sun Path.flac")
    owned(library, "Nova Reef - Tide.flac")
    accepted(cfg, "r-1")
    accepted(cfg, "r-gone")
    cause = unusable(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))
    said = cause["message"]
    assert "nothing is missing from the 1 release(s) that could be read, and 1 could not" in said
    assert not lists_dir(library).exists()


class Expired(StrictCatalogue):
    def release_tracks(self, release_id: str):
        self.releases_asked_for.append(release_id)
        raise refuse(
            "credential-missing", "the stored provider session expired",
            remedy=Remedy.REAUTHENTICATE_PROVIDER, origin=("suite",),
        )


def test_the_seams_own_refusal_passes_through_and_stops_the_run(cfg, library, monkeypatch):
    accepted(cfg, "r-1", "r-2")
    fake = Expired()
    bind(monkeypatch, fake)
    code, envelope = approved()
    assert envelope["cause"]["reason"] == "credential-missing", envelope
    assert code != int(ExitCode.OK)
    assert fake.releases_asked_for == ["r-1"]


def test_an_accepted_item_naming_no_release_is_a_named_failure(cfg, library, monkeypatch):
    stray = accepted_raw(
        cfg, {"imported": "row-9"}, {"title": "No Identifier EP", "label_name": "Tide Works"}
    )
    fake = one_release(cfg, monkeypatch)
    envelope = listed(monkeypatch)
    assert fake.releases_asked_for == ["r-1"]
    failure = check(envelope, f"release.{stray}")
    assert "names no release identifier" in failure["detail"]


def test_an_accepted_harvested_label_shares_the_queue_and_is_not_a_release(
    cfg, library, monkeypatch
):
    """Harvest offers label NAMES into the same queue, under another kind."""
    accepted_raw(
        cfg, {"name": "Tide Works"}, {"name": "Tide Works", "identity": "r-2"},
        kind=harvest.KIND, handler_key="label.harvest",
    )
    accepted(cfg, "r-1")
    glass = ([Track("401", "Mira Vale", "Glass Hour")], 2023)
    fake = StrictCatalogue(releases={"r-1": two_track_release(), "r-2": glass})
    envelope = listed(monkeypatch, fake)
    assert fake.releases_asked_for == ["r-1"]
    assert envelope["data"]["summary"]["accepted"] == 1
    assert check(envelope, "releases")["status"] == "ok"


def test_the_items_identity_names_the_release_and_a_payload_that_disagrees_does_not(
    cfg, library, monkeypatch
):
    accepted_raw(cfg, {"release_id": "r-1"}, {"identity": "r-2", "label_name": "Tide Works"})
    glass = ([Track("401", "Mira Vale", "Glass Hour")], 2023)
    fake = StrictCatalogue(releases={"r-1": two_track_release(), "r-2": glass})
    listed(monkeypatch, fake)
    assert fake.releases_asked_for == ["r-1"]


def test_an_imported_item_is_read_by_the_identifier_its_payload_carries(cfg, library, monkeypatch):
    """``review import`` carries no identity, so the payload's copy is all there is."""
    accepted_raw(
        cfg, {"imported": "row-4"},
        {"identity": "r-1", "label_id": "tide-works", "label_name": "Tide Works"},
    )
    fake = StrictCatalogue(releases={"r-1": two_track_release()})
    envelope = listed(monkeypatch, fake)
    assert fake.releases_asked_for == ["r-1"]
    assert envelope["data"]["summary"]["written"] == 2


# ── Nothing to do ────────────────────────────────────────────────────────────


def test_nothing_accepted_is_a_no_op_that_never_opens_the_catalogue(cfg, library, monkeypatch):
    offered(cfg, "r-3")
    def never(_cfg):
        raise AssertionError("the catalogue was resolved with nothing accepted")
    monkeypatch.setattr(catalogue, "resolve", never)
    code, envelope = approved()
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert check(envelope, "written")["detail"] == "nothing listed: no label release is accepted"
    assert envelope["data"]["summary"]["open"] == 1
    assert envelope["data"]["summary"]["list"] is None
    assert not lists_dir(library).exists()


def test_every_track_owned_is_a_no_op_and_writes_nothing(cfg, library, monkeypatch):
    owned(library, "Aurora Bloom - Sun Path.flac")
    owned(library, "Nova Reef - Tide.flac")
    envelope = listed_one(cfg, monkeypatch)
    assert envelope["outcome"] == "no_op"
    assert check(envelope, "written")["status"] == "info"
    assert "holds every track of the 1 accepted release(s)" in check(envelope, "written")["detail"]
    assert not lists_dir(library).exists()


# ── A second run ─────────────────────────────────────────────────────────────


def test_the_same_work_twice_writes_the_same_file_and_refuses_nothing(cfg, library, monkeypatch):
    one_release(cfg, monkeypatch)
    _code, first = approved()
    before = Path(first["data"]["summary"]["list"]).read_bytes()
    code, second = approved()
    assert code == int(ExitCode.OK), second
    assert second["data"]["summary"]["list"] == first["data"]["summary"]["list"]
    assert Path(second["data"]["summary"]["list"]).read_bytes() == before
    stem = the_list(lists_dir(library)).name.removesuffix(".list.json")
    assert sorted(path.name for path in lists_dir(library).iterdir()) == [
        f"{stem}.list.json", f"{stem}.manifest.json",
    ]


def test_a_track_landed_since_the_last_run_is_left_out_under_a_new_name(cfg, library, monkeypatch):
    one_release(cfg, monkeypatch)
    _code, first = approved()
    owned(library, "Aurora Bloom - Sun Path.flac")
    code, second = approved()
    assert code == int(ExitCode.OK), second
    assert second["data"]["summary"]["list"] != first["data"]["summary"]["list"]
    assert LIST_NAME.fullmatch(Path(second["data"]["summary"]["list"]).name)
    assert len(list(lists_dir(library).glob("*.list.json"))) == 2
    body = json.loads(Path(second["data"]["summary"]["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["302"]


def test_a_file_of_the_lists_name_holding_something_else_is_refused_and_kept(
    cfg, library, monkeypatch
):
    one_release(cfg, monkeypatch)
    # The name is learned by one run, then both files go so the squatter alone holds it.
    _code, first = approved()
    squatter = Path(first["data"]["summary"]["list"])
    Path(first["data"]["summary"]["manifest"]).unlink()
    squatter.write_text("somebody else's list\n")
    unusable(monkeypatch)
    assert squatter.read_text() == "somebody else's list\n"
    assert [path.name for path in lists_dir(library).iterdir()] == [squatter.name]


def test_an_out_that_is_a_file_is_refused(cfg, library, tmp_path, monkeypatch):
    one_release(cfg, monkeypatch)
    in_the_way = tmp_path / "in-the-way"
    in_the_way.write_text("a file\n")
    code, envelope = approved("--out", str(in_the_way))
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-list-unusable"
    assert "is not a folder" in envelope["cause"]["message"]


# ── The other three states, and the same recording twice ─────────────────────


def test_the_same_recording_on_two_releases_is_listed_once_under_the_first(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-single", title="Sun Path")
    accepted(cfg, "r-album", title="Harbour Lights")
    album = [Track("901", "Aurora Bloom", "Sun Path"), Track("902", "Nova Reef", "Tide")]
    single = [Track("301", "Aurora Bloom", "Sun Path")]
    fake = StrictCatalogue(releases={"r-single": (single, 2023), "r-album": (album, 2024)})
    envelope = listed(monkeypatch, fake)
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["duplicate"]) == (2, 1)
    assert listed_ids(envelope) == ["301", "902"]
    sidecar = json.loads(Path(summary["manifest"]).read_text())
    assert sidecar["rows"]["301"]["release_id"] == "r-single"
    assert sidecar["rows"]["301"]["year"] == 2023


def test_a_track_held_in_another_version_is_offered_under_this_verb_and_not_listed(
    cfg, library, monkeypatch
):
    owned(library, "Nova Reef - Tide (Someone Remix).flac")
    envelope = listed_one(cfg, monkeypatch)
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["offered"]) == (1, 1)
    assert listed_ids(envelope) == ["301"]
    with review.open_store(cfg) as items:
        asked = review.list_items(items, handler_key="label.approved").items
    assert len(asked) == 1
    assert asked[0].queue == match_cli.QUEUE


def test_a_track_deleted_on_purpose_is_not_listed(cfg, library, monkeypatch):
    row = RemovedRow(
        content_id="9001", recorded="2026-09-18", sequence=1, size=None, artist="Nova Reef",
        title="Tide",
    )
    stores.record_tombstone(cfg, row, actor="deletion")
    envelope = listed_one(cfg, monkeypatch)
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["suppressed"]) == (1, 1)
    assert listed_ids(envelope) == ["301"]


def test_a_release_with_no_year_is_listed_and_said_to_be_undated(cfg, library, monkeypatch):
    envelope = listed_one(cfg, monkeypatch, None)
    undated = check(envelope, "undated")
    assert undated["status"] == "fail"
    assert "release r-1" in undated["detail"]
    assert envelope["data"]["summary"]["undated"] == ["r-1"]
    sidecar = json.loads(Path(envelope["data"]["summary"]["manifest"]).read_text())
    assert sidecar["rows"]["301"]["year"] is None


def test_a_dated_release_says_every_release_carries_its_year(cfg, library, monkeypatch):
    envelope = listed_one(cfg, monkeypatch)
    assert check(envelope, "undated")["status"] == "ok"
    assert envelope["data"]["summary"]["undated"] == []


def test_a_track_with_no_provider_identifier_is_a_failing_line_and_not_dropped(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-1")
    tracks = [Track("301", "Aurora Bloom", "Sun Path"), Track("", "Nova Reef", "Tide")]
    envelope = listed(monkeypatch, StrictCatalogue(releases={"r-1": (tracks, 2024)}))
    unlisted = check(envelope, "unlisted")
    assert unlisted["status"] == "fail"
    assert unlisted["detail"].startswith("1 missing track(s) carry no provider identifier")
    tide = {"artist": "Nova Reef", "title": "Tide"}
    assert envelope["data"]["summary"]["unlisted_tracks"] == [tide]


def test_missing_tracks_none_of_which_can_be_asked_for_is_refused_and_not_a_no_op(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-1")
    cause = unusable(
        monkeypatch, StrictCatalogue(releases={"r-1": ([Track("", "Nova Reef", "Tide")], 2024)})
    )
    assert "1 missing track(s) and none carries a provider identifier" in (cause["message"])
    assert cause["detail"]["unlisted_tracks"] == [{"artist": "Nova Reef", "title": "Tide"}]
    assert not lists_dir(library).exists()


def test_the_list_name_moves_with_anything_the_emitter_would_write():
    def name(year: int | None, *ids: str, label: str = "Tide Works") -> str:
        body = {"tracks": [{"id": ref, "title": "T", "artist": "A"} for ref in ids]}
        provenance = {
            ref: listdoc.Provenance(source="label", label_name=label, year=year, release_id="r-1")
            for ref in ids
        }
        return approved_cli.list_name(body, provenance)
    assert LIST_NAME.fullmatch(name(2024, "301", "302") + ".list.json")
    assert name(2024, "301", "302") == name(2024, "301", "302")
    assert name(2024, "301", "302") != name(2024, "302", "301")
    assert name(2024, "301", "302") != name(None, "301", "302")
    assert name(2024, "301", "302") != name(2024, "301", "302", label="Glass Bay")


def test_the_verb_declares_what_it_is():
    entry = registry.entry("label.approved")
    assert entry.output_schema == "diagnostic/1"
    assert entry.adjudicates
    assert not entry.destructive
    assert entry.writes == frozenset()
    assert entry.landed


# ── What the unit's review found, each driven red before it was fixed ────────


class Parsing(StrictCatalogue):
    """Fails the way a client fails while parsing a payload it did not expect."""

    def release_tracks(self, release_id: str):
        if release_id == "r-odd":
            self.releases_asked_for.append(release_id)
            raise KeyError("numberOfTracks")
        return super().release_tracks(release_id)


def test_a_lookup_error_that_is_not_the_seams_own_is_never_read_as_a_gone_release(
    cfg, library, monkeypatch
):
    """``KeyError`` is a ``LookupError``. A parse failure is not a withdrawal."""
    accepted(cfg, "r-odd")
    accepted(cfg, "r-1")
    envelope = listed(monkeypatch, Parsing(releases={"r-1": two_track_release()}))
    failure = check(envelope, "release.r-odd")
    assert "is gone from the provider" not in failure["detail"]
    assert "review clear" not in failure["detail"]
    assert envelope["data"]["summary"]["failed"][0]["kind"] == "provider"


def test_the_same_tracks_with_a_corrected_year_take_a_new_name_and_are_not_refused(
    cfg, library, monkeypatch
):
    one_release(cfg, monkeypatch, None)
    _code, first = approved()
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))
    code, second = approved()
    assert code == int(ExitCode.OK), second
    assert second["data"]["summary"]["list"] != first["data"]["summary"]["list"]
    sidecar = json.loads(Path(second["data"]["summary"]["manifest"]).read_text())
    assert sidecar["rows"]["301"]["year"] == 2024


def test_a_folder_the_account_cannot_write_keeps_the_permission_refusal_and_its_path(
    cfg, library, monkeypatch
):
    """A refusal raised FROM a permission error keeps that cause (raised: root defeats chmod)."""
    one_release(cfg, monkeypatch)
    def denied(payload, path):
        raise PermissionError(errno.EACCES, "Permission denied", str(path))
    monkeypatch.setattr(listdoc.config, "atomic_write_bytes", denied)
    code, envelope = approved()
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "path-permission-denied"
    assert str(lists_dir(library)) in envelope["cause"]["detail"]["path"]


def test_a_write_the_disk_refuses_is_the_verbs_refusal_and_not_an_internal_error(
    cfg, library, monkeypatch
):
    one_release(cfg, monkeypatch)
    def full(payload, path):
        raise OSError(errno.ENOSPC, "No space left on device", str(path))
    monkeypatch.setattr(listdoc.config, "atomic_write_bytes", full)
    cause = unusable(monkeypatch)
    assert "No space left on device" in cause["message"]
    assert "name another folder with --out" in json.dumps(cause)


def test_one_unreadable_row_is_reported_and_the_rest_of_the_release_still_lists(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-1")
    tracks, _year = two_track_release()
    tracks.insert(1, Track("399", "", ""))
    envelope = listed(monkeypatch, StrictCatalogue(releases={"r-1": (tracks, 2024)}))
    assert listed_ids(envelope) == ["301", "302"]
    unreadable = check(envelope, "unreadable")
    assert unreadable["status"] == "fail"
    assert unreadable["detail"].startswith("1 track row(s)")
    assert "release r-1" in unreadable["detail"]
    assert envelope["data"]["summary"]["unreadable"] == 1


def test_an_item_naming_no_release_is_told_to_clear_it_and_not_to_wait(cfg, library, monkeypatch):
    stray = accepted_raw(cfg, {"imported": "row-9"}, {"title": "No Identifier EP"})
    envelope = listed_one(cfg, monkeypatch)
    failure = check(envelope, f"release.{stray}")
    assert f"crate review clear {stray}" in failure["detail"]
    assert "once the provider answers" not in failure["detail"]


class Down(StrictCatalogue):
    """A provider that has stopped answering for every release."""

    def release_tracks(self, release_id: str):
        self.releases_asked_for.append(release_id)
        raise ConnectionError("the provider timed out")


def test_a_provider_that_stopped_answering_is_not_asked_about_every_release(
    cfg, library, monkeypatch
):
    accepted(cfg, *(f"r-{number}" for number in range(1, 8)))
    fake = Down()
    bind(monkeypatch, fake)
    code, envelope = approved()
    assert code == int(ExitCode.PRECONDITION), envelope
    assert fake.releases_asked_for == ["r-1", "r-2", "r-3"]
    failed = envelope["cause"]["detail"]["failed"]
    assert [one["kind"] for one in failed] == ["provider"] * 3 + ["not-asked"] * 4


class Flaky(StrictCatalogue):
    """Two failures, an answer, then two more: never three in a row."""

    def release_tracks(self, release_id: str):
        if release_id in {"r-1", "r-2", "r-4", "r-5"}:
            self.releases_asked_for.append(release_id)
            raise ConnectionError("the provider timed out")
        return super().release_tracks(release_id)


def test_an_answer_resets_the_count_so_scattered_failures_never_stop_the_run(
    cfg, library, monkeypatch
):
    accepted(cfg, *(f"r-{number}" for number in range(1, 7)))
    glass = ([Track("601", "Mira Vale", "Glass Hour")], 2020)
    fake = Flaky(releases={"r-3": two_track_release(), "r-6": glass})
    envelope = listed(monkeypatch, fake)
    assert fake.releases_asked_for == ["r-1", "r-2", "r-3", "r-4", "r-5", "r-6"]
    assert envelope["data"]["summary"]["written"] == 3


def test_a_gone_release_does_not_count_towards_an_outage(cfg, library, monkeypatch):
    accepted(cfg, "g-1", "g-2", "g-3", "g-4")
    fake = one_release(cfg, monkeypatch)
    envelope = listed(monkeypatch)
    assert fake.releases_asked_for == ["g-1", "g-2", "g-3", "g-4", "r-1"]
    assert {one["kind"] for one in envelope["data"]["summary"]["failed"]} == {"gone"}


# ── The genre gate, U101: 10 house (no family) and 1 hip hop put hip_hop_rnb under 10% ──

#: How many house releases make one hip hop release out of place on a label.
HOUSE_RELEASES = 10


def house_label(cfg, releases: dict, *, label_id: str = "tide-works", prefix: str = "h") -> None:
    """Ten accepted house releases on one label, one track each."""
    ids = [f"{prefix}-{n}" for n in range(HOUSE_RELEASES)]
    accepted(cfg, *ids, label_id=label_id, label_name=label_id.title())
    for n, release_id in enumerate(ids):
        house = Track(f"{prefix}{n}", f"House Artist {prefix}{n}", "Deep Cut", genre="Deep House")
        releases[release_id] = ([house], 2024)


def held_label(cfg, **fields: str) -> dict:
    """The ten house releases, then hip hop ``r-hh`` accepted on Tide Works. The releases."""
    releases: dict = {}
    house_label(cfg, releases)
    accepted(cfg, "r-hh", **fields)
    releases["r-hh"] = ([Track("901", "Mira Vale", "Corner Talk", genre="Hip Hop")], 2024)
    return releases


def listed_ids(envelope: dict) -> list[str]:
    path = envelope["data"]["summary"]["list"]
    return [t["id"] for t in json.loads(Path(path).read_text())["tracks"]] if path else []


def test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed(
    cfg, library, monkeypatch
):
    fake = StrictCatalogue(releases=held_label(cfg, title="Corner Talk"))
    envelope = listed(monkeypatch, fake)
    assert "r-hh" in fake.releases_asked_for
    assert "901" not in listed_ids(envelope)
    assert len(listed_ids(envelope)) == HOUSE_RELEASES
    held = check(envelope, "held.r-hh")
    assert held["status"] == "info"
    assert "release r-hh ('Corner Talk' on Tide Works) is HELD by the genre gate" in held["detail"]
    assert "'Hip Hop' is the hip_hop_rnb family, 1 of the 11 release(s)" in held["detail"]
    assert "under the 10% share" in held["detail"]
    assert "1 accepted release(s) held by the genre gate" in check(envelope, "held")["detail"]
    assert envelope["data"]["summary"]["held"] == [
        {
            "release_id": "r-hh", "item_id": envelope["data"]["summary"]["held"][0]["item_id"],
            "genre": "Hip Hop", "family": "hip_hop_rnb", "of_family": 1, "classified": 11,
            "share": 0.10,
        }
    ]
    assert check(envelope, "ungated")["status"] == "ok"
    assert "from 10 accepted release(s)" in check(envelope, "written")["detail"]


def test_a_held_release_is_never_offered_for_review(cfg, library, monkeypatch):
    owned(library, "Mira Vale - Corner Talk (Club Mix).flac")
    releases = held_label(cfg)
    envelope = listed(monkeypatch, StrictCatalogue(releases=releases))
    assert envelope["data"]["summary"]["offered"] == 0
    with review.open_store(cfg) as items:
        page = review.list_items(items, queue=None, include_resolved=True, limit=None)
    assert not [one for one in page.items if "Corner Talk" in json.dumps(one.payload)]


def test_a_genre_the_label_makes_enough_of_is_listed(cfg, library, monkeypatch):
    accepted(cfg, "r-1", "r-2", "r-3")
    envelope = listed(monkeypatch, StrictCatalogue(releases={
        "r-1": ([Track("301", "Aurora Bloom", "Sun Path", genre="Deep House")], 2024),
        "r-2": ([Track("302", "Nova Reef", "Tide", genre="Deep House")], 2024),
        "r-3": ([Track("303", "Lumen Drift", "Iron", genre="Hip Hop")], 2024),
    }))
    assert listed_ids(envelope) == ["301", "302", "303"]
    assert check(envelope, "held") == {
        "key": "label.approved.held", "title": "held", "status": "info",
        "detail": "no release was held by the genre gate", "remedy": None,
    }
    assert envelope["data"]["summary"]["held"] == []
    assert check(envelope, "ungated")["detail"] == "every release read was judged by the genre gate"


def test_a_release_with_no_genre_known_is_listed_with_a_failing_line(cfg, library, monkeypatch):
    envelope = listed_one(cfg, monkeypatch)
    assert envelope["outcome"] == "ok"
    assert listed_ids(envelope) == ["301", "302"]
    ungated = check(envelope, "ungated")
    assert ungated["status"] == "fail"
    said = ungated["detail"]
    assert "1 release(s) the genre gate could not judge, so they are listed unjudged" in said
    assert "release r-1 ('Harbour Lights EP' on Tide Works): the catalogue reports no genre" in said
    assert envelope["data"]["summary"]["ungated"] == ["r-1"]


def test_tracks_that_disagree_on_the_genre_are_not_judged_and_are_listed(cfg, library, monkeypatch):
    releases: dict = {}
    house_label(cfg, releases)
    accepted(cfg, "r-mix")
    releases["r-mix"] = ([
        Track("901", "Mira Vale", "Corner Talk", genre="Hip Hop"),
        Track("902", "Mira Vale", "Corner Talk", version="Club Mix", genre="Deep House"),
    ], 2024)
    envelope = listed(monkeypatch, StrictCatalogue(releases=releases))
    assert {"901", "902"} <= set(listed_ids(envelope))
    assert envelope["data"]["summary"]["held"] == []
    ungated = check(envelope, "ungated")
    assert ungated["status"] == "fail"
    assert "its tracks report 'Hip Hop' and 'Deep House'" in ungated["detail"]


def test_one_genre_in_two_cases_is_one_genre_and_is_judged(cfg, library, monkeypatch):
    accepted(cfg, "r-1")
    tracks = [
        Track("301", "Aurora Bloom", "Sun Path", genre="Deep House"),
        Track("302", "Nova Reef", "Tide", genre="deep house"),
    ]
    bind(monkeypatch, StrictCatalogue(releases={"r-1": (tracks, 2024)}))
    _code, envelope = approved()
    assert check(envelope, "ungated")["status"] == "ok"
    assert envelope["data"]["summary"]["ungated"] == []


def test_each_label_is_judged_against_its_own_output(cfg, library, monkeypatch):
    releases = held_label(cfg)
    accepted(cfg, "r-other", label_id="salt-flats", label_name="Salt Flats")
    releases["r-other"] = ([Track("902", "Lumen Drift", "Iron", genre="Hip Hop")], 2024)
    envelope = listed(monkeypatch, StrictCatalogue(releases=releases))
    assert "902" in listed_ids(envelope)
    assert "901" not in listed_ids(envelope)
    assert [one["release_id"] for one in envelope["data"]["summary"]["held"]] == ["r-hh"]


def test_releases_naming_no_label_are_each_judged_alone(cfg, library, monkeypatch):
    releases = {
        f"h-{n}": ([Track(f"h{n}", f"House Artist {n}", "Deep Cut", genre="Deep House")], 2024)
        for n in range(HOUSE_RELEASES)
    }
    accepted(cfg, *releases, label_id="", label_name="")
    accepted(cfg, "r-hh", label_id="", label_name="")
    releases["r-hh"] = ([Track("901", "Mira Vale", "Corner Talk", genre="Hip Hop")], 2024)
    envelope = listed(monkeypatch, StrictCatalogue(releases=releases))
    assert "901" in listed_ids(envelope)
    assert envelope["data"]["summary"]["held"] == []


def test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one(
    cfg, library, monkeypatch
):
    releases: dict = {}
    house_label(cfg, releases)
    for n in range(HOUSE_RELEASES):
        owned(library, f"House Artist h{n} - Deep Cut.flac")
    accepted(cfg, "r-hh", label_id="tide-works", label_name="Tide Works")
    releases["r-hh"] = ([Track("901", "Mira Vale", "Corner Talk", genre="Hip Hop")], 2024)
    envelope = listed(monkeypatch, StrictCatalogue(releases=releases))
    assert envelope["outcome"] == "no_op"
    assert check(envelope, "written")["detail"] == (
        "nothing listed: the library holds every track of the 10 accepted release(s) "
        "the genre gate passed, and 1 more were held by it"
    )
    assert not lists_dir(library).exists()


def test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both(
    cfg, library, monkeypatch
):
    releases: dict = {}
    house_label(cfg, releases)
    for n in range(HOUSE_RELEASES):
        owned(library, f"House Artist h{n} - Deep Cut.flac")
    accepted(cfg, "r-hh", label_id="tide-works", label_name="Tide Works")
    releases["r-hh"] = ([Track("901", "Mira Vale", "Corner Talk", genre="Hip Hop")], 2024)
    accepted(cfg, "r-gone", label_id="salt-flats", label_name="Salt Flats")
    bind(monkeypatch, StrictCatalogue(releases=releases))
    code, envelope = approved()
    assert code == int(ExitCode.PRECONDITION), envelope
    assert (
        "nothing is missing from the 10 release(s) that could be read and passed the "
        "genre gate (1 more held by it), and 1 could not be"
    ) in envelope["cause"]["message"]


def test_the_default_human_output_names_a_held_release(cfg, library, monkeypatch):
    bind(monkeypatch, StrictCatalogue(releases=held_label(cfg, title="Corner Talk")))
    _code, text = human(["label", "approved"])
    assert "release r-hh ('Corner Talk' on Tide Works) is HELD by the genre gate" in text


def test_a_label_with_a_release_unread_this_run_is_not_judged_and_says_why(
    cfg, library, monkeypatch
):
    releases = held_label(cfg)
    accepted(cfg, "r-gone", label_id="tide-works", label_name="Tide Works")
    envelope = listed(monkeypatch, StrictCatalogue(releases=releases))
    assert "901" in listed_ids(envelope)
    assert envelope["data"]["summary"]["held"] == []
    assert "r-hh" in envelope["data"]["summary"]["ungated"]
    assert (
        "another accepted release on its label could not be read, so the label's "
        "share of its genre is not known"
    ) in check(envelope, "ungated")["detail"]


def test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged(
    cfg, library, monkeypatch
):
    releases = held_label(cfg)
    accepted(cfg, "r-gone", label_id="salt-flats", label_name="Salt Flats")
    envelope = listed(monkeypatch, StrictCatalogue(releases=releases))
    assert "901" not in listed_ids(envelope)
    assert [one["release_id"] for one in envelope["data"]["summary"]["held"]] == ["r-hh"]
    assert envelope["data"]["summary"]["ungated"] == []


def test_a_release_with_no_genre_is_not_counted_in_its_labels_share(cfg, library, monkeypatch):
    releases = held_label(cfg)
    accepted(cfg, "r-none", label_id="tide-works", label_name="Tide Works")
    releases["r-none"] = ([Track("902", "Lumen Drift", "Iron")], 2024)
    envelope = listed(monkeypatch, StrictCatalogue(releases=releases))
    assert "902" in listed_ids(envelope)
    assert envelope["data"]["summary"]["ungated"] == ["r-none"]
    assert "1 of the 11 release(s) with a genre" in check(envelope, "held.r-hh")["detail"]
    assert envelope["data"]["summary"]["held"][0]["classified"] == 11


def test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object(cfg, library, monkeypatch):
    releases: dict = {}
    house_label(cfg, releases)
    accepted(cfg, "r-hh")
    row = {"id": "901", "name": "Corner Talk", "artist": {"name": "Mira Vale"}, "genre": "Hip Hop"}
    releases["r-hh"] = ([row], 2024)
    envelope = listed(monkeypatch, StrictCatalogue(releases=releases))
    assert "901" not in listed_ids(envelope)
    assert [one["genre"] for one in envelope["data"]["summary"]["held"]] == ["Hip Hop"]



def test_a_family_exactly_at_the_share_belongs_and_is_listed(cfg, library, monkeypatch):
    """One hip hop release in ten is exactly the 10% share, and only UNDER it drops."""
    releases = {
        f"h-{n}": ([Track(f"h{n}", f"House Artist {n}", "Deep Cut", genre="Deep House")], 2024)
        for n in range(HOUSE_RELEASES - 1)
    }
    accepted(cfg, *releases)
    accepted(cfg, "r-hh")
    releases["r-hh"] = ([Track("901", "Mira Vale", "Corner Talk", genre="Hip Hop")], 2024)
    envelope = listed(monkeypatch, StrictCatalogue(releases=releases))
    assert "901" in listed_ids(envelope)
    assert envelope["data"]["summary"]["held"] == []
