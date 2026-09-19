"""U75: ``crate label approved``, driven through the real dispatcher.

A label sweep offers releases into the review queue and a person accepts or
rejects each. This verb turns the accepted ones into the list document
``acquire download`` reads, through the one emitter U68 landed, with a manifest
carrying the label and the year. The proofs here are that only an ACCEPTED
release is read, that only a MISSING track is written, that a release the
provider no longer has is named while the others still list, that nothing the
review item's payload says about a track reaches the list, and that a person
reading the DEFAULT output sees the path and the next command.

Every release is offered by the sweep's own ``offer_release`` and answered by
the queue's own ``resolve``, never by a row written straight into the store.
Every expected value is a literal taken from the fixtures, never a value the
verb or the emitter produced. D1 applies: nothing here names a real volume, a
real person, a real label or a real track.
"""

from __future__ import annotations

import io
import json
import re
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.acquire import match_cli
from cratekit.core import config, review
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.deletion import stores
from cratekit.deletion.library import RemovedRow
from cratekit.label import approved_cli, catalogue, sweep
from cratekit.sync import run
from tests.cli_drive import drive
from tests.label_fakes import StrictCatalogue, UnreadableCatalogue, catalogue_factory
from tests.test_config import valid_data

#: What a payload written before R-379 carries where the artist belongs.
ADDRESS = "<provider.artist.Artist object at 0x10b77ec00>"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


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

    def __init__(self, track_id: str, artist: str, name: str, *, version: str = "") -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = ""
        if version:
            self.version = version


def offered(
    cfg: config.Config,
    release_id: str,
    *,
    title: str = "Harbour Lights EP",
    label_id: str = "tide-works",
    label_name: str = "Tide Works",
    artist: str = ADDRESS,
) -> str:
    """One release offered by the sweep's own producer. Returns the item id."""
    with review.open_store(cfg) as items:
        item = sweep.offer_release(
            items,
            run.Candidate(
                identity=release_id,
                recency="2024",
                payload={
                    "artist": artist,
                    "title": title,
                    "label_id": label_id,
                    "label_name": label_name,
                    "identity": release_id,
                },
            ),
        )
    return item.item_id


def answered(cfg: config.Config, item_id: str, verdict: review.Verdict) -> None:
    with review.open_store(cfg) as items:
        review.resolve(items, item_id, verdict, actor="suite")


def accepted(cfg: config.Config, release_id: str, **fields: str) -> str:
    item_id = offered(cfg, release_id, **fields)
    answered(cfg, item_id, review.Verdict.ACCEPTED)
    return item_id


def bind(monkeypatch, fake) -> None:
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))


def approved(*extra: str) -> tuple[int, dict]:
    return drive(["label", "approved", *extra])


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
    """The ONE list in a folder, found on disk and never derived from the digest.

    The digest is over everything the emitter writes, so deriving a name here
    would be the module's own recipe copied into its test. What is pinned is
    the shape of the name and that there is exactly one.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# What is read, and what is listed
# ═══════════════════════════════════════════════════════════════════════════


def test_an_accepted_release_is_listed_and_a_rejected_or_open_one_is_never_read(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-1")
    answered(cfg, offered(cfg, "r-2"), review.Verdict.REJECTED)
    offered(cfg, "r-3")
    fake = StrictCatalogue(
        releases={
            "r-1": two_track_release(),
            "r-2": ([Track("401", "Mira Vale", "Glass Hour")], 2023),
            "r-3": ([Track("501", "Lumen Drift", "Salt Road")], 2022),
        }
    )
    bind(monkeypatch, fake)

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
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
        ("301", "Aurora Bloom", "Sun Path"),
        ("302", "Nova Reef", "Tide"),
    ]
    assert "1 rejected and 1 not yet answered" in check(envelope, "queue")["detail"]


def test_the_written_list_is_one_the_download_verbs_reader_accepts(cfg, library, monkeypatch):
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    _code, envelope = approved()

    wanted = match_cli.read_list(Path(envelope["data"]["summary"]["list"]))
    assert [(one.ref, one.artist, one.title) for one in wanted] == [
        ("301", "Aurora Bloom", "Sun Path"),
        ("302", "Nova Reef", "Tide"),
    ]


def test_an_owned_track_is_skipped(cfg, library, monkeypatch):
    owned(library, "Aurora Bloom - Sun Path.flac")
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["owned"], summary["missing"]) == (1, 1, 1)
    body = json.loads(Path(summary["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["302"]
    assert check(envelope, "owned")["detail"].startswith("1 already in the library")


def test_the_manifest_carries_the_label_the_year_and_the_release(cfg, library, monkeypatch):
    accepted(cfg, "r-1")
    accepted(cfg, "r-2", label_id="glass-bay", label_name="Glass Bay", title="Low Water")
    bind(
        monkeypatch,
        StrictCatalogue(
            releases={
                "r-1": two_track_release(),
                "r-2": ([Track("401", "Mira Vale", "Glass Hour")], 2019),
            }
        ),
    )

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
    """R-379: 98 live rows carry an address where the artist belongs."""
    accepted(cfg, "r-1", artist=ADDRESS)
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    _code, envelope = approved()

    summary = envelope["data"]["summary"]
    written = Path(summary["list"]).read_text() + Path(summary["manifest"]).read_text()
    assert "0x10b77ec00" not in written
    assert "object at" not in written
    assert "0x10b77ec00" not in json.dumps(envelope)


def test_the_default_human_output_names_the_list_and_the_next_command(cfg, library, monkeypatch):
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    code, text = human(["label", "approved"])

    assert code == int(ExitCode.OK), text
    path = the_list(lists_dir(library))
    assert (
        f"[ok  ] label.approved.written: 2 missing track(s) from 1 accepted release(s) "
        f"written to {path}" in text
    )
    assert f"next: crate acquire download {path}" in text


def test_out_names_the_folder_the_list_is_written_into(cfg, library, tmp_path, monkeypatch):
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))
    elsewhere = tmp_path / "elsewhere"

    _code, envelope = approved("--out", str(elsewhere))

    assert envelope["data"]["summary"]["list"] == str(the_list(elsewhere))
    assert not lists_dir(library).exists()


# ═══════════════════════════════════════════════════════════════════════════
# A release that cannot be read
# ═══════════════════════════════════════════════════════════════════════════


def test_a_vanished_release_is_named_and_the_others_still_list(cfg, library, monkeypatch):
    gone_item = accepted(cfg, "r-gone", title="Withdrawn EP")
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["read"], summary["accepted"]) == (2, 1, 2)
    assert [(one["release_id"], one["item_id"], one["gone"]) for one in summary["failed"]] == [
        ("r-gone", gone_item, True)
    ]
    named_failure = check(envelope, "release.r-gone")
    assert named_failure["status"] == "fail"
    assert "release r-gone ('Withdrawn EP' on Tide Works) is gone from the provider" in (
        named_failure["detail"]
    )
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
    bind(monkeypatch, OneOutage(releases={"r-1": two_track_release()}))

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    failure = check(envelope, "release.r-down")
    assert "could not be read" in failure["detail"]
    assert "RuntimeError: the provider timed out" in failure["detail"]
    assert "run this again once the provider answers" in failure["detail"]
    assert "review clear" not in failure["detail"]
    assert envelope["data"]["summary"]["failed"][0]["gone"] is False


def test_every_release_read_is_said_so(cfg, library, monkeypatch):
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    _code, envelope = approved()

    assert check(envelope, "releases") == {
        "key": "label.approved.releases",
        "title": "releases",
        "status": "ok",
        "detail": "every accepted release was read",
        "remedy": None,
    }
    assert envelope["data"]["summary"]["failed"] == []


def test_no_release_read_is_refused_and_never_a_clean_no_op(cfg, library, monkeypatch):
    accepted(cfg, "r-1")
    accepted(cfg, "r-2")
    bind(monkeypatch, UnreadableCatalogue())

    code, envelope = approved()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-list-unusable"
    assert "none of the 2 accepted release(s) could be read" in envelope["cause"]["message"]
    assert [one["release_id"] for one in envelope["cause"]["detail"]["failed"]] == ["r-1", "r-2"]
    assert not lists_dir(library).exists()


def test_nothing_missing_with_a_release_unread_is_refused_too(cfg, library, monkeypatch):
    owned(library, "Aurora Bloom - Sun Path.flac")
    owned(library, "Nova Reef - Tide.flac")
    accepted(cfg, "r-1")
    accepted(cfg, "r-gone")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    code, envelope = approved()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-list-unusable"
    assert "nothing is missing from the 1 release(s) that could be read, and 1 could not" in (
        envelope["cause"]["message"]
    )
    assert not lists_dir(library).exists()


class Expired(StrictCatalogue):
    def release_tracks(self, release_id: str):
        self.releases_asked_for.append(release_id)
        raise refuse(
            "credential-missing",
            "the stored provider session expired",
            remedy=Remedy.REAUTHENTICATE_PROVIDER,
            origin=("suite",),
        )


def test_the_seams_own_refusal_passes_through_and_stops_the_run(cfg, library, monkeypatch):
    accepted(cfg, "r-1")
    accepted(cfg, "r-2")
    fake = Expired()
    bind(monkeypatch, fake)

    code, envelope = approved()

    assert envelope["cause"]["reason"] == "credential-missing", envelope
    assert code != int(ExitCode.OK)
    assert fake.releases_asked_for == ["r-1"]


def test_an_accepted_item_naming_no_release_is_a_named_failure(cfg, library, monkeypatch):
    with review.open_store(cfg) as items:
        stray = review.offer(
            items,
            queue=str(review.Queue.LABEL_RELEASE),
            kind=sweep.KIND,
            identity={"imported": "row-9"},
            payload={"title": "No Identifier EP", "label_name": "Tide Works"},
            handler_key=sweep.HANDLER_KEY,
        )
        review.resolve(items, stray.item_id, review.Verdict.ACCEPTED, actor="suite")
    accepted(cfg, "r-1")
    fake = StrictCatalogue(releases={"r-1": two_track_release()})
    bind(monkeypatch, fake)

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    assert fake.releases_asked_for == ["r-1"]
    failure = check(envelope, f"release.{stray.item_id}")
    assert "names no release identifier" in failure["detail"]


def test_an_accepted_harvested_label_shares_the_queue_and_is_not_a_release(
    cfg, library, monkeypatch
):
    """Harvest offers label NAMES into the same queue, under another kind."""
    from cratekit.label import harvest

    with review.open_store(cfg) as items:
        name = review.offer(
            items,
            queue=str(review.Queue.LABEL_RELEASE),
            kind=harvest.KIND,
            identity={"name": "Tide Works"},
            payload={"name": "Tide Works", "identity": "r-2"},
            handler_key="label.harvest",
        )
        review.resolve(items, name.item_id, review.Verdict.ACCEPTED, actor="suite")
    accepted(cfg, "r-1")
    fake = StrictCatalogue(
        releases={"r-1": two_track_release(), "r-2": ([Track("401", "Mira Vale", "Glass Hour")], 2023)}
    )
    bind(monkeypatch, fake)

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    assert fake.releases_asked_for == ["r-1"]
    assert envelope["data"]["summary"]["accepted"] == 1
    assert check(envelope, "releases")["status"] == "ok"


def test_the_items_identity_names_the_release_and_a_payload_that_disagrees_does_not(
    cfg, library, monkeypatch
):
    """Mutation row A8 found nothing holding the order of the two reads."""
    with review.open_store(cfg) as items:
        item = review.offer(
            items,
            queue=str(review.Queue.LABEL_RELEASE),
            kind=sweep.KIND,
            identity={"release_id": "r-1"},
            payload={"identity": "r-2", "label_name": "Tide Works"},
            handler_key=sweep.HANDLER_KEY,
        )
        review.resolve(items, item.item_id, review.Verdict.ACCEPTED, actor="suite")
    fake = StrictCatalogue(
        releases={"r-1": two_track_release(), "r-2": ([Track("401", "Mira Vale", "Glass Hour")], 2023)}
    )
    bind(monkeypatch, fake)

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    assert fake.releases_asked_for == ["r-1"]


def test_an_imported_item_is_read_by_the_identifier_its_payload_carries(
    cfg, library, monkeypatch
):
    """``review import`` carries no identity, so the payload's copy is all there is."""
    with review.open_store(cfg) as items:
        carried = review.offer(
            items,
            queue=str(review.Queue.LABEL_RELEASE),
            kind=sweep.KIND,
            identity={"imported": "row-4"},
            payload={"identity": "r-1", "label_id": "tide-works", "label_name": "Tide Works"},
            handler_key=sweep.HANDLER_KEY,
        )
        review.resolve(items, carried.item_id, review.Verdict.ACCEPTED, actor="suite")
    fake = StrictCatalogue(releases={"r-1": two_track_release()})
    bind(monkeypatch, fake)

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    assert fake.releases_asked_for == ["r-1"]
    assert envelope["data"]["summary"]["written"] == 2


# ═══════════════════════════════════════════════════════════════════════════
# Nothing to do
# ═══════════════════════════════════════════════════════════════════════════


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
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert check(envelope, "written")["status"] == "info"
    assert "holds every track of the 1 accepted release(s)" in check(envelope, "written")["detail"]
    assert not lists_dir(library).exists()


# ═══════════════════════════════════════════════════════════════════════════
# A second run
# ═══════════════════════════════════════════════════════════════════════════


def test_the_same_work_twice_writes_the_same_file_and_refuses_nothing(cfg, library, monkeypatch):
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    _code, first = approved()
    before = Path(first["data"]["summary"]["list"]).read_bytes()
    code, second = approved()

    assert code == int(ExitCode.OK), second
    assert second["data"]["summary"]["list"] == first["data"]["summary"]["list"]
    assert Path(second["data"]["summary"]["list"]).read_bytes() == before
    stem = the_list(lists_dir(library)).name.removesuffix(".list.json")
    assert sorted(path.name for path in lists_dir(library).iterdir()) == [
        f"{stem}.list.json",
        f"{stem}.manifest.json",
    ]


def test_a_track_landed_since_the_last_run_is_left_out_under_a_new_name(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))
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
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))
    # The name is learned by running once, never derived, and both files are
    # then removed so the squatter is the only thing under that name.
    _code, first = approved()
    squatter = Path(first["data"]["summary"]["list"])
    Path(first["data"]["summary"]["manifest"]).unlink()
    squatter.write_text("somebody else's list\n")

    code, envelope = approved()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-list-unusable"
    assert squatter.read_text() == "somebody else's list\n"
    assert [path.name for path in lists_dir(library).iterdir()] == [squatter.name]


def test_an_out_that_is_a_file_is_refused(cfg, library, tmp_path, monkeypatch):
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))
    in_the_way = tmp_path / "in-the-way"
    in_the_way.write_text("a file\n")

    code, envelope = approved("--out", str(in_the_way))

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-list-unusable"
    assert "is not a folder" in envelope["cause"]["message"]


# ═══════════════════════════════════════════════════════════════════════════
# The other three states, and the same recording twice
# ═══════════════════════════════════════════════════════════════════════════


def test_the_same_recording_on_two_releases_is_listed_once_under_the_first(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-single", title="Sun Path")
    accepted(cfg, "r-album", title="Harbour Lights")
    bind(
        monkeypatch,
        StrictCatalogue(
            releases={
                "r-single": ([Track("301", "Aurora Bloom", "Sun Path")], 2023),
                "r-album": (
                    [Track("901", "Aurora Bloom", "Sun Path"), Track("902", "Nova Reef", "Tide")],
                    2024,
                ),
            }
        ),
    )

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["duplicate"]) == (2, 1)
    body = json.loads(Path(summary["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["301", "902"]
    sidecar = json.loads(Path(summary["manifest"]).read_text())
    assert sidecar["rows"]["301"]["release_id"] == "r-single"
    assert sidecar["rows"]["301"]["year"] == 2023


def test_a_track_held_in_another_version_is_offered_under_this_verb_and_not_listed(
    cfg, library, monkeypatch
):
    owned(library, "Nova Reef - Tide (Someone Remix).flac")
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["offered"]) == (1, 1)
    body = json.loads(Path(summary["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["301"]
    with review.open_store(cfg) as items:
        asked = review.list_items(items, handler_key="label.approved").items
    assert len(asked) == 1
    assert asked[0].queue == match_cli.QUEUE


def test_a_track_deleted_on_purpose_is_not_listed(cfg, library, monkeypatch):
    stores.record_tombstone(
        cfg,
        RemovedRow(
            content_id="9001", recorded="2026-09-18", sequence=1, size=None,
            artist="Nova Reef", title="Tide",
        ),
        actor="deletion",
    )
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["suppressed"]) == (1, 1)
    body = json.loads(Path(summary["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["301"]


def test_a_release_with_no_year_is_listed_and_said_to_be_undated(cfg, library, monkeypatch):
    accepted(cfg, "r-1")
    tracks, _year = two_track_release()
    bind(monkeypatch, StrictCatalogue(releases={"r-1": (tracks, None)}))

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    undated = check(envelope, "undated")
    assert undated["status"] == "fail"
    assert "release r-1" in undated["detail"]
    assert envelope["data"]["summary"]["undated"] == ["r-1"]
    sidecar = json.loads(Path(envelope["data"]["summary"]["manifest"]).read_text())
    assert sidecar["rows"]["301"]["year"] is None


def test_a_dated_release_says_every_release_carries_its_year(cfg, library, monkeypatch):
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    _code, envelope = approved()

    assert check(envelope, "undated")["status"] == "ok"
    assert envelope["data"]["summary"]["undated"] == []


def test_a_track_with_no_provider_identifier_is_a_failing_line_and_not_dropped(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-1")
    bind(
        monkeypatch,
        StrictCatalogue(
            releases={
                "r-1": (
                    [Track("301", "Aurora Bloom", "Sun Path"), Track("", "Nova Reef", "Tide")],
                    2024,
                )
            }
        ),
    )

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    unlisted = check(envelope, "unlisted")
    assert unlisted["status"] == "fail"
    assert unlisted["detail"].startswith("1 missing track(s) carry no provider identifier")
    assert envelope["data"]["summary"]["unlisted_tracks"] == [
        {"artist": "Nova Reef", "title": "Tide"}
    ]


def test_the_list_name_moves_with_anything_the_emitter_would_write():
    from cratekit.acquire import listdoc

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
    from cratekit.cli import registry

    entry = registry.entry("label.approved")
    assert entry.output_schema == "diagnostic/1"
    assert entry.adjudicates
    assert not entry.destructive
    assert entry.writes == frozenset()
    assert entry.landed


# ═══════════════════════════════════════════════════════════════════════════
# What the unit's review found, each driven red before it was fixed
# ═══════════════════════════════════════════════════════════════════════════


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
    bind(monkeypatch, Parsing(releases={"r-1": two_track_release()}))

    _code, envelope = approved()

    failure = check(envelope, "release.r-odd")
    assert "is gone from the provider" not in failure["detail"]
    assert "review clear" not in failure["detail"]
    assert envelope["data"]["summary"]["failed"][0]["kind"] == "provider"


def test_the_same_tracks_with_a_corrected_year_take_a_new_name_and_are_not_refused(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-1")
    tracks, _year = two_track_release()
    bind(monkeypatch, StrictCatalogue(releases={"r-1": (tracks, None)}))
    _code, first = approved()

    bind(monkeypatch, StrictCatalogue(releases={"r-1": (tracks, 2024)}))
    code, second = approved()

    assert code == int(ExitCode.OK), second
    assert second["data"]["summary"]["list"] != first["data"]["summary"]["list"]
    sidecar = json.loads(Path(second["data"]["summary"]["manifest"]).read_text())
    assert sidecar["rows"]["301"]["year"] == 2024


def test_a_folder_the_account_cannot_write_keeps_the_permission_refusal_and_its_path(
    cfg, library, tmp_path, monkeypatch
):
    """The cause constructor reclassifies a refusal raised FROM a permission
    error, so this verb's catch must not flatten the better answer."""
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))
    locked = tmp_path / "locked"
    locked.mkdir()
    locked.chmod(0o500)
    try:
        code, envelope = approved("--out", str(locked / "lists"))
    finally:
        locked.chmod(0o700)

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "path-permission-denied"
    assert str(locked) in envelope["cause"]["detail"]["path"]


def test_a_write_the_disk_refuses_is_the_verbs_refusal_and_not_an_internal_error(
    cfg, library, monkeypatch
):
    import errno

    from cratekit.acquire import listdoc

    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    def full(payload, path):
        raise OSError(errno.ENOSPC, "No space left on device", str(path))

    monkeypatch.setattr(listdoc.config, "atomic_write_bytes", full)

    code, envelope = approved()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "label-list-unusable"
    assert "No space left on device" in envelope["cause"]["message"]
    assert "name another folder with --out" in json.dumps(envelope["cause"])


def test_one_unreadable_row_is_reported_and_the_rest_of_the_release_still_lists(
    cfg, library, monkeypatch
):
    accepted(cfg, "r-1")
    bind(
        monkeypatch,
        StrictCatalogue(
            releases={
                "r-1": (
                    [
                        Track("301", "Aurora Bloom", "Sun Path"),
                        Track("399", "", ""),
                        Track("302", "Nova Reef", "Tide"),
                    ],
                    2024,
                )
            }
        ),
    )

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    body = json.loads(Path(envelope["data"]["summary"]["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["301", "302"]
    unreadable = check(envelope, "unreadable")
    assert unreadable["status"] == "fail"
    assert unreadable["detail"].startswith("1 track row(s)")
    assert "release r-1" in unreadable["detail"]
    assert envelope["data"]["summary"]["unreadable"] == 1


def test_an_item_naming_no_release_is_told_to_clear_it_and_not_to_wait(cfg, library, monkeypatch):
    with review.open_store(cfg) as items:
        stray = review.offer(
            items,
            queue=str(review.Queue.LABEL_RELEASE),
            kind=sweep.KIND,
            identity={"imported": "row-9"},
            payload={"title": "No Identifier EP"},
            handler_key=sweep.HANDLER_KEY,
        )
        review.resolve(items, stray.item_id, review.Verdict.ACCEPTED, actor="suite")
    accepted(cfg, "r-1")
    bind(monkeypatch, StrictCatalogue(releases={"r-1": two_track_release()}))

    _code, envelope = approved()

    failure = check(envelope, f"release.{stray.item_id}")
    assert f"crate review clear {stray.item_id}" in failure["detail"]
    assert "once the provider answers" not in failure["detail"]


class Down(StrictCatalogue):
    """A provider that has stopped answering for every release."""

    def release_tracks(self, release_id: str):
        self.releases_asked_for.append(release_id)
        raise ConnectionError("the provider timed out")


def test_a_provider_that_stopped_answering_is_not_asked_about_every_release(
    cfg, library, monkeypatch
):
    for number in range(1, 8):
        accepted(cfg, f"r-{number}")
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
    for number in range(1, 7):
        accepted(cfg, f"r-{number}")
    fake = Flaky(
        releases={
            "r-3": two_track_release(),
            "r-6": ([Track("601", "Mira Vale", "Glass Hour")], 2020),
        }
    )
    bind(monkeypatch, fake)

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    assert fake.releases_asked_for == ["r-1", "r-2", "r-3", "r-4", "r-5", "r-6"]
    assert envelope["data"]["summary"]["written"] == 3


def test_a_gone_release_does_not_count_towards_an_outage(cfg, library, monkeypatch):
    for name in ("g-1", "g-2", "g-3", "g-4"):
        accepted(cfg, name)
    accepted(cfg, "r-1")
    fake = StrictCatalogue(releases={"r-1": two_track_release()})
    bind(monkeypatch, fake)

    code, envelope = approved()

    assert code == int(ExitCode.OK), envelope
    assert fake.releases_asked_for == ["g-1", "g-2", "g-3", "g-4", "r-1"]
    assert {one["kind"] for one in envelope["data"]["summary"]["failed"]} == {"gone"}
