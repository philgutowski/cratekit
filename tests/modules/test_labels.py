"""U26: label registry, sweeps, import, and harvest.

The brief names six scenarios. Each one has a test below:

1. a sweep's review output is a review-queue item, not a file
2. a label whose crawl surfaces items outside a naive date floor still returns them
3. an unverified catalogue match is dropped and reported, never acquired
4. a tombstoned version is reported suppressed by the sweep
5. a listing longer than one page returns fully
6. the registry survives a label rename without orphaning its state

Scope is most-recent-N plus owned-dedup. A last-pulled year is an audit record
and never a floor (KTD11). Verification drops unconfirmed rather than guessing.
Listing goes through cratekit.acquire.listing. Tombstones are consulted through
cratekit.core.tombstone and the decision store U16 already owns.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.core import config, review, tombstone
from cratekit.core.review import DecisionStore, Queue
from cratekit.sync import artifacts, run, watermarks

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_ROOT = REPO_ROOT / "src"
LABEL_ROOT = SRC_ROOT / "cratekit" / "label"


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    install = tmp_path / "install"
    install.mkdir()
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(install))
    monkeypatch.setenv("CRATEKIT_CONFIG_DIR", str(tmp_path / "cfgdir"))
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(built)
    config.reset_cache()
    return built


class Album:
    """A provider release the listing wrappers can page."""

    def __init__(self, album_id: str, *, year: str, artist: str, title: str, copyright: str = ""):
        self.id = album_id
        self.year = year
        self.artist = artist
        self.title = title
        self.copyright = copyright
        self.tracks = [{"artists": [artist], "title": title}]


class PagedArtist:
    """A provider listing that truncates to one page when not given a limit.

    That is the real client shape: one page, no complaint. A crawl that
    calls this without pagination wrappers will silently lose everything
    after the first 100.
    """

    page_size = 100

    def __init__(self, albums: list[Album]) -> None:
        self._albums = list(albums)

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[Album]:
        size = self.page_size if limit is None else limit
        return self._albums[offset : offset + size]

    def get_ep_singles(self, limit: int | None = None, offset: int = 0) -> list[Album]:
        return []


def _always_confirm(claimed: str, album: Album) -> dict:
    return {
        "verdict": "confirmed",
        "resolved_label": claimed,
        "source": "fixture",
        "notes": "",
    }


def _confirm_named(allowed: set[str]):
    def search(claimed: str, album: Album) -> dict:
        if album.id in allowed:
            return _always_confirm(claimed, album)
        return {
            "verdict": "unconfirmed",
            "resolved_label": "",
            "source": "fixture",
            "notes": "no web match",
        }

    return search


# ═══════════════════════════════════════════════════════════════════════════
# 6. Registry identity survives a rename
# ═══════════════════════════════════════════════════════════════════════════


def test_the_registry_survives_a_label_rename_without_orphaning_its_state(cfg):
    from cratekit.label import marks as label_marks
    from cratekit.label import registry as labels

    store = labels.RegistryStore()
    label_id = store.add("Anjunadeep", match="anjunadeep", seed_artists=["Jody Wisternoff"])
    label_marks.advance(cfg, label_id, year="2024")

    store.rename(label_id, "Anjunadeep Recordings")

    reloaded = store.load()
    entry = reloaded.by_id(label_id)
    assert entry is not None
    assert entry.name == "Anjunadeep Recordings"
    assert entry.label_id == label_id
    assert label_marks.read(cfg, label_id) == "2024"
    assert reloaded.by_name("Anjunadeep") is None
    assert reloaded.by_name("Anjunadeep Recordings").label_id == label_id


def test_adding_the_same_label_again_keeps_its_identifier(cfg):
    from cratekit.label import registry as labels

    store = labels.RegistryStore()
    first = store.add("Colorize")
    second = store.add("Colorize", match="colorize")
    assert first == second
    entry = store.load().by_id(first)
    assert entry.match == "colorize"


# ═══════════════════════════════════════════════════════════════════════════
# 2. Date floor is not scope
# ═══════════════════════════════════════════════════════════════════════════


def test_a_crawl_outside_a_naive_date_floor_still_returns_those_items(cfg):
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    store = labels.RegistryStore()
    label_id = store.add("Sudbeat", match="sudbeat")
    artist = PagedArtist(
        [
            Album("new", year="2026", artist="Hernan Cattaneo", title="New Cut"),
            Album("old", year="2018", artist="Hernan Cattaneo", title="Old Cut"),
        ]
    )
    found = sweep.list_for_label(
        cfg,
        store.load().by_id(label_id),
        artist=artist,
        verify=_always_confirm,
        last_pulled="2024",
    )
    identities = {item.identity for item in found.candidates}
    assert "new" in identities
    assert "old" in identities


# ═══════════════════════════════════════════════════════════════════════════
# 3. Unverified matches are dropped and reported
# ═══════════════════════════════════════════════════════════════════════════


def test_an_unverified_catalogue_match_is_dropped_and_reported_never_acquired(cfg):
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    store = labels.RegistryStore()
    label_id = store.add("All Day I Dream", match="all day i dream")
    artist = PagedArtist(
        [
            Album("keep", year="2026", artist="Lee Burridge", title="Keep"),
            Album("guess", year="2026", artist="Someone Else", title="Guess"),
        ]
    )
    found = sweep.list_for_label(
        cfg,
        store.load().by_id(label_id),
        artist=artist,
        verify=_confirm_named({"keep"}),
    )
    assert [item.identity for item in found.candidates] == ["keep"]
    assert any(drop.identity == "guess" for drop in found.dropped)
    assert all(drop.reason != "confirmed" for drop in found.dropped)


# ═══════════════════════════════════════════════════════════════════════════
# 4. Tombstoned versions are reported suppressed
# ═══════════════════════════════════════════════════════════════════════════


def test_a_tombstoned_version_is_reported_suppressed_by_the_sweep(cfg):
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    store = labels.RegistryStore()
    label_id = store.add("Afterlife", match="afterlife")
    identity = tombstone.version_identity(artist="Anyma", title="Conscience")
    DecisionStore(tombstone.STORE_KEY, cfg).record(
        kind=tombstone.KIND_VERSION,
        identity=identity,
        actor="test",
    )
    artist = PagedArtist(
        [
            Album("dead", year="2026", artist="Anyma", title="Conscience"),
            Album("live", year="2026", artist="Anyma", title="The Light"),
        ]
    )
    found = sweep.list_for_label(
        cfg,
        store.load().by_id(label_id),
        artist=artist,
        verify=_always_confirm,
    )
    assert [item.identity for item in found.candidates] == ["live"]
    assert any(item.identity == "dead" for item in found.suppressed)
    assert all(item.identity != "dead" for item in found.candidates)


# ═══════════════════════════════════════════════════════════════════════════
# 5. Pagination
# ═══════════════════════════════════════════════════════════════════════════


def test_a_listing_longer_than_one_page_returns_fully(cfg):
    from cratekit.label import crawl

    albums = [
        Album(f"a{i}", year="2026", artist="Label Act", title=f"Track {i}")
        for i in range(180)
    ]
    artist = PagedArtist(albums)
    assert len(artist.get_albums()) == 100
    found = crawl.releases(artist)
    assert len(found) == 180
    assert [item.id for item in found] == [f"a{i}" for i in range(180)]


def test_the_sweep_does_not_call_a_provider_listing_directly():
    from tests.test_adapter_listing import direct_listing_calls

    problems: list[str] = []
    for path in sorted(LABEL_ROOT.rglob("*.py")):
        problems.extend(direct_listing_calls(path.read_text(), path.as_posix()))
    assert problems == []


# ═══════════════════════════════════════════════════════════════════════════
# 1. Review output is a queue item, not a file
# ═══════════════════════════════════════════════════════════════════════════


def test_a_sweep_review_output_is_a_review_queue_item_not_a_file(cfg, tmp_path):
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    store = labels.RegistryStore()
    label_id = store.add("Stil Vor Talent", match="stil vor talent")
    artist = PagedArtist(
        [Album("r1", year="2026", artist="Oliver Koletzki", title="First")]
    )
    source = sweep.LabelSource(
        cfg,
        registry=store.load(),
        artists={label_id: artist},
        verify=_always_confirm,
    )
    with review.open_store(cfg) as queue:
        source.process(
            run.Candidate(
                identity="r1",
                recency="2026",
                payload={
                    "artist": "Oliver Koletzki",
                    "title": "First",
                    "label_id": label_id,
                    "label_name": "Stil Vor Talent",
                },
            ),
            artifacts.ArtifactRegistry(cfg),
            "run-labels-1",
            store=queue,
        )
        items = list(review.list_items(queue, queue=Queue.LABEL_RELEASE))
    assert len(items) == 1
    assert items[0].queue == Queue.LABEL_RELEASE
    assert items[0].payload["identity"] == "r1"

    written = [path for path in tmp_path.rglob("*") if path.suffix in {".csv", ".tsv"}]
    assert written == []


def test_the_label_package_does_not_construct_a_csv_writer():
    from tests.test_cli_contract import constructs_a_csv_writer

    for path in sorted(LABEL_ROOT.rglob("*.py")):
        assert not constructs_a_csv_writer(path.read_text()), path


# ═══════════════════════════════════════════════════════════════════════════
# Acquisition set
# ═══════════════════════════════════════════════════════════════════════════


def test_a_sweep_produces_the_same_acquisition_set_as_the_source_algorithm(cfg):
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    albums = [
        Album("a", year="2026", artist="Act", title="A"),
        Album("b", year="2025", artist="Act", title="B"),
        Album("c", year="2024", artist="Act", title="C"),
        Album("d", year="2023", artist="Act", title="D"),
    ]
    store = labels.RegistryStore()
    label_id = store.add("Lost & Found", match="lost and found")
    found = sweep.list_for_label(
        cfg,
        store.load().by_id(label_id),
        artist=PagedArtist(albums),
        verify=_confirm_named({"a", "b", "d"}),
        owned={"b"},
        limit=2,
    )
    # c is unconfirmed. b is owned. Newest remaining, cap 2: a then d.
    assert [item.identity for item in found.candidates] == ["a", "d"]


def test_increment_does_not_use_the_watermark_as_a_date_floor(cfg):
    from cratekit.label import marks as label_marks
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    store = labels.RegistryStore()
    label_id = store.add("Crosstown Rebels", match="crosstown")
    label_marks.advance(cfg, label_id, year="2024")
    artist = PagedArtist(
        [
            Album("new", year="2026", artist="Damian Lazarus", title="New"),
            Album("old", year="2019", artist="Damian Lazarus", title="Old"),
        ]
    )
    source = sweep.LabelSource(
        cfg,
        registry=store.load(),
        artists={label_id: artist},
        verify=_always_confirm,
    )
    marks = watermarks.WatermarkStore(cfg)
    marks.advance("labels", cursor="old", items=1, library_id=cfg.library.volume_id)
    result = run.increment(
        source,
        owned=set(),
        limit=10,
        watermarks=marks,
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id="run-floor",
        staging=Path(cfg.paths.download_staging),
    )
    assert set(result.processed) == {"new", "old"}
    with review.open_store(cfg) as queue:
        items = list(review.list_items(queue, queue=Queue.LABEL_RELEASE))
    assert {item.payload["identity"] for item in items} == {"new", "old"}


# ═══════════════════════════════════════════════════════════════════════════
# Harvest: playlist to labels, imports nothing
# ═══════════════════════════════════════════════════════════════════════════


def test_harvest_offers_verified_labels_and_imports_nothing(cfg, tmp_path):
    from cratekit.label import harvest
    from cratekit.label import registry as labels

    tracks = [
        type("Track", (), {"copyright": "2026 Anjunadeep", "label": None, "id": "t1"})(),
        type("Track", (), {"copyright": "2026 Colorize", "label": None, "id": "t2"})(),
        type("Track", (), {"copyright": "2026 Mystery Distro", "label": None, "id": "t3"})(),
    ]

    def verify_name(name: str) -> dict:
        if name in {"Anjunadeep", "Colorize"}:
            return {"verdict": "confirmed", "resolved_label": name, "notes": ""}
        return {"verdict": "unconfirmed", "resolved_label": "", "notes": "no match"}

    with review.open_store(cfg) as queue:
        report = harvest.from_tracks(
            tracks,
            store=queue,
            verify=verify_name,
            extract=harvest.labels_from_copyright,
        )
        items = list(review.list_items(queue, queue=Queue.LABEL_RELEASE))

    names = {item.payload["name"] for item in items}
    assert names == {"Anjunadeep", "Colorize"}
    assert "Mystery Distro" in {drop.name for drop in report.dropped}
    assert labels.RegistryStore().load().labels == {}
    assert list(tmp_path.rglob("*.flac")) == []
    assert list(tmp_path.rglob("*.xml")) == []


# ═══════════════════════════════════════════════════════════════════════════
# Import is a single-label increment, not a date-floored crawl
# ═══════════════════════════════════════════════════════════════════════════


def test_an_unreadable_intent_file_refuses_rather_than_going_empty(cfg):
    from cratekit.core.cause import CratekitError
    from cratekit.label import registry as labels

    path = config.state_path("label_intent")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(CratekitError) as excinfo:
        labels.RegistryStore().load()
    assert excinfo.value.cause.reason == "label-intent-unusable"


def test_renaming_an_unknown_label_refuses(cfg):
    from cratekit.core.cause import CratekitError
    from cratekit.label import registry as labels

    with pytest.raises(CratekitError) as excinfo:
        labels.RegistryStore().rename("no-such-label", "Other")
    assert excinfo.value.cause.reason == "label-unknown"


def test_harvest_of_an_unreadable_playlist_refuses_and_offers_nothing(cfg):
    from cratekit.core.cause import CratekitError
    from cratekit.label import cli as label_cli

    class Args:
        playlist = "https://example.invalid/playlist"

    class Ctx:
        args = Args()
        entry = type("E", (), {"name": "label.harvest", "handler_key": "label.harvest"})()
        run = type("R", (), {"run_id": "run-h"})()

        def envelope(self, **kwargs):
            raise AssertionError("harvest must refuse before it emits")

    with pytest.raises(CratekitError) as excinfo:
        label_cli.harvest_playlist(Ctx())
    assert excinfo.value.cause.reason == "label-playlist-unreadable"
    with review.open_store(cfg) as queue:
        assert list(review.list_items(queue, queue=Queue.LABEL_RELEASE)) == []


def test_import_one_label_returns_the_unowned_confirmed_set(cfg):
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    store = labels.RegistryStore()
    label_id = store.add("Kompakt", match="kompakt")
    artist = PagedArtist(
        [
            Album("owned", year="2026", artist="WhoMadeWho", title="Owned"),
            Album("fresh", year="2025", artist="WhoMadeWho", title="Fresh"),
        ]
    )
    found = sweep.list_for_label(
        cfg,
        store.load().by_id(label_id),
        artist=PagedArtist(artist._albums),
        verify=_always_confirm,
        owned={"owned"},
    )
    assert [item.identity for item in found.candidates] == ["fresh"]


# ═══════════════════════════════════════════════════════════════════════════
# U52: the catalogue provider seam
#
# The seam is the one place the label package reads a provider through, and no
# shipped build fills it. These four tests hold the two halves of that: the
# refusals a person actually meets today, and the guard that keeps the stand-in
# the suite substitutes from growing a method the protocol never declared.
# ═══════════════════════════════════════════════════════════════════════════


def test_with_no_provider_session_the_catalogue_seam_names_the_credential(cfg):
    """Distinguishable from the no-adapter refusal, because doctor can fix one."""
    from cratekit.core import secrets
    from cratekit.core.cause import CratekitError
    from cratekit.label import catalogue

    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)
    cause = excinfo.value.cause
    assert cause.reason == "credential-missing"
    assert cause.detail["credential"] == str(secrets.Credential.PROVIDER_SESSION)


def test_with_a_session_recorded_the_catalogue_seam_refuses_that_nothing_is_bound(cfg):
    """The credential is real here, recorded through the module that owns it.

    Recorded rather than monkeypatched, because the point of the second refusal
    is that it survives a person doing everything right. The keychain is an
    in-memory dictionary for the whole suite, so this writes the presence index
    the way a login would and reads it back through the shipped function.
    """
    from cratekit.core import secrets
    from cratekit.core.cause import CratekitError
    from cratekit.label import catalogue

    secrets.set_json(secrets.Credential.PROVIDER_SESSION, {"token": "recorded"})
    assert secrets.exists(str(secrets.Credential.PROVIDER_SESSION))

    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)
    cause = excinfo.value.cause
    assert cause.reason == "label-catalogue-unbound"
    assert cause.remediation is not None
    # The words matter as much as the slug. A build with no adapter has not
    # reached a provider at all, so a message about anything being unreachable
    # would send a person to their network over a gap in this software.
    assert "adapter" in cause.message
    assert "unreachable" not in cause.message


def test_the_catalogue_seam_answers_bound_without_reading_a_credential(cfg, monkeypatch):
    """Asked at enqueue, where the answer is still useful, so it must not raise."""
    from cratekit.core import secrets
    from cratekit.label import catalogue

    del cfg

    def _refuse_to_be_asked(name: str) -> bool:
        raise AssertionError(
            f"bound() read the credential {name!r}. It is asked before a person "
            f"commits to the work and answers about this build, not this machine"
        )

    monkeypatch.setattr(secrets, "exists", _refuse_to_be_asked)
    assert catalogue.bound() is False


def test_the_strict_catalogue_raises_on_a_method_outside_the_protocol():
    """A caller cannot even NAME a provider read the seam does not declare."""
    from tests.label_fakes import PROTOCOL_METHODS, StrictCatalogue

    strict = StrictCatalogue()
    for method in sorted(PROTOCOL_METHODS):
        assert callable(getattr(strict, method))
    with pytest.raises(AssertionError) as excinfo:
        strict.delete_playlist
    assert "delete_playlist" in str(excinfo.value)
