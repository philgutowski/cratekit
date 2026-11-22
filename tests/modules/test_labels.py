"""U26: label registry, sweeps, import, and harvest."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import requests
from tidalapi.exceptions import TooManyRequests, http_error_to_tidal_error

from cratekit.acquire import listing
from cratekit.core import config, review, secrets, tombstone
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.review import DecisionStore, Queue
from cratekit.label import catalogue, crawl, harvest, sweep, verify
from cratekit.label import cli as label_cli
from cratekit.label import marks as label_marks
from cratekit.label import registry as labels
from cratekit.sync import artifacts, run, watermarks
from tests.label_fakes import PROTOCOL_METHODS, FakeTrack, StrictCatalogue, UnreadableCatalogue

LABEL_ROOT = Path(__file__).resolve().parent.parent.parent / "src" / "cratekit" / "label"


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (tmp_path / "install").mkdir()
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(tmp_path / "install"))
    monkeypatch.setenv("CRATEKIT_CONFIG_DIR", str(tmp_path / "cfgdir"))
    built = config.from_dict({
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {"root": str(root), "volume_id": "F1E2-D3C4",
                    "db_path": str(root / "db" / "master.db")},
        "paths": {"download_staging": str(tmp_path / "staging")},
        "profile": {"name": "full"},
    })
    config.save(built)
    config.reset_cache()
    return built


class ProviderArtist:
    """The real client shape: album.artist is an object with a name, not a string."""

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
    """A provider listing that truncates to one page when not given a limit."""

    page_size = 100

    def __init__(self, albums: list[Album]) -> None:
        self._albums = list(albums)

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[Album]:
        size = self.page_size if limit is None else limit
        return self._albums[offset : offset + size]

    def get_ep_singles(self, limit: int | None = None, offset: int = 0) -> list[Album]:
        return []


def _paged(artist: object, *releases: tuple[str, str, str]) -> PagedArtist:
    """A paged artist of (identifier, year, title) releases all credited to ``artist``."""
    return PagedArtist([Album(i, year=y, artist=artist, title=t) for i, y, t in releases])


def _always_confirm(claimed: str, album: Album) -> dict:
    return {"verdict": "confirmed", "resolved_label": claimed, "source": "fixture", "notes": ""}


def _confirm_named(allowed: set[str]):
    def search(claimed: str, album: Album) -> dict:
        if album.id in allowed:
            return _always_confirm(claimed, album)
        return {"verdict": "unconfirmed", "resolved_label": "", "source": "fixture",
                "notes": "no web match"}
    return search


def _listed(cfg, name: str, match: str, artist: object, **kwargs):
    """Register ``name`` and list it over ``artist``, confirming everything by default."""
    store = labels.RegistryStore()
    label_id = store.add(name, match=match)
    kwargs.setdefault("verify", _always_confirm)
    return sweep.list_for_label(cfg, store.load().by_id(label_id), artist=artist, **kwargs)


def _queued(cfg) -> list:
    with review.open_store(cfg) as queue:
        return list(review.list_items(queue, queue=Queue.LABEL_RELEASE))


# Registry identity survives a rename


def test_the_registry_survives_a_label_rename_without_orphaning_its_state(cfg):
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
    store = labels.RegistryStore()
    first = store.add("Colorize")
    assert first == store.add("Colorize", match="colorize")
    assert store.load().by_id(first).match == "colorize"


def test_the_registry_records_an_id_seed(cfg):
    store = labels.RegistryStore()
    label_id = store.add("Harbour Lights", seed_artists=["id:99"])
    entry = store.load().by_id(label_id)
    assert entry is not None
    assert entry.seed_artists == ("id:99",)


# Date floor is not scope; unverified and tombstoned releases are reported


def test_a_crawl_outside_a_naive_date_floor_still_returns_those_items(cfg):
    artist = _paged("Hernan Cattaneo", ("new", "2026", "New Cut"), ("old", "2018", "Old Cut"))
    found = _listed(cfg, "Sudbeat", "sudbeat", artist, last_pulled="2024")
    identities = {item.identity for item in found.candidates}
    assert "new" in identities
    assert "old" in identities


def test_an_unverified_catalogue_match_is_dropped_and_reported_never_acquired(cfg):
    artist = PagedArtist([Album("keep", year="2026", artist="Lee Burridge", title="Keep"),
                          Album("guess", year="2026", artist="Someone Else", title="Guess")])
    found = _listed(cfg, "All Day I Dream", "all day i dream", artist,
                    verify=_confirm_named({"keep"}))
    assert [item.identity for item in found.candidates] == ["keep"]
    assert any(drop.identity == "guess" for drop in found.dropped)
    assert all(drop.reason != "confirmed" for drop in found.dropped)


def test_a_tombstoned_version_is_reported_suppressed_by_the_sweep(cfg):
    identity = tombstone.version_identity(artist="Anyma", title="Conscience")
    DecisionStore(tombstone.STORE_KEY, cfg).record(
        kind=tombstone.KIND_VERSION, identity=identity, actor="test"
    )
    artist = _paged("Anyma", ("dead", "2026", "Conscience"), ("live", "2026", "The Light"))
    found = _listed(cfg, "Afterlife", "afterlife", artist)
    assert [item.identity for item in found.candidates] == ["live"]
    assert any(item.identity == "dead" for item in found.suppressed)
    assert all(item.identity != "dead" for item in found.candidates)


def test_a_listing_longer_than_one_page_returns_fully(cfg):
    artist = _paged("Label Act", *((f"a{i}", "2026", f"Track {i}") for i in range(180)))
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


# Review output is a queue item, not a file


def test_a_sweep_review_output_is_a_review_queue_item_not_a_file(cfg, tmp_path):
    store = labels.RegistryStore()
    label_id = store.add("Stil Vor Talent", match="stil vor talent")
    artist = _paged("Oliver Koletzki", ("r1", "2026", "First"))
    source = sweep.LabelSource(cfg, registry=store.load(), artists={label_id: artist},
                               verify=_always_confirm)
    payload = {"artist": "Oliver Koletzki", "title": "First", "label_id": label_id,
               "label_name": "Stil Vor Talent"}
    with review.open_store(cfg) as queue:
        source.process(run.Candidate(identity="r1", recency="2026", payload=payload),
                       artifacts.ArtifactRegistry(cfg), "run-labels-1", store=queue)
        items = list(review.list_items(queue, queue=Queue.LABEL_RELEASE))
    assert len(items) == 1
    assert items[0].queue == Queue.LABEL_RELEASE
    assert items[0].payload["identity"] == "r1"
    written = [path for path in tmp_path.rglob("*") if path.suffix in {".csv", ".tsv"}]
    assert written == []


def test_an_offered_release_records_the_artist_name_not_the_provider_object(cfg):
    """The live sweep stored str(album.artist), which is a memory address."""
    credited = ProviderArtist("Oliver Koletzki")
    assert "object at 0x" in str(credited)
    artist = _paged(credited, ("r1", "2026", "First"))
    found = _listed(cfg, "Stil Vor Talent", "stil vor talent", artist)
    assert len(found.candidates) == 1
    payload = found.candidates[0].payload
    assert payload["artist"] == "Oliver Koletzki"
    assert "object at 0x" not in payload["artist"]
    assert payload["title"] == "First"
    with review.open_store(cfg) as queue:
        stored = sweep.offer_release(queue, found.candidates[0]).payload["artist"]
    assert stored == "Oliver Koletzki"
    assert "object at 0x" not in stored


def test_a_string_artist_is_still_recorded_as_the_string(cfg):
    """The suite's stand-ins pass a string, and that spelling must keep working."""
    artist = _paged("Hernan Cattaneo", ("r1", "2026", "New Cut"))
    found = _listed(cfg, "Sudbeat", "sudbeat", artist)
    assert found.candidates[0].payload["artist"] == "Hernan Cattaneo"


def test_the_label_package_does_not_construct_a_csv_writer():
    from tests.test_cli_contract import constructs_a_csv_writer
    for path in sorted(LABEL_ROOT.rglob("*.py")):
        assert not constructs_a_csv_writer(path.read_text()), path


# Acquisition set


def test_a_sweep_produces_the_same_acquisition_set_as_the_source_algorithm(cfg):
    artist = _paged("Act", ("a", "2026", "A"), ("b", "2025", "B"), ("c", "2024", "C"),
                    ("d", "2023", "D"))
    found = _listed(cfg, "Lost & Found", "lost and found", artist,
                    verify=_confirm_named({"a", "b", "d"}), owned={"b"}, limit=2)
    # c is unconfirmed. b is owned. Newest remaining, cap 2: a then d.
    assert [item.identity for item in found.candidates] == ["a", "d"]


def _run(cfg, source, run_id: str, *, owned=None, limit=10, marks=None):
    return run.increment(
        source, owned=set() if owned is None else owned, limit=limit,
        watermarks=watermarks.WatermarkStore(cfg) if marks is None else marks,
        artifacts=artifacts.ArtifactRegistry(cfg), run_id=run_id,
        staging=Path(cfg.paths.download_staging),
    )


def test_increment_does_not_use_the_watermark_as_a_date_floor(cfg):
    store = labels.RegistryStore()
    label_id = store.add("Crosstown Rebels", match="crosstown")
    label_marks.advance(cfg, label_id, year="2024")
    artist = _paged("Damian Lazarus", ("new", "2026", "New"), ("old", "2019", "Old"))
    source = sweep.LabelSource(cfg, registry=store.load(), artists={label_id: artist},
                               verify=_always_confirm)
    marks = watermarks.WatermarkStore(cfg)
    marks.advance("labels", cursor="old", items=1, library_id=cfg.library.volume_id)
    result = _run(cfg, source, "run-floor", marks=marks)
    assert set(result.processed) == {"new", "old"}
    assert {item.payload["identity"] for item in _queued(cfg)} == {"new", "old"}


def test_an_owned_newest_release_does_not_hide_an_older_unowned_one(cfg):
    """R-137, driven through ``LabelSource.list_recent`` and the increment."""
    store = labels.RegistryStore()
    label_id = store.add("Kompakt", match="kompakt")
    owned = {"new"}
    artist = _paged("WhoMadeWho", ("new", "2026", "New"), ("old", "2025", "Old"))
    source = sweep.LabelSource(cfg, registry=store.load(), artists={label_id: artist},
                               verify=_always_confirm, owned=owned)
    result = _run(cfg, source, "run-owned-newest", owned=owned, limit=1)
    assert list(result.processed) == ["old"]


# Harvest: playlist to labels, imports nothing


def test_harvest_offers_verified_labels_and_imports_nothing(cfg, tmp_path):
    tracks = [type("Track", (), {"copyright": f"2026 {name}", "label": None, "id": f"t{n}"})()
              for n, name in enumerate(("Anjunadeep", "Colorize", "Mystery Distro"), 1)]
    def verify_name(name: str) -> dict:
        if name in {"Anjunadeep", "Colorize"}:
            return {"verdict": "confirmed", "resolved_label": name, "notes": ""}
        return {"verdict": "unconfirmed", "resolved_label": "", "notes": "no match"}
    with review.open_store(cfg) as queue:
        report = harvest.from_tracks(tracks, store=queue, verify=verify_name,
                                     extract=harvest.labels_from_copyright)
    assert {item.payload["name"] for item in _queued(cfg)} == {"Anjunadeep", "Colorize"}
    assert "Mystery Distro" in {drop.name for drop in report.dropped}
    assert labels.RegistryStore().load().labels == {}
    assert list(tmp_path.rglob("*.flac")) == []
    assert list(tmp_path.rglob("*.xml")) == []


# Import is a single-label increment, not a date-floored crawl


def test_an_unreadable_intent_file_refuses_rather_than_going_empty(cfg):
    path = config.state_path("label_intent")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(CratekitError) as excinfo:
        labels.RegistryStore().load()
    assert excinfo.value.cause.reason == "label-intent-unusable"


def test_renaming_an_unknown_label_refuses(cfg):
    with pytest.raises(CratekitError) as excinfo:
        labels.RegistryStore().rename("no-such-label", "Other")
    assert excinfo.value.cause.reason == "label-unknown"


class HarvestCtx:
    """A context for the two branches an UNBOUND build must refuse on."""

    def __init__(self, playlist: str = "https://example.invalid/playlist") -> None:
        self.args = type("Args", (), {"playlist": playlist})()
        self.entry = type("E", (), {"name": "label.harvest", "handler_key": "label.harvest"})()
        self.run = type("R", (), {"run_id": "run-h"})()

    def envelope(self, **kwargs):
        raise AssertionError("a build with no catalogue adapter emitted a review set, so it "
                             "harvested a playlist through a seam nothing fills")


def _adapter_absent(monkeypatch):
    """Make the catalogue adapter fail to import: a ``None`` in ``sys.modules`` cannot import."""
    monkeypatch.setitem(sys.modules, "cratekit.label.tidal_catalogue", None)


def test_harvest_on_a_build_with_no_adapter_refuses_that_nothing_is_bound(cfg, monkeypatch):
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
    # A refusal offers nothing, so nobody is left with review items over work that never ran.
    assert _queued(cfg) == []


def test_harvest_with_no_provider_session_refuses_the_credential_instead(cfg):
    """The other refusal a shipped build gives, and it is a different act to fix."""
    with pytest.raises(CratekitError) as excinfo:
        label_cli.harvest_playlist(HarvestCtx())
    assert excinfo.value.cause.reason == "credential-missing"
    assert _queued(cfg) == []


def test_import_one_label_returns_the_unowned_confirmed_set(cfg):
    artist = _paged("WhoMadeWho", ("owned", "2026", "Owned"), ("fresh", "2025", "Fresh"))
    found = _listed(cfg, "Kompakt", "kompakt", PagedArtist(artist._albums), owned={"owned"})
    assert [item.identity for item in found.candidates] == ["fresh"]


# U52: the catalogue provider seam, its refusals and the strict stand-in's guard


def test_with_no_provider_session_the_catalogue_seam_names_the_credential(cfg):
    """Distinguishable from the no-adapter refusal, because doctor can fix one."""
    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)
    cause = excinfo.value.cause
    assert cause.reason == "credential-missing"
    assert cause.detail["credential"] == str(secrets.Credential.PROVIDER_SESSION)


def test_with_a_session_recorded_and_no_adapter_the_seam_refuses_that_nothing_is_bound(
    cfg, monkeypatch
):
    """The credential is real here, recorded through the module that owns it."""
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, {"token": "recorded"})
    assert secrets.exists(str(secrets.Credential.PROVIDER_SESSION))
    _adapter_absent(monkeypatch)
    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)
    cause = excinfo.value.cause
    assert cause.reason == "label-catalogue-unbound"
    assert cause.remediation is not None
    # A build with no adapter reached no provider, so "unreachable" would mislead.
    assert "adapter" in cause.message
    assert "unreachable" not in cause.message


def test_the_catalogue_seam_answers_bound_without_reading_a_credential(cfg, monkeypatch):
    """Asked at enqueue, where the answer is still useful, so it must not raise."""
    def _refuse_to_be_asked(name: str) -> bool:
        raise AssertionError(f"bound() read the credential {name!r}; it answers about the build")
    monkeypatch.setattr(secrets, "exists", _refuse_to_be_asked)
    assert catalogue.bound() is True
    _adapter_absent(monkeypatch)
    assert catalogue.bound() is False


def test_the_strict_catalogue_raises_on_a_method_outside_the_protocol():
    """A caller cannot even NAME a provider read the seam does not declare."""
    strict = StrictCatalogue()
    for method in sorted(PROTOCOL_METHODS):
        assert callable(getattr(strict, method))
    with pytest.raises(AssertionError) as excinfo:
        strict.delete_playlist
    assert "delete_playlist" in str(excinfo.value)


# U52 / R-135: an unreadable catalogue is not an empty one, and an exhausted crawl stays empty


class UnpageableArtist:
    """A listing method that exists and refuses pagination arguments."""

    def get_albums(self):
        return []


class RaisingArtist:
    """A listing method that pages correctly and fails at the provider."""

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[Album]:
        raise RuntimeError("provider 503")


def _impatient_crawl(monkeypatch) -> None:
    """Run the real crawl with its retry backoff collapsed, and nothing else."""
    real = crawl.releases
    def impatient(artist, **kwargs):
        kwargs.setdefault("max_retries", 0)
        return real(artist, **kwargs)
    monkeypatch.setattr(crawl, "releases", impatient)


class SilentArtist:
    """An artist object exposing neither listing method the crawl tries."""


class AlbumsOnlyArtist:
    """ONE working listing method over a catalogue that really has nothing."""

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[Album]:
        return []


def _label_source(cfg, name: str, **kwargs):
    """One registered favourite label and a ``LabelSource`` over it."""
    store = labels.RegistryStore()
    label_id = store.add(name, match=name.lower())
    return label_id, sweep.LabelSource(cfg, registry=store.load(), **kwargs)


def _increment(cfg, source):
    return _run(cfg, source, "run-unreadable")


def _bare(cfg, artist: object = None):
    """Life and Death registered and confirmed, with ``artist`` its catalogue object if given."""
    label_id, source = _label_source(cfg, "Life and Death", artists={}, verify=_always_confirm)
    if artist is not None:
        source.artists = {label_id: artist}
    return source


def test_a_listing_that_cannot_be_paged_raises_instead_of_reporting_empty(cfg, monkeypatch):
    """R-135. The crawl's own exception becomes a LookupFailure, cause intact."""
    _impatient_crawl(monkeypatch)
    with pytest.raises(run.LookupFailure) as excinfo:
        _listed(cfg, "Diynamic", "diynamic", UnpageableArtist())
    assert "Diynamic" in str(excinfo.value)
    # The client's own words stay reachable behind this layer's summary.
    cause = excinfo.value.__cause__
    assert isinstance(cause, listing.ListingNotPaginated)
    assert isinstance(cause.__cause__, TypeError)


def test_a_provider_error_out_of_the_crawl_is_not_an_empty_catalogue(cfg, monkeypatch):
    """The wrap is not narrowed to the one exception type this layer knows."""
    _impatient_crawl(monkeypatch)
    with pytest.raises(run.LookupFailure) as excinfo:
        _listed(cfg, "Innervisions", "innervisions", RaisingArtist())
    assert isinstance(excinfo.value.__cause__, RuntimeError)
    assert "503" in str(excinfo.value.__cause__)


def test_an_artist_exposing_no_listing_method_raises_rather_than_crawling_nothing(cfg):
    """The producer is one layer down, and this pins BOTH halves of it."""
    silent = SilentArtist()
    # The wrapper skips each missing method and returns empty from an object it never read.
    assert crawl.releases(silent) == []
    with pytest.raises(run.LookupFailure) as excinfo:
        _listed(cfg, "Rekids", "rekids", silent)
    message = str(excinfo.value)
    assert "Rekids" in message
    for method in crawl.LISTING_METHODS:
        assert method in message


def test_one_working_listing_with_no_releases_still_reports_empty(cfg):
    """The adversarial half. A quiet label must not become an error."""
    label_id, source = _label_source(cfg, "Quiet Imprint", artists={}, verify=_always_confirm)
    source.artists = {label_id: AlbumsOnlyArtist()}
    result = _increment(cfg, source)
    assert result.shortfall == "empty"
    assert result.processed == ()


def test_an_unreadable_listing_stops_the_increment_at_the_lookup(cfg, monkeypatch):
    """Named where the run stopped, not merely that nothing came out of it."""
    _impatient_crawl(monkeypatch)
    label_id, source = _label_source(cfg, "Hotflush", artists={}, verify=_always_confirm)
    source.artists = {label_id: RaisingArtist()}
    with pytest.raises(CratekitError) as excinfo:
        _increment(cfg, source)
    cause = excinfo.value.cause
    assert cause.reason == "sync-source-lookups-failed"
    assert cause.detail["source_id"] == "labels"
    # A failed listing is not an empty catalogue: the two send a person to different places.
    assert "empty" not in cause.message or "not a verified empty" in cause.message


def test_a_label_the_catalogue_cannot_resolve_stops_the_increment(cfg):
    """The path ``list_for_label`` never sees, driven end to end."""
    unreadable = UnreadableCatalogue()
    label_id, source = _label_source(cfg, "Ostgut Ton", catalogue=unreadable)
    with pytest.raises(CratekitError) as excinfo:
        _increment(cfg, source)
    assert excinfo.value.cause.reason == "sync-source-lookups-failed"
    # The catalogue was genuinely asked: a failed read, not a label never looked up.
    assert unreadable.asked_for == [label_id]


def test_a_registered_label_with_no_artist_object_refuses_rather_than_skipping(cfg):
    with pytest.raises(CratekitError) as excinfo:
        _increment(cfg, _bare(cfg))
    assert excinfo.value.cause.reason == "sync-source-lookups-failed"


def test_the_missing_artist_refusal_names_the_missing_object_not_the_listing(cfg):
    """Remove each guard layer alone: this is the layer the test above cannot see."""
    with pytest.raises(run.LookupFailure) as excinfo:
        _bare(cfg).list_recent(10)
    said = str(excinfo.value)
    assert "no catalogue object was available" in said, said
    assert "Life and Death" in said, said


def test_a_source_with_neither_verifier_nor_catalogue_refuses_rather_than_confirming_nothing(cfg):
    artists = {labels.slug("Life and Death"): _paged("X", ("a", "2026", "A"))}
    _id, source = _label_source(cfg, "Life and Death", artists=artists)
    with pytest.raises(run.LookupFailure) as excinfo:
        source.list_recent(10)
    assert "neither a verification callable nor a catalogue" in str(excinfo.value)
    assert source.dropped == ()


def test_a_source_over_an_empty_registry_lists_nothing_rather_than_refusing_its_verifier(cfg):
    """A no-op stays a no-op: nothing to confirm means no way to confirm is needed."""
    source = sweep.LabelSource(cfg, registry=labels.Registry(labels={}))
    assert source.list_recent(10) == []
    assert source.read == 0


class ProxyThatFetchesOnAttributeAccess:
    """An artist object whose every attribute read goes to a provider that is down."""

    def __getattr__(self, name: str):
        raise ConnectionError(f"the provider did not answer for {name!r}")


def test_an_artist_object_that_raises_on_inspection_is_a_lookup_failure_not_a_defect(cfg):
    """The listing probe sits inside the boundary, as the listing itself does."""
    with pytest.raises(CratekitError) as excinfo:
        _increment(cfg, _bare(cfg, ProxyThatFetchesOnAttributeAccess()))
    assert excinfo.value.cause.reason == "sync-source-lookups-failed"
    assert "ConnectionError" in excinfo.value.cause.message


def test_a_refusal_raised_mid_crawl_passes_through_the_listing_boundary_unchanged(cfg):
    """The crawl's boundary keeps the rule the verifier's states."""
    class RefusingArtist:
        def get_albums(self, limit=None, offset=0):
            raise refuse("credential-missing", "the session expired mid page", origin=("tests",))
        def get_ep_singles(self, limit=None, offset=0):
            return []
    with pytest.raises(CratekitError) as excinfo:
        _increment(cfg, _bare(cfg, RefusingArtist()))
    assert excinfo.value.cause.reason == "credential-missing"


def test_the_crawl_probes_exactly_the_methods_the_listing_reads_by_default():
    assert crawl.LISTING_METHODS == listing.RELEASE_METHODS == ("get_albums", "get_ep_singles")


def _translated(status: int) -> BaseException:
    """What the client raises for an HTTP ``status`` whose body is not JSON."""
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


def test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from():
    """R-704. The sweep asks the error and every ``raise X from`` behind it."""
    limit = TooManyRequests("Album unavailable")
    assert sweep._lookup_failure("m", limit).rate_limited is True
    wrapped = RuntimeError("the client gave up")
    wrapped.__cause__ = limit
    assert sweep._lookup_failure("m", wrapped).rate_limited is True
    assert sweep._lookup_failure("m", RuntimeError("provider 503")).rate_limited is False
    # A gateway's non JSON 429 arrives as a decode error whose context carries the status.
    assert sweep._lookup_failure("m", _translated(429)).rate_limited is True
    assert sweep._lookup_failure("m", _translated(503)).rate_limited is False
    # A context is read for the status and never for the type.
    words = RuntimeError("raised while handling one")
    words.__context__ = TooManyRequests("Album unavailable")
    assert sweep._lookup_failure("m", words).rate_limited is False
    looped = RuntimeError("names itself")
    looped.__cause__ = looped
    looped.__context__ = looped
    assert sweep._lookup_failure("m", looped).rate_limited is False
    assert str(sweep._lookup_failure("the words", limit)) == "the words"


# U237: a copyright line keeps the label's first letter (names measured clipped on a live pass)

U237_NAMES = ("Cadenza", "Pressure Traxx", "Cronos", "Puls", "Cronos Barac", "Gettraum, LaMez")
U237_PREFIXES = ("", "2021 ", "(P) 2021 ", "(C) 2021 ", "(p) 2021 ", "(c) 2021 ", "℗ 2021 ", "© 2021 ",
                 "(P)", "(C) ", "℗", "© ", "(P)(C) 2021 ", "℗ © 2021 ")


def _copyright_track(text: str, *, field: str = "copyright"):
    return FakeTrack("t1", **{field: text})


def _read(text: str, **field: str) -> tuple[str, ...]:
    return harvest.labels_from_copyright(_copyright_track(text, **field))


@pytest.mark.parametrize("prefix", U237_PREFIXES)
@pytest.mark.parametrize("name", U237_NAMES)
def test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix(prefix, name):
    assert _read(prefix + name) == (name,)


@pytest.mark.parametrize("name", U237_NAMES)
def test_a_label_credit_read_when_no_copyright_line_keeps_its_first_letter(name):
    assert _read(name, field="label") == (name,)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("(P) 2021 Cadenza", ("Cadenza",)), ("℗ 2021 Cadenza", ("Cadenza",)),
        ("© 2025 Gettraum, LaMez", ("Gettraum, LaMez",)), ("2013 Cadenza", ("Cadenza",)),
        ("2013 Cadenza.", ("Cadenza",)),
        # A label that is only the letter P or C keeps it, prefix or none.
        ("2021 P", ("P",)), ("2021 C", ("C",)), ("(P) 2021 C", ("C",)), ("© 2021 P", ("P",)),
        ("(C) P", ("P",)),
        # A line that is only a mark and a year names no label at all.
        ("(P) 2021", ()), ("(P) 2021.", ()),
        # Four digits run into more digits are not a year: nothing is stripped.
        ("20211 Label", ("20211 Label",)),
        ("℗ 2021", ()), ("2021", ()), ("(C)", ()), ("", ()),
    ],
)
def test_only_the_parenthesised_or_symbol_mark_and_the_year_are_stripped(text, expected):
    assert _read(text) == expected


def test_a_letter_after_a_mark_is_not_a_second_mark():
    # ``P Cadenza`` and ``C 2021 Puls`` carry no mark this reader knows, so nothing is stripped.
    assert _read("(P) Cadenza") == ("Cadenza",)
    assert _read("P Cadenza") == ("P Cadenza",)
    assert _read("C 2021 Puls") == ("C 2021 Puls",)


def test_harvest_offers_cadenza_not_adenza(cfg):
    asked: list[str] = []
    def verify_name(name: str) -> dict:
        asked.append(name)
        return {"verdict": "confirmed", "resolved_label": name, "notes": ""}
    tracks = [_copyright_track("(P) 2021 Cadenza"), _copyright_track("Pressure Traxx")]
    with review.open_store(cfg) as queue:
        report = harvest.from_tracks(tracks, store=queue, verify=verify_name)
    assert asked == ["Cadenza", "Pressure Traxx"]
    assert {item.payload["name"] for item in _queued(cfg)} == {"Cadenza", "Pressure Traxx"}
    assert report.dropped == ()


@pytest.mark.parametrize(
    ("needle", "credit"),
    [
        ("Rawax", "Rawax"), ("Rawax", "RAWAX"), ("Rawax", "Rawax Records"),
        ("Rawax Records", "Rawax"), ("Liebe*Detail", "Liebe Detail"),
        ("Liebe*Detail", "Liebe*Detail"), ("Liebe*Detail", "Liebe Detail Spezial"),
        ("Crosstown", "Crosstown Rebels"), ("HL", "HL"), ("Harbour Lights", "Harbour Lights Ltd"),
        ("Some Label Rec", "Some Label Rec"), ("stil vor talent", "Stil Vor Talent"),
        ("all day i dream", "All Day I Dream Records"), ("Gettraum", "Gettraum, LaMez"),
        ("Cronos", "Cronos Barac"), ("Cadenza", "Cadenza Music"),
        ("Some Label Records", "(P) Some Label Records"), ("Rawax", "Exclusive licence to Rawax"),
        ("Rawax", "Under licence to Rawax Records"),
    ],
)
def test_a_needle_confirms_its_label_on_whole_words(needle, credit):
    assert verify.labels_match(needle, credit)


@pytest.mark.parametrize(
    ("needle", "credit"),
    [
        ("Rawax", "RAWAXXX"), ("RAWAXXX", "Rawax"), ("Rawax", "Rawaxxx Records"),
        ("adenza", "Cadenza"), ("ronos", "Cronos"), ("Puls", "Pulse"), ("tide", "Tidewater"),
        ("Rawax", ""), ("", "Rawax"), ("***", "Rawax"),
        # Two sides that both fold to nothing are not a match of nothing.
        ("***", "---"),
        ("日本", "Пластинка"),
    ],
)
def test_a_needle_inside_a_longer_word_confirms_nothing(needle, credit):
    assert not verify.labels_match(needle, credit)


def test_a_release_credited_to_a_longer_act_name_is_a_mismatch_not_a_confirmation():
    def search(claimed, release):
        return {"resolved_label": "RAWAXXX", "source": "fake"}
    verdict = verify.verify_release("Rawax", object(), search=search)
    assert verdict["verdict"] == "mismatch"
    assert verdict["notes"] == "credited as 'RAWAXXX'"
