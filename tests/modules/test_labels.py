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


class ProviderArtist:
    """The real client shape: album.artist is an object with a name, not a string.

    ``str`` of a tidalapi Artist is a memory address. A stand-in that
    stringifies to the name would hide the defect the live sweep wrote into
    98 review rows.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"<tidalapi.artist.Artist object at {hex(id(self))}>"


class Album:
    """A provider release the listing wrappers can page."""

    def __init__(self, album_id: str, *, year: str, artist: object, title: str, copyright: str = ""):
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


def test_the_registry_records_an_id_seed(cfg):
    del cfg
    from cratekit.label import registry as labels

    store = labels.RegistryStore()
    label_id = store.add("Harbour Lights", seed_artists=["id:99"])
    entry = store.load().by_id(label_id)
    assert entry is not None
    assert entry.seed_artists == ("id:99",)


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


def test_an_offered_release_records_the_artist_name_not_the_provider_object(cfg):
    """The live sweep stored str(album.artist), which is a memory address.

    Identity, label and title were correct. A stand-in whose str is the name
    would hide it, so this one stringifies the way the client does.
    """
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    credited = ProviderArtist("Oliver Koletzki")
    assert "object at 0x" in str(credited)
    store = labels.RegistryStore()
    label_id = store.add("Stil Vor Talent", match="stil vor talent")
    artist = PagedArtist(
        [Album("r1", year="2026", artist=credited, title="First")]
    )
    found = sweep.list_for_label(
        cfg,
        store.load().by_id(label_id),
        artist=artist,
        verify=_always_confirm,
    )
    assert len(found.candidates) == 1
    payload = found.candidates[0].payload
    assert payload["artist"] == "Oliver Koletzki"
    assert "object at 0x" not in payload["artist"]
    assert payload["title"] == "First"

    with review.open_store(cfg) as queue:
        item = sweep.offer_release(queue, found.candidates[0])
        stored = item.payload["artist"]
    assert stored == "Oliver Koletzki"
    assert "object at 0x" not in stored


def test_a_string_artist_is_still_recorded_as_the_string(cfg):
    """The suite's stand-ins pass a string, and that spelling must keep working."""
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    store = labels.RegistryStore()
    label_id = store.add("Sudbeat", match="sudbeat")
    found = sweep.list_for_label(
        cfg,
        store.load().by_id(label_id),
        artist=PagedArtist(
            [Album("r1", year="2026", artist="Hernan Cattaneo", title="New Cut")]
        ),
        verify=_always_confirm,
    )
    assert found.candidates[0].payload["artist"] == "Hernan Cattaneo"


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


def test_an_owned_newest_release_does_not_hide_an_older_unowned_one(cfg):
    """R-137, driven through ``LabelSource.list_recent`` and the increment.

    The source used to take its newest N before anything asked about ownership,
    and the increment's scope dropped the owned ones from that already sliced
    list. A label whose newest release was held then offered nothing at a limit
    of one, over an older release the library did not have. The owned identities
    now reach the listing, so they are dropped before the cap and not after it.
    """
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    store = labels.RegistryStore()
    label_id = store.add("Kompakt", match="kompakt")
    owned = {"new"}
    source = sweep.LabelSource(
        cfg,
        registry=store.load(),
        artists={
            label_id: PagedArtist(
                [
                    Album("new", year="2026", artist="WhoMadeWho", title="New"),
                    Album("old", year="2025", artist="WhoMadeWho", title="Old"),
                ]
            )
        },
        verify=_always_confirm,
        owned=owned,
    )
    result = run.increment(
        source,
        owned=owned,
        limit=1,
        watermarks=watermarks.WatermarkStore(cfg),
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id="run-owned-newest",
        staging=Path(cfg.paths.download_staging),
    )
    assert list(result.processed) == ["old"]


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


class HarvestCtx:
    """A context for the two branches an UNBOUND build must refuse on.

    ``envelope`` raises, which is what the test it replaces used, and it is kept
    for exactly the two cases where the property still holds: a build with no
    catalogue adapter never reaches an emit, so a call that emitted here has
    resolved something it could not have. The branches that DO emit are driven
    through the real dispatcher in ``tests/test_label_workers.py`` instead,
    because a context whose envelope raises cannot describe a verb that succeeds.
    """

    def __init__(self, playlist: str = "https://example.invalid/playlist") -> None:
        self.args = type("Args", (), {"playlist": playlist})()
        self.entry = type(
            "E", (), {"name": "label.harvest", "handler_key": "label.harvest"}
        )()
        self.run = type("R", (), {"run_id": "run-h"})()

    def envelope(self, **kwargs):
        raise AssertionError(
            "a build with no catalogue adapter emitted a review set, so it "
            "harvested a playlist through a seam nothing fills"
        )


def _adapter_absent(monkeypatch):
    """Make the catalogue adapter fail to import, the one build ``label-catalogue-unbound``
    still describes after U62. A ``None`` in ``sys.modules`` is what Python itself
    reads as a module that cannot be imported."""
    import sys

    monkeypatch.setitem(sys.modules, "cratekit.label.tidal_catalogue", None)


def test_harvest_on_a_build_with_no_adapter_refuses_that_nothing_is_bound(cfg, monkeypatch):
    """R14, and the false statement U52 removed.

    The old refusal told a person their playlist could not be listed, on every
    call, having contacted nothing at all. That is a refusal whose stated cause
    is false, and it sends somebody to check a playlist that is fine. The
    message assertion is the whole point rather than a nicety: the slug and the
    sentence have to agree about which of the two failed. Since U62 an adapter
    ships, so the build without one is made here by failing its import.
    """
    from cratekit.core import secrets
    from cratekit.core.cause import CratekitError
    from cratekit.label import cli as label_cli

    secrets.set_json(secrets.Credential.PROVIDER_SESSION, {"token": "recorded"})
    _adapter_absent(monkeypatch)

    with pytest.raises(CratekitError) as excinfo:
        label_cli.harvest_playlist(HarvestCtx())
    cause = excinfo.value.cause
    assert cause.reason == "label-catalogue-unbound"
    assert cause.reason != "label-playlist-unreadable"
    assert "adapter" in cause.message
    for blamed in ("could not be listed", "could not be read", "unreachable"):
        assert blamed not in cause.message, cause.message
    # The half the replaced test protected, kept unweakened: a refusal offers
    # nothing, so nobody is left with review items over work that never ran.
    with review.open_store(cfg) as queue:
        assert list(review.list_items(queue, queue=Queue.LABEL_RELEASE)) == []


def test_harvest_with_no_provider_session_refuses_the_credential_instead(cfg):
    """The other refusal a shipped build gives, and it is a different act to fix.

    A missing credential is the person's to undo and doctor already says how; a
    missing adapter is this build's own limitation and authenticating again
    would not move it. Harvest reaches both through one seam, so the pair is
    asserted here rather than only at ``catalogue.resolve``.
    """
    from cratekit.core.cause import CratekitError
    from cratekit.label import cli as label_cli

    with pytest.raises(CratekitError) as excinfo:
        label_cli.harvest_playlist(HarvestCtx())
    assert excinfo.value.cause.reason == "credential-missing"
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


def test_with_a_session_recorded_and_no_adapter_the_seam_refuses_that_nothing_is_bound(
    cfg, monkeypatch
):
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
    _adapter_absent(monkeypatch)

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
    """Asked at enqueue, where the answer is still useful, so it must not raise.

    Both answers are driven. The shipped build imports its adapter and says so,
    and a build whose adapter does not import says the opposite, so the answer
    is read off the build rather than written down as a constant.
    """
    from cratekit.core import secrets
    from cratekit.label import catalogue

    del cfg

    def _refuse_to_be_asked(name: str) -> bool:
        raise AssertionError(
            f"bound() read the credential {name!r}. It is asked before a person "
            f"commits to the work and answers about this build, not this machine"
        )

    monkeypatch.setattr(secrets, "exists", _refuse_to_be_asked)
    assert catalogue.bound() is True
    _adapter_absent(monkeypatch)
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


# ═══════════════════════════════════════════════════════════════════════════
# U52 / R-135: a catalogue that could not be read is not a catalogue with
# nothing in it.
#
# The pair below is the shape the watermark-as-date-floor note describes. The
# outcome tests are named after the mechanism, and the adversarial one,
# ``test_one_working_listing_with_no_releases_still_reports_empty``, is the test
# a literal reading of "an empty listing must raise" would turn red. An
# exhausted crawl is genuinely empty and has to stay that way, or every quiet
# label becomes an error and R-135 is traded for its mirror image.
# ═══════════════════════════════════════════════════════════════════════════


class UnpageableArtist:
    """A listing method that exists and refuses pagination arguments.

    The client shape ``listing.ListingNotPaginated`` is written for: a version
    that dropped the ``limit`` and ``offset`` keywords. The wrapper raises rather
    than taking the one page it could serve, and this is the object that drives
    it out of a crawl.
    """

    def get_albums(self):
        return []


class RaisingArtist:
    """A listing method that pages correctly and fails at the provider.

    The other half of the crawl's failure surface. ``listing.fetch_with_retry``
    re-raises this exception once its retries are spent, so what reaches the
    sweep is the PROVIDER's own type rather than anything this codebase defines.
    """

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[Album]:
        del limit, offset
        raise RuntimeError("provider 503")


def _impatient_crawl(monkeypatch) -> None:
    """Run the real crawl with its retry backoff collapsed, and nothing else.

    ``listing.fetch_with_retry`` retries ANY exception, deliberately and for a
    reason its own docstring gives, and its ladder sleeps thirty one real
    seconds before re-raising. That includes the ``ListingNotPaginated`` a method
    that cannot page raises, which is never going to succeed on attempt five.
    ``list_for_label`` exposes no seam to shorten the ladder and should not grow
    one for a test.

    So the retry COUNT is shortened here and nothing else is substituted. The
    pagination wrapper, the exception types and the conversion under test all run
    exactly as shipped, which is the difference between shortening a timer and
    replacing the mechanism.
    """
    from cratekit.label import crawl

    real = crawl.releases

    def impatient(artist, **kwargs):
        kwargs.setdefault("max_retries", 0)
        return real(artist, **kwargs)

    monkeypatch.setattr(crawl, "releases", impatient)


class SilentArtist:
    """An artist object exposing neither listing method the crawl tries.

    ``listing.artist_releases`` skips a missing method with a ``continue``, so
    this object produces an empty list from a catalogue that was never read.
    That is the R-135 producer this unit closes, and the empty list it still
    produces one layer down is asserted below rather than assumed.
    """


class AlbumsOnlyArtist:
    """ONE working listing method over a catalogue that really has nothing.

    The case that must keep reporting empty. It is the reason the fix is a check
    on the artist object and on the crawl's exceptions, and not a rule that an
    empty release list is an error.
    """

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[Album]:
        del limit, offset
        return []


def _label_source(cfg, name: str, **kwargs):
    """One registered favourite label and a ``LabelSource`` over it."""
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    store = labels.RegistryStore()
    label_id = store.add(name, match=name.lower())
    source = sweep.LabelSource(cfg, registry=store.load(), **kwargs)
    return label_id, source


def _increment(cfg, source):
    return run.increment(
        source,
        owned=set(),
        limit=10,
        watermarks=watermarks.WatermarkStore(cfg),
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id="run-unreadable",
        staging=Path(cfg.paths.download_staging),
    )


def test_a_listing_that_cannot_be_paged_raises_instead_of_reporting_empty(
    cfg, monkeypatch
):
    """R-135. The crawl's own exception becomes a LookupFailure, cause intact."""
    from cratekit.acquire import listing
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    _impatient_crawl(monkeypatch)
    store = labels.RegistryStore()
    label_id = store.add("Diynamic", match="diynamic")

    with pytest.raises(run.LookupFailure) as excinfo:
        sweep.list_for_label(
            cfg,
            store.load().by_id(label_id),
            artist=UnpageableArtist(),
            verify=_always_confirm,
        )

    assert "Diynamic" in str(excinfo.value)
    # The original is reachable rather than swallowed, so a person debugging
    # gets the client's own words and not only this layer's summary.
    cause = excinfo.value.__cause__
    assert isinstance(cause, listing.ListingNotPaginated)
    assert isinstance(cause.__cause__, TypeError)


def test_a_provider_error_out_of_the_crawl_is_not_an_empty_catalogue(cfg, monkeypatch):
    """The wrap is not narrowed to the one exception type this layer knows.

    ``ListingNotPaginated`` is Cratekit's own, and it is the exception a reader
    of ``listing`` notices first. The one that actually reaches a person is the
    PROVIDER's, re-raised by ``fetch_with_retry`` once the ladder is spent, and
    its type is whatever the installed client version raises. A conversion that
    only knew the first would report an unreadable catalogue as empty.
    """
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    _impatient_crawl(monkeypatch)
    store = labels.RegistryStore()
    label_id = store.add("Innervisions", match="innervisions")

    with pytest.raises(run.LookupFailure) as excinfo:
        sweep.list_for_label(
            cfg,
            store.load().by_id(label_id),
            artist=RaisingArtist(),
            verify=_always_confirm,
        )

    assert isinstance(excinfo.value.__cause__, RuntimeError)
    assert "503" in str(excinfo.value.__cause__)


def test_an_artist_exposing_no_listing_method_raises_rather_than_crawling_nothing(cfg):
    """The producer is one layer down, and this pins BOTH halves of it."""
    from cratekit.label import crawl, sweep
    from cratekit.label import registry as labels

    silent = SilentArtist()
    # The wrapper's silence is the thing being closed, so it is asserted rather
    # than described. It skips each missing method and returns an empty list from
    # an object it never read.
    assert crawl.releases(silent) == []

    store = labels.RegistryStore()
    label_id = store.add("Rekids", match="rekids")
    with pytest.raises(run.LookupFailure) as excinfo:
        sweep.list_for_label(
            cfg,
            store.load().by_id(label_id),
            artist=silent,
            verify=_always_confirm,
        )
    message = str(excinfo.value)
    assert "Rekids" in message
    for method in crawl.LISTING_METHODS:
        assert method in message


def test_one_working_listing_with_no_releases_still_reports_empty(cfg):
    """The adversarial half. A quiet label must not become an error.

    ``AlbumsOnlyArtist`` exposes one method the crawl can page and it answers
    with nothing, which is an exhausted crawl rather than an unread one. A fix
    that raised on an empty release list would pass every test above and turn
    this one red, which is the whole reason it is here.
    """
    label_id, source = _label_source(
        cfg,
        "Quiet Imprint",
        artists={},
        verify=_always_confirm,
    )
    source.artists = {label_id: AlbumsOnlyArtist()}

    result = _increment(cfg, source)

    assert result.shortfall == "empty"
    assert result.processed == ()


def test_an_unreadable_listing_stops_the_increment_at_the_lookup(cfg, monkeypatch):
    """Named where the run stopped, not merely that nothing came out of it."""
    from cratekit.core.cause import CratekitError

    _impatient_crawl(monkeypatch)
    label_id, source = _label_source(
        cfg,
        "Hotflush",
        artists={},
        verify=_always_confirm,
    )
    source.artists = {label_id: RaisingArtist()}

    with pytest.raises(CratekitError) as excinfo:
        _increment(cfg, source)

    cause = excinfo.value.cause
    assert cause.reason == "sync-source-lookups-failed"
    assert cause.detail["source_id"] == "labels"
    # The refusal has to say a listing failed rather than that a catalogue was
    # empty, because those two send a person to different places.
    assert "empty" not in cause.message or "not a verified empty" in cause.message


def test_a_label_the_catalogue_cannot_resolve_stops_the_increment(cfg):
    """The path ``list_for_label`` never sees, driven end to end.

    ``LabelSource.list_recent`` resolves the artist object BEFORE
    ``list_for_label`` is reached, so a fix that lived only in the checking
    function would leave this label silently skipped and the run reported empty.
    ``UnreadableCatalogue`` raises where the protocol says it must.
    """
    from cratekit.core.cause import CratekitError
    from tests.label_fakes import UnreadableCatalogue

    catalogue = UnreadableCatalogue()
    label_id, source = _label_source(cfg, "Ostgut Ton", catalogue=catalogue)

    with pytest.raises(CratekitError) as excinfo:
        _increment(cfg, source)

    assert excinfo.value.cause.reason == "sync-source-lookups-failed"
    # The catalogue was genuinely asked, so the refusal is about a failed read
    # and not about a label that was never looked up.
    assert catalogue.asked_for == [label_id]


def test_a_registered_label_with_no_artist_object_refuses_rather_than_skipping(cfg):
    """The bare ``continue`` this unit removed, asserted as gone.

    A favourite label the source cannot get an artist object for was skipped
    silently, so a registry of five labels and five missing objects produced a
    sweep that reported it had looked and found nothing new.
    """
    from cratekit.core.cause import CratekitError

    _label_source_id, source = _label_source(
        cfg,
        "Life and Death",
        artists={},
        verify=_always_confirm,
    )

    with pytest.raises(CratekitError) as excinfo:
        _increment(cfg, source)

    assert excinfo.value.cause.reason == "sync-source-lookups-failed"


def test_the_missing_artist_refusal_names_the_missing_object_not_the_listing(cfg):
    """REMOVE EACH GUARD LAYER ALONE, and this is the layer the test above cannot see.

    A source that answered ``None`` for the missing artist object would still
    refuse, one layer down: ``_crawl_or_refuse`` finds no listing method on
    ``None`` and raises for that. So the test above passes with the guard in
    ``_artist_for`` deleted, and a guard covered by another guard is a guard
    nothing covers. The two refusals send a person to different places, a
    catalogue that never produced an object against an object that cannot be
    paged, so the sentence is what distinguishes them and the sentence is what
    is pinned.
    """
    _label_source_id, source = _label_source(
        cfg,
        "Life and Death",
        artists={},
        verify=_always_confirm,
    )

    with pytest.raises(run.LookupFailure) as excinfo:
        source.list_recent(10)

    said = str(excinfo.value)
    assert "no catalogue object was available" in said, said
    assert "Life and Death" in said, said


def test_a_source_with_neither_verifier_nor_catalogue_refuses_rather_than_confirming_nothing(
    cfg,
):
    """The verifier's own missing-object case, which the docstring names and no test drove.

    A source built with neither piece cannot confirm anything, and a stub that
    answered "unconfirmed" for every release would drop them all and hand the
    increment an empty result over a catalogue it read in full. That is the
    absence-as-evidence shape in one more place, and it is a lookup failure
    rather than a sweep that found nothing.
    """
    from cratekit.label import registry as labels

    _label_source_id, source = _label_source(
        cfg,
        "Life and Death",
        artists={
            labels.slug("Life and Death"): PagedArtist(
                [Album("a", year="2026", artist="X", title="A")]
            )
        },
    )

    with pytest.raises(run.LookupFailure) as excinfo:
        source.list_recent(10)

    assert "neither a verification callable nor a catalogue" in str(excinfo.value)
    assert source.dropped == ()


def test_a_source_over_an_empty_registry_lists_nothing_rather_than_refusing_its_verifier(cfg):
    """A no-op stays a no-op: nothing to confirm means no way to confirm is needed."""
    from cratekit.label import registry as labels
    from cratekit.label import sweep

    source = sweep.LabelSource(cfg, registry=labels.Registry(labels={}))

    assert source.list_recent(10) == []
    assert source.read == 0


class ProxyThatFetchesOnAttributeAccess:
    """An artist object whose every attribute read goes to a provider that is down."""

    def __getattr__(self, name: str):
        raise ConnectionError(f"the provider did not answer for {name!r}")


def test_an_artist_object_that_raises_on_inspection_is_a_lookup_failure_not_a_defect(cfg):
    """The listing probe sits inside the boundary, as the listing itself does.

    ``crawl.can_list`` reads attributes off the artist object, and an adapter's
    artist may fetch on attribute access. Outside the ``try`` the provider's
    own error bypassed the increment's conversion and failed the item as an
    internal error telling the person to file a defect over an outage.
    """
    from cratekit.core.cause import CratekitError

    _label_source_id, source = _label_source(
        cfg,
        "Life and Death",
        artists={},
        verify=_always_confirm,
    )
    source.artists = {_label_source_id: ProxyThatFetchesOnAttributeAccess()}

    with pytest.raises(CratekitError) as excinfo:
        _increment(cfg, source)

    assert excinfo.value.cause.reason == "sync-source-lookups-failed"
    assert "ConnectionError" in excinfo.value.cause.message


def test_a_refusal_raised_mid_crawl_passes_through_the_listing_boundary_unchanged(cfg):
    """The crawl's boundary keeps the rule the verifier's states.

    An adapter that discovers mid page that the stored session expired refuses
    ``credential-missing``, which names an act the person can take. Wrapped
    into a lookup failure it would have become "retry when the provider is
    reachable".
    """
    from cratekit.core.cause import CratekitError, refuse

    class RefusingArtist:
        def get_albums(self, limit=None, offset=0):
            del limit, offset
            raise refuse("credential-missing", "the session expired mid page", origin=("tests",))

        def get_ep_singles(self, limit=None, offset=0):
            del limit, offset
            return []

    _label_source_id, source = _label_source(
        cfg,
        "Life and Death",
        artists={},
        verify=_always_confirm,
    )
    source.artists = {_label_source_id: RefusingArtist()}

    with pytest.raises(CratekitError) as excinfo:
        _increment(cfg, source)

    assert excinfo.value.cause.reason == "credential-missing"


def test_the_crawl_probes_exactly_the_methods_the_listing_reads_by_default():
    from cratekit.acquire import listing
    from cratekit.label import crawl

    assert crawl.LISTING_METHODS == listing.RELEASE_METHODS == ("get_albums", "get_ep_singles")


def test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from():
    """R-704. The sweep asks the error and every ``raise X from`` behind it.

    A client that wraps the provider's answer still carries it, so a wrapped
    ``TooManyRequests`` is a rate limit. An implicit context is read only for
    a structured 429 status, never for its type, and an error that is not a
    rate limit is not one.
    """
    from tidalapi.exceptions import TooManyRequests

    from cratekit.label import sweep

    limit = TooManyRequests("Album unavailable")
    assert sweep._lookup_failure("m", limit).rate_limited is True

    wrapped = RuntimeError("the client gave up")
    wrapped.__cause__ = limit
    assert sweep._lookup_failure("m", wrapped).rate_limited is True

    assert sweep._lookup_failure("m", RuntimeError("provider 503")).rate_limited is False

    # The client reads a 429's body as JSON before it builds its own error, so
    # a gateway's non JSON 429 arrives as a decode error raised while handling
    # it. The context counts because it carries the status itself.
    # Driven through the client's own translation rather than built by hand.
    import requests
    from tidalapi.exceptions import http_error_to_tidal_error

    def translated(status: int) -> BaseException:
        answered = requests.Response()
        answered.status_code = status
        answered._content = b"<html>slow down</html>"
        try:
            try:
                raise requests.HTTPError(f"{status} Client Error", response=answered)
            except requests.HTTPError as http:
                http_error_to_tidal_error(http)
        except Exception as undecoded:  # noqa: BLE001 - the error under test
            return undecoded
        raise AssertionError("the client read a non JSON body as JSON")

    assert sweep._lookup_failure("m", translated(429)).rate_limited is True
    assert sweep._lookup_failure("m", translated(503)).rate_limited is False

    # A context is read for the status and never for the type.
    words = RuntimeError("raised while handling one")
    words.__context__ = TooManyRequests("Album unavailable")
    assert sweep._lookup_failure("m", words).rate_limited is False

    looped = RuntimeError("names itself")
    looped.__cause__ = looped
    looped.__context__ = looped
    assert sweep._lookup_failure("m", looped).rate_limited is False
    assert str(sweep._lookup_failure("the words", limit)) == "the words"
